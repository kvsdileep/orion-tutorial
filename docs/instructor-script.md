# Orion: Instructor Script

Build an AI Coding Agent with LangChain and LangGraph. Sprint 6, Day 13, AI Engineering Accelerator.

For Dileep to deliver. 61 beats in the same order as the original session. Every beat points to a lesson cell (Lesson 1 to 3, file and cell tag), a curriculum-site chapter (1.1 to 3.6), the Orion IDE, a Cursor screen, or an Excalidraw drawing. Cell tags are the ones in the lesson files: C3 is the third cell of the original lesson, N1 is a cell added for this build. Appendix A maps every cell to a beat. Appendix C lists where the content departs from the original run.

Companion documents: [teaching-guide.md](teaching-guide.md) for the concepts and the why; [graphs/README.md](graphs/README.md) for the drawings; [../lessons/README.md](../lessons/README.md) for setup and rehearsal.

## How to read this

| Tag | Meaning |
|---|---|
| SHOW | What is on screen: lesson cell, site chapter, IDE, Cursor, Excalidraw, slide. |
| SAY | Script. Paraphrase freely, keep the point. |
| ASK | Question to the chat and the answer you want. Wait for it. |
| DO | Run the cell, toggle the tool, draw the node. |
| WATCH | Where a demo can fail live, and what to do. |
| NOTE | Context for you. Not said aloud. |

Setup the night before. In the repo: uv sync, then copy .env.example to .env with OPENROUTER_API_KEY (PARALLEL_API_KEY is optional; the search server works without it). Run uv run orion check-models, then uv run orion reset so workspace/ holds app.py, chat.py, config.py and test_app.py. Open the repository folder in Cursor, not a subfolder, and pick the .venv interpreter when the interactive window asks. Open lessons/ in the file tree. Excalidraw in a tab. The curriculum site in a browser. The Orion IDE running locally (backend on 8000, frontend on 5173; commands in orion-ide/README.md). Run every lesson file end to end once so you know the timings; ch16 and ch18 are the long ones. Run uv run orion reset again. uv run pytest must be green. Phone on silent.

Running cells. Put the cursor in a cell and press Shift+Enter. The output appears in the interactive window next to the code. Definition cells print the relevant source with inspect.getsource, so the code is on screen without opening the package file; open the file under src/orion_agent/ when you want to scroll.

Models: Lessons 1 and 2 use FAST (openai/gpt-4o-mini). Lesson 3 uses STRONG (anthropic/claude-sonnet-4.5). orion check-models verifies both IDs against OpenRouter.

Drawings. The six graphs in docs/graphs are learner-facing SVGs: agent_loop, self_correction, self_correction_with_review, orchestrator, orchestrator_state, parallel_coders. Open them in six browser tabs, in that order, before the session. The .excalidraw versions of the same files load at excalidraw.com if you want to draw over one or fill a state table live; docs/graphs/README.md has the notes for each drawing.

Learners watch. You run the code; nobody follows along on their machine. Whether to share the repo afterwards is your call and does not change the script.

## Run of show

Times are from T+0, instructor on mic. The original ran 10:10 to about 14:45 IST. Timings are estimates; rehearse ch16 and ch18 and adjust.

| T+ | Block | Beats | Minutes |
|---|---|---|---|
| -0:10 | Pre-session | 1-3 | 10 |
| 0:00 | Framing: reverse-engineer Cursor, Orion, three lessons | 4-8 | 12 |
| 0:12 | Lesson 1: hands | 9-22 | 58 + 5 break |
| 1:15 | Lesson 2: self-awareness | 23-36 | 60 + 10 break |
| 2:25 | Lesson 3: brain | 37-51 | 70 |
| 3:35 | Recap, book, connect the dots, roadmap | 52-55 | 25 |
| 4:00 | Program, Q&A, hackathon, feedback | 56-61 | 45 |

## Pre-session (host, T-10 to T+0)

### Beat 1: Warm-up while people join (T-10)

- **SAY** “Last learning session of the accelerator. Thirteen days. Two things before we start. Cameras on. Get something to eat and keep it next to you. This one runs long.”
- **DO** Name the two or three people already on camera. Confirm everyone has joined their hackathon WhatsApp group.

### Beat 2: The extra sessions and the breakout thank-you (T-7)

- **SAY** “Two extra sessions on Monday and Tuesday. We added them because the breakout rooms have been good and some of you have been teaching each other. Thank you for that.”

### Beat 3: Backup plan (T-3)

- **SAY** “If my machine or my API key dies, [backup mentor] picks up from the same lesson file. Nothing stops.”
- **NOTE** Fill in the backup name. Say it once. The backup needs the repo, uv sync done, and a .env.

## Framing (T+0 to T+12)

### Beat 4: What today is (T+0)

- **SAY** “You have built agents and RAG systems for twelve days. Today you see what a system that goes to production looks like. It is not one big agent that does everything. It is many small components that you build, test, improve and combine.”
- **ASK** “How many of you have used Cursor, Claude Code, Copilot or Antigravity for coding?” Expect most hands. Then: “Have you thought about what makes it good, and how hard it is to build?”

### Beat 5: The promise (T+2)

- **SAY** “Today we reverse-engineer Cursor. I show you a Cursor feature, then we build it with LangChain and LangGraph. About a fifth of this you saw with Paras. The rest is new. By the end you know the components of a coding agent and you have built bigger graphs than anything so far.”
- **NOTE** The framing is honest now: the codebase search, the rules files, the skills, the MCP server and the tests-before-review order are how Cursor, Claude Code and Codex work in September 2026. The embeddings cell in ch13 is the one place you say “this is how it used to be.”
- **NOTE** Ishan’s framing on the day (transcript L147): “Some part of it, maybe 15 to 20 percent, Paras had already covered. The majority is new.” Keep the credit to Paras.

### Beat 6: Orion, and where it came from (T+4)

- **SAY** “Orion is a coding agent Ishan built on our team. You give it a repo URL, a task and a branch. It clones the repo, reads the code, plans, edits, tests, reviews and opens a PR. He wired it to Discord so he never opens the editor. Today is the pipeline behind that. The Discord glue is 30 or 40 lines.”
- **ASK** “Who saw the Orion demo in the mastermind?” A few will. Name them.

### Beat 7: Three lessons, one analogy (T+6)

- **SHOW** Cursor with lessons/ expanded in the file tree: 01_hands, 02_self_awareness, 03_brain, eighteen files. Zoom in. Ask if the font is readable.
- **SAY** “Three lessons, one file per idea. Think of the agent as a person. Lesson 1 gives it hands: tools, files, chat. Lesson 2 gives it self-awareness: it runs its own code in a sandbox, sees the errors, fixes them, reviews itself. Lesson 3 is the brain: search the codebase, plan, delegate, run the tests, ask a human, run in parallel.”
- **SAY** “Each file is a list of cells. I run them one at a time. The agent itself lives in one Python package, src/orion_agent. The cells call it. When I say ‘open the file’, that is the package.”
- **SAY** Ishan’s wording, which landed (L218): “Always think of an agent as a human. The first lesson is where we give the human its hands and legs. The second is where we give it the brain to think on its own, reflect on its own, and improve on its own.”

### Beat 8: The curriculum site, the IDE, and the agenda (T+8)

- **SHOW** The curriculum site. Home, then Curriculum. Then the Orion IDE at localhost:5173.
- **SAY** “The site shows each piece visually, one chapter per idea. The IDE runs the same agent we build today: chat with tools on the right, files on the left, an agent mode with a plan, tests, a review and an approval dialog. Same package, two front ends.”
- **DO** In the IDE chat, type: list the files in this workspace and read config.py. Show the tool calls appear inline and the answer stream. Open the Curriculum page and read the Lesson 1 chapters aloud: LLM setup, defining tools, agent graph, code generation, system prompt and rules files, streaming, multi-turn.
- **SAY** “The graph we build in chapter 3 matters more than anything else today. Every later section is that graph with more nodes. Stay at full attention for Lesson 1 even though it looks easy.”
- **ASK** “Type excited in the chat if you want to build your own coding agent.”
- **NOTE** Nothing to share at this point. You run the code; they watch.

## Lesson 1: Hands (T+12 to T+70)

Site chapters 1.1 to 1.7. Files lessons/01_hands/ch01 to ch07. Model FAST. All generated files land in workspace/generated/.

### Beat 9: LLM setup and the model dropdown (T+12)

- **SHOW** ch01_llm_setup.py. Cell C1 (API key check) and C2 (get_llm(FAST), say hello in one sentence).
- **SAY** “You have done this. OpenRouter key from .env, ChatOpenAI pointed at openrouter.ai. get_llm wraps that one call so every lesson uses the same client. To use an OpenAI key directly, drop the openai/ prefix and the base URL. Nothing else changes.”
- **DO** Run C1, C2. Switch to site chapter 1.1. Show the model dropdown. Pick one, send say hello in one sentence, show the reply.
- **SAY** “This much code is the model dropdown in Cursor. A list of model names and one ChatOpenAI call.”
- **NOTE** Ishan’s model preferences on 9 May (L327, L954): Opus 4.6 for planning and small tasks, Sonnet 4.6 for backend APIs and system design, GPT for engineering-heavy work; he found 4.7 worse than 4.6 for planning and UI. His view that Claude models are strong at planning and front end while GPT has “the experience of a senior engineer” was contradicted by Siddharth later in the same session. If you share preferences, label them as yours on today’s date.

