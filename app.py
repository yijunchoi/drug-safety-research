import asyncio
import time
import json
import uuid
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

import litellm
import uvicorn
from agents import Agent, ModelSettings, RunContextWrapper, Runner, function_tool, set_tracing_disabled
from agents.extensions.models.litellm_model import LitellmModel
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel

from context_panel import AgentContexts, PanelHooks, add_context_panel
from tools import RESEARCHER_TOOLS, resolve_drug_name

# OPENFDA_API_KEY comes from the .env file locally, and from Cloud Run's environment when deployed.
load_dotenv(Path(__file__).parent / ".env")

# Traces upload to OpenAI by default, which needs an OpenAI key. We're on Gemini.
set_tracing_disabled(True)

# LiteLLM routes the call to Gemini. api_key is unused: Vertex AI uses your gcloud credentials.
MODEL_NAME = "vertex_ai/gemini-3.5-flash"
MODEL = LitellmModel(model=MODEL_NAME, api_key="unused")
# Researchers call tools and take notes: the cheaper model is enough.
RESEARCHER_MODEL = LitellmModel(model="vertex_ai/gemini-3.5-flash-lite", api_key="unused")
# A stalled model call would hang the page: give up after 90 s, and retry twice.
SETTINGS = ModelSettings(extra_args={"vertex_location": "global", "timeout": 90, "num_retries": 2})
# Researchers, the Writer and the Fact-checker follow clear rules, so they need little thinking.
# Less thinking makes each call several times faster. drop_params skips it if a model can't take it.
FAST = ModelSettings(extra_args={"vertex_location": "global", "timeout": 90, "num_retries": 2,
                                 "reasoning_effort": "low", "drop_params": True})

# Caps that keep one answer to a few minutes. Prompts ask for restraint; code enforces it.
MAX_RESEARCHERS = 8  # in all, across every round
MAX_ROUNDS = 3  # the first fan-out plus at most two follow-ups for gaps
LEAD_MAX_TURNS = 12
# Time budget per answer, in seconds, so nobody waits more than about 5 minutes.
RESEARCH_SECONDS = 150  # no new researchers after this
REWRITE_SECONDS = 210  # skip the Fact-checker's rewrite after this
RESEARCHER_MAX_TURNS = 10


@dataclass
class Research:
    """One answer's state, shared by every agent and tool in it. The model never sees it."""

    hooks: "Recorder"
    researchers: int = 0  # how many researchers have started, to number them
    lead_turns: int = 0  # how many times the Lead has called the model
    rounds: set = field(default_factory=set)  # the Lead turns that sent researchers out
    findings: list[str] = field(default_factory=list)  # what each researcher reported, for the Writer
    started: float = field(default_factory=time.monotonic)


class Recorder(PanelHooks):
    """PanelHooks, plus a record of every tool call for /chat's tool_calls, with the agent that made it.
    Sub-agents' calls land here too, because every Runner.run in an answer shares these hooks."""

    def __init__(self, contexts: AgentContexts, emit):
        super().__init__(contexts, emit)
        self.tool_calls: list[dict] = []
        self._open: dict[str, dict] = {}
        self.run: Research | None = None

    async def on_llm_start(self, context, agent, system_prompt, input_items):
        await super().on_llm_start(context, agent, system_prompt, input_items)
        if agent.name == "Lead" and self.run:
            self.run.lead_turns += 1

    async def on_tool_start(self, context, agent, tool):
        await super().on_tool_start(context, agent, tool)
        raw = getattr(context, "tool_arguments", None)
        try:
            args = json.loads(raw) if raw else {}
        except ValueError:
            args = {"raw": raw}
        call = {"agent": agent.name, "name": tool.name, "args": args, "result": None}
        self.tool_calls.append(call)
        self._open[getattr(context, "tool_call_id", None) or f"{agent.name}:{tool.name}"] = call
        self.emit({"type": "tool_start", "agent": agent.name, "name": tool.name, "args": args})

    async def on_tool_end(self, context, agent, tool, result):
        key = getattr(context, "tool_call_id", None) or f"{agent.name}:{tool.name}"
        call = self._open.pop(key, None)
        if call is not None:
            call["result"] = str(result)
        self.emit({"type": "tool_end", "agent": agent.name, "name": tool.name})


# --- The researcher: one task, answered from openFDA ---

