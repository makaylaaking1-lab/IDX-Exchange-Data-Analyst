"""
Week 1 Deliverable
Concatenates all monthly MLS files from January 2024 through the most recent
month available into two combined datasets (listings and sold), filters both
to PropertyType == 'Residential', and saves them as new CSVs.

Note: some sold months exist only as "_filled" files, so the script checks for
the standard name first and falls back to the _filled name when needed.
"""

from pathlib import Path
import pandas as pd

# --- Settings ---------------------------------------------------------------
DATA_DIR = Path( r"C:/Users/makay/OneDrive/Documents/IDX Internship/csv")   # folder with the monthly CSVs
OUTPUT_DIR = Path(r"C:/Users/makay/OneDrive/Documents/IDX Internship/new csv")        # where the combined CSVs are saved

START = "2024-01"
END = "2026-04"

LISTINGS_PATTERN = "CRMLSListing{ym}.csv"
SOLD_PATTERN = "CRMLSSold{ym}.csv"

months = pd.period_range(START, END, freq="M")


def build_dataset(pattern, label):
    print(f"\n--- {label} ---")

    monthly_frames = []
    rows_before_concat = 0

    for m in months:
        ym = m.strftime("%Y%m")

        # Use the standard file if it exists, otherwise the _filled version.
        path = DATA_DIR / pattern.format(ym=ym)
        if not path.exists():
            path = DATA_DIR / pattern.format(ym=ym).replace(".csv", "_filled.csv")

        df = pd.read_csv(path, low_memory=False)
        print(f"{m}: {len(df):,} rows")

        rows_before_concat += len(df)
        monthly_frames.append(df)

    # Row count BEFORE concatenation (sum of all individual monthly files)
    print(f"\n{label} rows before concatenation: {rows_before_concat:,}")

    combined = pd.concat(monthly_frames, ignore_index=True)

    # Row count AFTER concatenation (should match the count above)
    print(f"{label} rows after concatenation: {len(combined):,}")

    # Row count BEFORE the Residential filter
    rows_before_filter = len(combined)
    print(f"{label} rows before Residential filter: {rows_before_filter:,}")

    combined = combined[combined["PropertyType"] == "Residential"]

    # Row count AFTER the Residential filter
    print(f"{label} rows after Residential filter: {len(combined):,}")

    return combined


OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

listings = build_dataset(LISTINGS_PATTERN, "Listings")
listings.to_csv(OUTPUT_DIR / "listings_combined_residential.csv", index=False)

sold = build_dataset(SOLD_PATTERN, "Sold")
sold.to_csv(OUTPUT_DIR / "sold_combined_residential.csv", index=False)

print(f"\nSaved both files to {OUTPUT_DIR}")


# --- Row count confirmation (fill in after running) -------------------------
# Listings
#   Rows before concatenation: ______
#   Rows after concatenation:  ______
#   Rows before Residential filter: ______
#   Rows after Residential filter:  ______
#
# Sold
#   Rows before concatenation: ______
#   Rows after concatenation:  ______
#   Rows before Residential filter: ______
#   Rows after Residential filter:  ______
