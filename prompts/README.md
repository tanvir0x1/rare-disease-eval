# Prompts

All three ensemble members received identical text; nothing was tailored per provider.

| File | Used for |
| --- | --- |
| `rerank_system.txt` | system prompt for every re-ranking call, internal and external |
| `rerank_user_template.txt` | user message template; a typical instance is ~1,121 characters (~280 tokens) |
| `phenotype_extraction_prototype.txt` | free-text prototype only, not used for any reported result |
| `explanation_prototype.txt` | free-text prototype only, not used for any reported result |

The models return candidate indices only, never disease names, so a fabricated diagnosis
cannot enter the evaluated pipeline.

## Output parsing

Implemented in `src/parsing.py`, in this order:

1. Strip a leading ```` ```json ```` or ```` ``` ```` fence and a trailing fence.
2. Take the substring between the first `{` and the last `}`.
3. Parse as JSON and collect integers recursively from the `ranking` value, accepting
   integers, whole-valued floats and numeric strings, rejecting booleans.
4. If that yields nothing, fall back to every run of digits in the raw text.
5. If that also yields nothing, raise. The runner records an error rather than
   substituting retrieval order, which would otherwise score the retriever and label the
   result as the model.
6. Convert to zero-based positions; discard indices outside [1, 25] and repeats.
7. Append any omitted candidate in retrieval order, and record how many were appended.

Step 7 is the one to watch: a model returning nothing usable would be filled entirely from
retrieval order and would score identically to the retriever. The appended-candidate count
stayed at or below 0.06 per case for MedGemma and 0.02 for the two API models.
