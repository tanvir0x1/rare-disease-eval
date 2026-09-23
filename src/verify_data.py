"""Check the downloaded third-party files against the checksums in manifest.json.

Usage:  python -m src.verify_data [--data-dir data/raw]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import sys

EXPECTED_FILES = {
    "hpo": "hp.obo",
    "orphanet": "en_product4.csv",
    "rarebench": "rarebench/data.zip",
}


def sha256(path: pathlib.Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default="data/raw", type=pathlib.Path)
    ap.add_argument("--manifest", default="manifest.json", type=pathlib.Path)
    args = ap.parse_args()

    manifest = json.loads(args.manifest.read_text())
    sources = manifest["data_sources"]

    ok = True
    for key, relpath in EXPECTED_FILES.items():
        path = args.data_dir / relpath
        expected = sources.get(key, {}).get("sha256")
        if not path.exists():
            print(f"MISSING  {path}")
            ok = False
            continue
        if not expected or expected.startswith("FILL IN"):
            print(f"NO CHECKSUM IN MANIFEST  {key}: actual {sha256(path)}")
            ok = False
            continue
        actual = sha256(path)
        if actual == expected:
            print(f"OK       {path}")
        else:
            print(f"MISMATCH {path}\n  expected {expected}\n  actual   {actual}")
            ok = False

    print("\nAll files verified." if ok else "\nSome files failed verification.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
