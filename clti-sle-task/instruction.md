# Research task: proteomic prediction of three-year outcomes in CLTI

## Scientific question

Using the synthetic two-site PAD/CLTI study, investigate whether baseline protein measurements can improve prediction of adverse events over clinical variables alone among patients with chronic limb-threatening ischemia (CLTI). Develop your analysis on **site 1** and independently evaluate your frozen approach on **site 2**. Analyze `version_a` and `version_b` separately; they share the same baseline measurements but represent different follow-up scenarios. Report both positive and null findings faithfully.

The four outcomes are three-year MACE, MALE, all-cause death, and major amputation. Stable PAD patients have baseline data in site 1 for contextual or exploratory analyses, but no supplied follow-up outcomes. Site 2 outcomes are intentionally withheld; your final site 2 risk predictions will be checked against them after submission.

## Materials and scope

- Use **R** for the data work, statistical analysis, and reproducible figures.
- Read the two PDFs in `references/` as methodological context and consult the protein lookup there. Explain where the reference procedures are or are not applicable to these simulated files.
- There are six input CSVs per version: `data/shared/site{1,2}_npx.csv`, `data/shared/site{1,2}_experimental_metadata.csv`, and `data/version_{a,b}/site{1,2}_clinical.csv`. The shared files are used for both versions.
- You may choose and justify appropriate data preparation, feature discovery, modeling, and validation methods. Keep site 2 follow-up information out of all training and model selection. Any transformation learned from patients, score weighting, hyperparameters, and risk calibration must be determined without site 2 outcomes.
- Treat dates, limited observation, and competing events consistently with the three-year estimand. Explain your choices and limitations. Do not infer a perfect biological mechanism from synthetic data.

## Required submission

Write these files under `submission/`:

1. `report.md`: scientific question, sample flow, data and assay checks, analysis decisions, site 1 findings, site 2 evaluation plan, figures/tables, and limitations. Explain the comparison between a clinical-only model and a clinical-plus-protein model for **each scenario and endpoint**. External outcome metrics are calculated by the evaluator from your frozen predictions.
2. `analysis.R` (and any sourced R files): runnable from the repository root, creates the outputs below without using private files. Include package versions and a fixed seed.
3. `predictions.csv`: one row for every **retained** site 2 CLTI patient × version × endpoint, with columns `Scenario,StudyID,Endpoint,ClinicalRisk,CombinedRisk`. Document any exclusions in `submission.json`; apply the same eligibility rule to both versions and both models. `Scenario` is `version_a` or `version_b`; `Endpoint` is `MACE`, `MALE`, `Death`, or `MajorAmputation`. Scores are finite, numeric, and **higher means greater three-year risk**. Probabilities in [0,1] are preferred, but a consistent continuous risk score is acceptable.
4. `submission.json`: a machine-readable short audit of what was done. Use the template in `submission_example/submission.json`. Include paths to the actual produced evidence (R scripts, plots, result tables) and explicitly state decisions that were not applicable. This is an audit record, not a substitute for reproducible analysis.

Evaluation considers the defensibility and traceability of the full research path as well as external performance. There is no required protein list, model family, exact transformation, or guarantee that both scenarios have a protein signal. Use only site 1 follow-up outcomes to build or select a prognostic model. Report exploratory comparisons without treating them as external validation.
