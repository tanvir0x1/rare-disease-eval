# Delete this file before you tag the release

Placeholders to fill in:

1. `USERNAME` in README.md, CITATION.cff, manifest.json.
2. `10.5281/zenodo.XXXXXXX` in CITATION.cff and manifest.json - fill in after the first
   Zenodo release, then commit and re-release (the concept DOI stays stable afterwards).
3. `FILL IN` fields in manifest.json: git commit, Hugging Face revisions for MedGemma and
   SapBERT, Orphanet release date, RareBench source/commit, and the three checksums.
4. `requirements.txt` - replace the commented block with real `pip freeze` output.
5. Add the code to `src/`, the cleaned notebooks to `notebooks/`, the archived responses
   to `runs/`, and the figure script to `figures/`.
6. Add the four result tables not yet in `results/`:
   `table_rarebench_llm_v5.csv`, `table_rarebench_published.csv`,
   `table_pvalues_corrected.csv`, `table_final_summary.csv`.

Two inconsistencies between your own provenance files - resolve them and make
manifest.json match reality:

- `provenance_v4.json` says bitsandbytes 0.50.2; the thesis table says 0.50.1.
  manifest.json currently says 0.50.1.
- `provenance_v4.json` and the thesis say the MedGemma compute dtype was float16;
  `provenance_v5.json` says fp32. manifest.json currently says float16. A reviewer who
  opens both files will see this, so fix it in the paper too.

Also check: `provenance_v5.json` records `hpo_pinned_tag_requested: v2023-06-06` but
`hpo_data_version: hp/releases/2026-06-23`, i.e. the pin was requested but not applied.
The paper should say this plainly rather than leave the two fields to contradict each other.
