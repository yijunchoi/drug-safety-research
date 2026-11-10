# Drug Safety Lens

This is a deep research agent that investigates a medication's real-world safety record from the FDA's data, such as side-effect reports, label warnings and recalls. It is built for patients and caregivers who heard something about a drug (on the news, on social media, from a friend) and want to see what the evidence shows, and what it can't show.

**Live app:** <https://drug-safety-research-git-900827490817.europe-west1.run.app>

Ask "Has metformin been recalled, and why?" and a Lead agent plans the research, sends Researchers to query openFDA in parallel, goes back for more when the findings leave a gap, and hands the findings to a Writer. A Fact-checker then compares the report against the findings before you see it. Every number in the answer links to the openFDA query it came from, and every answer ends with what the data can't tell you.

## Why this data

General knowledge about a drug's side effects is not difficult to find, and Gemini already knows the textbook list. What it doesn't know is the live record, including how many reports of a given problem the FDA has received, how that changed year by year, which lots were recalled last month, or what the current label says. FAERS alone holds more than 20 million reports and grows every quarter, so the model can only answer these questions by querying the data.

The data also has hard limits, which the agent states every time. A FAERS report means a person was taking the drug when something happened, not that the drug caused it. FAERS has no count of how many people took each drug, so report counts are never risk rates. News coverage and lawsuits drive reporting up.

To get closer to a fair comparison, the agent joins FAERS with CMS Medicare Part D data on how many patients filled each drug each year. A rise in reports for semaglutide sounds alarming until you see that its Medicare users grew from about 297,000 in 2020 to 2.3 million in 2024. The agent reports these as reports per 100,000 Medicare users, and says plainly that this is a rough index (reports from all US patients, users from Medicare only), not anyone's personal risk.

## How it works

| Agent | Job | Tools |
| --- | --- | --- |
| **Lead** | Asks for clarification if the question is vague, turns brand names into ingredients, splits the question into 2-4 tasks, sends a Researcher per task in one turn (parallel, fresh contexts), reads the findings and sends more Researchers for any gap (at most 3 rounds, 8 Researchers) | `resolve_drug_name`, `research` |
| **Researcher** (x2-8) | Answers one task from openFDA and Medicare data and returns cited bullets | `faers_top_reactions`, `faers_trend`, `faers_reaction_detail`, `faers_compare_drugs`, `faers_report_rate`, `label_warnings`, `drug_recalls`, `medicare_users` |
| **Writer** | Writes the report from the findings alone, citing a source link on every fact, ending with "What this data can't tell you" | none |
| **Fact-checker** | Checks every number and link in the report against the findings, flags causal language; the Writer fixes the report once if it finds problems | none |

The Lead's message can end in three ways: `CLARIFY:` (a vague question such as "Is Ozempic safe?" gets one clarifying question with concrete choices), `OUT_OF_SCOPE:` (for example a price question: it says what FDA data can't answer and suggests a question it can), or `DONE`, which starts the Writer.

`research` is what `researcher.as_tool()` would do, written out so each Researcher gets a numbered name (Researcher 1, 2, ...), its own fresh context, and its own column in the context panel. The code enforces the caps on Researchers and rounds, plus a time budget: no new Researchers after 2.5 minutes, and no rewrite after 3.5, so an answer comes back in a few minutes.

**Showing its work.** `POST /chat` returns `response`, `session_id`, and `tool_calls` with the `name`, `args` and `result` of every call. Every call also has an `agent` field, so the Researchers' calls appear next to the Lead's (e.g. `{"agent": "Researcher 2", "name": "drug_recalls", ...}`). The page uses `GET /chat/stream`, which streams the same answer as Server-Sent Events: you watch each agent's lane fill in live, then open "How I found this" for every call and its raw result. "Show agent contexts" opens a context panel with a column per agent.

**Compare with plain Gemini.** Under each report, one click asks the same model the same question with no tools and no system prompt (`POST /baseline`) and shows the two answers side by side.

## Data

