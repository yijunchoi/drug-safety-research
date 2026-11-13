"""
Every tool the agents can call. Each one returns JSON with a source link, so every number can be traced back to where it came from.
If something goes wrong, a tool returns {“error”: ..., “hint”: ...} and that way the agent can read what happened and either tell the user or try a different search.

"""

import json
from collections import Counter
from datetime import date

from agents import function_tool

import medicare
import openfda

# What every FAERS answer must travel with. The Writer turns these into "what the data can't tell you".
FAERS_CAVEATS = (
    "FAERS reports are voluntary and unverified. A report means a drug was being taken when a problem "
    "happened, not that the drug caused it. FAERS has no count of how many people took the drug, so "
    "report counts are not risk rates (Medicare Part D user counts give only a rough denominator). Media attention and lawsuits raise report counts."
)


def _error(message: str, hint: str = "") -> str:
    return json.dumps({"error": message, "hint": hint} if hint else {"error": message})


def _name(names: dict, term) -> str:
    """openFDA returns coded fields as numbers or strings: '2' and 2 both mean female."""
    try:
        return names.get(int(term), str(term))
    except (TypeError, ValueError):
        return str(term)


def _share(part: int, whole: int) -> str:
    return f"{100 * part / whole:.1f}%" if whole else "n/a"


# --- Lead's tool: what is this drug called? ---


@function_tool
def resolve_drug_name(name: str) -> str:
    """Turn any drug name a user types (a brand like 'Ozempic', or a misspelling) into its active
    ingredient and its other brand names, using NIH RxNorm. Use search_names for every openFDA
    search. A combination drug (e.g. Adderall) has several: research each one by name.

    Args:
        name: The drug name as the user wrote it.
    """
    try:
        names = openfda.rxnorm_names(name.strip())
    except Exception as e:
        return _error(f"RxNorm did not respond: {type(e).__name__}", "Search openFDA with the name as given.")
    if not names or not names.get("ingredients"):
        return _error(f"RxNorm doesn't know a drug called '{name}'.", "Ask the user to check the spelling.")
    return json.dumps(names)


# --- Researcher tools: FAERS adverse event reports ---


@function_tool
def faers_top_reactions(drug: str, start_year: int | None = None, end_year: int | None = None,
                        serious_only: bool = False) -> str:
    """The side effects reported most often for a drug in FDA's Adverse Event Reporting System
    (FAERS), with the total number of reports. Use this first to see what people report.

    Args:
        drug: Active ingredient, e.g. 'semaglutide'.
        start_year: Only reports received in or after this year.
        end_year: Only reports received in or before this year.
        serious_only: Only reports marked serious (hospitalization, disability, death...).
    """
    search = openfda.event_search(drug, start_year, end_year, serious_only=serious_only)
    try:
        total, total_url = openfda.count_reports(search)
        rows, url = openfda.count_by(search, "patient.reaction.reactionmeddrapt.exact", limit=15)
    except Exception as e:
        return _error(f"openFDA failed: {type(e).__name__}: {e}")
    if not total:
        return _error(f"No FAERS reports mention '{drug}' in that period.",
                      "Check the ingredient name with resolve_drug_name, or widen the years.")
    return json.dumps({
        "drug": drug,
        "period": f"{start_year or 'start'}-{end_year or 'now'}",
        "serious_only": serious_only,
        "total_reports": total,
        "top_reactions": [
            {"reaction": r["term"], "reports": r["count"], "share_of_reports": _share(r["count"], total)}
            for r in rows
        ],
        "note": "One report can list several reactions, so shares add up to more than 100%.",
        "caveat": FAERS_CAVEATS,
        "source": url,
        "total_source": total_url,
    })


@function_tool
def faers_trend(drug: str, reaction: str = "") -> str:
    """How many FAERS reports were received each year for a drug, optionally only those that
    mention one reaction. Use this to see whether reports rose or fell, and when.

    Args:
        drug: Active ingredient, e.g. 'semaglutide'.
        reaction: Optional MedDRA reaction term, e.g. 'PANCREATITIS'. Leave empty for all reports.
    """
    search = openfda.event_search(drug, reaction=reaction)
    try:
        rows, url = openfda.count_by(search, "receivedate", limit=0)
    except Exception as e:
        return _error(f"openFDA failed: {type(e).__name__}: {e}")
    if not rows:
        return _error(f"No FAERS reports for '{drug}'" + (f" with '{reaction}'." if reaction else "."),
                      "Reaction names are MedDRA terms: take one from faers_top_reactions.")
    by_year = Counter()
    for row in rows:
        by_year[row["time"][:4]] += row["count"]
    this_year = str(date.today().year)
    return json.dumps({
        "drug": drug,
        "reaction": reaction or "all reactions",
        "reports_by_year": dict(sorted(by_year.items())),
        "note": f"{this_year} is a partial year. FAERS data lags a few months.",
        "caveat": FAERS_CAVEATS,
        "source": url,
    })


