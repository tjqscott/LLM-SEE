# systematic-review process

First, the full text of the Mohanani et al. (2018) systematic mapping study was reviewed. The 65 identified primary studies were screened, starting with the title, followed by the abstract, and finally a full-text reading where required, in order to identify papers concerned with Software Effort Estimation (SEE). Sixteen relevant papers were identified. Eight listed Magne Jørgensen as the primary author, with his University of Oslo colleague Kjetil Moløkken on a further four. The remaining four papers were first-authored by Haugen and Løhre (also of Oslo), as well as Abdel-Hamid and Connolly (of California and Arizona, USA, respectively).

The search process outlined in the Mohanani paper was replicated across the five scientific databases. This meant searching for papers with the phrases 'software' and "cognitive bias" in their full text or metadata, while filtering for english language papers in the field of Computing/ Software. This process yielded similar results to the Mohanani paper, with the notable exception of Science direct. That particular database yielded over 100 fewer results while every other database was within a margin of error. One possible cause for this discrepancy is the Subject areas selector which contains a serperate section for Engineering and Decision Sciences which might not reflect the state of Science direct in 2016, furthermore, it is also possible that large numbers of papers have been removed in the past decade.

| Source         | Mohanani | Me  |
| -------------- | -------- | --- |
| ACM            | 69       | 71  |
| IEEE           | 153      | 144 |
| Science Direct | 293      | 178 |
| Scopus         | 296      | 307 |
| Web of Science | 15       | 17  |
| Total          | 826      | 717 |
| Duplicates     | 300+     | 75  |

> See the parameters subdirectory of the '-2016' directory for screenshots of the search parameters.

A more in depth reading of the sixteen primary studies revealed that each contained the word estimate or some morphological relative (e.g. estimates, estimating) in its abstract. This fact was used to inform the search for modern papers by adding the term 'estim*' as a new search parameter, specifically in the abstract of candidate documents. The '*' character acts as a wildcard, allowing any word starting with 'estim' to satisfy the condition. Unfortunately, Science direct does not support wildcards, so the list: (estimated, estimate, estimates, estimating, estimator, estimation, estimative, estimability) was provided to cover all of the words identified in the primary studies and other potential morphological relatives.

This new search was submitted on each of the five databases and the resulting citations were downloaded along with the abstract of each paper for further anlysis.

| Source DB | Citation Count |
| --- | --- |
| ACM | 23 |
| IEEE | 22 |
| Science Direct | 40 |
| Scopus | 67 |
| Web of Science | 11 |
| Total | 163 |

> See the parameters subdirectory of the '-present' directory for screenshots of the addition of the additional search parameter.

The 163 total citations from the five databases were uploaded to 'rayyan' for deduplication and a relevance review. Deduplication was carried out using the built in comparison tool. Nineteen papers were removed, leaving 144 in total. These clashes came in exactly two forms: 2 papers with the same DOI; 1 paper with a DOI and one without. In all cases, the authors and title were the same, but for some formatting changes (e.g. John Smith vs. J Smith). The papers were then checked for relevance to the field of software effort estimation (SEE), without yet considering other keywords. This left just nineteen total papers, with many being completely irrelevent to the field of computing (e.g. Health, Agriculture) and many more being within the field, but outwith SEE (e.g. ML frameworks, Wearable tech).

Finally, these nineteen papers along were tabulated alongside the sixteen primary studies identified by Mohanani et. al. after a final relevance check, which ensured that each paper was concerned with cognitive biases in software effort estimation and conducted an experiment therein using human participants. A total of 21 papers met the complete criteria, with the final list still dominated by Oslo based researchers (Jørgensen, Moløkken, Løhre, Haugen). These papers underwent a comprehensive data extraction and tabulation that can be found in experiment_data.csv. Justification for the selection of columns can be found in column-selection.md with a language guide for cell values at language-guide.md

Finally, this table was used alongside re-reads of the papers to select a battery of experiments that, combined, would give a comprehensive impression of recurring cognitive biases from the literature such that the combination of these experiments might provide a more hollistic understanding of the overall existance of cognitive biases in large language model software effort estimation. On top of these subjective parameters, consideration was given to high quality experiments that were adaptable to large language models, this meant avoiding (or adapting) experiments where participants were asked to analyse real projects that they were working on and those using visual aids in their trials as these do not lend themselves to language model replication.
