# Notebooks

The notebooks the reported results were produced with. Outputs are cleared; clear them
before every commit:

```bash
pip install nbstripout
nbstripout --install          # run once inside the repo
```

Anything reused by more than one step belongs in `src/`, not here.

Check before committing: notebook outputs are a common place for API keys and absolute
paths containing a username to leak.