@function_tool
def faers_reaction_detail(drug: str, reaction: str, start_year: int | None = None,
                          end_year: int | None = None) -> str:
    """How serious the reports of one side effect are for one drug: how many reports, their share of
    all the drug's reports, and how many involved hospitalization or death, and who reported them.

    Args:
        drug: Active ingredient, e.g. 'semaglutide'.
        reaction: MedDRA reaction term, e.g. 'PANCREATITIS'.
        start_year: Only reports received in or after this year.
        end_year: Only reports received in or before this year.
    """
    all_search = openfda.event_search(drug, start_year, end_year)
    search = openfda.event_search(drug, start_year, end_year, reaction=reaction)
    try:
        total, _ = openfda.count_reports(all_search)
        with_reaction, url = openfda.count_reports(search)
        if not with_reaction:
            return _error(f"No FAERS reports for '{drug}' list '{reaction}'.",
                          "Reaction names are MedDRA terms: take one from faers_top_reactions.")
        hospital, _ = openfda.count_reports(search + " AND seriousnesshospitalization:1")
        deaths, _ = openfda.count_reports(search + " AND seriousnessdeath:1")
        sexes, _ = openfda.count_by(search, "patient.patientsex", limit=0)
        reporters, _ = openfda.count_by(search, "primarysource.qualification", limit=0)
    except Exception as e:
        return _error(f"openFDA failed: {type(e).__name__}: {e}")
    sex_names = {0: "unknown", 1: "male", 2: "female"}
    reporter_names = {1: "physician", 2: "pharmacist", 3: "other health professional", 4: "lawyer", 5: "consumer"}
    return json.dumps({
        "drug": drug,
        "reaction": reaction,
        "period": f"{start_year or 'start'}-{end_year or 'now'}",
        "reports_with_reaction": with_reaction,
        "all_reports_for_drug": total,
        "share_of_drug_reports": _share(with_reaction, total),
        "hospitalized": hospital,
        "died": deaths,
        "by_sex": {_name(sex_names, r["term"]): r["count"] for r in sexes},
        "reported_by": {_name(reporter_names, r["term"]): r["count"] for r in reporters},
        "note": "'died' counts reports where a death happened, not deaths caused by the drug.",
        "caveat": FAERS_CAVEATS,
        "source": url,
    })


@function_tool
def faers_compare_drugs(drugs: list[str], reaction: str) -> str:
    """Compare drugs on one side effect: for each drug, what share of all its FAERS reports mention
    the reaction. Shares are fairer than raw counts, since popular drugs get more reports of everything.

    Args:
        drugs: Two to five active ingredients, e.g. ['semaglutide', 'tirzepatide'].
        reaction: MedDRA reaction term, e.g. 'PANCREATITIS'.
    """
    if not 2 <= len(drugs) <= 5:
        return _error("Give between 2 and 5 drugs.")
    rows = []
    try:
        for drug in drugs:
            total, _ = openfda.count_reports(openfda.event_search(drug))
            hits, url = openfda.count_reports(openfda.event_search(drug, reaction=reaction))
            rows.append({"drug": drug, "all_reports": total, "reports_with_reaction": hits,
                         "share": _share(hits, total), "source": url})
    except Exception as e:
        return _error(f"openFDA failed: {type(e).__name__}: {e}")
    return json.dumps({
        "reaction": reaction,
        "drugs": rows,
        "note": "A higher share is a signal worth asking a doctor about, not proof of higher risk.",
        "caveat": FAERS_CAVEATS,
    })


# --- Researcher tools: labels and recalls ---

# Recall notices are free text. These buckets make "why was it recalled?" countable.
RECALL_REASONS = [
    ("NDMA or other nitrosamine impurity", ("ndma", "nitrosamine", "ndea", "nitroso")),
    ("Other impurity or contamination", ("impurit", "contamina", "microbial", "benzene", "bacteria")),
    ("Foreign material or wrong pill in the bottle", ("foreign", "particulate", "mix-up", "mixup", "wrong tablet", "found in")),
    ("Failed dissolution or potency test", ("dissolution", "subpotent", "superpotent", "assay", "potency", "out of specification", "oos")),
    ("Labeling or packaging error", ("label", "packag", "mislabel", "carton")),
    ("Storage temperature problem", ("temperature",)),
    ("Sterility or manufacturing practice problem", ("steril", "cgmp", "good manufacturing")),
]