researcher = Agent(
    name="Researcher",
    instructions=f"""\
Today is {date.today():%B %d, %Y}. You research one task about drug safety using the FDA's own data.

1. Call the tools that fit your task. Most tasks need 2 to 4 calls. Use the active ingredient
   name you are given for every search.
2. Reaction names are MedDRA terms in capitals, e.g. PANCREATITIS. Take them from
   faers_top_reactions before using them in other tools.
3. Reply with the facts that answer your task and nothing else, at most 10 bullets. Every
   bullet states exact numbers from a tool and ends with that tool's source link, e.g.
   ([openFDA FAERS](https://api.fda.gov/drug/event.json?...)). When a tool also gives
   users_source, cite it too as ([CMS](url)).
4. If the task compares reports with how many people use the drug, call faers_report_rate
   (US reports per 100,000 Medicare users) and use its US report counts: never divide numbers
   yourself, and don't set worldwide report counts beside Medicare users. If it compares a
   share across drugs, call faers_compare_drugs, so every drug uses the same years.
5. To check whether a label mentions something, call label_warnings with find (e.g.
   find="suicid"). Its sections are shortened, so never say a label lacks something unless
   find says found: false. Report what find returned: found, whether it is in the
   warnings, and which sections it names. Brands of one ingredient have separate labels (Ozempic and Wegovy
   are both semaglutide): look up each brand by name when the brands matter, and say which
   brand's label each fact comes from.
6. For recalls, report the totals in by_reason and by_year, not only the newest few.
7. Never write a number a tool didn't return. If the tools don't answer part of the task,
   say so in a last bullet, and say why (e.g. "FAERS has no denominator").""",
    model=RESEARCHER_MODEL,
    model_settings=FAST,
    tools=RESEARCHER_TOOLS,
)


@function_tool
async def research(ctx: RunContextWrapper[Research], task: str) -> str:
    """Send a researcher to answer one task from openFDA (side-effect reports, label, recalls)
    and Medicare Part D (how many patients use a drug).
    Returns its findings, each with the query it came from.

    Args:
        task: One specific thing to find out. Name the active ingredient(s), the years, and which
            data to use, e.g. 'Reports of pancreatitis for semaglutide by year since 2018 (FAERS)'.
    """
    run = ctx.context
    if run.researchers >= MAX_RESEARCHERS:
        return "No researchers left. Reply DONE."
    if time.monotonic() - run.started > RESEARCH_SECONDS:
        return "Time is up for research. Reply DONE."
    # Every research call in one Lead turn is the same round: they run in parallel.
    if run.lead_turns not in run.rounds and len(run.rounds) >= MAX_ROUNDS:
        return "The round limit is reached. Reply DONE."
    run.rounds.add(run.lead_turns)
    # What researcher.as_tool() does: run the researcher in a fresh context and return its answer.
    # Written out so each run gets a numbered copy, and its own column in the context panel.
    run.researchers += 1
    agent = researcher.clone(name=f"Researcher {run.researchers}")
    result = await Runner.run(agent, f"Task: {task}", context=run, hooks=run.hooks,
                              max_turns=RESEARCHER_MAX_TURNS)
    run.findings.append(f"Task: {task}\n\n{result.final_output}")
    return str(result.final_output)


# --- The lead: clarifies, plans, fans out to researchers, and checks for gaps ---

lead = Agent(
    name="Lead",
    instructions=f"""\
Today is {date.today():%B %d, %Y}. You lead a team that answers questions about a medication's
real-world safety record from FDA data (FAERS side-effect reports, the FDA label, FDA recalls) and
CMS Medicare Part D data on how many patients take each drug.
You see the conversation so far and the user's new message.

First decide which of these the message is:

A. Vague: no drug is named, or the question is so broad you can't plan research (e.g. "Is
   Ozempic safe?", "what about side effects"). Reply with one short clarifying question that
   offers 2-3 concrete choices (a specific side effect, a time period, a comparison drug, or a
   general overview), starting with "CLARIFY:". Do this only once: if you already asked and the
   user answered, or they asked for a general overview, go on to C.
B. Out of scope: FDA data can't answer it at all (prices, whether they personally should take
   it, dosing, how well a drug works). Reply "OUT_OF_SCOPE:" then say plainly what this data can't
   answer and suggest one related question it can.
C. Researchable. Then:
   1. Call resolve_drug_name for each drug the user names, to get its active ingredient.
   2. Split the question into 2 to 4 independent tasks and call research once per task, all in
      the same turn, so the researchers work in parallel. Usually one task per data source:
      side-effect reports, the label, recalls; or one task per drug for a comparison. When the
      question is about change over time or comparing drugs, include a task for reports per
      100,000 Medicare users (say "use faers_report_rate" in the task), so growth in use isn't
      mistaken for growth in harm. This task is required whenever the user compares reports
      with how many people take the drug. For a share comparison across drugs, send one task that
      names every drug (say "use faers_compare_drugs").
   3. Read the findings. If part of the question is still unanswered, or the findings raise an
      obvious next question (e.g. reports spiked in one year: was there a recall or label change
      then?), call research again for just that part. Do this at most twice.
   4. When the question is covered, reply DONE and nothing else: a writer writes the report.""",
    model=MODEL,
    model_settings=SETTINGS,
    tools=[resolve_drug_name, research],
)

