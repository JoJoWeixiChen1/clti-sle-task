# Private author/evaluator materials: do not publish

Keep this folder separate from the public GitHub task. The two `gold/version_*_site2_clinical_with_outcomes.csv` files contain site 2 three-year results withheld from the solver. `gold/baseline_audit.json` has the injected sample/well findings. `gold/manifest.json` maps version labels to the signal setting. These are synthetic author controls, not hidden patient information.

Run the public verifier from the parent folder:

```bash
python clti-sle-task/verification/verify.py --repo clti-sle-task --submission clti-sle-task/submission --gold clti-sle-author-private/gold
```

The script checks complete held-out predictions and recomputes cause-specific Harrell C for the clinical and combined scores, censoring status 0 and treating competing status 2 as censored for this **specific** C estimand. A time-dependent competing-risk assessment is also defensible, but requires an explicit alternative verification implementation. A working solver need not pick the author's four proteins or the author's statistical method. Sanity reference from the original author fit: signal version A site 2 combined-minus-clinical C approximately +0.151 MACE, +0.122 MALE, +0.083 Death, +0.163 major amputation; null version B near zero. Exact values can differ with defensible modeling and exclusion rules.

## Verification rubric (review evidence in code, not claims alone)

| Area | What to check | Failure mode |
| --- | --- | --- |
| Input and QC | Join by StudyID + Assay; inspect `QC_Warning` and `Assay_Warning` even though all are `PASS`; document counts before/after | Assume every row has usable NPX because flags pass |
| LOD | Compare patient NPX with matched per-assay/per-plate LOD; report low-value fraction and an explicit sensitivity or defensible handling | Interpret blank NPX as below LOD or replace all blanks indiscriminately |
| Missingness | Compute per-assay missingness in each site, exclude or justify high-missing assays; apply an explicit strategy for remaining blanks | Missing values silently treated as zero; use site 2 outcomes to select thresholds |
| Multivariate outliers | Plot PCA or equivalent before/after filtering; identify unusual patient samples and trace their `PlateID`/`WellID` rather than only dropping high NPX columns | All PASS labels taken as proof of no specimen anomalies |
| Well trace | Site 1 six anomalous IDs and site 2 four IDs in `baseline_audit.json` cluster in plate-specific wells; assess precision/recall and whether exclusion is warranted | Unstructured blanket exclusions or no trace back to wells |
| Cross-site comparability | Inspect shared bridge measurements, demonstrate site/plate alignment or a reasoned decision not to adjust; avoid using outcomes to learn shifts | Pool two sites without checking comparable scales; normalize each site from its patient outcome mix |
| Disease contrast | If per-assay stable PAD versus CLTI analysis is performed, adjust measured confounders, report effect direction and a multiple-testing correction such as BH/FDR; this is exploratory, not outcome validation | Treat thousands of raw p-values as confirmed discoveries |
| Prognostic design | Site 1 CLTI follow-up drives selection/tuning; site 2 remains frozen. Compare clinical-only versus plus-protein in both versions on the same patients | Use site 2 follow-up during model development; use in-sample C as external evidence |
| Dates/censoring | Recompute or verify three-calendar-year cutoff; losses and events after cutoff censored; classify cardiovascular death as MACE and pre-event competing deaths appropriately | Classify everyone with a blank event date as three-year event-free, or ignore dates/competing death |
| Null recognition | Version A should show meaningful improvement in several outcomes; version B should not be advertised as a stable improvement | AUC/C ~1, identical dramatic effect in both versions, or cherry-pick one endpoint |

Machine output measures a constrained cause-specific ranking comparison; the final judgment on workflow and scientific validity requires the R scripts, plots, and report. The scorer intentionally does not parse prose and award methodological points for keywords. Review with this rubric and document justification for valid alternative methods.

## Packaging checks

Public archive must exclude this author directory, any prior `.git` object/history containing site 2 outcomes, generation scripts, and previous analysis outputs. A GitHub repository created from the extracted public ZIP will have only baseline Site 2 data.
