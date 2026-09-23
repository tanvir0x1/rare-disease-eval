# Archived model responses

One JSON file per model call, from the runs reported in the paper. These are what make
the results reproducible even though two of the three ensemble members are provider
aliases that can be repointed without notice.

```
runs/internal/<tier>/<case_id>__<model_slug>.json      1,200 files (100 cases x 4 tiers x 3 models)
runs/external/<case_id>__<model_slug>.json             1,668 files (834 cases x 2 models)
```

Each file:

```json
{
  "case_id": "RAMEDIS_0",
  "split": "external",
  "tier": null,
  "model_alias": "mistral-small-latest",
  "model_reported_id": "<whatever the response reported, if anything>",
  "requested_at_utc": "2026-06-29T00:00:00Z",
  "prompt_sha256": "<sha256 of system + user message as sent>",
  "candidates": ["ORPHA:...", "..."],
  "raw_response": "<the completion text exactly as returned>",
  "parsed_ranking": [4, 1, 17, "..."],
  "n_appended_by_parser": 0,
  "error": null
}
```

Nothing here is edited. Failed or retried calls are kept with `error` filled in.

Recompute every table from these files, with no network access:

```bash
python -m src.rerank --replay runs/ --split internal
python -m src.eval_external --replay runs/
```

If `llm_rerank_checkpoint.pkl` from the original run is the only copy you have, export it
to this layout with `python -m src.export_runs llm_rerank_checkpoint.pkl runs/`.