| Source | What it holds | Endpoint |
| --- | --- | --- |
| [openFDA Drug Adverse Events (FAERS)](https://open.fda.gov/apis/drug/event/) | Voluntary side-effect reports from patients, doctors, pharmacists and manufacturers, 2004 to now | `https://api.fda.gov/drug/event.json` |
| [openFDA Drug Labeling](https://open.fda.gov/apis/drug/label/) | Current FDA-approved labels: boxed warning, warnings, adverse reactions | `https://api.fda.gov/drug/label.json` |
| [openFDA Drug Recalls (Enforcement Reports)](https://open.fda.gov/apis/drug/enforcement/) | Every drug recall since 2004: class, reason, firm, status | `https://api.fda.gov/drug/enforcement.json` |
| [CMS Medicare Part D Spending by Drug](https://data.cms.gov/summary-statistics-on-use-and-payments/medicare-medicaid-spending-by-drug/medicare-part-d-spending-by-drug) | Medicare patients (beneficiaries) and claims per drug brand, 2020-2024 | `data/medicare_part_d_users.csv` (committed, 290 KB) |
| [NIH RxNorm](https://lhncbc.nlm.nih.gov/RxNav/APIs/RxNormAPIs.html) | Drug names: brand to active ingredient (Ozempic to semaglutide) | `https://rxnav.nlm.nih.gov/REST` |

openFDA and RxNorm are free public APIs, queried live, so their answers stay current. The Medicare file is the CMS download (data year 2024, 14,536 rows by manufacturer) trimmed to the 3,625 "Overall" rows per brand and the user and claim columns. To rebuild it, download the CSV from the CMS page above and run `uv run medicare.py DSD_PTD_RY26_P04_V10_DY24_BGM.csv`. To load the data yourself, open any query URL from an answer's citations in a browser, or see the openFDA docs above. openFDA works without a key, but a free [openFDA API key](https://open.fda.gov/apis/authentication/) (set as `OPENFDA_API_KEY`) lets the app make more requests a day.

## Three sample queries

Each expected answer below is computed straight from the data with plain code (`sample_runs.py`), with no model involved. Numbers are as of November 10, 2026: FAERS and recalls grow every quarter, so a later run will show slightly higher counts. [SAMPLE_RUNS.md](SAMPLE_RUNS.md) has the full agent answers, the baseline answers and every trace.

### 1. "Since 2020, have FDA reports of pancreatitis for semaglutide (Ozempic, Wegovy) grown faster than the number of Medicare patients taking it, and does its official FDA label warn about pancreatitis?"

- **Expected:** No. US pancreatitis reports went 143 → 126 → 120 → 150 → 225 (2020-2024) while Medicare users went 297,488 → 2,315,591, so reports per 100,000 Medicare users fell from 48.1 to 9.7. Yes, pancreatitis appears on the current semaglutide label.
- **Source:** `/drug/event.json`, US reports counted by `receivedate` for `patient.reaction.reactionmeddrapt:"PANCREATITIS"`; `data/medicare_part_d_users.csv` for Medicare users per year; `/drug/label.json` for semaglutide (cited as its DailyMed page)
- **This agent:** Matches. It answers "No", shows a year-by-year table of Medicare users, US reports and the rate (48.1, 22.2, 12.4, 8.6, 9.7), keeps the worldwide counts (164 → 393) in a separate section so they aren't set against Medicare users, and says yes on the label: acute pancreatitis is in Warnings and Precautions (5.2) of the Ozempic label and in its Medication Guide. 4 Researchers in parallel, 9 tool calls.
- **Same model (Gemini) with no tools and no system prompt:** Gets the label right, but has no report counts, so its "No" is a guess. Its Medicare numbers are attributed to KFF and don't match CMS: it says about 225,000 Ozempic users in 2020 and over 1.2 million by 2023 (CMS: 269,663 and 1,464,468). It also gives an unsourced "4 to 5 cases per 1,000 patient-years".

### 2. "Compare semaglutide, tirzepatide and liraglutide: what share of each drug's FDA adverse event reports mention suicidal ideation?"

- **Expected:** semaglutide 520 of 78,023 reports (0.67%), liraglutide 169 of 51,303 (0.33%), tirzepatide 509 of 181,068 (0.28%). Semaglutide's share is about twice the other two.
- **Source:** `/drug/event.json`, report totals per drug with and without `patient.reaction.reactionmeddrapt:"SUICIDAL IDEATION"`, all years
- **This agent:** Matches: 520/78,023 (0.7%), 509/181,068 (0.3%), 169/51,303 (0.3%), from one `faers_compare_drugs` call so every drug uses the same years. The Lead also sent Researchers to the labels and recalls, then a second round to check the brand labels one by one (Wegovy, Saxenda, Mounjaro). It reports that the Wegovy label on file (April 2024) has the suicidal behavior and ideation warning, while the current Saxenda and Zepbound labels say it was removed in February 2026. 4 Researchers, 17 tool calls.
- **Same model (Gemini) with no tools and no system prompt:** Gives ranges instead of counts, and all three are too low: semaglutide "0.2% to 0.4%" (actual 0.67%), liraglutide "0.1% to 0.3%" (actual 0.33%), tirzepatide "0.1% to 0.2%" (actual 0.28%). It misses that semaglutide's share is about twice the others, and it describes Saxenda's suicidal-ideation warning as current, not knowing the label changed in 2026.

### 3. "Has metformin been recalled since 2019, and why?"

- **Expected:** Yes, 65 recalls started since 2019. By year: 2020: 44, 2021: 15, then 1-2 a year. By reason: NDMA or other nitrosamine impurity 47, storage temperature 6, foreign material or wrong pill 5, sterility or manufacturing practice 4, failed dissolution or potency 2, other impurity 1.
- **Source:** `/drug/enforcement.json` for metformin (generic name, brand name or product description), `recall_initiation_date` from 2019
- **This agent:** Matches every count: 65 recalls (62 Class II, 3 Class III), the year table and all six reasons. It also checked whether the current label mentions NDMA (it doesn't) and listed the firms behind the 10 newest recalls. 3 Researchers, 9 tool calls.
- **Same model (Gemini) with no tools and no system prompt:** Knows the NDMA story and names manufacturers, but gives no counts ("multiple recalls") and misses the 18 recalls that weren't about NDMA, such as storage temperature and wrong pills in the bottle.

### Two more to try

- **"Is Ozempic safe?"** is vague; the Lead asks which concern you mean (a specific side effect, a time period, a comparison, or an overview) before any research.
- **"How much does Wegovy cost without insurance?"** is something FDA data can't answer. The agent says so and suggests a question it can answer.

## Running it locally

You need a GCP project with billing enabled and the Vertex AI API turned on.

```bash
cp .env.example .env              # optional: add your openFDA API key
gcloud auth application-default login
uv run app.py
```

Then open http://localhost:8000. To regenerate [SAMPLE_RUNS.md](SAMPLE_RUNS.md), keep the app running and run `uv run sample_runs.py http://127.0.0.1:8000` in a second terminal.

## Deployment

Cloud Run with continuous deployment from GitHub. The service sets `OPENFDA_API_KEY` as an environment variable and raises the request timeout to 600 seconds, since a research run with several rounds can take a few minutes.

## Not medical advice

This agent shows public FDA data and explains what it can and can't show. It doesn't tell anyone whether to take a drug. Talk to a doctor or pharmacist before changing any medication.
