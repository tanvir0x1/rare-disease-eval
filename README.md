# Zero-cost retrieval-augmented rare disease diagnosis: how benchmark construction inverts the measured value of LLM re-ranking

Code, prompts, archived model outputs and result tables for the study of the same name.

**What the paper claims.** A phenotype-driven retriever over 4,289 Orphanet disorders is
evaluated twice: once on queries sampled from the annotation table that indexes the
knowledge base, and once on 834 real cases from RareBench. The direction of the
re-ranking effect reverses between the two. Internally every LLM re-ranker is worse than
plain retrieval; externally, conditional on the gold disease having been retrieved,
MedGemma 27B raises Recall@5 from 0.480 to 0.811 over 513 cases. The tuned fusion
selected on internal data ranks second of eleven internally and sixth externally.

## Repository layout

```
src/         pipeline modules (KB build, tiers, retrieval, fusion, re-ranking, stats)
notebooks/   the notebooks the results were produced with, outputs cleared
prompts/     the exact prompts sent to every model, verbatim
data/        no raw third-party data; see data/README.md for how to fetch it
runs/        archived raw model responses, one JSON per call
results/     the result tables reported in the paper, as CSV
figures/     figure-generation scripts and generated figures
manifest.json  versions, model revisions, seeds, run dates, checksums
```

## Install

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Python 3.12.13 was used. The local model needs two GPUs with at least 14 GiB each
(the runs used 2x NVIDIA Tesla T4, compute capability sm_75).

## Get the data

The Orphanet, HPO, SapBERT and RareBench files are third-party and are not
redistributed here. `data/README.md` gives the exact releases, sources and checksums.

## Reproduce

| Step | Command | Produces |
| --- | --- | --- |
| 1. Build the knowledge base | `python -m src.build_kb` | `disease_kb_v3.pkl` (4,289 disorders) |
| 2. Generate the noise tiers | `python -m src.make_tiers` | `test_sets_tiered.pkl`, `dev_sets_tiered.pkl` |
| 3. Tune and freeze the fusion | `python -m src.tune_fusion` | `results/best_rrf.json`, `results/table_rrf_tuning_dev.csv` |
| 4. Retrieval evaluation | `python -m src.eval_retrieval` | `results/table_retrieval_ablation.csv` |
| 5. LLM re-ranking, internal | `python -m src.rerank --split internal` | `runs/`, `results/table_llm_systems.csv` |
| 6. External validation | `python -m src.eval_external` | `results/table_rarebench_*.csv`, `results/rarebench_ranks.csv` |
| 7. Abstention analysis | `python -m src.abstention` | `results/table_aurc.csv`, `results/table_operating_points.csv` |
| 8. Significance tests | `python -m src.stats` | `results/table_pvalues_corrected.csv` |
| 9. Figures | `python -m figures.make_figures` | `figures/*.png` |

Steps 1-4 are fully deterministic given seed 42. Steps 5-6 call language models.

### Reproducing without calling any model

Two of the three ensemble members are provider aliases (`gemini-3.5-flash-lite`,
`mistral-small-latest`) which the providers can repoint to different weights without
notice, so a live rerun on a later date is not guaranteed to reproduce the reported
numbers. Every raw response from the reported runs is archived under `runs/`, and the
re-ranking and analysis steps accept `--replay runs/` to recompute every table from
those archived responses with no network access:

```bash
python -m src.rerank --replay runs/ --split internal
python -m src.eval_external --replay runs/
```

This is the reproduction path we recommend, and the one the reported tables come from.

## Which table is which

| File | Paper table |
| --- | --- |
| `results/table_rrf_tuning_dev.csv` | fusion tuning grid (228 configurations) |
| `results/table_retrieval_ablation.csv` | retrieval ablation on the evaluation split |
| `results/table_llm_systems.csv` | recall of each system by tier |
| `results/table_pairwise_disagreement.csv` | mean pairwise disagreement per tier |
| `results/table_aurc.csv` | area under the accuracy-coverage curve |
| `results/table_operating_points.csv` | operating points for the disagreement signal |
| `results/table_rarebench_coverage.csv` | RareBench coverage after mapping |
| `results/table_rarebench_retrieval.csv` | retrieval on 834 RareBench cases |
| `results/rarebench_ranks.csv` | per-case external retrieval ranks |
| `results/best_rrf.json` | the frozen fusion weights |
| `results/provenance_v5.json` | run configuration written by the notebook |

## Known limits

- MedGemma 27B ran at 4-bit NF4 quantisation on Turing hardware. These are results for
  that quantised artefact, not for the released checkpoint.
- The external re-ranking arm reads candidates from the untuned `hybrid` configuration.
  That choice was made after seeing external retrieval results and is declared in the paper.
- The classical baselines (Phrank-style, Resnik-style, LIRICAL-style) are
  re-implementations written from published descriptions and were never checked against
  the original code.
- The HPO release used is `hp/releases/2026-06-23`; RareBench was curated against
  2023-06-06.

## Licence

Code: MIT (`LICENSE`). Result tables, prompts and archived outputs: CC BY 4.0
(`LICENSE-DATA`). Third-party data keeps its own licence and is not redistributed here.

## Citation

See `CITATION.cff`, or cite the archived release DOI listed there.