### Beat 10: What an agent is (T+15)

- **SAY** “One definition before tools. An LLM is a model trained on language. Text in, text out. On its own it does nothing else.”
- **ASK** “Can an LLM read a file on its own?” Fish for no.
- **SAY** “It cannot. When you upload a PDF to ChatGPT, a PDF reader tool extracts the text and hands it to the model. Web search is a tool. Reading a file, writing a file, hitting S3: all tools. So we have two things. A model that understands language, and functions that do things. An agent is the harness that lets the model call the functions. If you get this, the rest of today makes sense.”
- **SAY** “A smaller model, an SLM, is the same idea trained on less data. Text in, text out. Neither reads a file on its own.” (L368)

### Beat 11: Three tools and the @tool decorator (T+18)

- **SHOW** ch02_tools.py, cell C3: basic_tools(ws) and the loop that prints name, description and schema. Then open src/orion_agent/tools.py and scroll to read_file, write_file, list_directory.
- **SAY** “Three plain Python functions. Read a file. Write a file. List a directory. Same shape in CrewAI, in the Agents SDK, anywhere. Now look at the line above each one.”
- **ASK** “Why write @tool on top of a function that already works?” Chat will say register it, decorate it, give it a definition. All partly right.
- **SAY** “Picture an agent with a hundred tools and one task. With three tools the model rarely picks wrong. With a hundred it does. So what does the model need in order to choose? Look at read_file. Name. One parameter, filepath. Docstring: read a file inside the workspace and return its contents. Do you need the function body to know what it does? No. @tool builds a schema from the name, the type hints and the docstring. The model sees the schema. It never sees the code. That is why the docstring quality matters.”
- **DO** Run C3. Point at the printed schema for each tool: description, properties, types.
- **SAY** “One more thing in the body. Every path goes through a Workspace object that resolves it against workspace/ and refuses anything outside. An escape comes back as an error string the model can read. Cursor, Claude Code and Codex all do this. It is the first safety rule of a coding agent.”
- **SAY** Ishan’s counterfactual, if the room likes numbers (L475): “A hundred tools, a thousand lines each. That is a hundred thousand lines the model would have to read every time it picks a tool. It does not need the code. It needs the name, the parameters and the docstring.”

### Beat 12: bind_tools: the model picks, it does not run (T+24)

- **SHOW** ch03_agent_graph.py, cells C4 and C5.
- **SAY** “Model and tools are separate objects. llm.bind_tools(tools) puts them in one system. Now ask it something that needs a tool.”
- **DO** Run C4: what files are in the current directory. Print content and tool_calls.
- **ASK** “Three tools. Which one does this question need?” list_directory. It will be in tool_calls.
- **SAY** “Content is empty. tool_calls says list_directory. But nothing was listed. Hold that.”
- **DO** Run C5: what is Python. Content is a paragraph, tool_calls is empty.
- **ASK** “Why did the second one answer and the first one gave me nothing?” Expect silence. Wait ten seconds, then answer.
- **SAY** “One invoke is one turn. In the first turn the model decides which tool it needs. It does not run it. Running is a second step, and we have not built that step yet. What is Python needs no tool, so the model answered in turn one. To execute the tool we need a graph with a tool node. That is next.”
- **NOTE** This two-turn explanation is the strongest mental model in Lesson 1. Keep it close to this wording.

### Beat 13: Site 1.2: toggling tools (T+29)

- **SHOW** Site chapter 1.2. Three tool toggles.
- **DO** Disable list_directory. Ask what files are in the current directory. It says it has no tool for that. Reset, enable, ask again. It lists the workspace files.
- **SAY** “Same code, agent in the backend. No tool, no answer. Tool on, answer.”
- **SAY** “Recap so far. LLM set up, that is the dropdown. Tools defined, that is @tool and the schema. Bound to the model, but binding alone only tells us which tool it wants. Now the graph.”

### Beat 14: The first graph, drawn before it runs (T+32)

- **SHOW** [agent_loop.svg](graphs/agent_loop.svg) in a browser tab. The finished drawing: START, agent, tools, END, and the caption underneath.
- **SAY** “This is the whole graph. Two nodes. agent runs the model with the tools bound. tools runs whatever the model asked for. One edge is conditional: if the last message has tool calls, go to tools; if it is empty, END. The edge from tools back to agent is the loop. Read the caption with me: the model decides, the tool runs, the model sees the result and decides again.”
- **DO** Trace both prompts on the drawing with the cursor. ‘What is Python’: START, agent, tool_calls empty, END. ‘List the files’: START, agent, tool_calls has list_directory, tools, back to agent, answer, END.
- **NOTE** If you prefer to draw it live, open agent_loop.excalidraw at excalidraw.com, set opacity to 20 percent, and draw over it. The two steps below are the live version.
- **SHOW** ch03_agent_graph.py cell C6 on one side, Excalidraw on the other.
- **DO** Draw two circles: agent, tools. START above agent. Edge START to agent. From agent, a conditional edge: if tool_calls is non-empty go to tools, else END. Edge tools back to agent.
- **SAY** “Two nodes. agent runs llm_with_tools on the messages. tools is a ToolNode, a prebuilt node that reads the last AI message and executes the tool calls in it. The conditional edge is route. Last message has tool calls, go to tools. Empty list, we are done. That is C4 and C5 again: non-empty list, empty list.”
- **DO** Trace what is Python on the drawing: START, agent, no tool calls, END. Trace list files: START, agent, tool_calls has list_directory, tools runs it, result returns to agent, agent writes the answer, END.
- **DO** Run C6. It prints the source of build_tool_agent and compiles the graph. Walk the printed function: bind_tools, the agent node, the route, the two add_node calls, the three edges. Run C7 to draw it. Compare to the drawing.
- **WATCH** show() draws a PNG through mermaid.ink over the internet. If the network blocks it, it falls back to printing the mermaid text. Read the text or use the drawing.
- **SAY** “Nodes are where the work happens. Edges connect them. A conditional edge is a node deciding where to go next.” (L707)

### Beat 15: Run the agent and read the message trace (T+38)

- **SHOW** ch03_agent_graph.py cell C8.
- **SAY** “Two kinds of messages in a chat window. What you type is a HumanMessage. What comes back is an AIMessage. agent.invoke with one human message: list the files.”
- **DO** Run C8. Walk the printed steps in order: human; agent calls list_directory; tool returns the raw listing; agent writes the formatted answer.
- **SAY** “The first AI message is the decision, not the answer. Then the tool runs. Then the model turns the raw output into a sentence. That formatting is the agent too.”
- **DO** Run N1: the same loop from langchain.agents.create_agent, one line. Say: “What we just built by hand is what the library ships. We build it by hand so you can change it.”
- **DO** Run the same prompt in Cursor chat. Show Cursor running a list command and formatting the output.
- **ASK** “Is this clear? Just this much.” Wait for at least five yeses before moving on. Do this after every graph today.

### Beat 16: Code generation: the calculator (T+42)

- **SHOW** ch04_code_generation.py cells C9, C10. Site chapter 1.4.
- **SAY** “Now a real task. Create generated/calculator.py with a Calculator class: add, subtract, multiply, divide, a history list, get_history. There is no generated folder yet.”
- **DO** Run C9. Show workspace/generated/ appear in the file tree. Run C10 to print the file. Run the same prompt in site chapter 1.4 and show the file being created in the UI.
- **DO** Back to Excalidraw. Trace: human message; agent decides write_file; the model generates the code as the content argument; tools writes the file; tool message says File written; agent says done.
- **ASK** Someone will ask how you know the code works. Answer: “We do not yet. That is Lesson 2.” Note the name and call back to it when Lesson 2 starts.
- **NOTE** In the original run a learner (Ayan) asked “how do you even know this code works?” at this point and Ishan answered it in Lesson 2 by name (L941, L1297). If someone asks, write the name down and call it back at beat 23.

### Beat 17: System prompt and rules files (T+47)

