# Climate Finance Portfolio

**Independent consulting-grade climate and ESG analysis built from primary sources.**

This portfolio demonstrates the analytical skills required for climate finance, ESG advisory, and sustainable investment roles — including at multilateral development banks (MDBs), development finance institutions (DFIs), ESG research houses, and sustainable investment teams. Every deliverable is sourced from official, publicly available documents. Every figure is cited. Where data could not be verified, it is marked **UNVERIFIED**.

Built using real regulatory filings, public hazard databases, and global emissions datasets — no paywalled tools, no invented numbers.

---

## Portfolio at a Glance

### Case Study 1 — Reliance Industries (India's largest company)

A complete, five-deliverable independent ESG case study on Reliance Industries Limited, built from the company's BRSR 2024-25 (Deloitte-assured) and Annual Report 2024-25.

| Deliverable | What it does | View |
|---|---|---|
| **Carbon Dashboard** | Interactive 4-year Scope 1/2 trend, segment breakdown, Net Zero target, data quality alerts | [Live app ↗](https://vivaanm.github.io/Climate_Portfolio/deliverables/reliance_dashboard.html) |
| **Double Materiality Matrix** | CSRD-style scatter plot scoring 12 ESG issues on financial and impact axes; independent scores vs Reliance's self-assessment with 3 flagged discrepancies | [Live app ↗](https://vivaanm.github.io/Climate_Portfolio/deliverables/reliance_materiality_matrix.html) |
| **Strategy Note** | Ranked analysis of 9 disclosed carbon reduction initiatives — what's operational vs what's announced, and why the current pace is 20× too slow for the 2035 Net Zero target | [Read ↗](deliverables/reliance_strategy_note.md) |
| **Physical Risk Register** | Interactive Leaflet map of 10 manufacturing sites with ThinkHazard (World Bank) hazard ratings across cyclone, coastal flood, river flood, extreme heat, water scarcity, and earthquake | [Live app ↗](https://vivaanm.github.io/Climate_Portfolio/deliverables/reliance_risk_register.html) |
| **TCFD Analyst Report** | Full TCFD-aligned independent analyst report covering all four pillars (Governance, Strategy, Risk Management, Metrics & Targets), key findings, and a structured compliance gap table | [Read ↗](deliverables/reliance_tcfd_report.md) |

**The headline findings across the case study:**
- Reliance discloses 37.93 Mt CO₂e of Scope 1+2 (BRSR p.36, Deloitte-assured) — but discloses no Scope 3, which for an oil refining business is estimated to be 8–10× larger (UNVERIFIED — sector peer estimate)
- 8 of 10 manufacturing sites are rated High overall physical risk; the Jamnagar refinery complex scores High on 5 of 6 hazard categories
- At the demonstrated reduction pace of ~0.19 Mt/yr, the 2035 Net Zero target would require a 20× acceleration with no disclosed pathway
- Three discrepancies found between Reliance's self-reported materiality framing and the independent data assessment

---

### Case Study 2 — EDGAR v8.0 Global CO₂ Audit

A professional data quality audit of the IEA-EDGAR CO₂ 1970–2022 dataset (221 countries, 53 years, 11,713 data cells) — the same dataset used by the IPCC and European Commission for country emissions benchmarking.

| Deliverable | What it does | View |
|---|---|---|
| **Data Audit Memo** | Six-check audit covering missing values, zeros, negatives, implausible jumps, coverage gaps, and a 2022 emissions snapshot; found 18 implausible single-year jumps worth investigating | [Read ↗](deliverables/edgar_data_audit_memo.md) |

---

### Case Study 3 — India Climate Profile

A 20-year (2004–2024) climate and development data profile for India, built from World Bank Open Data APIs, with CO₂ emissions, renewable energy share, GDP, and population — every data point source-cited with a URL.

| Deliverable | What it does | View |
|---|---|---|
| **India Climate Profile** | Country-level data table, key findings, and per-capita derived calculations — a model for sovereign climate analysis | [Read ↗](deliverables/india_climate_profile.md) |

---

## Skills Demonstrated

### Climate & ESG Frameworks
- **TCFD** (Task Force on Climate-related Financial Disclosures) — applied at full four-pillar depth to an Indian industrial company
- **CSRD double materiality** (EU Corporate Sustainability Reporting Directive) — two-axis scoring of financial and impact materiality across 12 issues
- **Scope 1 / 2 / 3 emissions accounting** — extraction from Deloitte-assured BRSR filings, gap identification, peer comparison
- **BRSR** (India's SEBI-mandated Business Responsibility and Sustainability Report) — reading and extracting data from primary regulatory filings
- **Physical risk assessment** — ThinkHazard (GFDRR/World Bank) and WRI Aqueduct 4.0 for multi-hazard and water risk analysis
- **PAT scheme and Indian regulatory compliance** — India's energy efficiency regulatory programme

### Data and Research
- Extracting structured data from PDF regulatory filings using Python (pdfplumber)
- Working with World Bank Open Data API for sovereign climate indicators
- Auditing a 221-country, 53-year global emissions dataset (EDGAR v8.0) for data quality
- Cross-referencing multiple official sources to identify disclosure gaps and discrepancies
- Applying independent judgment against self-reported corporate narratives
- Disciplined source citation: every figure cited to an exact document and page; UNVERIFIED flags applied consistently

### Technical
- Python (pandas, pdfplumber, requests, openpyxl) — data extraction, cleaning, audit scripts
- HTML / CSS / JavaScript — single-file interactive dashboard and risk register applications
- Chart.js — data visualisation (bar, donut, scatter, line charts)
- Leaflet.js — open-source geospatial mapping with OpenStreetMap tiles
- Git / GitHub — version control, commit history, GitHub Pages hosting

---

## Data Sources

All data comes from official, publicly available sources. No paywalled data was used.

| Source | Used for |
|---|---|
| [RIL BRSR 2024-25](https://www.ril.com) — Deloitte-assured | Scope 1/2 emissions, energy, air, water, materiality, site list |
| [RIL Annual Report 2024-25](https://www.ril.com) | Net Zero target, Giga Complex, Jio renewable commitment |
| [EDGAR v8.0](https://edgar.jrc.ec.europa.eu/dataset_ghg80) — JRC/IEA | Global CO₂ 1970–2022, 221 countries |
| [World Bank Open Data API](https://data.worldbank.org) | India CO₂, GDP, population, renewable energy 2004–2024 |
| [ThinkHazard — GFDRR/World Bank](https://thinkhazard.org) | Multi-hazard ratings for all 10 Reliance manufacturing sites |
| [WRI Aqueduct 4.0](https://www.wri.org/applications/aqueduct/water-risk-atlas/) | Water stress — India country level; site-level UNVERIFIED |
| [SEBI BRSR Framework](https://www.sebi.gov.in) | India's mandatory sustainability reporting standard |
| [TCFD Recommendations](https://www.fsb-tcfd.org/recommendations/) | Four-pillar climate disclosure framework |
| [SBTi](https://sciencebasedtargets.org) | Target validation standard (Jio renewable target) |

---

## Repository Structure

```
climate-portfolio/
├── data/                         # Raw and cleaned input data
│   ├── RIL_BRSR_2024-25.pdf      # Primary source — Reliance BRSR
│   ├── RIL_BRSR_2023-24.pdf
│   ├── RIL_BRSR_2022-23.pdf
│   ├── IEA_EDGAR_CO2_1970_2022.xlsx   # EDGAR v8.0 global emissions
│   ├── india_co2.csv             # World Bank API pull
│   ├── india_gdp.csv
│   ├── india_population.csv
│   └── india_renewable_energy.csv
│
├── analysis/                     # Scripts and audit code
│   ├── edgar_audit.py            # 6-check EDGAR data quality audit
│   ├── audit_implausible_jumps.csv    # 18 flagged country-year pairs
│   └── audit_2022_summary.csv    # 221 countries ranked by 2022 emissions
│
├── deliverables/                 # Final outputs
│   ├── reliance_dashboard.html        # Interactive carbon dashboard
│   ├── reliance_materiality_matrix.html   # CSRD double materiality matrix
│   ├── reliance_strategy_note.md     # Ranked reduction initiative analysis
│   ├── reliance_risk_register.html   # Physical risk register with map
│   ├── reliance_risk_brief.md        # One-page lender/investor brief
│   ├── reliance_tcfd_report.md       # Full TCFD independent analyst report
│   ├── edgar_data_audit_memo.md      # EDGAR data quality audit memo
│   └── india_climate_profile.md      # India 20-year climate data profile
│
└── CLAUDE.md                     # Project standing instructions
```

---

## About

This portfolio was built independently as a demonstration of climate finance analytical practice. It follows consulting-grade standards: primary sources only, exact page citations, UNVERIFIED flags on anything that cannot be verified, and independent judgment applied separately from self-reported corporate narratives.

Deliverables are hosted on GitHub Pages at [vivaanm.github.io/Climate_Portfolio](https://vivaanm.github.io/Climate_Portfolio/).

---

*All analysis is independent. No figures have been invented. This portfolio has not been validated by any of the companies or data providers cited.*
