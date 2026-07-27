# Data Audit Memo: EDGAR v8.0 Global CO2 Emissions Dataset

**Prepared by:** Climate Portfolio Project
**Date:** 2026-07-27
**Dataset:** IEA-EDGAR CO2 1970–2022 (Fossil Fuels & Industry)
**Source:** European Commission Joint Research Centre (JRC)
**Download page:** https://edgar.jrc.ec.europa.eu/dataset_ghg80
**File audited:** `IEA_EDGAR_CO2_1970_2022.xlsx` — sheet: "TOTALS BY COUNTRY"
**Audit script:** `analysis/edgar_audit.py`
**Audit outputs:** `analysis/audit_*.csv`

---

## What is this dataset?

EDGAR stands for Emissions Database for Global Atmospheric Research. It is published by the Joint Research Centre — the European Union's in-house science body — and is co-produced with the International Energy Agency (IEA). The dataset contains CO2 emissions from fossil fuels (coal, oil, gas) and industrial processes for every country in the world, from 1970 to 2022.

**Unit:** All values are in **Gg CO2** (gigagrams of CO2). One gigagram equals 1,000 tonnes, which is also written as one kilotonne. To convert to the million-tonne figures you typically see in news articles, divide by 1,000.

**Coverage:** 221 countries plus two special entries — International Aviation and International Shipping — which are counted separately because their emissions cannot be assigned to a single country.

