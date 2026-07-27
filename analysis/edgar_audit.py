"""
EDGAR v8.0 CO2 Data Audit
==========================
Dataset : IEA-EDGAR CO2 1970-2022 (fossil fuels and industry)
Source  : European Commission Joint Research Centre
URL     : https://edgar.jrc.ec.europa.eu/dataset_ghg80
File    : data/IEA_EDGAR_CO2_1970_2022.xlsx
Run on  : 2026-07-27

What this script does, in plain English:
-----------------------------------------
It loads the EDGAR CO2 spreadsheet and runs six quality checks:

  1. STRUCTURE CHECK — How many countries, years, sectors are there?
     What are the column names and data types?

  2. MISSING VALUES — Are there any blank cells? Missing data is a real
     problem because a blank and a zero look the same in a chart but mean
     very different things (no data vs. genuinely no emissions).

  3. ZERO VALUES — Which countries have a lot of zeros? Zeros might be
     real (a tiny island with no industry) or a placeholder for missing data.

  4. NEGATIVE VALUES — CO2 emissions cannot be negative. If any appear,
     it is either a data entry error or a methodological quirk worth flagging.

  5. IMPLAUSIBLE JUMPS — If a country's emissions more than double or halve
     in a single year, that is suspicious. It could be a real event (a war,
     a major industry closing) or a reporting error or a methodology change.

  6. COVERAGE GAPS — Which countries have the most missing years across
     the full 1970-2022 series?

All results are saved as CSV files in analysis/ for use in the memo.
"""

import pandas as pd
import numpy as np
import os

# ── 0. Setup ──────────────────────────────────────────────────────────────────

DATA_PATH = "/Users/vivaanmadhok/Documents/Climate-Portfolio/climate-portfolio/data/IEA_EDGAR_CO2_1970_2022.xlsx"
OUT_DIR   = "/Users/vivaanmadhok/Documents/Climate-Portfolio/climate-portfolio/analysis/"
SOURCE_URL = "https://edgar.jrc.ec.europa.eu/dataset_ghg80"

os.makedirs(OUT_DIR, exist_ok=True)

print("=" * 65)
print("EDGAR v8.0 CO2 Data Audit")
print(f"Source: {SOURCE_URL}")
print("=" * 65)

# ── 1. LOAD DATA ──────────────────────────────────────────────────────────────
# The spreadsheet has 9 rows of metadata before the actual table.
# We skip those and read the rest as a proper table.

print("\n[1] Loading data...")

df_raw = pd.read_excel(
    DATA_PATH,
    sheet_name="TOTALS BY COUNTRY",
    header=9  # Row index 9 (the 10th row) contains the column headers
)

# Year columns are named Y_1970, Y_1971, ... Y_2022
year_cols = [c for c in df_raw.columns if str(c).startswith("Y_")]
years     = [int(c.replace("Y_", "")) for c in year_cols]
id_cols   = ["IPCC_annex", "C_group_IM24_sh", "Country_code_A3", "Name", "Substance"]

print(f"  Rows loaded       : {len(df_raw):,}")
print(f"  Columns total     : {len(df_raw.columns)}")
print(f"  Year columns      : {years[0]}–{years[-1]} ({len(year_cols)} years)")
print(f"  Unique countries  : {df_raw['Name'].nunique()}")
print(f"  Unique IPCC annex : {df_raw['IPCC_annex'].unique().tolist()}")
print(f"  Unit              : Gg CO2 (gigagrams = 1,000 tonnes = kilotonnes)")

# Separate real countries from special aggregates like Int. Aviation, Int. Shipping
special = df_raw[df_raw["Country_code_A3"].isin(["AIR", "SEA", "AIR+SEA"])]
df      = df_raw[~df_raw["Country_code_A3"].isin(["AIR", "SEA", "AIR+SEA"])].copy()

print(f"\n  Special entries excluded from country analysis:")
for _, row in special.iterrows():
    print(f"    {row['Country_code_A3']:8s} — {row['Name']}")
print(f"\n  Country rows for analysis: {len(df):,}")

# ── 2. MISSING VALUES ─────────────────────────────────────────────────────────

print("\n[2] Checking for missing values (blank cells)...")

