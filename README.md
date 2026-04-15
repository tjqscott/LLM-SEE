# Replication Package — Uncovering the Cognitive Biases of LLMs in Software Effort Estimation

This package contains all materials required to replicate the experiments and reproduce
the results reported in the dissertation. It accompanies the following work:

> Taylor Scott (2025). *Uncovering the Cognitive Biases of LLMs in Software Effort
> Estimation*. University of Glasgow, School of Computing Science.

## Repository Structure

- `experiment_selection/` — systematic review process, database search parameters, and paper selection data
- `experiments/` — Jupyter notebooks implementing all 16 experiments, plus shared utility code
- `figures/` — all figures appearing in the dissertation and the script to generate them
- `requirements_documents/` — all requirements documents used as estimation inputs, plus SQL queries
- `results/` — numerical outputs from all experiments and pilot anchor data
- `statistical_analysis/` — R script and output for all statistical tests

Each directory contains its own README with further details.

## Prerequisites

### Python
```bash
pip install openai asyncio pandas
```

An OpenRouter API key is required to run the experiments:

```bash
export OPENROUTER_API_KEY=your_key_here
```

### R
R can be obtained from https://www.r-project.org/. The following packages are required:

```r
install.packages("jsonlite")
install.packages("effsize")
```

### TAWOS
The requirements documents were constructed from the TAWOS dataset. Pre-constructed
documents are provided in `requirements_documents/` and do not need to be regenerated
to run the experiments. If you wish to regenerate them from source, the dataset is
publicly available at https://doi.org/10.1145/3524842.3528029 and the SQL queries
used to extract source data are provided in `requirements_documents/`.

## Replication Steps

### 1. Run the Experiments

The `requirements_documents/` folder and `utils.py` must be present in the same
directory as the notebooks. Results will be written to `results/`, which must also
be present in the same directory. Open and run each notebook in `experiments/`;
see the README there for the full list. Note that regenerated results may differ
slightly from those provided due to implementation-level non-determinism in model
providers, even at temperature zero. See Section 3.2 of the dissertation for discussion.

### 2. Run the Statistical Analysis

Run `statistical_analysis/analysis.R` from the same directory as `results/`. This
will produce `output.md` containing all test statistics, corrected p-values, and
effect sizes.

### 3. Regenerate Figures

Run `figures/visualise_results.py` from the same directory as `results/`. This will
regenerate all figures reported in the dissertation.

## Notes

- Failure logs were used during execution to guide post-hoc recovery of malformed
  responses but were not retained as artefacts. Recovery logic is implemented in
  `utils.py`.
- Full methodological details are documented in the dissertation, including prompt
  structure, experimental design, and deviations from original study designs.
