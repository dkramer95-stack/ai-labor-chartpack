# AI × Labor Markets — a descriptive chart pack

What has actually happened to U.S. employment and wages in the sectors most exposed to generative AI, and what can this data honestly support?

This is a **descriptive** chart pack. It documents movements in U.S. Bureau of Labor Statistics (BLS) data from **January 2016 to September 2026** (JOLTS through August 2026). It does not estimate a causal effect of AI on employment. It is a careful statement of what moved, by how much, and what that movement cannot tell us.

**Last built:** 1 November 2026. **Latest headline month:** September 2026. **Latest JOLTS month:** August 2026.

## The question

Generative AI reached broad public use at the end of 2022. If it were displacing exposed cognitive work, we would expect employment in exposed sectors to fall relative to less-exposed sectors, and we would expect hiring and wage pressure to weaken there first.

The pack asks three questions:

1. Did employment in the most AI-exposed sectors fall relative to the rest of the labor market?
2. Did real wages in those sectors weaken?
3. Can monthly sector data distinguish AI from the other large forces acting on those sectors at the same time?

The answers are: in the information sector, yes, employment fell — and it fell noticeably. In health care, no. And on the third question: **no, it cannot.** That last answer is the reason this pack is framed the way it is.

## Headline findings

Every number below is recomputed from `data/labor-model.csv` by [`analysis/verify.py`](analysis/verify.py). Run it and compare.

1. **Information-sector employment peaked in November 2022 at 108.77** on a 2019 = 100 index. In September 2026 it was **95.64** — down **12.07% from its peak**, **4.36% below its 2019 average**, and **4.20% below the same month a year earlier**.
2. **Health care & social assistance** was **115.90 in September 2026**: **15.90% above its 2019 average** and **25.31% above its January 2016 reading of 92.49** (up 1.88% year over year). Same labor market, opposite direction.
3. **Professional & business services** — the other large cognitive-work sector — peaked in **May 2023 at 106.89** and was **105.17 in September 2026**, only **1.61% below its peak**, **5.17% above 2019**, and up **0.55%** year over year. The weakness is concentrated in information, not in cognitive work generally.
4. **Manufacturing** stood at **99.01** — essentially flat: **0.99% below** its 2019 average and **0.32%** above a year earlier. It does not show a comparable break.
5. The labor market as a whole is still growing, but slowly: **unemployment was 4.20%** in September 2026 and **payrolls were up 0.31%** over 12 months. **Nominal wage growth was 3.02%** against **CPI inflation of 3.74%**, so **real wages fell 0.69%** — a **negative** reading. (The comparison is multiplicative: the naive difference of the two growth rates would misstate it.)
6. **Job openings per unemployed worker were 1.01 in August 2026** (7,079 thousand openings against 7,031 thousand unemployed), down from a peak of **2.04 in March 2022**. Labor demand has normalized; vacancies no longer outnumber unemployed workers.

## The information-sector decline is real. Its cause is not identified.

The information sector's decline is the most suggestive object in this pack, and it is easy to over-read.

The peak is dated **November 2022** — the month ChatGPT was released. That coincidence is worth stating plainly, and it is not evidence. The same decline lines up with several other forces acting on the same sector at the same time:

- the end of pandemic-era over-hiring in technology and digital media, and the layoffs that followed;
- the sharp rise in the cost of capital from 2022 onward, which hits long-duration, speculative and ad-funded businesses hardest;
- the advertising and digital-media downturn that accompanied the rate cycle;
- a longer-run shift in how software, publishing and telecom firms staff themselves.

The information-sector decline **coincides with both generative AI and the rate cycle**. Monthly sector data **cannot separate them**. There is no measure of AI adoption in this data set, no sector-level exposure measure, no counterfactual, and only one short post-2022 window in which all of these forces moved at once. Anyone claiming on this evidence that "AI did this" is making a causal claim the data cannot support.

## What the data cannot show

This section is required reading, not a disclaimer.

- **Exposure is not displacement.** Every AI-exposure index in the literature scores whether a model *could* do a task. None of it shows an employer cancelling a role. This pack contains no adoption channel, so it cannot test displacement.
- **Sector is not occupation.** The information sector mixes software, publishing, telecom and data processing. It averages over high-exposure and low-exposure jobs. Occupation-level exposure data does not map cleanly onto it.
- **Aggregates cannot see seniority.** The displacement mechanism most discussed — junior cognitive work being automated first — would show up as a change in hiring composition, not in total sector headcount. That is invisible here.
- **Reallocation is not measured.** Health care sits 15.90% above its 2019 average while information is 4.36% below. Aggregate demand did not collapse; workers and dollars may be moving between sectors, and this data cannot see where they land.
- **The real-wage reading is economy-wide.** Real wages falling 0.69% is a CPI-versus-nominal-wage fact about the whole private economy, not a sector-specific AI signal.
- **Revisions and vintage matter.** BLS revises payroll and wage series; the API returns only the current vintage. The 2019 = 100 base is a presentation choice, not a measurement.
- **CPI is not seasonally adjusted while wages are.** The pack uses 12-month changes, which are unaffected by this mismatch. The monthly levels are not comparable on that basis.
- **JOLTS lags.** Openings data run one month behind the headline employment data.