def _recall_reason(text: str) -> str:
    lowered = text.lower()
    for bucket, words in RECALL_REASONS:
        if any(w in lowered for w in words):
            return bucket
    return "Other"



@function_tool
def label_warnings(drug: str, find: str | None = None) -> str:
    """The FDA-approved label for a drug: its boxed warning (FDA's strongest), warnings, and
    listed adverse reactions, plus the label's date. Use it to see whether a reported side effect
    is already on the label.

    Args:
        drug: Active ingredient or brand name, e.g. 'semaglutide' or 'Wegovy'. Brands that share
            an ingredient can have different labels, so use the brand name when it matters.
        find: A word to look for in the whole label, e.g. 'pancreatitis' or 'suicid'. The sections
            returned are shortened, so use this before saying a label does or doesn't mention something.
    """
    try:
        found = openfda.latest_label(drug)
    except Exception as e:
        return _error(f"openFDA failed: {type(e).__name__}: {e}")
    if not found:
        return _error(f"No FDA label found for '{drug}'.",
                      "Try the active ingredient from resolve_drug_name. Some old or OTC drugs have no label here.")
    label = found["label"]
    meta = label.get("openfda", {})
    effective = label.get("effective_time", "")
    set_id = label.get("set_id")
    out = {
        "drug": drug,
        "brand_names": meta.get("brand_name", [])[:5],
        "other_brands_with_this_ingredient": [b for b in found["brands"] if b not in meta.get("brand_name", [])][:8],
        "manufacturer": meta.get("manufacturer_name", [])[:3],
        "label_date": f"{effective[:4]}-{effective[4:6]}-{effective[6:8]}" if len(effective) >= 8 else effective,
        "boxed_warning": openfda.section(label, "boxed_warning") or "None: this label has no boxed warning.",
        "warnings": openfda.section(label, "warnings_and_cautions") or openfda.section(label, "warnings"),
        "adverse_reactions": openfda.section(label, "adverse_reactions"),
        "note": "Sections are cut at 2,500 characters: use find to search the whole label. openFDA serves "
                "the current label, not its history. Other brands of the same ingredient have their own labels.",
        # DailyMed shows the same label as a readable page, so cite it rather than the raw API JSON.
        "source": f"https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid={set_id}" if set_id else found["source"],
    }
    if find:
        out["find"] = _find_in_label(label, find)
    return json.dumps(out)


LABEL_SECTIONS = {
    "boxed_warning": "Boxed warning",
    "warnings_and_cautions": "Warnings and precautions",
    "warnings": "Warnings",
    "contraindications": "Contraindications",
    "adverse_reactions": "Adverse reactions",
    "postmarketing_experience": "Postmarketing experience",
    "spl_medguide": "Medication guide",
    "information_for_patients": "Patient information",
}


def _find_in_label(label: dict, term: str) -> dict:
    """Where a word appears in the full label, with a short passage around the first hit per section.
    Every text section is searched, not only the warnings, because labels file things in many places."""
    t = term.lower().strip()
    skip = {"openfda", "set_id", "id", "version", "effective_time"}
    keys = list(LABEL_SECTIONS) + sorted(k for k in label if k not in LABEL_SECTIONS and k not in skip
                                         and not k.endswith("_table"))
    hits = []
    for key in keys:
        text = openfda.full_text(label, key)
        i = text.lower().find(t)
        if i >= 0:
            title = LABEL_SECTIONS.get(key, key.replace("_", " ").capitalize())
            hits.append({"section": title, "passage": "..." + text[max(0, i - 200):i + 300] + "..."})
    warning_titles = {LABEL_SECTIONS[k] for k in ("boxed_warning", "warnings_and_cautions", "warnings")}
    return {"term": term, "found": bool(hits),
            "in_boxed_warning_or_warnings": any(h["section"] in warning_titles for h in hits),
            "sections": hits[:6]}