- **SHOW** Cursor: the repo’s .cursor/rules folder and AGENTS.md in the file tree. Open python.mdc. Point at the frontmatter: description, globs, alwaysApply.
- **SAY** “You cannot change Cursor’s system prompt. You add rules on top of it, and today rules are files in the repo. AGENTS.md applies everywhere. A .mdc file applies to the paths that match its globs. Cursor reads these. So does the agent we are building. Same files.”
- **SHOW** Site chapter 1.5: two system prompts, no rules and python.mdc. Same task: DataProcessor with filter_by, group_by, summarize.
- **DO** Run with no rules. Point out no type hints, no docstrings. Run with python.mdc. Point out type hints everywhere, docstrings, PEP 8.
- **ASK** “Same task, same model. What changed?” Only the system prompt.
- **SHOW** ch05_rules.py cell N1: list_rules prints every rule file with its globs; load_rules(ROOT, 'workspace/generated/data_processor.py') assembles the system prompt for that path.
- **DO** Run N1. Read the output: a header per source, AGENTS.md first, then python.mdc because the path ends in .py. Point out that frontend-design.mdc is not in it.
- **SHOW** ch05_rules.py cell C11: build_tool_agent(llm, tools, system_prompt=SYSTEM_PROMPT); the DataProcessor request. Run it, then C12 to print data_processor.py.
- **SAY** “In code, the system prompt is one more message at the front of the list. The graph adds it for you. The text comes from the files. Change the file, every run changes.”
- **NOTE** Ishan’s own rules file, shown live (L984): never generate a Jupyter notebook, never create or edit markdown files, never create tests, no defensive checks, FastAPI conventions. Show ours (python.mdc, tests.mdc, frontend-design.mdc) and mention his as an example of how personal these get. Rules live under Cursor Settings, Rules, and in the repo; the repo copy is the one both agents read.

### Beat 18: Streaming (T+53)

- **SHOW** Cursor chat. Type write a basic calculator. Watch the tokens appear.
- **SAY** “It prints word by word. That is streaming. The model already produces tokens one at a time. invoke holds everything until the run is done. astream_events gives you the live feed.”
- **SHOW** Site chapter 1.6. Run list files in the generated directory and read calculator.py with streaming off, then on.
- **SHOW** ch06_streaming.py cell C13. Do not read it line by line. Point at three things: astream_events instead of invoke; on_chat_model_stream prints each chunk; on_tool_start and on_tool_end print when tools fire. The call is wrapped in run() because a cell cannot await.
- **DO** Run C13 with the same prompt. Let the tokens scroll. Then run N1: astream with stream_mode='messages', the short form.
- **SAY** “The code looks heavier than it is. One change, astream_events instead of invoke, and you choose which events to print. N1 is the same thing in five lines. Streaming stays off in the rest of the lessons so the code stays readable.”
- **SAY** “It is not the agent doing this. The model itself produces tokens one at a time. invoke waits for all of them. astream gives them to you as they arrive.” (L1053)

### Beat 19: Multi-turn conversation (T+58)

- **SHOW** ChatGPT tab. Ask for code, then say now explain the code. Point out the second answer uses the first.
- **SAY** “Single turn: one question, one answer. Multi-turn: the history stays and the next question builds on it.”
- **SHOW** ch07_multi_turn.py cells C14, C15. Site chapter 1.7.
- **DO** Run C14: create generated/logger.py with SimpleLogger. Show the file. Run C15: append a HumanMessage (read logger.py, add log levels and a filter method). Run. Show the same file changed in place.
- **SAY** “What changed? Nothing in the graph. I kept the messages list from turn one and appended a new human message. The agent had the full context. That is multi-turn.”
- **DO** Run N1: the same two turns with checkpointer=InMemorySaver() and a thread_id. Say: “This is the native way. The graph keeps the history for you, keyed by thread. Lesson 3 uses this everywhere.”
- **DO** Same two prompts in site chapter 1.7.

### Beat 20: Step-by-step visibility: the six-step trace (T+63)

- **SHOW** ch07_multi_turn.py cells C16, C17.
- **SAY** “One more run, printed step by step, so nobody leaves Lesson 1 with a gap. Read generated/calculator.py, then write generated/test_calculator.py with pytest tests.”
- **DO** Run C16. Walk the steps aloud. Step 0 system prompt. Step 1 human message. Step 2 agent decides read_file. Step 3 tool returns the file. Step 4 agent generates tests and decides write_file with the content. Step 5 tool writes the file. Step 6 agent says done.
- **ASK** “Take a moment. Is every step clear?” A common question: why did step 2 not create the file? Step 2 is a read. The write is step 5. Two tools, two steps.
- **DO** Run C17 to show the test file.
- **NOTE** In the original run one learner (Kuldeep, L1181) did not follow the read-then-write task. Ishan re-explained from scratch: read the calculator, then write a test file for it, two tools, two steps. Be ready to do the same.

### Beat 21: Lesson 1 recap (T+67)

- **SHOW** Site Curriculum page with the Lesson 1 chapters.
- **SAY** “LLM set up. Tools defined with @tool, schema not code, jailed to the workspace. Bound to the model: it picks, it does not run. First graph: agent, tools, loop. Code generation with write_file. System prompt from rules files. Streaming with astream_events. Multi-turn by appending, or by a checkpointer. The six-step trace. Two patterns: the agent loop and tool use.”
- **SAY** “Next: how do we know the code works? Lesson 2. Structured output, a sandbox, self-correction, reflection, rules and skills, inline edit.”
- **SAY** “Real systems get built by solving one problem after another. Small pieces coming together.”

### Beat 22: Break (T+70)

- **DO** Five minutes. Timer on screen. Ask for back in chat when you return and count. Do not run C18 (it resets the workspace).

## Lesson 2: Self-awareness (T+75 to T+135)

Site chapters 2.1 to 2.5. Files lessons/02_self_awareness/ch08 to ch12. Model FAST.

### Beat 23: Agenda for Lesson 2 (T+75)

- **SAY** “Five things. Structured output and why we need it. A sandbox that runs the code. A conditional retry loop, which is how you send the graph back to an earlier node when you are not happy with the result. A reflection node. Rules scoped by path, and skills the agent loads on demand. Then inline edit, which looks impressive and is small.”
- **DO** ch08_structured_output.py: run C1, C2 (say ready if you can hear me).
- **SAY** “Still the fast model. Cheapest model for demos. Do not spend tokens on experiments.”
- **NOTE** Ishan withheld the notebooks on the day (L322, L1312) and gave the reason at the end. Not relevant now: you run the code, nothing is handed out during the session.

### Beat 24: Structured output: raw vs structured (T+78)

- **SHOW** Site chapter 2.1 with the raw/structured toggle. Then ch08 cell C3.
- **DO** On the site, set raw. Ask write a Python function that checks if a number is prime. Show one blob: prose, code, example, more prose. Run C3 and show the same blob in the interactive window.
- **SAY** “One string. Code, explanation, example, mixed. I want the code in a file. Pulling it out of this with regex is a bad job.”
- **DO** Site: set structured. Same question. Show explanation and code in separate boxes.
- **NOTE** Do not say ChatGPT shows code blocks because of structured output. That is markdown rendering. Structured output is the model returning a typed object, which the next cell shows.
- **SHOW** ch08 cell C4: CodeOutput(BaseModel) with code and explanation, from src/orion_agent/schemas.py; structured(llm, CodeOutput).
- **SAY** “This looks complex the first time. It is not. I want two things back, code and explanation. So I define a class with two fields. Each field has a description so the model knows what goes where. Then instead of llm.invoke I call structured(llm, CodeOutput).invoke. structured is with_structured_output with one setting fixed: function calling, because that is the one method every provider on OpenRouter supports.”
- **DO** Run C4, C5 (type is CodeOutput, not str), C6 (result.explanation), C7 (result.code).
- **SAY** “result.code is the code. I can write it straight to a file. That is the reason for all of this.”
- **ASK** Someone may ask whether Pydantic costs more tokens. The schema goes in the prompt, so twenty fields cost more than two. For two fields it is negligible.

### Beat 25: Execute: the sandbox (T+85)

- **ASK** “What does Cursor do to check whether the code it wrote works?” It runs it.
- **SHOW** A terminal. python -c "print('hello world')". Then python -c "print(1/0)". Show ZeroDivisionError.
- **SAY** “python -c runs whatever string you give it. subprocess lets me run that from inside Python. The question is how.”
- **SHOW** ch09_self_correction.py cell C8: sandbox = LocalSandbox(). Open src/orion_agent/sandbox.py. Point at four things: sys.executable -I, the scrubbed environment (PATH and HOME only), the temp working directory, and the except TimeoutExpired that returns a result.
- **DO** Run C9 (hello world: stdout set, returncode 0, ok True). Run C10 (1/0: stderr traceback, returncode 1). Run N1: time.sleep(20) with a 3-second timeout. Show timed_out True, no exception.
- **SAY** “One terminal line wrapped in a function, with the accidents removed. The code cannot read my API key from the environment. It cannot import from my user site-packages. It runs in a temp folder. And a hang becomes a failed attempt instead of a crash.”
- **DO** Run N2 and read it: “This is a jail, not a sandbox. It does not stop network access or resource exhaustion. Claude Code uses Seatbelt on macOS and bubblewrap on Linux. Codex the same, network off by default. Cursor’s cloud agents run in Firecracker microVMs. DockerSandbox in sandbox.py is the stub to fill in when you need that.”
- **WATCH** This still runs model-written code on your laptop. Give it safe tasks. A timeout no longer crashes the graph, so a sleeping task is fine to demo.
- **ASK** Someone may ask about pip install. The sandbox sees the repo’s virtual environment. The code can only use what is installed there, which matters in the next demo.
- **NOTE** Ishan on the environment (L1555): everything the sandbox can import is what is installed in the venv. He restricted the agent from installing packages on purpose (L1789) so the hard task in beat 28 fails honestly. Python because “it is the easiest one to teach”; compiled languages need a build step in the sandbox.

