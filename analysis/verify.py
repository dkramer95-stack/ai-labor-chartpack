#!/usr/bin/env python3
"""Recompute every headline number quoted in README.md from data/labor-model.csv.

Standard library only. Run from the repository root:

    python3 analysis/verify.py

The script prints the numbers used in the README and docs/FINDINGS.md, then
re-runs the arithmetic checks that justify the method. Exit code is 0 when
every check passes, 1 otherwise.
"""

import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.normpath(os.path.join(HERE, "..", "data", "labor-model.csv"))

INDEX_COLUMNS = ("idx_info", "idx_profbiz", "idx_mfg", "idx_health")


def load_rows(path):
    """Return the CSV as a list of dicts, preserving file order."""
    with open(path, newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise SystemExit("verify: no data rows in {}".format(path))
    return rows


def value(row, column):
    """Return a float, or None for blank / missing cells."""
    raw = row.get(column)
    if raw is None or str(raw).strip() == "":
        return None
    return float(raw)


def fmt(value, digits=2):
    """Fixed-point number, no thousands separators."""
    return "{:.{}f}".format(value, digits)


def month_label(iso_date):
    """'2022-11-01' -> 'November 2022', so README dates map to verify dates."""
    import datetime
    parsed = datetime.date.fromisoformat(iso_date)
    return parsed.strftime("%B %Y")


def pct(change):
    """Signed percentage with two decimals, e.g. '+15.90%'."""
    text = "{:+.2f}%".format(change)
    if text == "-0.00%":
        text = "0.00%"
    return text


class Checker(object):
    """Accumulate pass/fail results so the script can exit non-zero on error."""

    def __init__(self):
        self.failures = 0

    def check(self, label, condition, detail=""):
        if condition:
            print("[ok]   {}".format(label))
        else:
            self.failures += 1
            print("[FAIL] {} {}".format(label, detail).rstrip())


def main():
    rows = load_rows(CSV_PATH)
    checks = Checker()

    print("AI x Labor Markets - chart pack verification")
    print("=" * 66)
    print("Source: data/labor-model.csv")
    print("Coverage: {} monthly observations, {} to {}".format(
        len(rows), rows[0]["date"], rows[-1]["date"]))
    print()

    # --- data-integrity checks -------------------------------------------
    print("Data checks")
    print("-" * 66)
    checks.check("row count is 129", len(rows) == 129, "(got {})".format(len(rows)))
    checks.check(
        "date range is 2016-01 to 2026-09",
        rows[0]["date"] == "2016-01-01" and rows[-1]["date"] == "2026-09-01",
        "(got {} to {})".format(rows[0]["date"], rows[-1]["date"]),
    )

    latest_rows = [row for row in rows if row.get("latest_flag") == "1"]
    checks.check(
        "exactly one row is flagged latest_flag=1",
        len(latest_rows) == 1,
        "(got {})".format(len(latest_rows)),
    )
    latest = latest_rows[0]
    checks.check(
        "latest_flag=1 row is 2026-09 (latest headline month)",
        latest["date"] == "2026-09-01",
        "(got {})".format(latest["date"]),
    )

    for name in ("idx_info", "idx_profbiz", "idx_mfg", "idx_health"):
        avg_2019 = sum(
            value(row, name) for row in rows if row["year"] == "2019"
        ) / 12.0
        checks.check(
            "{} 2019 average = 100.00 (index base)".format(name),
            abs(avg_2019 - 100.0) < 1e-6,
            "(got {:.6f})".format(avg_2019),
        )

    # --- 1. information sector -------------------------------------------
    info_points = [(row["date"], value(row, "idx_info")) for row in rows]
    info_peak_date, info_peak = max(info_points, key=lambda point: point[1])
    info_latest = value(rows[-1], "idx_info")
    info_yoy = value(rows[-1], "yoy_info")
    print()
    print("1. Information sector - payroll employment index (2019 = 100)")
    print("-" * 66)
    print("   peak date          {} ({})".format(info_peak_date, month_label(info_peak_date)))
    print("   peak value         {}".format(fmt(info_peak)))
    print("   latest date        {} ({})".format(rows[-1]["date"], month_label(rows[-1]["date"])))
    print("   latest value       {}".format(fmt(info_latest)))
    print("   change from peak   {}".format(
        pct((info_latest / info_peak - 1.0) * 100.0)))
    print("   vs 2019 average    {}".format(pct(info_latest - 100.0)))
    print("   12-month change    {}".format(pct(info_yoy)))

    # --- 2. health care ---------------------------------------------------
    health_first_date = rows[0]["date"]
    health_first = value(rows[0], "idx_health")
    health_latest = value(rows[-1], "idx_health")
    health_yoy = value(rows[-1], "yoy_health")
    print()
    print("2. Health care & social assistance - payroll employment index (2019 = 100)")
    print("-" * 66)
    print("   latest date        {} ({})".format(rows[-1]["date"], month_label(rows[-1]["date"])))
    print("   latest value       {}".format(fmt(health_latest)))
    print("   vs 2019 average    {}".format(pct(health_latest - 100.0)))
    print("   first 2016 value   {} ({}) = {}".format(health_first_date, month_label(health_first_date), fmt(health_first)))
    print("   vs first 2016      {}".format(pct((health_latest / health_first - 1.0) * 100.0)))
    print("   12-month change    {}".format(pct(health_yoy)))

    # --- 3. professional & business services -----------------------------
    prof_points = [(row["date"], value(row, "idx_profbiz")) for row in rows]
    prof_peak_date, prof_peak = max(prof_points, key=lambda point: point[1])
    prof_latest = value(rows[-1], "idx_profbiz")
    prof_yoy = value(rows[-1], "yoy_profbiz")
    print()
    print("3. Professional & business services - payroll employment index (2019 = 100)")
    print("-" * 66)
    print("   peak date          {} ({})".format(prof_peak_date, month_label(prof_peak_date)))
    print("   peak value         {}".format(fmt(prof_peak)))
    print("   latest date        {} ({})".format(rows[-1]["date"], month_label(rows[-1]["date"])))
    print("   latest value       {}".format(fmt(prof_latest)))
    print("   change from peak   {}".format(pct((prof_latest / prof_peak - 1.0) * 100.0)))
    print("   vs 2019 average    {}".format(pct(prof_latest - 100.0)))
    print("   12-month change    {}".format(pct(prof_yoy)))

    # --- 4. manufacturing -------------------------------------------------
    mfg_latest = value(rows[-1], "idx_mfg")
    mfg_yoy = value(rows[-1], "yoy_mfg")
    print()
    print("4. Manufacturing - payroll employment index (2019 = 100)")
    print("-" * 66)
    print("   latest date        {} ({})".format(rows[-1]["date"], month_label(rows[-1]["date"])))
    print("   latest value       {}".format(fmt(mfg_latest)))
    print("   vs 2019 average    {}".format(pct(mfg_latest - 100.0)))
    print("   12-month change    {}".format(pct(mfg_yoy)))

    # --- 5. latest labor-market readings ---------------------------------
    unrate = value(latest, "unrate")
    payroll_yoy = value(latest, "payroll_yoy")
    wage_nom = value(latest, "wage_yoy_nom")
    cpi_yoy = value(latest, "cpi_yoy")
    wage_real = value(latest, "wage_yoy_real")
    real_sign = "negative" if wage_real < 0 else ("positive" if wage_real > 0 else "zero")
    print()
    print("5. Latest month ({})".format(latest["month"]))
    print("-" * 66)
    print("   unemployment rate, unrate         {}".format(fmt(unrate) + "%"))
    print("   payrolls, 12-month change         {}".format(pct(payroll_yoy)))
    print("   nominal wages, 12-month change    {}".format(pct(wage_nom)))
    print("   CPI-U, 12-month change            {}".format(pct(cpi_yoy)))
    print("   real wages, 12-month change       {} ({})".format(pct(wage_real), real_sign))

    # --- 6. JOLTS: latest valid openings-per-unemployed ------------------
    valid_rows = [
        row for row in rows
        if row.get("latest_valid_flag") == "1" and value(row, "v_u_ratio") is not None
    ]
    jolts = valid_rows[-1]
    jolts_date = jolts["date"]
    jolts_ratio = value(jolts, "v_u_ratio")
    jolts_openings = value(jolts, "openings_k")
    jolts_unemployed = value(jolts, "unemployed_k")
    ratio_points = [(row["date"], value(row, "v_u_ratio"))
                    for row in rows if value(row, "v_u_ratio") is not None]
    ratio_peak_date, ratio_peak = max(ratio_points, key=lambda point: point[1])
    print()
    print("6. JOLTS - job openings per unemployed worker")
    print("-" * 66)
    print("   latest valid date  {} ({}) - JOLTS lags the headline month by one".format(jolts_date, month_label(jolts_date)))
    print("   v_u_ratio          {}".format(fmt(jolts_ratio)))
    print("   openings (k)       {}".format("{:,.0f}".format(jolts_openings)))
    print("   unemployed (k)     {}".format("{:,.0f}".format(jolts_unemployed)))
    print("   peak date          {} ({})".format(ratio_peak_date, month_label(ratio_peak_date)))
    print("   peak value         {}".format(fmt(ratio_peak)))

    # --- 7. arithmetic re-checks -----------------------------------------
    print()
    print("Arithmetic checks")
    print("-" * 66)
    checks.check(
        "openings / unemployed = v_u_ratio ({})".format(fmt(jolts_ratio)),
        abs(jolts_openings / jolts_unemployed - jolts_ratio) < 1e-9,
        "(got {:.9f})".format(jolts_openings / jolts_unemployed),
    )
    checks.check(
        "real wage = (1 + nominal) / (1 + CPI) - 1 ({})".format(pct(wage_real)),
        abs((1.0 + wage_nom / 100.0) / (1.0 + cpi_yoy / 100.0) - 1.0
            - wage_real / 100.0) < 1e-9,
        "(got {:.9f})".format(
            ((1.0 + wage_nom / 100.0) / (1.0 + cpi_yoy / 100.0) - 1.0) * 100.0),
    )
    formula_mismatches = 0
    for row in rows:
        nominal = value(row, "wage_yoy_nom")
        cpi = value(row, "cpi_yoy")
        stored = value(row, "wage_yoy_real")
        if nominal is None or cpi is None or stored is None:
            continue
        rebuilt = ((1.0 + nominal / 100.0) / (1.0 + cpi / 100.0) - 1.0) * 100.0
        if abs(rebuilt - stored) > 1e-8:
            formula_mismatches += 1
    checks.check(
        "real-wage formula holds on every row where it is defined",
        formula_mismatches == 0,
        "({} mismatched rows)".format(formula_mismatches),
    )
    yoy_mismatches = 0
    by_date = {row["date"]: row for row in rows}
    for row in rows:
        prior = by_date.get(str(int(row["year"]) - 1) + row["date"][4:])
        if prior is None:
            continue
        for column, source in (("yoy_info", "idx_info"), ("yoy_profbiz", "idx_profbiz"),
                               ("yoy_mfg", "idx_mfg"), ("yoy_health", "idx_health")):
            stored = value(row, column)
            if stored is None:
                continue
            rebuilt = (value(row, source) / value(prior, source) - 1.0) * 100.0
            if abs(rebuilt - stored) > 1e-6:
                yoy_mismatches += 1
    checks.check(
        "12-month sector changes match the index columns",
        yoy_mismatches == 0,
        "({} mismatched cells)".format(yoy_mismatches),
    )

    print()
    if checks.failures:
        print("RESULT: {} check(s) FAILED - numbers above are not trustworthy."
              .format(checks.failures))
        return 1
    print("RESULT: all checks passed. README.md quotes only numbers printed above.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
