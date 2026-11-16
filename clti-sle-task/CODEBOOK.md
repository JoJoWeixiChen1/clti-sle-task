# Data dictionary

All CSVs are UTF-8, comma-separated. Empty cells mean unavailable/not applicable; they are **not** zero. `StudyID` identifies the person within the site, `Assay` identifies the protein, and NPX is on a log2-like Olink normalized expression scale. All observations are synthetic. For each version the six logical inputs comprise four shared files and two version-specific clinical files.

| File | Unit/rows | Key and contents |
| --- | --- | --- |
| `data/shared/site1_npx.csv` | 325 patients × 2,923 assays | `StudyID`, then one NPX column per `Assay` |
| `data/shared/site2_npx.csv` | 175 patients × 2,923 assays | Same column names as site 1 |
| `data/shared/site1_experimental_metadata.csv` | 1,008,435 assay × sample records | Patient/bridge placement, assay annotation, QC, LOD |
| `data/shared/site2_experimental_metadata.csv` | 569,985 assay × sample records | Same schema as site 1 |
| `data/version_{a,b}/site1_clinical.csv` | 325 patients | Baseline covariates; three-year event and censoring information for 175 CLTI patients; 150 stable PAD follow-up fields blank |
| `data/version_{a,b}/site2_clinical.csv` | 175 CLTI patients | Baseline covariates and `BaselineDate` only; outcomes withheld |

`Site 1` means `S1-...` IDs, `site 2` means `S2-...`. `version_a` and `version_b` share baseline and laboratory tables; version-specific follow-up is present only in the respective site 1 table. One metadata record for a PATIENT is joined to the corresponding wide NPX value by `StudyID` and `Assay`. BRIDGE rows do not appear in the wide patient matrix.

## Laboratory data

| Field | Meaning / exact values |
| --- | --- |
| `StudyID` | Person ID in NPX; for PATIENT metadata the same ID; empty on BRIDGE rows |
| Protein columns in NPX | Names match `Assay` exactly; numeric NPX or blank |
| `SampleID` | Laboratory specimen identifier; may differ from `StudyID` |
| `Sample_Type` | `PATIENT` or `BRIDGE` (shared reference sample) |
| `BridgeID` | Reference sample ID for BRIDGE; blank for PATIENT |
| `Assay` | Protein assay symbol, one of the wide protein columns |
| `UniProt` | Protein identifier as listed in assay lookup |
| `Panel`, `Block`, `PlateID`, `WellID` | Laboratory panel, processing block, plate, and physical well, respectively; the combination helps trace a specimen |
| `QC_Warning`, `Assay_Warning` | Laboratory warning label; observed values are `PASS` throughout these synthetic files, so these flags alone do not establish that all samples are free of other problems |
| `LOD` | Assay/plate-specific lower limit of detection, in NPX units; compare against the corresponding observed NPX |
| `BridgeNPX` | Bridge-reference NPX on BRIDGE rows; blank for patients. Patient NPX resides in the wide files |
| `Normalization` | Laboratory-provided label `Plate control`; it does not assert that site effects have already been removed |

The protein list `references/ukb-olink-explore-3072-protein-list.csv` is an annotation aid; the actually measured 2,923 assay columns define the analyzable panel.

## Clinical baseline

| Field | Meaning / exact coding |
| --- | --- |
| `ClinicalGroup` | `CLTI` or `Stable PAD`; site 2 has CLTI only |
| `Age` | Years at baseline, numeric |
| `Sex` | `Male`, `Female` (text, not 0/1) |
| `BMI` | kg/m², numeric |
| `Diabetes`, `Hypertension`, `CKD`, `CAD` | Binary history: `0` = absent, `1` = present. CKD = chronic kidney disease; CAD = coronary artery disease |
| `Smoking` | `Never`, `Former`, `Current` (text categories; **no numerical 0/1/2 coding in the CSV**) |
| `ABI` | Ankle-brachial index, numeric |
| `PADSeverityScore` | Simulated continuous 0–100 measure, larger = more severe. **Not Rutherford stage** and not a real validated score |
| `Education` | `High_school_or_less`, `Some_college`, `College_or_more` |
| `AnnualIncomeUSD` | Simulated annual USD income, numeric |
| `Race` | `White`, `Black`, `Asian`, `Other` |
| `Ethnicity` | `Hispanic`, `Non_Hispanic` |
| `BaselineDate` | Baseline specimen/clinical assessment date, ISO `YYYY-MM-DD` |

## Site 1 follow-up fields (CLTI only)

All dates are `YYYY-MM-DD` when present. The follow-up dates are raw information; the time/status columns are provided for audit and do not replace defining an explicit estimand. The window ends on `ThreeYearCutoffDate` (baseline + three calendar years; time can be 1,095 or 1,096 days).

| Field | Meaning / exact coding |
| --- | --- |
| `LastContactDate` | Last known contact; may be after three years |
| `ThreeYearCutoffDate` | End of the fixed three-year horizon |
| `DeathDate`, `DeathCause` | Death date and `Cardiovascular` / `Noncardiovascular`; blank if no documented death |
| `FollowupEndReason` | `Death`, `LostToFollowup`, or `ObservedBeyondThreeYears` |
| `MIDate`, `StrokeDate` | Myocardial infarction and stroke component dates |
| `MajorAmputationDate`, `MajorRevascularizationDate` | Limb event component dates |
| `MACEDate` | First MI, stroke, or cardiovascular death date |
| `MALEDate` | First major amputation or major revascularization date |
| `MACETimeDays`, `MALETimeDays`, `MajorAmputationTimeDays`, `DeathTimeDays` | Supplied observed time from baseline in days, capped at the three-year horizon, last observation, event or competing death as applicable |
| `MACEStatus`, `MALEStatus`, `MajorAmputationStatus` | `1.0` = event of interest within observation/horizon; `0.0` = administratively censored or lost to follow-up; `2.0` = death before the nonfatal/composite event, treated as a competing event in the supplied status convention |
| `DeathStatus` | `1.0` = all-cause death within observation/horizon; `0.0` = censored. No status `2.0` for death |

For MACE, a noncardiovascular death before its components is a competing event; cardiovascular death is part of MACE. For MALE and major amputation, death before the event is competing. Events dated after the cutoff should not count as three-year events. Distinguish cause-specific and competing-risk analyses when interpreting effect estimates.