### Beat 26: Agent state (T+90)

- **SHOW** ch09 cell C11: prints the AgentState fields: task, code, explanation, execution_result, error, attempts, max_attempts, status, rules.
- **SAY** “The graph is now complex enough to track state. At every node I want to know the task, the code so far, the explanation, what happened when it ran, the error if any, how many attempts, the cap, a status, and any rules. The whole state goes into every node. Every node returns only the fields it changed.”
- **SHOW** ch09 cell C12: prints the source of _generate_prompt and _make_nodes: generate (adds the previous error to the prompt if present, increments attempts), execute (calls sandbox.run_python, sets status), should_retry (success, retry, give_up).
- **DO** Run C11, C12. Read the printed source, not the file.
- **ASK** Someone may ask how the LLM knows what to put in the state when the fields have no descriptions. It does not. I fill the state myself in each node’s return dict. The model only sees the prompt.

### Beat 27: Draw the self-correcting graph with a state table (T+94)

- **SHOW** [self_correction.svg](graphs/self_correction.svg). Left: START, generate, execute, give up, END, with the dashed retry edge. Right: the state table, already filled.
- **SAY** “Generate writes code. Execute runs it in the sandbox. Three exits from execute. Success: END. Failed with attempts left: the dashed edge back to generate, and the error goes into the prompt. Failed at max: give up, then END. That dashed edge is the whole idea of self-correction.”
- **DO** For the row-by-row fill, use self_correction.excalidraw with the cell text cleared (docs/graphs/README.md explains). Fill it as the room answers. Come back to the SVG for the finished table.
- **SHOW** Excalidraw.
- **DO** Draw START, generate, execute. Edge START to generate, generate to execute. From execute a decision with three exits: success to END; failed and attempts below max back to generate (label it retry); failed at max to a box give up, then END.
- **SAY** “Generate writes code. Execute runs it. Three outcomes. It ran: end. It failed with attempts left: back to generate with the error. It failed three times: give up.”
- **DO** Draw a state table beside it with columns task, code, expl, error, attempt. Fill it row by row and ask the chat before each cell.
- **ASK** “At START, which fields have values?” Only task, attempt 0. “After generate?” code = func_v1, explanation filled, attempt 1. “Is error filled after generate?” No, generate cannot run code. “After execute, say it fails?” error = traceback_v1. “Back to generate. Attempt?” 2. “Does generate know the error?” Yes, it is in the prompt. code = func_v2. Continue to v3 and success.
- **SAY** “v1 fails, v2 fails with a different error, v3 passes. If v3 had failed, give up.”
- **ASK** “Max attempts is your choice. I do not go past three or four. Why?” If a current model cannot fix it in three tries, something else is wrong and a person should look. That is human-in-the-loop, Lesson 3.
- **DO** Remind people to eat and drink water. The next hour is dense.
- **SAY** Ishan’s rule of thumb (L1754): “I do not go over three or four. Most models get it in one shot now. If it cannot do it after three tries there is some issue I need to get into.”
- **NOTE** Max attempts can be counted per node or per system (L2132). This graph counts per system: generate, execute and review share one counter.

### Beat 28: Compile, run easy, run hard (T+101)

- **SHOW** ch09 cells C13 (build_bugbot), C14 (draw). Site chapter 2.2 with the easy/hard task selector.
- **DO** Run C13, C14. On the site pick the easy task, print first 10 Fibonacci numbers. Run the self-correcting agent. Show success on the first try. Pick the hard task, stable diffusion with the diffusers package. Run. Show three failed retries.
- **ASK** “Why did it fail three times when the code it wrote is correct?” diffusers is not installed and the agent has no tool to install packages. Same error every time. Retrying cannot fix an environment problem.
- **DO** Run C15 (bugbot.invoke, Fibonacci, attempts 0, max 3). Show status success, attempts 1, structured code and explanation. Run C16 (diffusers task via bugbot.stream). Read the stream: generate attempt 1, execute FAILED ModuleNotFoundError, attempt 2 FAILED, attempt 3 FAILED.
- **SAY** “The graph is named bugbot on purpose. Run it, catch the error, fix it, bounded. That is the Cursor feature.”
- **ASK** “Clear to everyone? I want each of you to respond.” Wait.
- **NOTE** The diffusers failure is deliberate, not a bug (L1779). Say so before you run it, or the room will think the demo broke.

### Beat 29: The reflection question (T+108)

- **ASK** “Execute tells us the code runs. Is that enough?” Fish for no, it can run and still be bad code.
- **SAY** “I can write a function with single-letter variables, no types, no docstrings, and it runs. Nothing in execute checks quality. So we add a node that reflects on the output. That is the reflection pattern.”
- **SHOW** ch10_reflection.py cell C17: ReviewResult(approved, feedback); structured(llm, ReviewResult); the test on x = [1,2,3] / for i in x: print(i).
- **DO** Run C17. Approved: False. Read the feedback aloud: no type hints, single-letter names, not PEP 8.
- **SAY** “The code works. The reviewer rejects it. Two outputs: approved, true or false, and feedback that goes back to the generator.”

### Beat 30: Draw the full graph: generate, execute, review (T+112)

- **SHOW** [self_correction_with_review.svg](graphs/self_correction_with_review.svg). The reviewer node added below execute; two dashed edges back to generate; the second state table on the right.
- **SAY** “One node added, review, and one new dashed edge: rejected, the feedback goes into the prompt. Everything else is the drawing you already know. Execute proves the code runs. Review judges whether it is good. Both kinds of feedback, an error or a rejection, land in the same place: the next generate prompt.”
- **NOTE** The both-orders cost argument is not on the SVG. Draw order A and order B on a blank Excalidraw canvas as scripted below.
- **SHOW** Excalidraw, fresh area. ch10 cell C18 for reference: it prints the FullAgentState fields and the source of build_full_agent.
- **DO** Draw START, generate, execute, review. Edges START to generate, generate to execute. Then rapid-fire the remaining edges with the chat.
- **ASK** “At execute and it passed. Where do I go?” review. “At execute and it failed?” generate. “Failed three times?” give up, END. “At review and approved?” END. “At review and rejected?” generate, with feedback. There is no give-up branch after review in this graph; the attempts counter is shared.
- **ASK** Someone will ask why not review before execute. This exchange got the strongest response in the original session, so give it three minutes. Draw both orders. Order A: generate, execute, review. Order B: generate, review, execute. Max attempts three, execution fails twice. In A the reviewer runs once. In B it runs three times, twice on code that did not work. “You paid for reviews of broken code. At scale that is real money, and production systems have several reviewers, not one. Lesson 3 takes this one step further: tests run before the reviewer sees anything.”
- **SAY** “Same generate node as before. One difference: the prompt now also carries review_feedback when the reviewer rejected. Read it in the printed source.”
- **DO** Second state table: task, code, error, review, attempt. Walk it. Attempt 1 code v1, execute fails, error tb_v1. Attempt 2 code v2, execute passes, review rejects with feedback_1. Attempt 3 code v3, execute passes, review approves, END.
- **ASK** “Max attempts three and the review fails on the third?” The graph stops and reports the last state with max attempts reached. It does not loop. You can count attempts per node or per system. This graph counts per system.
- **NOTE** Ishan’s exact line (L1927): “Something should first work for me to be able to review it. Otherwise I ran the review node three times, which is tokens wasted on something that did not even work.”

### Beat 31: Run the full agent and trace it (T+121)

- **DO** Run C18, C19 (build_full_agent), C20 (draw). Run C21: Sieve of Eratosthenes up to 50. Show status approved after N attempts, output, code. Run C22: the Point dataclass task via stream. Read generate, execute OK, review approved, or needs_revision and then the second pass.
- **WATCH** C22 may approve on the first pass, which makes the trace short. Say so and move on. Do not rerun hoping for a rejection.
- **SAY** “At home, give it tasks that fail execution or fail review and read the trace. That is where you learn the graph.”

### Beat 32: Rules by path, and skills on demand (T+126)

