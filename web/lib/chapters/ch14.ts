import type { ChapterDef } from "../schema";

export const ch14: ChapterDef = {
  slug: "orchestrator-state",
  number: 14,
  lesson: "Lesson 3",
  subtopicLabel: "3.2 Orchestrator State",
  title: "Toolkit, MCP & Planner",
  subtitle: "Local tools, tools from an MCP server, and a planner that researches before it plans.",
  cursorFeature: "Agent Mode, MCP",
  designPatterns: ["Planning"],
  intro: "The toolkit is the workspace tools from Lesson 1 plus grep, glob, a sandboxed run_python, and run_command, and then two more that arrive over the Model Context Protocol from Parallel's search server: web_search and web_fetch. They bind like any other tool. The planner uses them in a research loop before it emits a structured Plan: one entry per file, create or modify, what changes. The same MCP server is in .cursor/mcp.json, so Cursor's agent has it too.",
  takeaway: "Tools are the agent's reach. MCP makes that reach configuration instead of code, and a planner that reads before it writes makes fewer, better file tasks.",
  demos: [],
  codeContent: `class OrchestratorState(TypedDict):
    feature_request: str
    codebase_context: str
    plan: str
    file_tasks: list[dict]
    generated_code: list[dict]
    review_result: str
    review_attempts: int
    human_decision: str
    test_output: str
    status: str`,
  codeFilename: "orchestrator_state.py",
  backendCode: `/* lesson:begin */
# synced from lessons/03_brain/ch14_toolkit_and_planner.py
/* lesson:end */`,
  backendFilename: "ch14_toolkit_and_planner.py",
  chatConfig: {
    mode: "planner",
    defaultPrompt: "Add a system prompt setting to the chatbot",
    conversations: {
      default: [
        {
          role: "tool",
          toolName: "search_codebase",
          toolArgs: { query: "system prompt chatbot config" },
          content: `--- config.py ---
PAGE_TITLE = "My ChatBot"
PAGE_ICON = "🤖"
MODEL = "openai/gpt-4o-mini"
BASE_URL = "https://openrouter.ai/api/v1"

--- chat.py ---
def stream_response(client, messages):
    response = client.chat.completions.create(model=MODEL, messages=messages, stream=True)

--- app.py ---
st.session_state.messages.append({"role": "user", "content": prompt})`,
        },
        {
          role: "tool",
          toolName: "planner",
          toolArgs: { feature: "Add a system prompt setting to the chatbot" },
          content: `{
  "summary": "Add SYSTEM_PROMPT to config.py, update chat.py to inject system prompt into messages, and modify app.py to use the system prompt in chat initialization",
  "file_tasks": [
    {
      "filepath": "config.py",
      "action": "modify",
      "description": "Add a SYSTEM_PROMPT constant with a default value for the chatbot's system instructions"
    },
    {
      "filepath": "chat.py",
      "action": "modify",
      "description": "Modify stream_response to accept an optional system_prompt parameter and inject it as the first message"
    },
    {
      "filepath": "app.py",
      "action": "modify",
      "description": "Import SYSTEM_PROMPT from config and pass it to stream_response when calling the function"
    }
  ]
}`,
        },
        {
          role: "assistant",
          content: `**Plan**: Add SYSTEM_PROMPT to config.py, update chat.py to inject system prompt into messages, and modify app.py to use the system prompt in chat initialization\n\n**File Tasks:**\n\n| # | Action | File | Description |\n|---|--------|------|-------------|\n| 1 | modify | config.py | Add SYSTEM_PROMPT constant with default value |\n| 2 | modify | chat.py | Add system_prompt parameter to stream_response |\n| 3 | modify | app.py | Import and pass SYSTEM_PROMPT to stream_response |\n\nThe planner searched the codebase first to understand the current structure, then produced a typed Plan with 3 FileTask entries.`,
        },
      ],
    },
  },
};