missing_per_country = df[year_cols].isnull().sum(axis=1)
countries_with_missing = df[missing_per_country > 0][["Country_code_A3", "Name", "IPCC_annex"]].copy()
countries_with_missing["missing_years"] = missing_per_country[missing_per_country > 0].values
countries_with_missing = countries_with_missing.sort_values("missing_years", ascending=False)

total_cells    = len(df) * len(year_cols)
total_missing  = df[year_cols].isnull().sum().sum()

print(f"  Total data cells          : {total_cells:,}")
print(f"  Missing (blank) cells     : {int(total_missing):,}  ({100*total_missing/total_cells:.2f}%)")
print(f"  Countries with any missing: {len(countries_with_missing)}")

if len(countries_with_missing) > 0:
    print(f"\n  Top 10 countries with most missing years:")
    print(countries_with_missing.head(10).to_string(index=False))

countries_with_missing["source"] = SOURCE_URL
countries_with_missing.to_csv(OUT_DIR + "audit_missing_values.csv", index=False)
print(f"\n  Saved: analysis/audit_missing_values.csv")

# ── 3. ZERO VALUES ────────────────────────────────────────────────────────────

print("\n[3] Checking for zero values...")

zeros_per_country = (df[year_cols] == 0).sum(axis=1)
countries_with_zeros = df[zeros_per_country > 0][["Country_code_A3", "Name", "IPCC_annex"]].copy()
countries_with_zeros["zero_years"] = zeros_per_country[zeros_per_country > 0].values
countries_with_zeros = countries_with_zeros.sort_values("zero_years", ascending=False)

total_zeros = (df[year_cols] == 0).sum().sum()
print(f"  Total zero cells          : {int(total_zeros):,}  ({100*total_zeros/total_cells:.2f}%)")
print(f"  Countries with any zeros  : {len(countries_with_zeros)}")

if len(countries_with_zeros) > 0:
    print(f"\n  Top 15 countries with most zero-value years:")
    print(countries_with_zeros.head(15).to_string(index=False))

countries_with_zeros["source"] = SOURCE_URL
countries_with_zeros.to_csv(OUT_DIR + "audit_zero_values.csv", index=False)
print(f"\n  Saved: analysis/audit_zero_values.csv")

# ── 4. NEGATIVE VALUES ────────────────────────────────────────────────────────

print("\n[4] Checking for negative values...")

neg_mask = df[year_cols] < 0
negatives = []
for col in year_cols:
    year = int(col.replace("Y_", ""))
    neg_rows = df[neg_mask[col]][["Country_code_A3", "Name", "IPCC_annex"]].copy()
    if len(neg_rows) > 0:
        neg_rows["year"]  = year
        neg_rows["value_gg"] = df.loc[neg_mask[col], col].values
        negatives.append(neg_rows)

if negatives:
    neg_df = pd.concat(negatives).sort_values("value_gg")
    print(f"  Negative values found: {len(neg_df)}")
    print(neg_df.to_string(index=False))
    neg_df["source"] = SOURCE_URL
    neg_df.to_csv(OUT_DIR + "audit_negative_values.csv", index=False)
    print(f"\n  Saved: analysis/audit_negative_values.csv")
else:
    print("  No negative values found.")
    pd.DataFrame({"result": ["No negative values found"], "source": [SOURCE_URL]}).to_csv(
        OUT_DIR + "audit_negative_values.csv", index=False)

# ── 5. IMPLAUSIBLE JUMPS ──────────────────────────────────────────────────────
# A "jump" is when emissions change by more than 100% in a single year.
# (i.e., more than double or less than half the previous year.)
# We only check countries where the prior year value is > 100 Gg
# to avoid false alarms from tiny countries where small absolute changes
# look enormous in percentage terms.

print("\n[5] Checking for implausible year-on-year jumps (>100% change)...")

JUMP_THRESHOLD  = 1.0   # 100% change
MIN_BASE_VALUE  = 100   # Gg — ignore very small emitters to avoid noise