# --- The writer: one call, after the research ends ---

writer = Agent(
    name="Writer",
    instructions="""\
Write a short report in markdown that answers the user's question, using only the findings you're
given. Your reader is a patient or caregiver with no medical training.

- Start with "**Short answer:**" and two or three plain sentences.
- The first time you mention the label, explain it in plain words: the FDA label is the
  official prescribing information that comes with the drug and lists its known risks.
- When comparing reports with Medicare users, use the US report counts and the rate per
  100,000 users from the findings. Don't set worldwide report counts beside Medicare users.
- Then a short section per part of the question, with the key numbers. A small table is welcome
  when it compares drugs or years.
- Cite everything: end every sentence that states a number or fact with the link from its
  finding, as a short markdown link like ([FAERS](url)), ([label](url)) or ([recalls](url)).
  Numbers from Medicare user counts cite ([CMS](url)); a rate per 100,000 users cites both.
- In a table, put no links in the cells: cite every source the table uses once, in the
  sentence just above it.
- Always end with a "### What this data can't tell you" section with only the limits of the data
  this report actually used. Side-effect reports: they don't prove the drug caused the problem,
  FAERS has no count of users so there is no risk rate, the Medicare rate is only a rough index
  for Medicare patients, and reporting rises with news coverage. Recalls: a recall is about a
  batch, not proof anyone was harmed, and older or smaller recalls may name the drug differently.
  Add any part of the question the findings didn't answer. These are general limits: don't put
  source links on them.
- Never add a number or fact that isn't in the findings. Say "reports", never "cases" or "risk".
- Don't tell the reader whether to take a drug. End with: "_Not medical advice: talk to your
  doctor or pharmacist._" """,
    model=MODEL,
    model_settings=FAST,
)

# --- The fact-checker: reads the report against the findings before the user sees it ---

checker = Agent(
    name="Fact-checker",
    instructions="""\
You check a drug-safety report against the research findings it was written from.

List every problem you find, one per line:
- a number that doesn't appear in the findings, or differs from them
- a factual sentence with no source link, or a link that isn't in the findings (a table's
  numbers are cited by the links in the sentence just above it)
- a claim that a drug causes something, or a "risk" or "rate", when the data are only reports
- a missing "What this data can't tell you" section

If there are no problems, reply OK and nothing else.""",
    model=MODEL,
    model_settings=FAST,
)


# --- One answer: Lead -> Researchers -> Writer -> Fact-checker ---


def _transcript(history: list[dict]) -> str:
    lines = []
    for turn in history[-8:]:
        text = turn["content"]
        lines.append(f"{turn['role']}: {text[:1500] + ' [...]' if len(text) > 1500 else text}")
    return "\n\n".join(lines) or "(none)"


async def answer(message: str, history: list[dict], hooks: Recorder) -> str:
    run = Research(hooks=hooks)
    hooks.run = run

    # 1. Research: clarify or plan, fan out, check for gaps
    prompt = f"Conversation so far:\n{_transcript(history)}\n\nNew message from the user: {message}"
    planned = await Runner.run(lead, prompt, context=run, hooks=hooks, max_turns=LEAD_MAX_TURNS)
    verdict = str(planned.final_output).strip()
    for prefix in ("CLARIFY:", "OUT_OF_SCOPE:"):
        if verdict.upper().startswith(prefix):
            return verdict[len(prefix):].strip()
    if not run.findings:
        return verdict  # the Lead answered without research, e.g. a greeting

    # 2. Write: the Writer sees only the question and the findings, not the Lead's reasoning
    findings = "\n\n---\n\n".join(run.findings)
    question = f"Conversation so far:\n{_transcript(history)}\n\nQuestion: {message}"
    draft = await Runner.run(writer, f"{question}\n\nFindings:\n\n{findings}", hooks=hooks)
    report = str(draft.final_output)

    # 3. Check: one review, and at most one rewrite
    review = await Runner.run(checker, f"Findings:\n\n{findings}\n\n---\n\nReport:\n\n{report}", hooks=hooks)
    problems = str(review.final_output).strip()
    if problems.upper().rstrip(".") != "OK" and time.monotonic() - run.started < REWRITE_SECONDS:
        hooks.activity("Fact-checker", "sent the report back to the Writer")
        fixed = await Runner.run(
            writer,
            f"{question}\n\nFindings:\n\n{findings}\n\nYour draft:\n\n{report}\n\n"
            f"A fact-checker found these problems. Fix them and return the whole report:\n{problems}",
            hooks=hooks,
        )
        report = str(fixed.final_output)
    return report