## What the data deliberately leaves out

An occupation-level AI exposure score. Joining a measure such as AIOE, the Anthropic Economic Index or a task-level coding of your own to these sector aggregates is the analytical step that turns a descriptive pack into a test — and it is a choice of design, not a data default. This pack stops short of it on purpose.

## Data

All series are from the BLS public API (`api.bls.gov`). Series IDs are taken from the workbook's README tab.

| Series ID | Measure | Adjustment |
|---|---|---|
| `LNS14000000` | Unemployment rate, % | SA |
| `LNS13000000` | Unemployed level, thousands | SA |
| `JTS000000000000000JOL` | Job openings, total nonfarm, thousands | SA |
| `CES0000000001` | Total nonfarm payrolls, thousands | SA |
| `CES0500000003` | Average hourly earnings, total private, $/hr | SA |
| `CUUR0000SA0` | CPI-U, all items (1982–84 = 100) | NSA |
| `CES3000000001` | Employees, manufacturing, thousands | SA |
| `CES5000000001` | Employees, information, thousands | SA |
| `CES6000000001` | Employees, professional & business services, thousands | SA |
| `CES6500000001` | Employees, health care & social assistance, thousands | SA |

`data/labor-model.csv` is the normalized monthly table used by everything in this repository: the workbook, the dashboard and the verification script. `data/bls-raw.json` holds the raw API payloads grouped by series ID.

## Method

- **Sector indexes.** Each sector's payroll employment level is rebased so that its **2019 calendar year averages 100**. The script checks that this holds for every index.
- **Year-over-year changes** are 12-month percent changes: the same calendar month one year earlier is the comparison. The script recomputes every `yoy_*` column from the indexes.
- **Real wages.** Real wage growth is `(1 + nominal) / (1 + CPI) - 1`, where nominal is average hourly earnings growth and CPI is the all-items CPI-U change. The script checks this identity on every row where it is defined.
- **Openings per unemployed** is job openings divided by the unemployed level; the script checks the division.
- **Latest readings.** Rows carry `latest_flag = 1` for the final headline month and `latest_valid_flag = 1` for the last row carrying JOLTS data. The latest valid openings-per-unemployed reading is the last flagged row with a non-missing `v_u_ratio`.

## Files

| Path | What it is |
|---|---|
| `labor-market-chartpack.xlsx` | Workbook with README (sources, methods, caveats), Data (the monthly table), Papers, Synthesis and Dashboard tabs. |
| `dashboard.html` | Self-contained static dashboard of the headline charts. Opens in a browser with no server. |
| `chartpack-preview.png` | Image preview of the dashboard. |
| `negative-case.html` | The strongest version of the displacement case, with the counter-evidence kept in the same table. Read it as the prosecution, not the verdict. |
| `negative-case.png` | Image preview of the negative case. |
| `notebook-brief.md` | Brief for a notebook-style literature review: the sources to upload, the tensions to interrogate and the prompts to run. |
| `data/labor-model.csv` | Normalized monthly BLS series and derived metrics. |
| `data/bls-raw.json` | Raw BLS API payloads, grouped by series ID. |
| `data/literature.csv` | Ranked sources on AI and labor markets, with DOIs. |
| `data/evidence-negative.csv` | Counter-evidence to the displacement thesis, including its strongest cases. |
| `analysis/verify.py` | Standard-library script that recomputes and checks every number quoted here. |
| `docs/FINDINGS.md` | Short brief version of the findings, usable as a post or memo source. |
| `LICENSE` | CC BY 4.0 for data and prose; MIT for code. |

## Verify and rebuild

```bash
python3 analysis/verify.py
```

No network access is needed and no third-party packages are required: the script reads `data/labor-model.csv` with the standard library, prints every headline number, then re-checks the index base, the year-over-year arithmetic, the real-wage identity and the openings-per-unemployed division. It exits non-zero if any check fails.

To use the workbook, open `labor-market-chartpack.xlsx`; its README tab documents sources, methods and caveats. To use the dashboard, open `dashboard.html` in any browser. To refresh the data, re-request the series above from the BLS public API for the same window and rebuild the normalized table; the index, year-over-year and real-wage formulas are in `analysis/verify.py` and repeat the workbook's README tab.

## License and citation

Data and prose are released under **CC BY 4.0**; the code is released under the **MIT License**. See [`LICENSE`](LICENSE).

If you use this pack, cite it as: *AI × Labor Markets chart pack*, Derek Kramer, 2026, CC BY 4.0. BLS data are in the public domain; the derived table and the analysis are the licensed contribution.

## Credit where it is due

The literature tab and `notebook-brief.md` are compiled from open-access papers, each cited by DOI in `data/literature.csv` and `data/evidence-negative.csv`. Numbers are BLS. Framing decisions — including the decision not to claim causation — are the author's.
