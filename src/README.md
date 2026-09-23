# Source

Modules extracted from `notebooks/`. Each is runnable as `python -m src.<name>`.

| Module | What it does |
| --- | --- |
| `build_kb.py` | builds the 4,289-disorder knowledge base with frequency weights and the HPO ancestor closure |
| `make_tiers.py` | generates the T0-T3 noise tiers for the 100 evaluation and 60 development diseases (seed 42) |
| `retrievers.py` | BM25, SapBERT dense, information-content overlap, and the classical Phrank-/Resnik-/LIRICAL-style baselines |
| `fusion.py` | weighted reciprocal rank fusion |
| `tune_fusion.py` | the 228-configuration grid search on the development split; writes `best_rrf.json` |
| `eval_retrieval.py` | retrieval ablation on the evaluation split |
| `rerank.py` | the ensemble re-ranking runner; live or `--replay` |
| `parsing.py` | the output parser described in `prompts/README.md` |
| `eval_external.py` | the RareBench arm: mapping, coverage, retrieval and re-ranking |
| `abstention.py` | disagreement signals, accuracy-coverage curves, AURC, operating points |
| `stats.py` | exact McNemar tests with Holm and Benjamini-Hochberg correction inside the four pre-declared families |
| `verify_data.py` | checks `data/raw/` against the checksums in `manifest.json` |
| `export_runs.py` | converts `llm_rerank_checkpoint.pkl` into the per-call layout in `runs/` |

Keep the module names or update this table and the README reproduction steps to match.

## Before you push

- No API keys anywhere, including in notebook outputs and in `runs/`.
- `pip freeze > requirements.txt` from the environment that produced the results.