# --- Sessions ---


@dataclass
class Session:
    history: list[dict] = field(default_factory=list)  # {"role": "user"|"assistant", "content"}
    contexts: AgentContexts = field(default_factory=AgentContexts)  # every agent's context, for the panel


# session_id -> Session. In-memory, single process.
sessions: dict[str, Session] = {}


class _PanelView(dict):
    """add_context_panel reads sessions[id] and expects AgentContexts: hand it each session's."""

    def get(self, key, default=None):
        session = sessions.get(key)
        return session.contexts if session else default


def _session(session_id: str | None) -> tuple[str, Session]:
    session_id = session_id or str(uuid.uuid4())
    return session_id, sessions.setdefault(session_id, Session())


async def _answer_in_session(message: str, session: Session, emit) -> tuple[str, list[dict]]:
    hooks = Recorder(session.contexts, emit)
    try:
        response = await answer(message, session.history, hooks)
    except Exception as e:
        # Auth, quota, a model that won't stop: show it in the chat, not as a 500.
        response = f"Something went wrong: {type(e).__name__}: {str(e)[:300]}"
    session.history += [{"role": "user", "content": message}, {"role": "assistant", "content": response}]
    return response, hooks.tool_calls


# --- FastAPI App ---

HERE = Path(__file__).parent

app = FastAPI()
add_context_panel(app, _PanelView())


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None


class ChatResponse(BaseModel):
    response: str
    session_id: str
    tool_calls: list[dict]  # {agent, name, args, result} for every call, the Researchers' included


@app.get("/")
def index():
    # no-cache: browsers otherwise keep serving an old page after a redeploy
    return FileResponse(HERE / "index.html", headers={"Cache-Control": "no-cache"})


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """One JSON answer once the research is done, with every tool call behind it."""
    session_id, session = _session(request.session_id)
    response, tool_calls = await _answer_in_session(request.message, session, lambda event: None)
    return ChatResponse(response=response, session_id=session_id, tool_calls=tool_calls)


@app.get("/chat/stream")
async def chat_stream(message: str, session_id: str | None = None):
    """The same answer, streamed as Server-Sent Events so the page can show each agent at work.
    The last event carries the same response, session_id and tool_calls as /chat."""
    session_id, session = _session(session_id)
    queue: asyncio.Queue = asyncio.Queue()

    async def work():
        response, tool_calls = await _answer_in_session(message, session, queue.put_nowait)
        queue.put_nowait({"type": "done", "response": response, "session_id": session_id, "tool_calls": tool_calls})

    task = asyncio.create_task(work())

    async def events():
        try:
            yield f"data: {json.dumps({'type': 'start', 'session_id': session_id})}\n\n"
            while True:
                event = await queue.get()
                yield f"data: {json.dumps(event, default=str)}\n\n"
                if event["type"] == "done":
                    break
        finally:
            task.cancel()  # the page closed the stream: stop spending tokens

    return StreamingResponse(events(), media_type="text/event-stream")


class BaselineRequest(BaseModel):
    message: str


@app.post("/baseline")
async def baseline(request: BaselineRequest):
    """The same model with no tools and no system prompt, for the README's comparison."""
    try:
        reply = await litellm.acompletion(
            model=MODEL_NAME, vertex_location="global", timeout=90,
            messages=[{"role": "user", "content": request.message}],
        )
        return {"response": reply.choices[0].message.content, "model": MODEL_NAME}
    except Exception as e:
        return {"response": f"Model call failed: {type(e).__name__}: {str(e)[:300]}", "model": MODEL_NAME}


@app.post("/clear")
def clear(session_id: str | None = None):
    sessions.pop(session_id, None)
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
