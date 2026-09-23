"""Export archived model responses from the run checkpoint into runs/.

The evaluation stores every model response in llm_rerank_checkpoint.pkl. This writes one
JSON file per call, so the responses are readable and diffable in the repository and the
tables can be recomputed with --replay.

Usage:  python -m src.export_runs llm_rerank_checkpoint.pkl runs/

The checkpoint is a dict keyed by (split, tier, case_id, model_alias); adapt `record_of`
if your key or value layout differs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import pickle
import re
import sys

SECRET_PATTERNS = [
    re.compile(r"AIza[0-9A-Za-z_\-]{30,}"),   # Google API key shape
    re.compile(r"sk-[0-9A-Za-z]{20,}"),        # common key shape
    re.compile(r"Bearer\s+[0-9A-Za-z._\-]{20,}"),
]


def scrub(text: str) -> str:
    for pattern in SECRET_PATTERNS:
        text = pattern.sub("[REDACTED]", text)
    return text


def slug(name: str) -> str:
    return re.sub(r"[^0-9A-Za-z]+", "-", name).strip("-").lower()


def record_of(key, value) -> dict:
    split, tier, case_id, model_alias = key
    prompt = value.get("prompt", "")
    raw = value.get("raw_response", "")
    return {
        "case_id": case_id,
        "split": split,
        "tier": tier,
        "model_alias": model_alias,
        "model_reported_id": value.get("model_reported_id"),
        "requested_at_utc": value.get("requested_at_utc"),
        "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest() if prompt else None,
        "candidates": value.get("candidates"),
        "raw_response": scrub(raw),
        "parsed_ranking": value.get("parsed_ranking"),
        "n_appended_by_parser": value.get("n_appended", 0),
        "error": value.get("error"),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("checkpoint", type=pathlib.Path)
    ap.add_argument("out_dir", type=pathlib.Path)
    args = ap.parse_args()

    with args.checkpoint.open("rb") as fh:
        checkpoint = pickle.load(fh)

    written = 0
    for key, value in checkpoint.items():
        record = record_of(key, value)
        parts = [record["split"] or "unknown"]
        if record["tier"]:
            parts.append(record["tier"])
        directory = args.out_dir.joinpath(*parts)
        directory.mkdir(parents=True, exist_ok=True)
        name = f"{record['case_id']}__{slug(record['model_alias'])}.json"
        (directory / name).write_text(json.dumps(record, indent=2) + "\n")
        written += 1

    print(f"Wrote {written} response files under {args.out_dir}")
    print("Now grep the output for any key that the scrubber missed before committing.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
