# CLTI proteomics: two-site research benchmark

This repository is a synthetic, reproducible research task. Work from [instruction.md](instruction.md); use [CODEBOOK.md](CODEBOOK.md) to interpret the supplied CSV files. No patient records are real.

Two versions share the same baseline proteomic and laboratory data. Each version supplies **six logical input tables**: four files in `data/shared/` plus two clinical files in `data/version_a/` or `data/version_b/`. Site 1 includes stable PAD and CLTI; site 2 includes CLTI only. Site 2 outcomes are reserved for independent evaluation and are absent from this repository.

The intended GitHub upload is the **extracted folder**, not the ZIP as a single file. The large CSVs are ordinary files; use `git push` from a local clone if the browser upload has a per-file size limit. This package has a clean history and contains no private evaluation data.

## Layout

| Path | Purpose |
| --- | --- |
| `instruction.md` | Agent-facing research question and deliverables |
| `CODEBOOK.md` | Dictionary and exact observed coding |
| `data/shared/` | Two NPX matrices and two assay-level laboratory tables |
| `data/version_a/`, `data/version_b/` | Site 1 follow-up and site 2 baseline clinical data, respectively |
| `references/` | Two supplied background PDFs and the protein lookup |
| `verification/verify.py` | Independent scorer; requires author-held gold files |
| `submission_example/` | Output schema illustration with **no actual predictions** |

See [references/README.md](references/README.md) for provenance and limits of the reference materials. Do not put private validation outcomes or the author gold bundle in this public repository.
