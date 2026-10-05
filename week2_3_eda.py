"""
Weeks 2-3 Deliverable
Documents unique property types, applies the Residential filter, reports null
counts and columns above 90% null, summarises the distribution of ClosePrice,
LivingArea and DaysOnMarket, and saves the filtered dataset as a new CSV.
"""

from pathlib import Path
import pandas as pd

# --- Settings ---------------------------------------------------------------
DATA_DIR = Path(r"C:/Users/makay/OneDrive/Documents/IDX Internship/csv")   # the monthly CSVs
OUTPUT_DIR = Path(r"C:/Users/makay/OneDrive/Documents/IDX Internship/new csv")        # where results are saved

START, END = "2024-01", "2026-04"

LISTINGS_PATTERN = "CRMLSListing{ym}.csv"
SOLD_PATTERN = "CRMLSSold{ym}.csv"

DISTRIBUTION_FIELDS = ["ClosePrice", "LivingArea", "DaysOnMarket"]
PERCENTILES = [0.01, 0.05, 0.25, 0.50, 0.75, 0.95, 0.99]

months = pd.period_range(START, END, freq="M")

pd.set_option("display.max_rows", 200)
pd.set_option("display.width", 200)


def load_combined(pattern):
    """Concatenate the monthly files WITHOUT filtering, so the unique property
    types and the effect of the filter can both be documented."""
    frames = []
    for m in months:
        ym = m.strftime("%Y%m")
        path = DATA_DIR / pattern.format(ym=ym)
        if not path.exists():
            path = DATA_DIR / pattern.format(ym=ym).replace(".csv", "_filled.csv")
        frames.append(pd.read_csv(path, low_memory=False))
    return pd.concat(frames, ignore_index=True)


def analyze(pattern, label, outfile):
    print(f"\n{'=' * 70}\n{label.upper()}\n{'=' * 70}")

    df = load_combined(pattern)

    # --- Inspect structure --------------------------------------------------
    print(f"Rows: {len(df):,}   Columns: {df.shape[1]}")

    # --- Unique property types found ----------------------------------------
    print("\nUnique property types found:")
    type_counts = df["PropertyType"].value_counts(dropna=False)
    type_table = pd.DataFrame({
        "count": type_counts,
        "pct": (type_counts / len(df) * 100).round(2),
    })
    print(type_table.to_string())

    # --- Filtering logic applied --------------------------------------------
    # Keep only records where PropertyType is exactly 'Residential'. Note that
    # ResidentialLease and ResidentialIncome are separate categories and are
    # excluded by this filter.
    rows_before = len(df)
    df = df[df["PropertyType"] == "Residential"]
    rows_after = len(df)

    print("\nFiltering logic: df[df['PropertyType'] == 'Residential']")
    print(f"  rows before filter: {rows_before:,}")
    print(f"  rows after filter:  {rows_after:,}")
    print(f"  rows removed:       {rows_before - rows_after:,} "
          f"({(rows_before - rows_after) / rows_before * 100:.1f}%)")

    # --- Null-count summary table -------------------------------------------
    nulls = pd.DataFrame({
        "null_count": df.isnull().sum(),
        "null_pct": (df.isnull().mean() * 100).round(2),
    }).sort_values("null_pct", ascending=False)

    print("\nNull-count summary table:")
    print(nulls.to_string())

    # --- Missing value report: columns above 90% null -----------------------
    over_90 = nulls[nulls["null_pct"] > 90]
    print(f"\nColumns above 90% null ({len(over_90)}):")
    print(over_90.to_string() if len(over_90) else "  none")

    nulls.to_csv(OUTPUT_DIR / f"null_report_{label.lower()}.csv")

    # --- Numeric distribution summary ---------------------------------------
    print("\nNumeric distribution summary:")
    rows = {}
    for field in DISTRIBUTION_FIELDS:
        s = pd.to_numeric(df[field], errors="coerce").dropna()
        if s.empty:
            continue
        stats = {
            "count": len(s),
            "min": s.min(),
            "max": s.max(),
            "mean": s.mean(),
            "median": s.median(),
        }
        for p in PERCENTILES:
            stats[f"p{int(p * 100)}"] = s.quantile(p)
        rows[field] = stats

    summary = pd.DataFrame(rows).T.round(2)
    print(summary.to_string())
    summary.to_csv(OUTPUT_DIR / f"distribution_summary_{label.lower()}.csv")

    # --- Save the filtered dataset ------------------------------------------
    df.to_csv(OUTPUT_DIR / outfile, index=False)
    print(f"\nSaved filtered dataset: {outfile}  ({len(df):,} rows)")


OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

analyze(SOLD_PATTERN, "Sold", "sold_residential_filtered.csv")
analyze(LISTINGS_PATTERN, "Listings", "listings_residential_filtered.csv")

print("\nDone.")