- **SHOW** ch11_rules_and_skills.py cell C23: load_rules for workspace/app.py and for workspace/tests/test_sort.py; the sort-a-list-of-dicts task run with the test-file rules.
- **SAY** “Rules are the system prompt idea again, but two things are new. They come from files, and they are scoped by path. tests.mdc only applies to test files. So the same agent gets stricter rules when the target is a test than when it is app code. The rules go into the state, and generate puts them at the front of the prompt.”
- **DO** Run C23. First the two booleans: tests.mdc is in the rules for the test path and not for app.py. Then the output: type hints, Google docstrings, comprehensions, descriptive names, a main guard.
- **SHOW** Cursor: Customize, then Skills. The repo’s .cursor/skills folder: add-feature, web-research, frontend-design, commit-deploy. Open add-feature/SKILL.md. Point at name and description in the frontmatter.
- **SAY** “A rule is always on. A skill is a playbook the agent loads when it needs it. The agent sees one line per skill, the description. When a description matches the task it calls read_skill and the full body arrives. That is how Cursor and Claude Code do it too, and it keeps the context small.”
- **DO** Run N1: the skills catalog, three lines. Point out commit-deploy is not listed; it is marked manual, a slash command, not something the model picks. Run N2: an agent with only read_skill, asked to add a feature safely. Read the trace: the agent calls read_skill('add-feature'), the tool returns the body, the agent lists the steps.
- **ASK** “Why not put all four skills in the system prompt?” Context. Four skills is fine. Forty is not. Load what you need when you need it.

### Beat 33: Inline edit: Cmd+K (T+128)

- **SHOW** Cursor. Select a block of code. Cmd+K. Type an instruction. Show the in-place diff.
- **ASK** “Who has used this? Select code, Cmd+K, type what you want.”
- **SHOW** Site chapter 2.5: the greet() function. Select it, Cmd+K, add type hints, docstring, optional greeting param, return instead of print, add tests. Edit selection.
- **SAY** “Selecting the code copies it into a variable. Cmd+K opens a box. Your instruction plus the copied code become the task. Then it is the same full_agent.invoke as before.”
- **SHOW** ch12_inline_edit.py cell C24: existing_code string inside the task prompt.
- **DO** Run C24. Show the modified code and tests.

### Beat 34: Rules plus inline edit (T+131)

- **SHOW** ch12 cell C25: legacy CSV reader, MODERNIZE_RULES.
- **DO** Run C25. Show context manager, pathlib, type hints in the output.
- **SAY** “This one is for you to try after. Legacy code plus a modernisation rule set.”

### Beat 35: Lesson 2 recap (T+133)

- **SHOW** Site Curriculum page, Lesson 2.
- **SAY** “Structured output, so code and explanation come back separately. A sandbox from one terminal command with the accidents removed. The self-correcting graph. Two tasks, one passed, one could not. A reviewer, the reflection pattern. Why execute comes before review. Rules from files, scoped by path. Skills loaded on demand. Inline edit is copy the selection and invoke. Three patterns: prompt chaining, reflection, exception handling.”
- **SAY** “Lesson 3 puts it together. Search over the codebase, tools from an MCP server, a planner, planner-coder-reviewer, tests before review, a human gate where I stop the graph and approve or reject with a reason, parallel generation, and time-travel debugging.”
- **ASK** “How are you feeling? Can you follow?” Then: “I am not taking many questions now so the flow holds. Write them down. Q&A at the end.”
- **SAY** “If you understood this drawing, you can hand it to Cursor and it will write the code.”
- **NOTE** At this point in the original run a learner said “it is a little overwhelming for the first time” (L2343). Expect it. The answer that worked: “You do not need to remember the syntax. Remember the drawing. The syntax you can hand to Cursor.”

### Beat 36: Break (T+135)

- **DO** Ten minutes. Tell people to eat. Timer on screen. Roll call in chat when back.

## Lesson 3: Brain (T+145 to T+215)

Site chapters 3.1 to 3.6. Files lessons/03_brain/ch13 to ch18. Model STRONG. The agent works on workspace/: app.py, chat.py, config.py, test_app.py. ch16, ch17 and ch18 share one agent when they run in the same interactive window.

### Beat 37: Lesson 3 agenda and the new APIs (T+145)

- **SAY** “Final lesson. Search over the codebase. A toolkit that includes tools from an MCP server. A planner. The full multi-agent graph with tests in it. Human in the loop. Parallel generation. Time travel. Four new LangGraph APIs. interrupt and Command pause the graph and resume it with my decision. InMemorySaver checkpoints state, so if the run dies at attempt three you resume from attempt three. Send fans one node out into parallel copies. Reducers merge the parallel results.”
- **DO** ch13_codebase_search.py: run C1, C2 (say Agent Mode activated). Say you switched to the stronger model for this lesson.
- **ASK** Ishan opened Lesson 3 with a callback (L2534): “How many of you did the LangGraph and LangChain assignment from yesterday? Did you find it hard?” Ask it. The graph we build now is that assignment with more nodes.
- **SAY** Connect the dots (L2307, L2479): “Remember the RAG sessions and Atlas. Atlas was a much bigger version of what the embeddings cell does. Today you also learn when not to reach for it.”

### Beat 38: Part 1: the codebase brain (T+148)

- **SHOW** Cursor. Ask in chat: how does streaming work in this project, in brief, without naming a file. Watch the tool calls: it greps, it reads chat.py, it answers.
- **SAY** “Did I name a file? No. Cursor searched. Not with an index. With grep, then read. That is what every shipped coding agent does now: Cursor, Claude Code, Codex. A model with grep in its hands.”
- **SHOW** workspace/: app.py, chat.py, config.py, test_app.py. Open each for a few seconds.
- **SAY** “The sample project is the Streamlit ChatGPT clone from day 3. Three files and a test file. config has the model name and base URL. chat has get_client and stream_response. app is the UI. The tests check config and chat without importing app.”
- **SHOW** ch13 cell C3: ws.grep('stream'), repo_map(ws), search_codebase(ws, 'streaming chat response').
- **DO** Run C3. Read the grep hits with line numbers, then the repo map (one line per file with its functions), then the ranked search result.
- **SHOW** ch13 cell C4: build_tool_agent with grep_files, glob_files, read_file, asked how streaming works.
- **DO** Run C4. Walk the trace: agent calls grep_files, reads chat.py, answers with the file and the function.
- **SAY** “No index to build, no embeddings to pay for, nothing to keep fresh. The model decides what to search and what to read. Chapter 3’s loop with three different tools.”
- **DO** Run N1: the same question through embeddings and InMemoryVectorStore. Read the printed note. Say: “This is how Cursor did it from 2023 to 2025. It turned that index off. You built the bigger version in the RAG sprint. Keep it for documents; for code, grep won.”
- **WATCH** N1 calls the embeddings endpoint on OpenRouter. If it fails, skip it and say the sentence anyway. Before the session, uv run orion reset so the workspace is clean.
- **SAY** For the embeddings footnote, Ishan’s explanation of chunking (L2510): “Chunking means splitting a file into overlapping pieces, lines 1 to 4, 4 to 8, 8 to 10, before embedding, so a search hit comes back with its neighbours.” One sentence, then move on.

### Beat 39: Part 2: the toolkit, and tools from MCP (T+156)

- **SHOW** ch14_toolkit_and_planner.py cell C5: make_tools(ws, sandbox) plus aget_mcp_tools(); the printed list.
- **SAY** “The local toolkit: read, write, list, grep, glob, run_python in the sandbox, and run_command, which takes an argument list, never a shell string. Then two more that did not come from our code: web_search and web_fetch. They come over the Model Context Protocol from Parallel’s search server. One URL in a config, and they bind like any other tool.”
- **DO** Run C5. Read the names. Open .cursor/mcp.json: the same server, one line, so Cursor’s agent has the same tool.
- **DO** Run C6: run_command with python -c import config; print(config.PAGE_TITLE, config.MODEL). Show the title and model print.
- **DO** Run N1: a research agent with grep, read, web_search and web_fetch, asked to check chat.py against the current OpenAI streaming API. Read the trace: web_search, then read_file, then an answer that cites a URL.
- **WATCH** N1 needs the network. The search server needs no key. If it is down, say what the cell does and move on. Mute your phone; “cd to this project” read aloud can trigger Siri.

### Beat 40: Part 3: the planner (T+160)

- **SHOW** ch14 cell C7: FileTask(filepath, description, action) and Plan(summary, file_tasks) from schemas.py; structured(llm, Plan); a one-shot plan for add a system prompt setting.
- **SAY** “Until now the agent went from task straight to code. Cursor plans first. Two Pydantic structures. Plan has a summary and a list of file tasks. Each file task says which file, what to do, and whether to create or modify.”
- **DO** Run C7. Read the output: the summary; then [modify] config.py add DEFAULT_SYSTEM_PROMPT; [modify] chat.py; [modify] app.py add sidebar text area.
- **ASK** “Is the planner clear? It only says, per file, what to change and whether the file exists.” Wait.
- **SAY** Ishan’s line here (L2752): “The planner only tells me, file by file, what has to change. Hold onto the graph. Once you see the whole thing working it will make a lot more sense.”

### Beat 41: Part 4: orchestrator state (T+164)

- **SHOW** ch14 cell C8: OrchestratorState fields: feature_request, codebase_context, plan, file_tasks, generated_code, test_output, test_attempts, review_result, review_attempts, human_decision, human_feedback, status, error.
- **SAY** “Same idea as the Lesson 2 state, different fields. The task. The context the planner found. The plan and the per-file tasks. The generated code, replaced on each pass so stale code does not pile up. Then two counters, one for test rounds and one for review rounds, and two pieces of feedback: what the reviewer said and what the human said.”
- **DO** Run C8.

