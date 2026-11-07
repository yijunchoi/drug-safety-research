"""Run the README's sample queries three ways and write SAMPLE_RUNS.md:

1. Expected answer: computed straight from openFDA with plain code, no model involved.
2. This agent: the deployed /chat, with its full trace of tool calls.
3. Baseline: the same model with no tools and no system prompt (/baseline).

Usage: uv run sample_runs.py https://your-agent.run.app
"""

import json
import sys
from datetime import date
from pathlib import Path

import httpx
from dotenv import load_dotenv

import medicare
import openfda

load_dotenv(Path(__file__).parent / ".env")

QUERIES = [
    "Since 2020, have FDA reports of pancreatitis for semaglutide (Ozempic, Wegovy) grown faster than the number "
    "of Medicare patients taking it, and is pancreatitis mentioned on its label?",
    "Compare semaglutide, tirzepatide and liraglutide: what share of each drug's FDA adverse event reports "
    "mention suicidal ideation?",
    "Has metformin been recalled since 2019, and why?",
]


def expected_pancreatitis() -> str:
    search = openfda.event_search("semaglutide", 2020, 2024, reaction="PANCREATITIS", country="US")
    rows, url = openfda.count_by(search, "receivedate", limit=0)
    by_year: dict[int, int] = {}
    for row in rows:
        by_year[int(row["time"][:4])] = by_year.get(int(row["time"][:4]), 0) + row["count"]
    users = medicare.users("semaglutide")["total_users"]
    years = "; ".join(
        f"{y}: {by_year.get(y, 0)} US reports / {users[y]:,} Medicare users = "
        f"{100_000 * by_year.get(y, 0) / users[y]:.1f} per 100k" for y in medicare.YEARS if users[y]
    )
    label = openfda.latest_label("semaglutide")
    text = json.dumps(label["label"]).lower() if label else ""
    on_label = "pancreatitis" in text
    return (f"US reports listing PANCREATITIS, by year received: {years}. "
            f"Pancreatitis on the current label: {'yes' if on_label else 'no'}.\n\n"
            f"Source: `/drug/event.json` count by receivedate ({url}), `data/medicare_part_d_users.csv` "
            f"(CMS Medicare Part D Spending by Drug) and `/drug/label.json` ({label and label['source']})")


def expected_compare() -> str:
    parts = []
    for drug in ("semaglutide", "tirzepatide", "liraglutide"):
        total, _ = openfda.count_reports(openfda.event_search(drug))
        hits, url = openfda.count_reports(openfda.event_search(drug, reaction="SUICIDAL IDEATION"))
        share = f"{100 * hits / total:.2f}%" if total else "n/a"
        parts.append(f"{drug}: {hits} of {total} reports ({share})")
    return "; ".join(parts) + ".\n\nSource: `/drug/event.json` report totals, with and without `patient.reaction.reactionmeddrapt:\"SUICIDAL IDEATION\"`"


def expected_recalls() -> str:
    rows, total, url = openfda.recalls("metformin", start_year=2019)
    reasons: dict[str, int] = {}
    for r in rows:
        key = (r.get("reason_for_recall") or "")[:90]
        reasons[key] = reasons.get(key, 0) + 1
    top = "; ".join(f"{n}x \"{k}\"" for k, n in sorted(reasons.items(), key=lambda kv: -kv[1])[:3])
    return f"{total} recall records since 2019. Most common reasons: {top}.\n\nSource: `/drug/enforcement.json` ({url})"


EXPECTED = [expected_pancreatitis, expected_compare, expected_recalls]


def main(base: str) -> None:
    base = base.rstrip("/")
    out = [f"# Sample runs\n\nGenerated {date.today()} against {base} by `uv run sample_runs.py {base}`.\n"]
    with httpx.Client(timeout=600) as client:
        for i, (query, expected) in enumerate(zip(QUERIES, EXPECTED), 1):
            print(f"[{i}/3] {query[:60]}...")
            agent = client.post(f"{base}/chat", json={"message": query}).json()
            plain = client.post(f"{base}/baseline", json={"message": query}).json()
            researchers = sorted({c["agent"] for c in agent["tool_calls"] if c["agent"].startswith("Researcher")})
            trace = "\n".join(
                f"| {c['agent']} | `{c['name']}` | `{json.dumps(c['args'])[:120]}` |" for c in agent["tool_calls"]
            )
            out.append(f"""
## {i}. {query}

### Expected (computed directly from openFDA, no model)

{expected()}

### This agent

{agent['response']}

<details><summary>Trace: {len(agent['tool_calls'])} tool calls, {len(researchers)} researchers</summary>

| Agent | Tool | Arguments |
| --- | --- | --- |
{trace}

Full results: `tool_calls` in the /chat response.
</details>

### Same model, no tools and no system prompt

{plain['response']}
""")
    Path("SAMPLE_RUNS.md").write_text("\n".join(out))
    print("Wrote SAMPLE_RUNS.md")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000")