jumps = []
for i in range(1, len(year_cols)):
    prev_col = year_cols[i - 1]
    curr_col = year_cols[i]
    curr_year = int(curr_col.replace("Y_", ""))

    prev_vals = df[prev_col]
    curr_vals = df[curr_col]

    # Only check rows where previous value exists and is large enough
    valid = prev_vals.notna() & curr_vals.notna() & (prev_vals.abs() > MIN_BASE_VALUE)
    pct_change = ((curr_vals - prev_vals) / prev_vals.abs()).abs()

    flagged = df[valid & (pct_change > JUMP_THRESHOLD)][["Country_code_A3", "Name", "IPCC_annex"]].copy()
    if len(flagged) > 0:
        flagged["year"]          = curr_year
        flagged["prev_value_gg"] = prev_vals[valid & (pct_change > JUMP_THRESHOLD)].values
        flagged["curr_value_gg"] = curr_vals[valid & (pct_change > JUMP_THRESHOLD)].values
        flagged["pct_change"]    = pct_change[valid & (pct_change > JUMP_THRESHOLD)].values
        jumps.append(flagged)

if jumps:
    jumps_df = pd.concat(jumps).sort_values("pct_change", ascending=False)
    print(f"  Implausible jumps found: {len(jumps_df)}")
    print(f"\n  Top 20 largest single-year jumps:")
    print(jumps_df.head(20)[["Country_code_A3", "Name", "year", "prev_value_gg", "curr_value_gg", "pct_change"]].to_string(index=False))
    jumps_df["source"] = SOURCE_URL
    jumps_df.to_csv(OUT_DIR + "audit_implausible_jumps.csv", index=False)
    print(f"\n  Saved: analysis/audit_implausible_jumps.csv")
else:
    print("  No implausible jumps found.")

# ── 6. COVERAGE GAPS ──────────────────────────────────────────────────────────
# A "coverage gap" is a country that has data in some years but not others,
# creating a hole in the time series. This is different from being missing
# across the whole dataset.

print("\n[6] Checking coverage gaps (countries with patchy time series)...")

def find_gaps(row):
    """Count internal gaps: years missing between first and last non-null year."""
    vals = row[year_cols]
    non_null_idx = vals.notna()
    if non_null_idx.sum() == 0:
        return 0
    first = non_null_idx.idxmax()
    last  = non_null_idx[::-1].idxmax()
    first_pos = year_cols.index(first)
    last_pos  = year_cols.index(last)
    span = vals.iloc[first_pos:last_pos + 1]
    return span.isnull().sum()

df["internal_gaps"] = df.apply(find_gaps, axis=1)
gapped = df[df["internal_gaps"] > 0][["Country_code_A3", "Name", "IPCC_annex", "internal_gaps"]].sort_values(
    "internal_gaps", ascending=False)

print(f"  Countries with internal gaps in time series: {len(gapped)}")
if len(gapped) > 0:
    print(f"\n  Top 15:")
    print(gapped.head(15).to_string(index=False))
    gapped["source"] = SOURCE_URL
    gapped.to_csv(OUT_DIR + "audit_coverage_gaps.csv", index=False)
    print(f"\n  Saved: analysis/audit_coverage_gaps.csv")

# ── 7. SUMMARY STATISTICS ─────────────────────────────────────────────────────

print("\n[7] Summary statistics for 2022 (most recent year)...")

latest = df[["Country_code_A3", "Name", "IPCC_annex", "Y_2022"]].copy()
latest.columns = ["code", "country", "annex", "co2_gg_2022"]
latest = latest.dropna(subset=["co2_gg_2022"]).sort_values("co2_gg_2022", ascending=False)

print(f"\n  Top 10 emitters in 2022 (Gg CO2 = kilotonnes):")
print(latest.head(10).to_string(index=False))

print(f"\n  Bottom 10 non-zero emitters in 2022:")
bottom = latest[latest["co2_gg_2022"] > 0].tail(10)
print(bottom.to_string(index=False))

print(f"\n  Countries with zero or null for 2022: {latest[latest['co2_gg_2022'] <= 0].shape[0]}")

latest["source"] = SOURCE_URL
latest.to_csv(OUT_DIR + "audit_2022_summary.csv", index=False)
print(f"\n  Saved: analysis/audit_2022_summary.csv")

# ── 8. DONE ───────────────────────────────────────────────────────────────────

print("\n" + "=" * 65)
print("Audit complete. Files saved to analysis/:")
for f in sorted(os.listdir(OUT_DIR)):
    if f.startswith("audit_"):
        path = os.path.join(OUT_DIR, f)
        print(f"  {f:45s} ({os.path.getsize(path):,} bytes)")
print("=" * 65)