### Beat 42: Part 5: three specialist nodes (T+167)

- **SHOW** ch15_specialists.py cells C9, C10, C11. Each prints a prompt or a node’s source.
- **SAY** “Three nodes. The planner runs the chapter 3 loop with grep, glob, read and read_skill to gather context, then asks for a Plan, and checks every planned path against the workspace before anything else runs. The coder generates one complete file per task. The reviewer sees only the files and the test output, with no memory of how they were written.”
- **DO** Run C9: the research prompt, the plan prompt, and check_task_paths. Run C10: build_code_prompt, then an example prompt for a task in the needs_revision state. Read the sections aloud: the file task, the rules that apply to that path, the codebase context, and Reviewer feedback with the reviewer’s sentence in it. Run C11: the review prompt and run_tests.
- **SAY** “This is the part that makes the loop real. The reviewer’s feedback lands in the coder’s next prompt. A failing test lands there too. So does the human’s reason for rejecting. If feedback never reaches the node that acts on it, you have a loop that spins, not one that improves.”
- **ASK** “Why does the reviewer get fresh context?” The node that wrote the code should not be the one grading it. It will agree with itself.
- **NOTE** Ishan ran three nodes and dropped the execute node “because it is already getting complex” (L2775). Ours keeps a test node instead, and the loop feedback is real now (Appendix C, beat 42).

### Beat 43: Part 6: human-in-the-loop (T+172)

- **SHOW** ch16_human_in_the_loop.py cell C12: prints the source of human_review_node. The payload dict, decision = interrupt(payload), and the two returns: approve, or reject with the feedback and both counters reset to zero.
- **SAY** “Everything so far ran on its own. I did not touch anything between plan and review. Here I have to give an input. So I interrupt the graph. interrupt(payload) stops execution and hands the plan, the file previews, the test output and the review back to whoever called invoke. The state is frozen by the checkpointer. It moves again only when I resume with a decision. Approve, or reject with a sentence. The sentence goes to the coder verbatim, and the counters reset so the reviewer gets a fresh look at the new code.”
- **SAY** “Apply writes the generated code into the real files. Until then it only exists in state. Then verify runs the tests once more on the real files. A real agent runs pytest; ours does too.”
- **DO** Run C12.
- **SHOW** Cursor. Cmd+K on a small function, add an option, show the Accept and Reject bar.
- **SAY** “The accept button is apply. Reject leaves the file as it was.”
- **SAY** Ishan’s definition of apply (L2856): “Until here the code is just plain text in the state. Apply is what puts it in your files.” And of interrupt (L2826): “Here I need to give an input manually. Approved or rejected. That is why I have to interrupt the graph, give my feedback, and then it can resume.”

### Beat 44: Part 7: draw the full graph (T+177)

- **SHOW** [orchestrator.svg](graphs/orchestrator.svg). Seven nodes left to right; four dashed routes; the path check from plan to a second END; the caption.
- **SAY** “Read it left to right. plan, code, test, AI review, human review, apply, verify. Tests run on a copy before anyone reviews. Only passing code reaches the AI reviewer. Only reviewed code reaches me. Now the dashed edges, which are the routes back: test to code with the traceback; AI review to code with the feedback; human review to code with my reason, and the counters reset. One more: test at the cap goes straight to me, so I see the failures. And plan can end the run on its own if a planned file is outside the workspace.”
- **DO** Run the rapid-fire routes below with the drawing on screen, pointing at each edge as the room answers.
- **NOTE** Draw it live only if the room is fresh. Otherwise show the SVG and spend the drawing time on the routes and the state table.
- **SHOW** Excalidraw. ch16 cell C13 for reference.
- **DO** Draw START, plan, code, test, AI review, human review, apply, verify, END. Edges: START to plan, plan to code, code to test. Conditional at test: pass to AI review, fail with attempts left back to code, fail at the cap to human review. Conditional at AI review: approved to human review, else back to code (auto-approve after two). Conditional at human review: approve to apply, reject back to code. apply to verify, verify to END. One more: plan can end the run if a planned path escapes the workspace.
- **ASK** Rapid-fire. “At test, passed?” AI review. “Failed, attempts left?” code, with the traceback. “At AI review, approved?” human review. “Rejected?” code, with the feedback. “At human review, I approve?” apply. “I reject?” code, with my reason. “After apply?” verify. “After verify?” end.
- **SAY** “Plan decides the file-level changes. Code generates them. Test runs them on a scratch copy. AI review reads them with fresh eyes. Human review is me. Apply writes them. Verify runs the tests on the real files.”
- **DO** Run C13 (demo_orchestrator; the print says 7 nodes, 4 conditional routes, checkpointing enabled, then the node names). Run C14 for the diagram. Compare to the drawing.

### Beat 45: Part 8: watch it think, then pause (T+183)

- **SHOW** ch16 cell C15: thread_id demo-1; the feature request to add a system prompt across config.py, chat.py, app.py.
- **DO** Open workspace/config.py, chat.py, app.py first and show there is no system prompt anywhere. Run C15.
- **SAY** “Read the console. Plan: modify three files. Code: three files generated. Test: pytest on a copy, three passed. Review: needs revision, so code runs again, or approved. Then: agent paused, waiting for human review, and the payload printed: plan, review, tests, files.”
- **DO** Open config.py again. Show DEFAULT_SYSTEM_PROMPT is not there.
- **ASK** “The agent says it added DEFAULT_SYSTEM_PROMPT. I open the file and it is not there. Why?” We have not applied it. It is only in state. The tests ran on a copy.
- **DO** Run C16: aget_state. Show next is human_review, then every generated file in full.
- **SAY** “This is what I read before anything touches disk. Now my call.”
- **WATCH** If the generated code looks wrong, do not rerun from scratch. Say “this is the run where the human rejects,” resume with decision reject and a reason, and let it regenerate. That is the feature; beat 47 has the scripted version on a copy.
- **WATCH** In the original run this demo misfired once (L3021) and a mentor said the fix was a stronger model. STRONG is already set for Lesson 3. If a run still goes wrong, use beat 47’s reject path rather than restarting.

### Beat 46: Approve, apply, verify (T+189)

- **SHOW** ch16 cell C17: agent.ainvoke(Command(resume={'decision': 'approve', 'feedback': ''}), config) through run().
- **DO** Run C17. Show status done and the test output: pytest, 3 passed, on the real files. Run C18 to print all three files. Open config.py in the editor: DEFAULT_SYSTEM_PROMPT is there. chat.py: system_prompt parameter. app.py: sidebar text area.
- **SAY** “Now the changes are on disk. Before approve, the agent proposed. After approve, it acted, and it checked its own work once more.”

### Beat 47: Trace the state, then reject with a reason (T+192)

- **SHOW** [orchestrator_state.svg](graphs/orchestrator_state.svg). Twelve rows, one per node the run passed through, with the two counters in the last column.
- **SAY** “One run, row by row. START: only the request. plan: three files to modify. code: v1 of each, not on disk. test: three passed, on a copy. AI review: rejected, reason one. Now the row that matters: code again, v2, written with that reason in the prompt. test passes, AI review approves, human review: I approve. apply writes the files. verify runs the tests on the real files. END. Watch the last column: tests two, reviews two.”
- **SHOW** Excalidraw state table: feature_request, plan, code, test, AI review, human, attempts.
- **DO** Walk it. START: only feature_request. plan: modify config.py, chat.py, app.py. code: v1 of each, not on disk. test: 3 passed on a copy. AI review: rejected, reason_1. Back to code, review attempt 2: v2. test: passed. AI review: approved. Human review: I approve. apply: files written. verify: 3 passed. END.
- **SHOW** ch16 cell N1: a second thread on a snapshot copy of the workspace, a small feature (PAGE_SUBTITLE), then resume with decision reject and feedback: call it TAGLINE, under 40 characters.
- **DO** Run N1. Read: paused with the first proposal; after the reject, both counters back to zero, and the new preview uses TAGLINE.
- **SAY** “A reject alone sends the coder back to the same prompt. A reject with a reason changes the prompt. That sentence is the most valuable input in the whole graph.”
- **ASK** “Is the whole flow clear now?” Wait.

### Beat 48: Part 9: parallel code generation with Send (T+196)

