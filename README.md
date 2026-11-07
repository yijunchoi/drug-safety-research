# Second Look: FDA drug safety research

A deep research agent that investigates a medication's real-world safety record from the FDA's own data: side-effect reports, label warnings and recalls. It is built for patients and caregivers who heard something about a drug (on the news, on TikTok, from a friend) and want to see what the evidence shows, and what it can't show.

**Live app:** <https://REPLACE-WITH-YOUR-CLOUD-RUN-URL.run.app>

Ask "Has metformin been recalled, and why?" and a Lead agent plans the research, sends Researchers to query openFDA in parallel, goes back for more when the findings leave a gap, and hands the findings to a Writer. A Fact-checker then compares the report against the findings before you see it. Every number in the answer links to the openFDA query it came from, and every answer ends with what the data can't tell you.

## Why this data

General knowledge about a drug's side effects is easy to find, and Gemini already knows the textbook list. What it doesn't know is the live record: how many reports of a given problem the FDA has received, how that changed year by year, which lots were recalled last month, or what the current label says. FAERS alone holds more than 20 million reports and grows every quarter, so the model can only answer these questions by querying the data.

The data also has hard limits, which the agent states every time. A FAERS report means a person was taking the drug when something happened, not that the drug caused it. FAERS has no count of how many people took each drug, so report counts are never risk rates. News coverage and lawsuits drive reporting up.

To get closer to a fair comparison, the agent joins FAERS with CMS Medicare Part D data on how many patients filled each drug each year. A rise in reports for semaglutide sounds alarming until you see that its Medicare users grew from about 297,000 in 2020 to 2.3 million in 2024. The agent reports these as reports per 100,000 Medicare users, and says plainly that this is a rough index (reports from all US patients, users from Medicare only), not anyone's personal risk.

## How it works

| Agent | Model | Job | Tools |
| --- | --- | --- | --- |
| **Lead** | gemini-3.5-flash | Asks for clarification if the question is vague, turns brand names into ingredients, splits the question into 2-4 tasks, sends a Researcher per task **in one turn** (parallel, fresh contexts), reads the findings and sends more Researchers for any gap (at most 3 rounds, 8 Researchers) | `resolve_drug_name`, `research` |
| **Researcher** (x2-8) | gemini-3.5-flash-lite | Answers one task from openFDA and returns cited bullets | `faers_top_reactions`, `faers_trend`, `faers_reaction_detail`, `faers_compare_drugs`, `faers_report_rate`, `label_warnings`, `drug_recalls`, `medicare_users` |
| **Writer** | gemini-3.5-flash | Writes the report from the findings alone, citing a source link on every fact, ending with "What this data can't tell you" | none |
| **Fact-checker** | gemini-3.5-flash | Checks every number and link in the report against the findings, flags causal language; the Writer fixes the report once if it finds problems | none |

The Lead's message can end in three ways: `CLARIFY:` (a vague question such as "Is Ozempic safe?" gets one clarifying question with concrete choices), `OUT_OF_SCOPE:` (for example a price question: it says what FDA data can't answer and suggests a question it can), or `DONE`, which starts the Writer.

`research` is what `researcher.as_tool()` would do, written out so each Researcher gets a numbered name (Researcher 1, 2, ...), its own fresh context, and its own column in the context panel. The code enforces the caps on Researchers and rounds, so a run stays well under the 5-minute limit.

**Showing its work.** `POST /chat` keeps Project 1's response shape: `response`, `session_id`, and `tool_calls` with the `name`, `args` and `result` of every call. Every call also has an `agent` field, so the Researchers' calls appear next to the Lead's (e.g. `{"agent": "Researcher 2", "name": "drug_recalls", ...}`). The page uses `GET /chat/stream`, which streams the same answer as Server-Sent Events: you watch each agent's lane fill in live, then open "How I found this" for every call and its raw result. "Show agent contexts" opens the course's context panel, with a column per agent.

**Compare with plain Gemini.** Under each report, one click asks the same model the same question with no tools and no system prompt (`POST /baseline`) and shows the two answers side by side.

## Data

