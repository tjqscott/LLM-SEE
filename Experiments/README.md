# Experiments

This folder contains one Python package per source paper replicated in this study. Each
package implements the full set of experimental conditions for its corresponding paper
family, assembles prompts at runtime, queries the LLMs via the OpenRouter API, parses
responses, and writes results to the `results/` directory. `main.py` is the single CLI
entry point used to run them.

## Requirements

Install dependencies with:

```bash
pip install openai asyncio pandas
```

An OpenRouter API key is required. Set it as an environment variable before running any
experiment:

```bash
export OPENROUTER_API_KEY=your_key_here
```

## Usage

Run `main.py` from the **repository root** (not from inside `Experiments/`) so that the
relative paths to `Requirements documents/` and `Results/` resolve correctly:

```bash
python Experiments/main.py
```

With no arguments it prints full usage, including every paper and the studies available
for it. The general form is:

```bash
python Experiments/main.py <paper> [<study>]
```

Omitting `<study>` runs every study for that paper in order, matching the original
notebook's top-to-bottom execution. Some papers only produce their final combined results
file once every study has run in the same invocation (marked `(combined)` in the usage
output) -- this mirrors the original notebook, where the final save cell depended on
variables set by earlier cells.

Examples:

```bash
python Experiments/main.py jorgensen2009                # run all 4 experiments, write combined results
python Experiments/main.py jorgensen2009 experiment_a    # run just Experiment A
python Experiments/main.py molokken2003                  # run the (only) study and write its results
```

## Layout

Each paper is a package containing:

- `setup.py` -- shared code equivalent to the original notebook's first cell: constants,
  document loading, and prompt/parsing helpers used by every study in that paper.
- One module per study/experiment (e.g. `study_a.py`, `experiment1.py`), each equivalent
  to one of the original notebook's later cells and exposing a `run()` function.
- `__init__.py` -- empty, except for papers whose final results file combines multiple
  studies' output, where it defines a `combine()` function called by `main.py`.

`utils.py` is unchanged and shared across every package: it provides the OpenRouter API
interaction, response logging, and parse recovery used across all experiments.

## Papers

| Package | Source Paper | Bias Category |
|---|---|---|
| `aranda2005` | Aranda & Easterbrook (2005) | Anchoring |
| `lohre2014` | Løhre & Jørgensen (2014) | Anchoring |
| `haugen2006` | Haugen (2006) | Over-optimism |
| `molokken2003` | Moløkken & Jørgensen (2003) | Over-optimism |
| `jorgensen2009` | Jørgensen (2009) | Over-optimism |
| `connolly1997` | Connolly & Dean (1997) | Over-confidence |
| `jorgensen2002` | Jørgensen et al. (2002) | Over-confidence |

## Notes

- All models are queried at temperature zero to minimise stochastic variation. See Section
  3.2 of the dissertation for a full discussion of this design decision and its implications.
- Prompts are assembled as Python f-strings at runtime and passed as a single user-turn
  message with no system prompt. The output format instruction always appears last. See
  Section 3.4 of the dissertation for the complete prompt structure and per-experiment
  output format specifications.
- Execution is asynchronous via Python's `asyncio` library.
- Kimi K2.5 uses a raised token limit (10,000 tokens) and an extended timeout (300 seconds)
  due to its tendency to produce lengthy reasoning traces. This is configured within
  `utils.py`.
- Failure logs were used during execution to guide post-hoc recovery of malformed responses
  (e.g. week-format values from DeepSeek) but were not retained as artefacts. Recovery
  logic is implemented within `utils.py`.
- Full methodological details, including deviations from original study designs, are
  documented in Section 3.6 of the dissertation.