@function_tool
def drug_recalls(drug: str, start_year: int | None = None) -> str:
    """FDA drug recalls (enforcement reports) that name this drug: when, why, how serious
    (Class I is the most dangerous), which company, and whether the recall is still open.

    Args:
        drug: Active ingredient or brand name, e.g. 'semaglutide'.
        start_year: Only recalls started in or after this year.
    """
    try:
        rows, total, url = openfda.recalls(drug, start_year)
    except Exception as e:
        return _error(f"openFDA failed: {type(e).__name__}: {e}")
    if not rows:
        return json.dumps({
            "drug": drug,
            "total_recalls": 0,
            "result": "No FDA recalls name this drug" + (f" since {start_year}." if start_year else "."),
            "note": "Enforcement reports start in 2004. Compounded or counterfeit versions may be listed under other names.",
            "source": url,
        })

    def when(d: str) -> str:
        return f"{d[:4]}-{d[4:6]}-{d[6:8]}" if len(d) >= 8 else d

    return json.dumps({
        "drug": drug,
        "total_recalls": total,
        "recalls_summarized": len(rows),
        "by_class": dict(Counter(r.get("classification", "?") for r in rows)),
        "by_year": dict(sorted(Counter((r.get("recall_initiation_date") or "????")[:4] for r in rows).items())),
        # The newest 10 alone can hide the main story (e.g. the 2020-2021 NDMA wave), so count every reason.
        "by_reason": dict(Counter(_recall_reason(r.get("reason_for_recall") or "") for r in rows).most_common()),
        "newest_recalls": "the 10 most recent are listed below",
        "recalls": [
            {
                "recall_number": r.get("recall_number"),
                "started": when(r.get("recall_initiation_date", "")),
                "class": r.get("classification"),
                "status": r.get("status"),
                "firm": r.get("recalling_firm"),
                "reason": (r.get("reason_for_recall") or "")[:300],
                "product": (r.get("product_description") or "")[:200],
            }
            for r in rows[:10]
        ],
        "note": "Class I: could cause serious harm or death. Class II: temporary or reversible harm. Class III: unlikely to cause harm.",
        "source": url,
    })


# --- Researcher tools: how many people take the drug (CMS Medicare Part D) ---


@function_tool
def medicare_users(drug: str) -> str:
    """How many Medicare Part D patients filled a prescription for a drug each year, 2020-2024, by
    brand. Use it to show how widely a drug is used, or how fast use grew.

    Args:
        drug: Active ingredient, e.g. 'semaglutide'.
    """
    try:
        found = medicare.users(drug)
    except Exception as e:
        return _error(f"Could not read the Medicare file: {type(e).__name__}: {e}")
    if not found["brands"]:
        return _error(f"No Medicare Part D data for '{drug}'.",
                      "It may not be a Part D drug (e.g. given in a clinic, or over the counter). Use the active ingredient.")
    return json.dumps({
        "drug": drug,
        "medicare_part_d_users_by_year": found["total_users"],
        "by_brand": [{"brand": b["brand"], "generic": b["generic"], "users": b["users"]} for b in found["brands"]],
        "note": "Users are Medicare Part D beneficiaries (mostly 65+), not all Americans. A patient who used two "
                "brands of the same drug counts once per brand. Combination products are listed but not in the total.",
        "source": medicare.SOURCE,
    })


@function_tool
def faers_report_rate(drug: str, reaction: str = "") -> str:
    """US side-effect reports per 100,000 Medicare Part D users, per year 2020-2024. The fairest way
    here to compare years or drugs: raw report counts grow just because more people take a drug.

    Args:
        drug: Active ingredient, e.g. 'semaglutide'.
        reaction: Optional MedDRA reaction term, e.g. 'PANCREATITIS'. Leave empty for all reports.
    """
    found = medicare.users(drug)
    if not found["brands"]:
        return _error(f"No Medicare Part D data for '{drug}', so no rate can be computed.",
                      "Use faers_trend for raw counts instead.")
    search = openfda.event_search(drug, 2020, 2024, reaction=reaction, country="US")
    try:
        rows, url = openfda.count_by(search, "receivedate", limit=0)
    except Exception as e:
        return _error(f"openFDA failed: {type(e).__name__}: {e}")
    reports = Counter()
    for row in rows:
        reports[int(row["time"][:4])] += row["count"]
    years = []
    for year in medicare.YEARS:
        users = found["total_users"][year]
        years.append({
            "year": year,
            "us_reports": reports.get(year, 0),
            "medicare_users": users,
            "reports_per_100k_users": round(100_000 * reports.get(year, 0) / users, 1) if users else None,
        })
        # Few Medicare users (a new drug, or one Medicare barely covers) make the rate meaningless.
        if users and users < 100_000:
            years[-1]["warning"] = "Under 100,000 Medicare users this year: most reports likely come from people outside Medicare, so this rate overstates."
    return json.dumps({
        "drug": drug,
        "reaction": reaction or "all reactions",
        "by_year": years,
        "note": "A rough reporting rate, not a risk: the reports come from US patients of all ages and insurers, "
                "the users only from Medicare Part D. Use it to compare years or similar drugs, never as 'your chance'.",
        "caveat": FAERS_CAVEATS,
        "source": url,
        "users_source": medicare.SOURCE,
    })


RESEARCHER_TOOLS = [faers_top_reactions, faers_trend, faers_reaction_detail, faers_compare_drugs,
                    faers_report_rate, label_warnings, drug_recalls, medicare_users]