| Source | What it holds | Endpoint |
| --- | --- | --- |
| [openFDA Drug Adverse Events (FAERS)](https://open.fda.gov/apis/drug/event/) | Voluntary side-effect reports from patients, doctors, pharmacists and manufacturers, 2004 to now | `https://api.fda.gov/drug/event.json` |
| [openFDA Drug Labeling](https://open.fda.gov/apis/drug/label/) | Current FDA-approved labels: boxed warning, warnings, adverse reactions | `https://api.fda.gov/drug/label.json` |
| [openFDA Drug Recalls (Enforcement Reports)](https://open.fda.gov/apis/drug/enforcement/) | Every drug recall since 2004: class, reason, firm, status | `https://api.fda.gov/drug/enforcement.json` |
| [CMS Medicare Part D Spending by Drug](https://data.cms.gov/summary-statistics-on-use-and-payments/medicare-medicaid-spending-by-drug/medicare-part-d-spending-by-drug) | Medicare patients (beneficiaries) and claims per drug brand, 2020-2024 | `data/medicare_part_d_users.csv` (committed, 290 KB) |
| [NIH RxNorm](https://lhncbc.nlm.nih.gov/RxNav/APIs/RxNormAPIs.html) | Drug names: brand to active ingredient (Ozempic to semaglutide) | `https://rxnav.nlm.nih.gov/REST` |

openFDA and RxNorm are free public APIs, queried live, so their answers stay current. The Medicare file is the CMS download (data year 2024, 14,536 rows by manufacturer) trimmed to the 3,625 "Overall" rows per brand and the user and claim columns. To rebuild it, download the CSV from the CMS page above and run `uv run medicare.py DSD_PTD_RY26_P04_V10_DY24_BGM.csv`. To load the data yourself, open any query URL from an answer's citations in a browser, or see the openFDA docs above. A free [openFDA API key](https://open.fda.gov/apis/authentication/) raises the limit from 1,000 to 120,000 requests a day.

## Three sample queries

Each expected answer below is computed straight from openFDA with plain code (`sample_runs.py`), with no model involved. [SAMPLE_RUNS.md](SAMPLE_RUNS.md) has the full agent answers, the baseline answers and every trace.

### 1. "Since 2020, have FDA reports of pancreatitis for semaglutide (Ozempic, Wegovy) grown faster than the number of Medicare patients taking it, and is pancreatitis mentioned on its label?"

- **Expected:** ⟨fill from SAMPLE_RUNS.md⟩
- **Source:** `/drug/event.json`, US reports counted by `receivedate` for `patient.reaction.reactionmeddrapt:"PANCREATITIS"`; `data/medicare_part_d_users.csv` for Medicare users per year; `/drug/label.json` for semaglutide
- **This agent:** ⟨fill⟩
- **Gemini, no tools, no system prompt:** ⟨fill⟩

### 2. "Compare semaglutide, tirzepatide and liraglutide: what share of each drug's FDA adverse event reports mention suicidal ideation?"

- **Expected:** ⟨fill from SAMPLE_RUNS.md⟩
- **Source:** `/drug/event.json`, report totals per drug with and without `patient.reaction.reactionmeddrapt:"SUICIDAL IDEATION"`
- **This agent:** ⟨fill⟩
- **Gemini, no tools, no system prompt:** ⟨fill⟩

### 3. "Has metformin been recalled since 2019, and why?"

- **Expected:** ⟨fill from SAMPLE_RUNS.md⟩
- **Source:** `/drug/enforcement.json` for metformin, `recall_initiation_date` from 2019
- **This agent:** ⟨fill⟩
- **Gemini, no tools, no system prompt:** ⟨fill⟩

### Two more to try

- **"Is Ozempic safe?"** is vague: the Lead asks which concern you mean (a specific side effect, a time period, a comparison, or an overview) before any research.
- **"How much does Wegovy cost without insurance?"** is something FDA data can't answer: the agent says so and suggests a question it can answer.

## Running it locally

You need a GCP project with billing enabled and the Vertex AI API turned on.

```bash
cp .env.example .env              # optional: add your openFDA API key
gcloud auth application-default login
uv run app.py
```

Then open http://localhost:8000. To regenerate the sample runs against any deployment: `uv run sample_runs.py https://your-url.run.app`.

## Deployment

Cloud Run with continuous deployment from GitHub. The service sets `OPENFDA_API_KEY` as an environment variable and raises the request timeout to 600 seconds, since a research run with several rounds can take a few minutes.

## Built with

Gemini on Vertex AI through LiteLLM, openFDA, CMS and NIH data, the OpenAI Agents SDK, FastAPI, and the context panel from the course's `wikipedia-deep-research` example.

## Not medical advice

This agent shows public FDA data and explains what it can and can't show. It doesn't tell anyone whether to take a drug. Talk to a doctor or pharmacist before changing any medication.
