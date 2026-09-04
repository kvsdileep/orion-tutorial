# %% setup
"""Chapter 16: plan, code, test, review, then stop and ask."""
from orion_agent.lesson import setup, run, show, print_file, demo_orchestrator

ROOT, ws = setup()

# %% C12 the human node web
import inspect

from orion_agent.graphs import orchestrator

source = inspect.getsource(orchestrator.build_orchestrator)
start = source.index("def human_review_node")
print(source[start : source.index("def route_after_human")])

# %% C13 compile web
agent = demo_orchestrator(ROOT, ws)
nodes = set(agent.get_graph().nodes) - {"__start__", "__end__"}
print(f"Agent compiled: {len(nodes)} nodes, 4 conditional routes, checkpointing enabled")
print(sorted(nodes))

# %% C14 draw it
show(agent, "plan -> code -> test -> ai_review -> human_review -> apply -> verify")

# %% C15 watch it think, then pause web
FEATURE = (
    "Add a system prompt feature to the chatbot. "
    "Add a DEFAULT_SYSTEM_PROMPT constant in config.py. "
    "Modify chat.py so stream_response accepts an optional system_prompt parameter "
    "and prepends it as a system message. "
    "Modify app.py to add a sidebar text area where users can edit the system prompt, "
    "and pass it to stream_response."
)
config = {"configurable": {"thread_id": "demo-1"}}
print("Sending feature request to the agent...\n")
result = run(agent.ainvoke({"feature_request": FEATURE}, config))

payload = result["__interrupt__"][0].value  # what interrupt() handed back to us
print("=" * 60)
print("Agent paused. Waiting for human review")
print("=" * 60)
print(f"Plan: {payload['plan']}")
print(f"Review: {payload['review_result'][:200]}")
print(f"Tests:\n{payload['test_output'][:400]}")
for change in payload["changes"]:
    print(f"  {change['filepath']}: {change['explanation'][:80]}")

# %% C16 the frozen state web
state = run(agent.aget_state(config))
print(f"Agent is waiting at node: {state.next}\n")
for item in state.values["generated_code"]:
    print("=" * 60)
    print(f"  {item['filepath']}")
    print("=" * 60)
    print(item["code"])
    print()

# %% C17 approve, apply, verify web
from langgraph.types import Command

result = run(agent.ainvoke(Command(resume={"decision": "approve", "feedback": ""}), config))
print(f"Status: {result['status']}")
print(f"\nTest output:\n{result['test_output']}")

# %% C18 the applied files
for rel in ("config.py", "chat.py", "app.py"):
    print_file(ws, rel)

# %% N1 reject with a reason, on a second thread web
config_b = {"configurable": {"thread_id": "demo-1b"}}
snapshot = ws.snapshot()  # keep the approved files; this thread works on a copy
from orion_agent.workspace import Workspace

scratch_agent = demo_orchestrator(ROOT, Workspace(snapshot))
paused = run(scratch_agent.ainvoke({"feature_request": "Add a PAGE_SUBTITLE constant to config.py and show it under the title in app.py."}, config_b))
print("paused with:", [c["filepath"] for c in paused["__interrupt__"][0].value["changes"]])

paused_again = run(scratch_agent.ainvoke(
    Command(resume={"decision": "reject", "feedback": "Call the constant TAGLINE, not PAGE_SUBTITLE, and keep it under 40 characters."}),
    config_b,
))
state_b = run(scratch_agent.aget_state(config_b))
print("attempt counters after the reject:", state_b.values["review_attempts"], state_b.values["test_attempts"])
for change in paused_again["__interrupt__"][0].value["changes"]:
    print(f"--- {change['filepath']} ---\n{change['preview']}\n")
