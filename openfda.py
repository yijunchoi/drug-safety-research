"""Small clients for the two public APIs the agent reads: openFDA and NIH RxNorm.

Every function returns plain dicts that already carry a `source` URL, so the Researchers can cite
exactly which query a number came from. The URLs never include the API key.

openFDA answers "no matches" with HTTP 404, not an empty list. We turn that into an empty result so
the agent can say "no reports found" instead of "the API failed".
"""

import os
import time
from functools import lru_cache

import httpx

OPENFDA = "https://api.fda.gov"
RXNAV = "https://rxnav.nlm.nih.gov/REST"
TIMEOUT = 30

# Label sections are long legal text. This much is enough to quote the warnings.
SECTION_CHARS = 2_500


class NoMatches(Exception):
    """openFDA found nothing for this search."""


def _public_url(path: str, params: dict) -> str:
    """The query URL a person can open in a browser to check a number. No API key in it."""
    return str(httpx.URL(f"{OPENFDA}{path}", params=params))


@lru_cache(maxsize=512)
def _get_cached(path: str, frozen_params: tuple) -> dict:
    params = dict(frozen_params)
    key = os.environ.get("OPENFDA_API_KEY")
    if key:
        params["api_key"] = key
    # openFDA sometimes fails for a moment (500, 503) or rate-limits (429): wait and try again.
    for wait in (1, 3, 6, None):
        response = httpx.get(f"{OPENFDA}{path}", params=params, timeout=TIMEOUT)
        if response.status_code == 404:
            raise NoMatches(params.get("search", ""))
        if response.status_code < 400:
            return response.json()
        if response.status_code not in (429, 500, 502, 503, 504) or wait is None:
            break
        time.sleep(wait)
    # The error names the public URL, never the one with the API key in it.
    public = _public_url(path, {k: v for k, v in params.items() if k != "api_key"})
    if response.status_code == 429:
        raise RuntimeError("openFDA rate limit reached. Set OPENFDA_API_KEY for a higher limit.")
    raise RuntimeError(f"openFDA returned {response.status_code} for {public}")


def openfda_get(path: str, params: dict) -> tuple[dict, str]:
    """GET an openFDA endpoint. Returns (json, public_url). Raises NoMatches on no results."""
    return _get_cached(path, tuple(sorted(params.items()))), _public_url(path, params)


# --- Search strings ---


def _year_range(field: str, start_year: int | None, end_year: int | None) -> str:
    if not start_year and not end_year:
        return ""
    start = f"{int(start_year)}0101" if start_year else "19000101"
    end = f"{int(end_year)}1231" if end_year else "29991231"
    return f" AND {field}:[{start} TO {end}]"


def _clean(name: str) -> str:
    # Quotes would end the phrase early. openFDA phrase search is case-insensitive.
    return name.replace('"', "").strip()


def event_search(drug: str, start_year=None, end_year=None, reaction: str = "", serious_only=False,
                 country: str = "") -> str:
    """FAERS search: reports that list this drug (by generic or brand name)."""
    d = _clean(drug)
    search = f'(patient.drug.openfda.generic_name:"{d}" OR patient.drug.openfda.brand_name:"{d}")'
    if reaction:
        search += f' AND patient.reaction.reactionmeddrapt:"{_clean(reaction)}"'
    if serious_only:
        search += " AND serious:1"
    if country:
        search += f' AND occurcountry:"{_clean(country)}"'
    return search + _year_range("receivedate", start_year, end_year)


# --- FAERS: adverse event reports ---


def count_reports(search: str) -> tuple[int, str]:
    """How many FAERS reports match a search."""
    try:
        data, url = openfda_get("/drug/event.json", {"search": search, "limit": 1})
    except NoMatches:
        return 0, _public_url("/drug/event.json", {"search": search, "limit": 1})
    return data["meta"]["results"]["total"], url


def count_by(search: str, field: str, limit: int = 100) -> tuple[list[dict], str]:
    """openFDA's count API: [{term, count}, ...] for a field, over the reports a search matches."""
    params = {"search": search, "count": field}
    if limit:
        params["limit"] = limit
    try:
        data, url = openfda_get("/drug/event.json", params)
    except NoMatches:
        return [], _public_url("/drug/event.json", params)
    return data.get("results", []), url


