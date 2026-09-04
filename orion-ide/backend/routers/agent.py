import json
import uuid

from fastapi import APIRouter, Header, HTTPException
from langgraph.types import Command
from starlette.responses import StreamingResponse

from config import DEFAULT_MODEL, OPENROUTER_API_KEY
from models.schemas import AgentApproveRequest, AgentRunRequest

router = APIRouter(prefix="/agent", tags=["agent"])

orchestrators: dict[str, tuple] = {}

STATUS_MAP = {
    "plan": "planning",
    "code": "coding",
    "test": "testing",
    "ai_review": "reviewing",
    "human_review": "waiting_approval",
    "apply": "applying",
    "verify": "verifying",
}


def _sse(payload: dict) -> str:
    return f"data: {json.dumps(payload)}\n\n"


async def _stream(graph, loaded: list[str], graph_input, config):
    """Translate graph updates into the IDE's SSE events."""
    seen_skills = 0
    try:
        async for chunk in graph.astream(graph_input, config=config, stream_mode="updates"):
            for node_name, update in chunk.items():
                if node_name == "__interrupt__":
                    for interrupt_val in update:
                        yield _sse({"type": "approval_needed", **interrupt_val.value})
                    continue
                if node_name in STATUS_MAP:
                    yield _sse({"type": "status", "status": STATUS_MAP[node_name]})
                if not isinstance(update, dict):
                    continue
                if node_name == "plan":
                    for name in loaded[seen_skills:]:
                        yield _sse({"type": "skill_loaded", "name": name})
                    seen_skills = len(loaded)
                    if update.get("status") == "path_rejected":
                        yield _sse({"type": "error", "message": update.get("error", "plan rejected")})
                    elif update.get("plan"):
                        yield _sse({"type": "plan", "plan": update["plan"], "tasks": update.get("file_tasks", [])})
                elif node_name == "code":
                    for item in update.get("generated_code", []):
                        yield _sse({
                            "type": "code",
                            "filepath": item["filepath"],
                            "description": item.get("explanation", ""),
                            "status": "done",
                        })
                elif node_name == "test":
                    yield _sse({"type": "test", "status": update.get("status", ""), "output": update.get("test_output", "")})
                elif node_name == "ai_review":
                    yield _sse({"type": "review", "status": update.get("status", ""), "result": update.get("review_result", "")})
                elif node_name == "verify":
                    yield _sse({"type": "test", "status": update.get("status", ""), "output": update.get("test_output", "")})
                    yield _sse({"type": "status", "status": "done" if update.get("status") == "done" else "error"})
                elif node_name == "apply" and update.get("status") == "apply_failed":
                    yield _sse({"type": "error", "message": update.get("error", "apply failed")})
    except Exception as exc:  # noqa: BLE001 - the UI shows whatever went wrong
        yield _sse({"type": "error", "message": str(exc)})
    yield _sse({"type": "done"})


@router.post("/run")
async def run_agent(request: AgentRunRequest, x_api_key: str | None = Header(None)):
    api_key = request.api_key or x_api_key or OPENROUTER_API_KEY
    model = request.model or DEFAULT_MODEL
    thread_id = request.thread_id or str(uuid.uuid4())

    from agent.graph import create_orchestrator

    graph, loaded = create_orchestrator(api_key=api_key, model=model)
    orchestrators[thread_id] = (graph, loaded)
    config = {"configurable": {"thread_id": thread_id}}
    return StreamingResponse(
        _stream(graph, loaded, {"feature_request": request.feature_request}, config),
        media_type="text/event-stream",
        headers={"X-Thread-ID": thread_id},
    )


@router.post("/approve")
async def approve_agent(request: AgentApproveRequest):
    if request.thread_id not in orchestrators:
        raise HTTPException(status_code=404, detail="Thread not found")
    graph, loaded = orchestrators[request.thread_id]
    config = {"configurable": {"thread_id": request.thread_id}}
    resume = Command(resume={"decision": request.decision, "feedback": request.feedback})
    return StreamingResponse(_stream(graph, loaded, resume, config), media_type="text/event-stream")


@router.get("/history/{thread_id}")
async def get_history(thread_id: str):
    if thread_id not in orchestrators:
        return {"steps": []}
    graph, _ = orchestrators[thread_id]
    config = {"configurable": {"thread_id": thread_id}}
    keys = ("status", "plan", "review_result", "test_output", "human_decision", "human_feedback", "error")
    steps = []
    for i, state in enumerate(graph.get_state_history(config)):
        steps.append({
            "step": i,
            "status": state.values.get("status", ""),
            "next": list(state.next) if state.next else [],
            "state": {
                k: (str(v)[:200] if isinstance(v, (list, dict)) else v)
                for k, v in state.values.items()
                if k in keys
            },
        })
    return {"steps": steps}
