# Requirements Documents

This folder contains all requirements documents used as estimation inputs across the 16
replicated experiments, together with the SQL queries used to extract source data from the
TAWOS dataset. Documents are organised into five subdirectories.

## Subdirectories

### `aranda2005/`
Contains the original requirements documents from the Aranda & Easterbrook (2005) study,
used as format exemplars during the construction of TAWOS-based equivalents. Split into
two subdirectories:

- `Authentic PDF files/` — the authentic documents as recovered from the original study package
- `Recreation MD files/` — Markdown reproductions created for use in this project

### `full_specification/`
The 34 full-length narrative requirements documents used in experiments requiring a
whole-project specification (principally the Aranda, Løhre, and Jørgensen 2009 replication
families). Each document corresponds to a real open-source software project drawn from the
TAWOS dataset. Both full and brief versions were piloted under a control condition to
establish baseline effort estimates; see `results/pilot_anchors.json` for these values.
See Section 3.3.1 of the dissertation for details of the construction process.

### `project_brief/`
Abbreviated versions of the 34 narrative documents in `full_specification/`. Each brief
covers the same project as its full counterpart and was produced through the same
human-in-the-loop review process.

### `user_stories/`
55 agile-format issue documents used in experiments requiring story-level estimation
(principally the Moløkken and Haugen replication families). Each document contains
between 7 and 12 user stories extracted from the TAWOS dataset, filtered for issues of
type Story whose description follows the "As a..." format. See Section 3.3.2 of the
dissertation for the full extraction and grouping procedure.

### `completion_times/`
Ground truth completion times for each agile-format issue document in `user_stories/`,
sourced directly from TAWOS as the sum of `Resolution_Time_Minutes` across the issues in
each file, converted to hours. These provide an objective baseline against which LLM
estimates can be evaluated.

## SQL Queries

Two SQL files are provided for reference. Both require access to a local TAWOS instance
and cannot be run in isolation.

- `issues.sql` — extracts agile-format user story issues used to construct the documents
  in `user_stories/` and `completion_times/`
- `summary.sql` — extracts project-level summaries (name, description, issue titles, and
  creation dates for the first 50 issues per project) used to construct the narrative
  documents in `full_specification/` and `project_brief/`

The TAWOS dataset is publicly available at:
https://doi.org/10.1145/3524842.3528029