# --- Drug labels ---


def latest_label(drug: str) -> dict | None:
    """The most recent FDA label for a drug, or None."""
    d = _clean(drug)
    for search in (f'openfda.generic_name:"{d}"', f'openfda.brand_name:"{d}"'):
        try:
            data, url = openfda_get("/drug/label.json", {"search": search, "limit": 20})
        except NoMatches:
            continue
        labels = sorted(data.get("results", []), key=lambda l: l.get("effective_time", ""), reverse=True)
        if labels:
            # One ingredient can have several labels (Ozempic and Wegovy are both semaglutide),
            # and their warnings differ, so say which brands there are.
            brands = sorted({b for l in labels for b in l.get("openfda", {}).get("brand_name", [])})
            return {"label": labels[0], "versions_found": len(labels), "brands": brands, "source": url}
    return None


def full_text(label: dict, name: str) -> str:
    value = label.get(name) or ""
    return " ".join(value) if isinstance(value, list) else str(value)


def section(label: dict, name: str) -> str | None:
    value = label.get(name)
    if not value:
        return None
    text = " ".join(value) if isinstance(value, list) else str(value)
    return text if len(text) <= SECTION_CHARS else text[:SECTION_CHARS] + " [truncated]"


# --- Recalls (enforcement reports) ---


def recalls(drug: str, start_year=None) -> tuple[list[dict], int, str]:
    """Drug recalls that name this drug, newest first. Returns (recalls, total, url)."""
    d = _clean(drug)
    search = f'(openfda.generic_name:"{d}" OR openfda.brand_name:"{d}" OR product_description:"{d}")'
    search += _year_range("recall_initiation_date", start_year, None)
    params = {"search": search, "limit": 100}
    try:
        data, url = openfda_get("/drug/enforcement.json", params)
    except NoMatches:
        return [], 0, _public_url("/drug/enforcement.json", params)
    rows = sorted(data.get("results", []), key=lambda r: r.get("recall_initiation_date", ""), reverse=True)
    return rows, data["meta"]["results"]["total"], url


# --- RxNorm: brand name -> active ingredient ---


SALTS = {"sulfate", "aspartate", "saccharate", "hydrochloride", "hcl", "sodium", "potassium", "calcium",
         "maleate", "tartrate", "bitartrate", "citrate", "phosphate", "succinate", "fumarate", "mesylate",
         "besylate", "acetate", "bromide", "chloride", "monohydrate", "dihydrate", "anhydrous", "hyclate"}


def base_names(ingredients: list[str]) -> list[str]:
    """Ingredient names without their salt, deduplicated: 'amphetamine aspartate' and 'amphetamine
    sulfate' both become 'amphetamine'. openFDA matches the base name inside every salt's name."""
    out: list[str] = []
    for ingredient in ingredients:
        base = " ".join(w for w in ingredient.lower().split() if w not in SALTS) or ingredient.lower()
        if base not in out:
            out.append(base)
    return out


@lru_cache(maxsize=256)
def rxnorm_names(name: str) -> dict:
    """Map any drug name (brand, misspelling) to its active ingredient(s) and brand names."""
    found = httpx.get(f"{RXNAV}/approximateTerm.json", params={"term": name, "maxEntries": 1}, timeout=TIMEOUT)
    found.raise_for_status()
    candidates = found.json().get("approximateGroup", {}).get("candidate", [])
    if not candidates:
        return {}
    rxcui = candidates[0]["rxcui"]
    related = httpx.get(f"{RXNAV}/rxcui/{rxcui}/related.json", params={"tty": "IN BN"}, timeout=TIMEOUT)
    related.raise_for_status()
    names: dict[str, list[str]] = {"IN": [], "BN": []}
    for group in related.json().get("relatedGroup", {}).get("conceptGroup", []):
        for concept in group.get("conceptProperties", []) or []:
            names.setdefault(group.get("tty"), []).append(concept["name"])
    ingredients = names.get("IN", [])
    return {
        "rxcui": rxcui,
        "ingredients": ingredients,
        "search_names": base_names(ingredients),
        "brand_names": names.get("BN", [])[:15],
        "source": f"https://mor.nlm.nih.gov/RxNav/search?searchBy=RXCUI&searchTerm={rxcui}",
    }
