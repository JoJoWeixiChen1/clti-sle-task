#!/usr/bin/env python3
"""Author-side check: public code, private gold argument. No gold is shipped here."""

import argparse
import csv
import json
import math
from pathlib import Path

SCENARIOS = ("version_a", "version_b")
ENDPOINTS = ("MACE", "MALE", "Death", "MajorAmputation")
FIELDS = ("Scenario", "StudyID", "Endpoint", "ClinicalRisk", "CombinedRisk")


def c_index(rows, risk_key, endpoint):
    """Cause-specific Harrell concordance; status 2 is a competing censoring event."""
    comparable = concordant = 0.0
    for i, a in enumerate(rows):
        ta = float(a[endpoint + "TimeDays"])
        ea = int(float(a[endpoint + "Status"])) == 1
        ra = float(a[risk_key])
        for b in rows[i + 1 :]:
            tb = float(b[endpoint + "TimeDays"])
            eb = int(float(b[endpoint + "Status"])) == 1
            rb = float(b[risk_key])
            if ta < tb and ea:
                comparable += 1
                concordant += float(ra > rb) + 0.5 * float(ra == rb)
            elif tb < ta and eb:
                comparable += 1
                concordant += float(rb > ra) + 0.5 * float(ra == rb)
            elif ta == tb and ea != eb:
                comparable += 1
                event_risk, other_risk = (ra, rb) if ea else (rb, ra)
                concordant += float(event_risk > other_risk) + 0.5 * float(event_risk == other_risk)
    return round(concordant / comparable, 5) if comparable else None


def read_csv(path):
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def score(repo, submission, gold):
    report = submission / "report.md"
    script = submission / "analysis.R"
    audit_path = submission / "submission.json"
    pred_path = submission / "predictions.csv"
    files = (report, script, audit_path, pred_path)
    if any(not p.is_file() for p in files):
        raise ValueError("Missing required submission files: " + ", ".join(str(p) for p in files if not p.is_file()))
    audit = json.loads(audit_path.read_text())
    pred = read_csv(pred_path)
    if not pred or not set(FIELDS).issubset(pred[0]):
        raise ValueError("predictions.csv must contain all five required columns")
    gold_meta = json.loads((gold / "manifest.json").read_text())
    if not set(SCENARIOS) == set(gold_meta["scenarios"]):
        raise ValueError("Private manifest is incomplete")
    excluded = {r.get("StudyID") for r in audit.get("excluded_samples", []) if r.get("Site") == "site2"}
    site2_ids = {r["StudyID"] for r in read_csv(repo / "data/version_a/site2_clinical.csv")}
    if excluded - site2_ids:
        raise ValueError("An excluded site 2 patient ID does not exist")
    allowed = site2_ids - excluded
    if len(allowed) < 150:
        raise ValueError("Excessive exclusions from site 2")
    by_key = {}
    for r in pred:
        key = r["Scenario"], r["StudyID"], r["Endpoint"]
        if key[0] not in SCENARIOS or key[1] not in allowed or key[2] not in ENDPOINTS or key in by_key:
            raise ValueError("Unknown or duplicated scenario/person/endpoint prediction: " + str(key))
        for field in ("ClinicalRisk", "CombinedRisk"):
            if not math.isfinite(float(r[field])):
                raise ValueError("Risk scores must be finite")
        by_key[key] = r
    expected = {(s, ident, e) for s in SCENARIOS for ident in allowed for e in ENDPOINTS}
    if set(by_key) != expected:
        raise ValueError(f"Prediction grid incomplete: expected {len(expected)}, found {len(by_key)}")

    all_scores = {}
    for scenario in SCENARIOS:
        actual = read_csv(gold / gold_meta["scenarios"][scenario])
        outcomes = {r["StudyID"]: r for r in actual if r["ClinicalGroup"] == "CLTI"}
        if set(outcomes) != site2_ids:
            raise ValueError("Private site 2 outcome set differs from public baseline")
        for endpoint in ENDPOINTS:
            joined = []
            for ident in sorted(allowed):
                row = dict(outcomes[ident])
                row.update(by_key[(scenario, ident, endpoint)])
                joined.append(row)
            c_clin = c_index(joined, "ClinicalRisk", endpoint)
            c_comb = c_index(joined, "CombinedRisk", endpoint)
            all_scores[(scenario, endpoint)] = c_comb - c_clin
            print(f"{scenario:10s} {endpoint:16s} clinical C={c_clin:.3f} combined C={c_comb:.3f} delta={c_comb-c_clin:+.3f}")

    # The truth mapping is held only in the author manifest, never in this program.
    positive = gold_meta["signal_scenario"]
    null = next(s for s in SCENARIOS if s != positive)
    signal_hits = sum(all_scores[(positive, e)] >= 0.04 for e in ENDPOINTS)
    null_hits = sum(abs(all_scores[(null, e)]) <= 0.05 for e in ENDPOINTS)
    print(f"External comparison: {signal_hits}/4 positive-scenario improvements; {null_hits}/4 null-scenario stable comparisons")
    print("Method audit is separate: review actual R code/plots for QC, LOD, missingness, PCA and well trace, bridge/site handling, multiplicity, and event-time logic.")
    return {"signal_hits": signal_hits, "null_hits": null_hits, "delta_c": {s: {e: all_scores[(s, e)] for e in ENDPOINTS} for s in SCENARIOS}}


def self_test():
    rows = [
        {"DeathTimeDays": "5", "DeathStatus": "1", "Risk": "3"},
        {"DeathTimeDays": "10", "DeathStatus": "0", "Risk": "2"},
        {"DeathTimeDays": "12", "DeathStatus": "2", "Risk": "1"},
    ]
    assert c_index(rows, "Risk", "Death") == 1.0
    rows[0]["Risk"] = "0"
    assert c_index(rows, "Risk", "Death") == 0.0
    print("Verifier self-test passed")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    p.add_argument("--submission", type=Path)
    p.add_argument("--gold", type=Path, help="Directory with private author manifest and held-out outcomes")
    p.add_argument("--self-test", action="store_true")
    a = p.parse_args()
    if a.self_test:
        self_test()
    else:
        if a.gold is None or a.submission is None:
            p.error("Independent evaluation requires --submission and author-held --gold")
        score(a.repo, a.submission, a.gold)
