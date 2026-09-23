# Data

No third-party data is redistributed here. Fetch each source yourself, then verify it
against the checksums in `manifest.json` before running anything.

| Source | File | Version used | Where |
| --- | --- | --- | --- |
| Human Phenotype Ontology | `hp.obo` | data version `hp/releases/2026-06-23`, 19,836 active terms, 3,964 alternate ids | obophenotype/human-phenotype-ontology releases |
| Orphanet | `en_product4.csv` | disorder-to-phenotype associations with documented frequency, 115,878 rows | Orphadata |
| RareBench | `data.zip` + `mapping/disease_mapping.json` (11,150 entries) | subsets RAMEDIS, MME, HMS, LIRICAL | the RareBench repository |
| SapBERT | `cambridgeltl/SapBERT-from-PubMedBERT-fulltext` | see `manifest.json` for the pinned revision | Hugging Face |
| MedGemma 27B (text) | `google/medgemma-27b-text-it` | see `manifest.json` for the pinned revision | Hugging Face, gated under the HAI-DEF terms |

Expected layout after download:

```
data/raw/hp.obo
data/raw/en_product4.csv
data/raw/rarebench/            # unpacked data.zip
data/raw/rarebench/mapping/disease_mapping.json
```

`data/raw/` is git-ignored.

## Notes

- The RareBench loader script is not supported by the current `datasets` library, so the
  archive was downloaded and unpacked directly rather than loaded through the dataset API.
- The `PUMCH_ADM` subset is not present in that archive and was not used.
- The HPO release used here is newer than the 2023-06-06 release RareBench was curated
  against. Terms renamed or reparented between the two are resolved through the
  alternate-identifier map. This is declared as a limitation in the paper.

## Verify checksums

```bash
python -m src.verify_data          # compares data/raw/ against manifest.json
```

## Licences

Each source keeps its own licence and terms of use. Check them before redistributing
anything derived from them.
