import type { ChapterDef } from "../schema";

export const ch16: ChapterDef = {
  slug: "human-in-the-loop",
  number: 16,
  lesson: "Lesson 3",
  subtopicLabel: "3.4 Human-in-the-Loop",
  title: "Human-in-the-Loop with Tests",
  subtitle: "Plan, code, test, review, then stop and ask. A reject carries a reason back to the coder.",
  cursorFeature: "Agent Mode",
  designPatterns: ["Human-in-the-Loop"],
  intro: "Tests run before anyone reviews. The graph applies the generated files to a scratch copy of the workspace, runs pytest there, and routes failures back to the coder with the output. Only passing code reaches the AI reviewer, and only reviewed code reaches you. interrupt() freezes the graph with the plan, the diff previews, the test output, and the review in hand. You resume it with approve, or with reject and a sentence of feedback that the coder reads verbatim. Then it applies for real and verifies again.",
  takeaway: "Tests are the verification primitive; the model reviewer is a second opinion; the human is the gate. A reject with a reason is worth more than a reject alone, so the graph resets its counters and tries again with your words in the prompt.",
  demos: [],
  backendCode: `/* lesson:begin */
# synced from lessons/03_brain/ch16_human_in_the_loop.py
/* lesson:end */`,
  backendFilename: "ch16_human_in_the_loop.py",
  chatConfig: {
    mode: "human-in-the-loop",
    defaultPrompt: "Add a system prompt feature to the chatbot",
    conversations: {
      approve: [
        {
          role: "tool",
          toolName: "plan",
          toolArgs: { feature: "Add a system prompt feature" },
          content: `Plan: Add system prompt feature with default config, modify chat logic, and add sidebar UI

File Tasks:
  [modify] sample_project/config.py
  [modify] sample_project/chat.py
  [modify] sample_project/app.py`,
        },
        {
          role: "tool",
          toolName: "code",
          toolArgs: { files: "3 file tasks" },
          content: `Generated: sample_project/config.py (244 chars)
Generated: sample_project/chat.py (546 chars)
Generated: sample_project/app.py (1385 chars)`,
        },
        {
          role: "tool",
          toolName: "review",
          toolArgs: { attempt: "1/2" },
          content: `Review [1/2]: APPROVED — Code is functional and well-structured.`,
        },
        {
          role: "system",
          content: `⏸️ AGENT PAUSED — Waiting for human review\n\nPlan: Add system prompt feature with default config, modify chat logic, and add sidebar UI\nReview attempts: 1\nFiles: 3\n  sample_project/config.py: Added DEFAULT_SYSTEM_PROMPT variable\n  sample_project/chat.py: Added optional system_prompt parameter\n  sample_project/app.py: Added system prompt editing sidebar`,
        },
        {
          role: "tool",
          toolName: "human_decision",
          toolArgs: { decision: "approve" },
          content: `Command(resume="approve") → Resuming agent...`,
        },
        {
          role: "tool",
          toolName: "apply",
          toolArgs: { files: "3" },
          content: `Applied: sample_project/config.py
Applied: sample_project/chat.py
Applied: sample_project/app.py`,
        },
        {
          role: "tool",
          toolName: "test",
          toolArgs: { command: "import check" },
          content: `Tests: PASS\nAll imports OK`,
        },
        {
          role: "assistant",
          content: `**Approved & Applied** ✓\n\nHuman decision: **approve**\n\nThe agent applied all 3 files and ran smoke tests:\n- ✓ sample_project/config.py\n- ✓ sample_project/chat.py\n- ✓ sample_project/app.py\n\nTest output: All imports OK\n\nFinal status: **tested**`,
        },
      ],
      reject: [
        {
          role: "tool",
          toolName: "plan",
          toolArgs: { feature: "Add a system prompt feature" },
          content: `Plan: Add system prompt feature with default config, modify chat logic, and add sidebar UI

File Tasks:
  [modify] sample_project/config.py
  [modify] sample_project/chat.py
  [modify] sample_project/app.py`,
        },
        {
          role: "tool",
          toolName: "code",
          toolArgs: { files: "3 file tasks" },
          content: `Generated: sample_project/config.py (244 chars)
Generated: sample_project/chat.py (546 chars)
Generated: sample_project/app.py (1385 chars)`,
        },
        {
          role: "tool",
          toolName: "review",
          toolArgs: { attempt: "1/2" },
          content: `Review [1/2]: APPROVED — Code is functional and well-structured.`,
        },
        {
          role: "system",
          content: `⏸️ AGENT PAUSED — Waiting for human review\n\nPlan: Add system prompt feature with default config, modify chat logic, and add sidebar UI\nReview attempts: 1\nFiles: 3\n  sample_project/config.py: Added DEFAULT_SYSTEM_PROMPT variable\n  sample_project/chat.py: Added optional system_prompt parameter\n  sample_project/app.py: Added system prompt editing sidebar`,
        },
        {
          role: "tool",
          toolName: "human_decision",
          toolArgs: { decision: "reject" },
          content: `Command(resume="reject") → Routing back to coder...`,
        },
        {
          role: "tool",
          toolName: "code",
          toolArgs: { files: "3 file tasks (regenerating)" },
          content: `Regenerated: sample_project/config.py (268 chars)
Regenerated: sample_project/chat.py (612 chars)
Regenerated: sample_project/app.py (1520 chars)`,
        },
        {
          role: "tool",
          toolName: "review",
          toolArgs: { attempt: "2/2" },
          content: `Review [2/2]: APPROVED — Improved implementation with better error handling and documentation.`,
        },
        {
          role: "assistant",
          content: `**Rejected → Regenerated** ↻\n\nHuman decision: **reject**\n\nThe agent looped back to the coder node and regenerated all 3 files with improvements:\n- config.py: 244 → 268 chars (added docstring)\n- chat.py: 546 → 612 chars (better error handling)\n- app.py: 1385 → 1520 chars (improved UI)\n\nReviewer approved on second attempt. Agent is paused again at human review gate.`,
        },
      ],
    },
    generatedFile: {
      filename: "config.py",
      content: `PAGE_TITLE = "My ChatBot"
PAGE_ICON = "🤖"
MODEL = "openai/gpt-4o-mini"
BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_SYSTEM_PROMPT = "You are a helpful AI assistant. Please provide clear, accurate, and helpful responses to user questions."
`,
    },
  },
};
