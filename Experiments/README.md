# Experiments

This folder contains seven Jupyter notebooks, one per source paper replicated in this study.
Each notebook implements the full set of experimental conditions for its corresponding paper
family, assembles prompts at runtime, queries the LLMs via the OpenRouter API, parses
responses, and writes results to the `results/` directory.

## Requirements

Install dependencies with:

```bash
pip install openai asyncio pandas
```

An OpenRouter API key is required. Set it as an environment variable before running any
notebook:

```bash
export OPENROUTER_API_KEY=your_key_here
```

## Usage

The `requirements_documents/` folder must be present in the same directory as the notebooks,
as must `utils.py`, which provides shared utility code for API interaction, response logging,
and parse recovery used across all notebooks. Results will be written to `results/`, which
must also be present in the same directory.

## Notebooks

| Notebook | Source Paper | Bias Category |
|---|---|---|
| `aranda2005.ipynb` | Aranda & Easterbrook (2005) | Anchoring |
| `lohre2014.ipynb` | Løhre & Jørgensen (2014) | Anchoring |
| `haugen2006.ipynb` | Haugen (2006) | Over-optimism |
| `molokken2003.ipynb` | Moløkken & Jørgensen (2003) | Over-optimism |
| `jorgensen2009.ipynb` | Jørgensen (2009) | Over-optimism |
| `connolly1997.ipynb` | Connolly & Dean (1997) | Over-confidence |
| `jorgensen2002.ipynb` | Jørgensen et al. (2002) | Over-confidence |

## Notes

- All models are queried at temperature zero to minimise stochastic variation. See Section
  3.2 of the dissertation for a full discussion of this design decision and its implications.
- Prompts are assembled as Python f-strings at runtime and passed as a single user-turn
  message with no system prompt. The output format instruction always appears last. See
  Section 3.4 of the dissertation for the complete prompt structure and per-experiment
  output format specifications.
- Execution is asynchronous via Python's `asyncio` library.
- Kimi K2.5 uses a raised token limit (10,000 tokens) and an extended timeout (300 seconds)
  due to its tendency to produce lengthy reasoning traces. This is configured within the
  notebook.
- Failure logs were used during execution to guide post-hoc recovery of malformed responses
  (e.g. week-format values from DeepSeek) but were not retained as artefacts. Recovery
  logic is implemented within `utils.py`.
- Full methodological details, including deviations from original study designs, are
  documented in Section 3.6 of the dissertation.