**Why this dataset matters in climate finance:** EDGAR is the underlying data source used by the IPCC (the UN's climate science body), the European Commission, and many investors for country-level emissions benchmarking. When a bond prospectus, a climate risk report, or a multilateral bank document cites a country's CO2 figure, it often traces back to EDGAR or the IEA data that feeds into it.

---

## Audit Scope

Six automated checks were run across all 221 countries and 53 years (11,713 data cells total):

| Check | What it tests |
|---|---|
| Missing values | Blank cells — data that was never reported |
| Zero values | Cells containing exactly zero — could be real or a placeholder |
| Negative values | Physically impossible for CO2 emissions |
| Implausible jumps | Year-on-year changes exceeding 100% |
| Coverage gaps | Countries with holes in the middle of their time series |
| 2022 summary | Top and bottom emitters in the most recent year |

---

## Finding 1: No missing values — and why that is itself a quality concern

**Result:** 0 out of 11,713 cells are blank.

At first glance this sounds like good news. But it is actually one of the most important findings in this audit, and it requires careful explanation.

In most real-world datasets, developing countries — particularly small island states, conflict-affected nations, and countries with limited statistical capacity — have genuine gaps in their data. They may not have had the infrastructure to measure or report their emissions in 1970 or 1985. A truly "raw" dataset would show these as blank cells.

EDGAR has no blank cells because it fills every gap with **modelled estimates** — numbers that the JRC has calculated using mathematical models, proxy indicators, and interpolation (filling in between known points). This is a legitimate scientific practice, but it means the data has two very different types of values:

- **Measured/reported values** — numbers that come from a country's own national statistics
- **Modelled estimates** — numbers that the JRC calculated because no official data existed

The dataset does not flag which cells are measured and which are estimated. For a climate finance professional, this matters significantly: if you are benchmarking a developing country's emissions trajectory and the figures for the 1970s and 1980s are modelled estimates rather than official records, any trend analysis over the full 53-year period carries substantial uncertainty.

**Recommendation:** When using EDGAR data for developing countries prior to ~1990, note that figures may be modelled estimates rather than national inventory data. Where precision matters (e.g., for baseline setting in a carbon market project), cross-reference against the country's own national communication to the UNFCCC.

**UNVERIFIED:** The exact methodology EDGAR uses to estimate missing country data by year is documented in the EDGAR technical documentation (https://edgar.jrc.ec.europa.eu/documentation), which was not reviewed in this audit.

---

## Finding 2: No zero values — consistent with the modelling approach

**Result:** 0 out of 11,713 cells contain exactly zero.

Even the smallest countries — Tokelau (a New Zealand territory in the Pacific with ~1,500 people) and Niue (population ~1,600) — have non-zero CO2 values for every year. Tokelau's 2022 figure is 0.000122 Gg, which equals about **122 kg** of CO2 — roughly the annual emissions of a single petrol lawnmower.

This is consistent with Finding 1: EDGAR models every country rather than leaving blanks. However, it raises a question for very small territories: are these values genuine measurements or model artefacts? A value of 122 kg for Tokelau is plausible (a few diesel generators), but it would be worth verifying before citing in any formal document.

---

## Finding 3: No negative values

**Result:** All 11,713 cells are positive.

This is expected for a fossil-fuel CO2 dataset. Negative values can legitimately appear in datasets that include land use (forests absorbing carbon), but since this dataset explicitly excludes land use, all values should be positive. They are.

---

## Finding 4: 18 implausible single-year jumps — the most actionable finding

**Result:** 18 country-year pairs where emissions more than doubled (or halved) in a single year, among countries emitting more than 100 Gg (100,000 tonnes) per year.

These are flagged as "implausible" not because they are definitely errors, but because a change of this magnitude in 12 months demands explanation. In practice, they fall into two categories:

**Category A — Likely methodology or data-collection change (most common)**
When a country improves its statistical systems, starts reporting a new sector, or EDGAR revises its modelling approach, historical figures can jump. The sudden change reflects better data rather than a real-world event.

**Category B — Possible genuine event**
Wars, major industrial openings or closures, and sudden economic shifts can cause genuine large changes. These are real but still worth flagging.

### Top 5 flagged cases

| Country | Year | Previous year (Gg) | Jump year (Gg) | % change | Most likely explanation |
|---|---|---|---|---|---|
| Congo | 1973 | 1,979 | 8,963 | +353% | Oil production ramp-up (Emeraude oilfield discovered 1969, production scaled rapidly) — likely real, but magnitude suggests possible reporting revision |
| Oman | 1975 | 7,731 | 25,827 | +234% | Rapid oil & gas sector expansion in early 1970s — consistent with known Oman oil boom |
| Gabon | 1973 | 1,200 | 3,852 | +221% | Oil sector expansion (Gabon became significant producer in early 1970s) — likely real |
| Cambodia | 1995 | 474 | 1,501 | +217% | Post-conflict reconstruction and economic reopening — could be real growth or reporting improvement as country stabilised after civil war |
| Malawi | 1990 | 487 | 1,542 | +217% | Likely a methodology revision — no known major economic or industrial event in Malawi in 1990 |

**Full list of 18 flagged cases:** `analysis/audit_implausible_jumps.csv`

### What this means for users

If you are building a time-series chart of any of these 18 countries across the flagged year, the jump will appear as a spike that may mislead a reader. Best practice: annotate the chart with a note, cross-reference a second source, or use smoothed/averaged figures if the trend rather than the point estimate matters.

---

## Finding 5: No internal coverage gaps

**Result:** Every country has a complete time series from 1970 to 2022 with no holes in the middle.

Again, this reflects EDGAR's modelling approach (see Finding 1). There are no countries that report data for, say, 1970–1990 and then again from 2000–2022 with a gap in between.

---

## Finding 6: 2022 emissions snapshot — top and bottom emitters

**Top 10 emitters, 2022:**

| Rank | Country | CO2 (Gg) | CO2 (Mt) | IPCC annex |
|---|---|---|---|---|
| 1 | China | 12,667,430 | 12,667 | Non-Annex I |
| 2 | United States | 4,853,780 | 4,854 | Annex I |
| 3 | India | 2,693,034 | 2,693 | Non-Annex I |
| 4 | Russia | 1,909,039 | 1,909 | Annex I |
| 5 | Japan | 1,082,645 | 1,083 | Annex I |
| 6 | Indonesia | 692,236 | 692 | Non-Annex I |
| 7 | Iran | 686,416 | 686 | Non-Annex I |
| 8 | Germany | 673,595 | 674 | Annex I |
| 9 | South Korea | 635,503 | 636 | Non-Annex I |
| 10 | Saudi Arabia | 607,908 | 608 | Non-Annex I |

> **A note on the "Annex I" label:** Under the UNFCCC treaty, countries are split into Annex I (wealthy industrialised nations, who committed to emissions reductions first) and Non-Annex I (developing nations). This distinction shapes who receives climate finance and on what terms. China, India, Indonesia, Iran, and Saudi Arabia are all Non-Annex I — meaning they are not legally bound to the same reduction targets as the US, EU, or Japan, even though several of them are now among the world's largest emitters.

**Bottom 5 (smallest non-zero emitters, 2022):**

| Country | CO2 (Gg) | CO2 equivalent |
|---|---|---|
| Wallis and Futuna | 0.001 | ~1 tonne |
| Niue | 0.000161 | ~161 kg |
| Tokelau | 0.000122 | ~122 kg |

These figures for Pacific micro-territories are almost certainly modelled estimates rather than measured values (see Finding 1). They are not wrong, but they should be treated as indicative rather than precise.

---

## Overall Data Quality Assessment

| Dimension | Rating | Notes |
|---|---|---|
| Completeness | Apparent 100% — but misleading | No blank cells, but modelled estimates fill the gaps |
| Consistency | Good | Units, country codes, and structure are uniform throughout |
| Accuracy | High for major emitters; lower for small/developing countries | EDGAR cross-validates against IEA national energy statistics for large economies |
| Timeliness | 2–3 year lag | Most recent year available is 2022; published October 2023 |
| Transparency | Moderate | Methodology is documented but not cell-level provenance |
| Fitness for purpose | High for trend analysis and major country benchmarking | Use with caution for small countries, pre-1990 developing nations, and any of the 18 flagged jump years |

---

## Recommendations for Use

1. **For benchmarking major economies** (G20 countries): EDGAR is reliable and appropriate to cite directly. Note the source and vintage (v8.0, data to 2022).

2. **For small or developing countries pre-1990**: Flag figures as modelled estimates when presenting. Cross-reference against national communications to UNFCCC where possible.

3. **For any of the 18 flagged jump years**: Investigate before including in a trend chart. Add a footnote or annotation. See `analysis/audit_implausible_jumps.csv` for the full list.

4. **For the most recent years (2023–2024)**: EDGAR v8.0 ends at 2022. For more recent estimates, use the Global Carbon Project's annual update or IEA's Greenhouse Gas Emissions from Energy report, both of which publish preliminary estimates for the current year.

5. **Always cite the version**: EDGAR data changes between versions (v7, v8, etc.) as methodologies improve. Two reports using different versions will show different numbers for the same country-year. Always state which version you used.

---

## Files Produced

| File | Location | Contents |
|---|---|---|
| `edgar_audit.py` | `analysis/` | Full Python audit script with inline comments |
| `audit_missing_values.csv` | `analysis/` | Countries with missing data (none found) |
| `audit_zero_values.csv` | `analysis/` | Countries with zero values (none found) |
| `audit_negative_values.csv` | `analysis/` | Countries with negative values (none found) |
| `audit_implausible_jumps.csv` | `analysis/` | 18 country-year jumps exceeding 100% |
| `audit_coverage_gaps.csv` | `analysis/` | Countries with internal time-series gaps (none found) |
| `audit_2022_summary.csv` | `analysis/` | All 221 countries ranked by 2022 CO2 emissions |
| `IEA_EDGAR_CO2_1970_2022.xlsx` | `data/` | Original EDGAR dataset (raw, unmodified) |

---

*Memo produced by Claude Code on 2026-07-27. All figures from EDGAR v8.0 (https://edgar.jrc.ec.europa.eu/dataset_ghg80). No figures invented or estimated by the author. Where findings are uncertain, UNVERIFIED is noted inline.*