- **SHOW** [parallel_coders.svg](graphs/parallel_coders.svg). plan, three code_file copies side by side, collect, END, with Send on each fan-out edge and the reducer named on the merge.
- **SAY** “Same node, three copies, different inputs. fan_out_to_coders returns one Send per file task. They run at the same time. The reducer, add_to_list, merges the three results into one list. This is the only reducer of the day; MessagesState was using one all along for messages.”
- **ASK** “The plan says three files. Code generated them one after another. They are independent. What if I want all three at once?”
- **SHOW** ch17_parallel.py cell C19: a snapshot copy of the workspace; ParallelState with generated_code: Annotated[list, add_to_list]; the source of add_to_list and build_parallel_agent (plan_node, fan_out_to_coders returning a Send per task, code_file, collect_results).
- **SAY** “LangGraph has Send. fan_out_to_coders takes each file task and sends it to its own copy of the code_file node. They run at the same time. The reducer add_to_list merges their outputs into one list. This is the only place today we need a reducer. The demo works on a copy so the files we just approved stay as they are.”
- **DO** Draw it: START, plan, three code nodes side by side (config, app, chat), collect, END.
- **SAY** “Same node, three copies, different inputs. One line does the fan-out.”
- **DO** Run C19, C20 (compile and draw), C21 (feature: export button and model selector). Show the three results. Run C22: apply to the copy, then run the tests there.
- **WATCH** C22 writes to the snapshot copy only. The real workspace is untouched, which is what ch18 needs.

### Beat 49: Part 10: time travel (T+203)

- **SHOW** ch18_time_travel.py cell C23: agent.get_state_history(config), printing status, files, test and review counters, and next per checkpoint.
- **SAY** “Every step of demo-1 was checkpointed. This walks the history: planned, coded, tests passed, approved, human approved, applied, done. You can see what it planned, what it generated, what the tests said, what the reviewer said, what I decided.”
- **DO** Run C23. Read the steps.
- **NOTE** N0 only does something if demo-1 has no history in this kernel, which happens when you restarted the interactive window after ch16. Then it replays the feature and takes a few minutes. Run it before the session if you plan to restart.

### Beat 50: Part 11: second feature end to end (T+207)

- **SHOW** ch18 cell C24: thread demo-2, Clear Chat button and message counter, streamed; C25 approve; C26 final file summary.
- **DO** Run C24. Read PLAN, CODE, TEST, REVIEW, PAUSED. Run C25 (approve). Show the tests pass. Run C26.
- **SAY** “New thread, same architecture, different feature. Plan, code, test, review, pause, approve, apply, verify.”

### Beat 51: Lesson 3 recap: the pattern table (T+211)

- **SHOW** Site chapter 3.6, or the Curriculum page, Lesson 3.
- **SAY** “Codebase search with grep in the loop: knowledge retrieval, done the way the tools do it now. Tools from an MCP server: tool use as configuration. Structured planning: planning. Per-file generation: multi-agent. Tests before review: verification. AI review with a retry cap and fresh context: reflection plus exception handling. Human approval with a reason: human-in-the-loop. Parallel files: parallelisation. Checkpoints and time travel: memory management. Conditional edges: routing.”

## Close (T+215 to T+240)

### Beat 52: The full recap, first graph to last (T+215)

- **SHOW** The six drawings in browser tabs, in order: agent_loop, self_correction, self_correction_with_review, orchestrator, orchestrator_state, parallel_coders. Flip through them in twenty seconds.
- **SAY** “Two nodes. Then a loop with a retry. Then a reviewer. Then seven nodes with a human in the middle. Then three copies at once. Same shape every time: a node, and a function that reads the state and picks the next node.”
- **SHOW** Site Curriculum page. Scroll from 1.1 to 3.6. Then the Excalidraw canvas from the two-node graph to the seven-node graph.
- **SAY** “We started here: agent, tools, a loop. We ended here: plan, code, test, review, human, apply, verify, in parallel, with checkpoints. Everything in between was the first graph with more nodes.”
- **SAY** “Lesson 1, hands. Lesson 2, self-awareness. Lesson 3, brain.”
- **ASK** “Are you all alive? Did you get something from seeing how this is built, rather than one agent that does one thing?”
- **NOTE** Do not announce the chapter count as an achievement. Eighteen chapters said out loud makes the tired half of the room feel worse.
- **ASK** A learner said at this point (L3312): “How to remember syntax? I do not remember syntax anymore.” Answer: “You do not. You remember the drawing. Nine graphs today, one shape. The syntax is what you hand to Cursor.”
- **NOTE** Ishan (L3297): “Knowingly I did not tell you at the start that we are covering 18 chapters. People would have stopped.”

### Beat 53: One book (T+219)

- **SAY** “One book on agentic design patterns covers the pattern names you heard today, one chapter each, with code. Link in the chat. Go deeper there.”
- **NOTE** Name the book you mean and check the link before the session. Do not say the session covered the book.
- **NOTE** Ishan called it a gold mine and said the session covered its 400 pages in four hours (L3346). Do not repeat that claim. One book, one link.

### Beat 54: Connect the dots: the 14 days (T+224)

- **SHOW** The sprint slides. Sprint 1 prompt engineering and automations. Sprint 2 full-stack open-source apps, Gradio, Hugging Face, multimodal. Sprint 3 RAG and vector databases. Sprint 4 agents, LangChain, LangGraph, LangSmith. Sprint 5 OpenClaw deployment, cost, Claude, MCP. Sprint 6 today. Sprint 7 hackathon.
- **SAY** “Fourteen days. The RAG from sprint 3 is the embeddings cell you saw, and you now know when grep beats it. The graphs from sprint 4 became the orchestrator. The MCP from sprint 5 is where web_search came from. The deployment from sprint 5 is how Orion runs on Discord. Today is where they connect.”

### Beat 55: The roadmap (T+228)

- **SHOW** The base-camp slide, then the four-level roadmap.
- **SAY** “You are at base camp. Higher than most people around you. Not the summit. Four levels from here. Level 1, ML fundamentals, so you can tell when a problem does not need an LLM. Level 2, RAG depth: hybrid retrieval, chunking, semi-structured data, SQL. Level 3, multimodal processing, model architecture, evals, MCP. Level 4, agent frameworks compared, routing and error handling, cloud infra for LangGraph. Across all of them: small language models, evals, fine-tuning versus RAG, production reliability, deployment, CI/CD with offline evals, scaling, inference optimisation. The tests-before-review order you saw today is one optimisation.”
- **NOTE** Four minutes, not eight. The slide carries the detail.
- **SAY** Ishan’s frame (L3474): “The accelerator is the top of the T. Broad, so you can see the whole field the way an AI-native engineer sees it: advanced prompting, multimodal, autonomous agents, production RAG. The roadmap is the depth.”

## Program pitch, Q&A, hackathon (T+240 to T+285)

### Beat 56: Generative AI Engineering Program (T+240)

- **SAY** “One minute on what is next, then your questions. Six-month weekend program, production-level, capstone with a demo day. Accelerator alumni price and a form for a call are in the chat. Decide by Wednesday if you want the alumni price.”
- **NOTE** Keep it to five minutes at the very end, with a link and an optional call. If leadership wants the full block, run it after Q&A so the people who came for the content get their questions first. Check every claim before repeating it.

### Beat 57: Q&A (T+245)

- **SAY** “The questions you parked. Go.”
- **ASK** Take questions in chat order, two minutes each. Program questions go to the form. Likely questions: is this for a DevOps person; which of Claude Code, Codex, Cursor to use; hitting subscription limits; open-source models; recordings from other mentors; is the repo shared. Have a one-line answer ready for each.
- **NOTE** Ishan’s answers on 9 May, for reference. DevOps person (L4094): “The era of specialisation is over; non-engineers on my team ship code with these tools now.” Hitting limits (L4309): “Use Cursor, switch between Claude and GPT, and let sub-agents run on the cheaper composer models; I have never hit a limit on the ultra plan.” Which tool (L4497): “Codex for software engineering. Opus 4.6 for UI design and refinement. 4.7 is twice the price and not better.” Open-source models: fine for learning, pick a hosted one for a deadline. Recordings: on the platform. Label all of these as his views on that date.

### Beat 58: How this was built (T+258)

- **SAY** “For those who asked. The repo you watched today was built the way it teaches. One package with the agent. Rules in .cursor/rules and AGENTS.md. Skills in .cursor/skills, including commit-deploy, which runs the tests, commits and deploys the site in one line. A DESIGN.md that every UI change reads first. The MCP server in .cursor/mcp.json. The site and the IDE were written in Cursor against those files, in plan mode first, implementation second. The part that made it work was knowing what I wanted before prompting.”
- **SHOW** The repo root in Cursor: AGENTS.md, DESIGN.md, .cursor/rules, .cursor/skills, .cursor/mcp.json. Ten seconds.
- **NOTE** Whether learners get the repo after the hackathon is your call. Say it here if you have decided.
- **SAY** How Ishan built the original site, for the people who asked (L4379 to L4465): he decided what it should look like before touching a tool; laid the sections out in Excalidraw; generated screens in Google Stitch with Cursor’s colour scheme, several iterations, driven from Cursor over MCP; wrote very detailed per-chapter plans in Cursor plan mode with Opus 4.6 and implemented with GPT 5.5; a custom skill committed, tested and deployed to Vercel in one line; rules for React and FastAPI came from cursor.directory. About 70 hours. His line: “What separates a good product from AI slop is taste. Can you think through the smallest nuances.”
- **SAY** Ishan also built a LeetCode for AI agents in under two days (L4341): a hundred problems, four frameworks, five hundred solutions. “This you cannot one-shot. Code is commoditised. Knowing what you want is not.”

