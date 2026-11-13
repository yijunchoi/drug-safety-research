"""
How many Medicare patients filled each drug, per year. FAERS counts reports but not how many people take a drug, so these user counts let us compare report counts against usage.

data/medicare_part_d_users.csv is trimmed from CMS's "Medicare Part D Spending by Drug" (data year
2024, released 2026): one row per brand, the "Overall" row across manufacturers, with total
beneficiaries (users) and claims for 2020-2024. Rebuild it with build_medicare_csv() below.
"""

import csv
from functools import lru_cache
from pathlib import Path

CSV = Path(__file__).parent / "data" / "medicare_part_d_users.csv"
YEARS = list(range(2020, 2025))
SOURCE = "https://data.cms.gov/summary-statistics-on-use-and-payments/medicare-medicaid-spending-by-drug/medicare-part-d-spending-by-drug"


@lru_cache(maxsize=1)
def _rows() -> list[dict]:
    with open(CSV, newline="") as f:
        return list(csv.DictReader(f))


def _int(value: str) -> int | None:
    return int(float(value)) if value else None


def users(drug: str) -> dict:
    """Medicare Part D users per year for every brand whose generic name contains `drug`.
    A blank year means CMS reported no data (not yet on the market, or suppressed)."""
    needle = drug.strip().lower()
    brands = []
    for row in _rows():
        if needle and needle in row["generic"].lower():
            brands.append({
                "brand": row["brand"],
                "generic": row["generic"],
                "combination": "/" in row["generic"],
                "users": {y: _int(row[f"users_{y}"]) for y in YEARS},
                "claims": {y: _int(row[f"claims_{y}"]) for y in YEARS},
            })
    single = [b for b in brands if not b["combination"]]
    total = {y: sum(b["users"][y] or 0 for b in single) or None for y in YEARS}
    return {"brands": brands, "total_users": total}


def build_medicare_csv(source_csv: str) -> None:
    """Trim the CMS download (46 columns, every manufacturer) to what the agent needs."""
    with open(source_csv, encoding="utf-8-sig", newline="") as f:
        rows = [r for r in csv.DictReader(f) if r["Mftr_Name"] == "Overall"]
    CSV.parent.mkdir(exist_ok=True)
    with open(CSV, "w", newline="") as f:
        out = csv.writer(f)
        out.writerow(["brand", "generic"] + [f"users_{y}" for y in YEARS] + [f"claims_{y}" for y in YEARS])
        for r in rows:
            out.writerow([r["Brnd_Name"].strip(), r["Gnrc_Name"].strip()]
                         + [r[f"Tot_Benes_{y}"] for y in YEARS] + [r[f"Tot_Clms_{y}"] for y in YEARS])


if __name__ == "__main__":
    # Rebuild: uv run medicare.py DSD_PTD_RY26_P04_V10_DY24_BGM.csv
    import sys

    if len(sys.argv) > 1:
        build_medicare_csv(sys.argv[1])
    print(users("semaglutide"))
