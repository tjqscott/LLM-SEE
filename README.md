# Replication Package — Uncovering the Cognitive Biases of LLMs in Software Effort Estimation

This package contains all materials required to replicate the experiments and reproduce
the results reported in the dissertation. It accompanies the dissertation titled:

> Uncovering the Cognitive Biases of LLMs in Software Effort Estimation

## Repository Structure

```
├── experiment_selection/       # Systematic review process and paper selection
├── experiments/                # Jupyter notebooks implementing all 16 experiments
│   ├── utils.py                # Shared utility code for all notebooks
│   └── ...
├── figures/                    # Figures appearing in the dissertation and the script to generate them
├── requirements_documents/     # All requirements documents used as estimation inputs
├── statistical_analysis/       # R script and output for all statistical tests
└── results/                    # Numerical outputs from all experiments
```

## Prerequisites

### Python
Install dependencies with:

```bash
pip install openai asyncio pandas
```

An OpenRouter API key is required to run the experiments. Set it as an environment
variable before running any notebook:

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
The requirements documents were constructed from the TAWOS dataset, which must be
obtained and set up independently if you wish to regenerate them from source. The
dataset is publicly available at:

https://doi.org/10.1145/3524842.3528029

The SQL queries used to extract source data are provided in
`requirements_documents/issues.sql` and `requirements_documents/summary.sql`.
Pre-constructed documents are provided in the `requirements_documents/` folder and
do not need to be regenerated to run the experiments.

## Replication Steps

Follow these steps in order to fully replicate the study.

### 1. Run the Experiments

Each experiment notebook is self-contained and can be run independently. The
`requirements_documents/` folder and `utils.py` must be present in the same directory
as the notebooks. Results will be written to the `results/` folder, which must also
be present in the same directory.

Open and run each of the following notebooks:

| Notebook | Source Paper | Bias Category |
|---|---|---|
| `aranda2005.ipynb` | Aranda & Easterbrook (2005) | Anchoring |
| `lohre2014.ipynb` | Løhre & Jørgensen (2014) | Anchoring |
| `haugen2006.ipynb` | Haugen (2006) | Over-optimism |
| `molokken2003.ipynb` | Moløkken & Jørgensen (2003) | Over-optimism |
| `jorgensen2009.ipynb` | Jørgensen (2009) | Over-optimism |
| `connolly1997.ipynb` | Connolly & Dean (1997) | Over-confidence |
| `jorgensen2002.ipynb` | Jørgensen et al. (2002) | Over-confidence |

Note that regenerated results may differ slightly from those provided due to
implementation-level non-determinism in model providers, even at temperature zero.
See Section 3.2 of the dissertation for a discussion of this limitation.

### 2. Run the Statistical Analysis

With the `results/` folder populated, run `statistical_analysis/analysis.R` from the
same directory as `results/`. This will produce `output.md` containing all test
statistics, corrected p-values, and effect sizes.

### 3. Regenerate Figures

With the `results/` folder populated, run `figures/visualise_results.py` from the
same directory as `results/`. This will regenerate all figures reported in the
dissertation.

## Notes

- Full methodological details, including prompt structure, experimental design, and
  deviations from original study designs, are documented in the dissertation.
- Failure logs were used during execution to guide post-hoc recovery of malformed
  responses but were not retained as artefacts. Recovery logic is implemented within
  `utils.py`.
- Each subdirectory contains its own README with further details.