### Beat 59: Hackathon logistics (T+263)

- **SHOW** Hackathon slide or chat message.
- **SAY** “Hackathon starts at 3 PM IST today. Submission by 5 PM IST tomorrow. Form in the chat: GitHub repo, demo video under five minutes, group number, optional deployed link on Vercel or Render. One repo per team with everyone as collaborator. Upload the code, not a zip. Start the video with the demo, not an introduction. Judging: design, code cleanliness, topic depth, end result. Bonus for going beyond the problem statement in ways that make sense. All topics are multi-agent. No extensions.”
- **NOTE** Reasons Ishan gave (L4204, L4293, L4776): videos over five minutes are not watched; zips break the review agent that scans every repo; extensions turn a hackathon into an assignment. Say the rules, not the reasons, unless asked.

### Beat 60: Thanks (T+268)

- **SAY** “Age is not the variable. Two of the most active people we have had were over seventy.”
- **DO** Thank the backup mentor and the hosts by name. Ask for thanks in chat.
- **SAY** Ishan’s advice for after the course (L4254): “Build something for yourself, to solve your own problem. That is how this gets ingrained. Once you start applying it, it takes less time than people assume.”

### Beat 61: Learner feedback round (T+273)

- **SAY** “Two minutes each. What was it like from day zero to day thirteen. Raise hand, camera on.”
- **NOTE** Write the feedback down verbatim. That is the signal for the next cohort.
- **SAY** “Hackathon has started. Go to your WhatsApp groups. Submission form tomorrow morning. See you Monday.”
- **NOTE** On 9 May: Sunil said the connect-the-dots slide made the vector DB sprint make sense for the first time and asked for it mid-course (L4890); Shreya proposed a dot-connecting session around day 7 or 8 (L4923); Pushkar said the pace was overwhelming while still learning Python (L4230). Two learners, hardware and cloud backgrounds, thanked the depth of explanation (L4759). Carry the day-7 idea to the next cohort.

## Appendix A: Cell-to-beat map

| Lesson file | Cells | Beat | Site chapter |
|---|---|---|---|
| 01_hands/ch01_llm_setup.py | C1-C2 setup | 9 | 1.1 |
| 01_hands/ch02_tools.py | C3 tools | 11 | 1.2 |
| 01_hands/ch03_agent_graph.py | C4-C5 bind_tools; C6-C8 graph, run; N1 prebuilt | 12, 14-15 | 1.3 |
| 01_hands/ch04_code_generation.py | C9-C10 calculator | 16 | 1.4 |
| 01_hands/ch05_rules.py | N1 rule sources; C11-C12 rules as system prompt | 17 | 1.5 |
| 01_hands/ch06_streaming.py | C13 astream_events; N1 stream_mode=messages | 18 | 1.6 |
| 01_hands/ch07_multi_turn.py | C14-C15 multi-turn; N1 checkpointer; C16-C17 step trace; C18 reset (do not run) | 19-20, 22 | 1.7 |
| 02_self_awareness/ch08_structured_output.py | C1-C2 setup; C3-C7 structured output | 23-24 | 2.1 |
| 02_self_awareness/ch09_self_correction.py | C8-C10 sandbox; N1 timeout; N2 jail note; C11-C12 state, nodes; C13-C16 bugbot | 25-28 | 2.2 |
| 02_self_awareness/ch10_reflection.py | C17 reviewer; C18-C20 full graph; C21-C22 runs, trace | 29-31 | 2.3 |
| 02_self_awareness/ch11_rules_and_skills.py | C23 rules by path; N1 skills catalog; N2 read_skill trace | 32 | 2.4 |
| 02_self_awareness/ch12_inline_edit.py | C24 inline edit; C25 rules plus edit | 33-34 | 2.5 |
| 03_brain/ch13_codebase_search.py | C1-C2 setup; C3 grep, repo map; C4 search agent; N1 embeddings | 37-38 | 3.1 |
| 03_brain/ch14_toolkit_and_planner.py | C5 toolkit plus MCP; C6 run_command; N1 web research; C7 planner; C8 state | 39-41 | 3.2 |
| 03_brain/ch15_specialists.py | C9-C11 prompts and nodes | 42 | 3.3 |
| 03_brain/ch16_human_in_the_loop.py | C12 human node; C13-C14 graph; C15-C18 run, pause, approve, verify; N1 reject with a reason | 43-47 | 3.4 |
| 03_brain/ch17_parallel.py | C19-C22 parallel on a copy | 48 | 3.5 |
| 03_brain/ch18_time_travel.py | N0 replay if needed; C23 time travel; C24-C26 second feature | 49-50 | 3.6 |

## Appendix B: Lines that landed

These got the strongest response in the original session. Use them as they are.

1. Think of an agent as a person. Lesson one gives it hands. Lesson two gives it self-awareness. Lesson three, the brain.
2. An agent is a harness that lets your LLM use a set of tools, plus whatever code is needed to make that happen.
3. If I give you the name of the tool, the parameter it takes and what it does, is that enough to know what it does? You do not need the code.
4. In the first run the agent figures out which tool it needs. Only in the second run does it execute the tool. How many runs did I give it? One.
5. Do you want to spend money reviewing code that does not run?
6. The LLM is not filling the state. I fill the state myself in every node’s return.
7. Everything so far ran on its own. Here I need to give an input. That is why I interrupt the graph.
8. If feedback never reaches the node that acts on it, you have a loop that spins, not one that improves.
9. Real systems get built by solving one problem after another. Small pieces coming together.
10. Nodes are where the work happens. Edges connect them.
11. Until here the code is just plain text in the state. Apply is what puts it in your files.
12. Hold onto the graph. Once you see the whole thing working it will make a lot more sense.
13. You do not remember syntax. You remember the drawing.

## Appendix C: Where this script departs from the original

| Beat | Original session | This script |
|---|---|---|
| 7 | Three notebooks in Cursor | Three lessons, eighteen Python files, one package |
| 8 | Site tour; notebooks promised for later | Site plus the local IDE; nothing shared, learners watch |
| 11 | Tools write anywhere on disk | Tools jailed to workspace/; said in one sentence |
| 17 | “Equivalent to .cursorrules”; system prompt as a string | Rules from AGENTS.md and .cursor/rules, scoped by glob; load_rules builds the prompt |
| 25 | python -c in a bare subprocess; timeout crashes the graph | LocalSandbox: isolated interpreter, scrubbed env, timeout as a failed attempt; the jail note |
| 32 | STRICT_RULES string in state | tests.mdc versus python.mdc by path; skills catalog and read_skill trace |
| 38 | FAISS index; “this is how @codebase works” | grep, repo map, a searching agent; embeddings as the 2023-2025 footnote |
| 39 | search_codebase, read, write, execute_shell with shell=True; tools never bound | Local tools plus web_search and web_fetch over MCP; run_command takes argv; all bound |
| 42 | Reviewer feedback never reached the coder (known bug) | Fixed; C10 prints the coder prompt with the feedback section |
| 43-47 | plan, code, review, human, apply, test; reject resumed with a string | plan, code, test, ai_review, human_review, apply, verify; reject carries a reason and resets counters |
| 48 | C19 claimed to restore files and did not | Parallel demo runs on a snapshot copy |
| 58 | Stitch, Excalidraw, cursor.directory rules, 70 hours | The repo’s own rules, skills, DESIGN.md and MCP config |
| Cut | Sick-voice disclaimer, Stanford friend story, personal model preferences, Amazon history, age-guessing, band | Not transferable to another instructor |

## Appendix D: The drawings

Learner-facing SVGs in `docs/graphs`. Open them in browser tabs before the session; the `.excalidraw` twins load at excalidraw.com.

| Beat | Open | What it shows | One line to say |
|---|---|---|---|
| 14 | [agent_loop.svg](graphs/agent_loop.svg) | agent, tools, one conditional edge | The model decides, the tool runs, the model sees the result and decides again. |
| 27 | [self_correction.svg](graphs/self_correction.svg) | generate, execute, retry, give up, and the state table | A failure goes back to generate with the error in the prompt. Three failures and it gives up. |
| 30 | [self_correction_with_review.svg](graphs/self_correction_with_review.svg) | the reviewer added, second state table | Execution proves it runs. Review judges whether it is good. Both feed the next prompt. |
| 44 | [orchestrator.svg](graphs/orchestrator.svg) | seven nodes, four routes, the path check | Tests before review. Only reviewed code reaches me. A reject carries my reason back. |
| 47 | [orchestrator_state.svg](graphs/orchestrator_state.svg) | the state through one run | The second code row is the one to notice: v2 was written with the reviewer’s reason. |
| 48 | [parallel_coders.svg](graphs/parallel_coders.svg) | one coder per file, Send, the reducer | Same node, three copies, different inputs. One reducer merges the results. |
| 52 | all six, in order | the recap | Same shape every time: a node, and a function that picks the next node. |
