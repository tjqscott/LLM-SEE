#!/usr/bin/env python3
"""CLI entry point for the LLM software-estimation-bias replication experiments.

Each paper below used to be a Jupyter notebook; each notebook cell that fired
prompts at the LLMs is now a "study" module with a run() function. This script
runs one study, or every study for a paper in order, and writes results to
results/ -- exactly like the notebooks did.

Run with no arguments to see usage.
"""
import importlib
import sys

REGISTRY = {
    "aranda2005": {
        "title": "Aranda & Easterbrook 2005 -- Anchoring and Adjustment in Software Estimation",
        "studies": ["run"],
    },
    "molokken2003": {
        "title": "Moløkken & Jørgensen 2003 -- Unstructured Group Discussion as a Method to Reduce Individual Biases",
        "studies": ["run"],
    },
    "haugen2006": {
        "title": "Haugen 2006 -- An Empirical Study of Using Planning Poker for User Story Estimation",
        "studies": ["experiment1"],
    },
    "connolly1997": {
        "title": "Connolly & Dean 1997 -- Decomposed Versus Holistic Estimates of Effort Required for Software Writing Tasks",
        "studies": ["study1_ab", "study1_cd", "study2"],
        "combine": True,
    },
    "jorgensen2002": {
        "title": "Jørgensen, Teigen & Moløkken 2002 -- Over-Confidence in Judgement Based Software Development Effort Prediction Intervals",
        "studies": ["study_a", "study_b", "study_c", "study_d"],
    },
    "jorgensen2009": {
        "title": "Jørgensen 2009 -- Identification of More Risks Can Lead to Increased Over-Optimism",
        "studies": ["experiment_a", "experiment_b", "experiment_c", "experiment_d"],
        "combine": True,
    },
    "lohre2014": {
        "title": "Løhre & Jørgensen 2014 -- Numerical Anchors and Their Strong Effects on Software Development Effort Estimates",
        "studies": ["experiment1", "experiment2", "experiment3"],
        "combine": True,
    },
}


def print_usage():
    print("Usage: python main.py <paper> [<study>]")
    print()
    print("Runs one paper's replication experiment(s) and writes results to results/.")
    print("Omit <study> to run every study for that paper in order. This is required")
    print("to produce the combined results file for papers marked (combined) below --")
    print("their final save step needs every study's output, just like the original")
    print("notebook's last cell needed every earlier cell to have already run.")
    print()
    print("Papers:")
    for paper, info in REGISTRY.items():
        tag = "  (combined)" if info.get("combine") else ""
        print(f"  {paper}{tag}")
        print(f"      {info['title']}")
        print(f"      studies: {', '.join(info['studies'])}")
    print()
    print("Examples:")
    print("  python main.py jorgensen2009                # run all 4 experiments, write combined results")
    print("  python main.py jorgensen2009 experiment_a    # run just Experiment A")
    print("  python main.py molokken2003                  # run the (only) study and write its results")


def run_paper(paper, study=None):
    info = REGISTRY[paper]

    if study is not None:
        if study not in info["studies"]:
            print(f"Unknown study '{study}' for paper '{paper}'.")
            print(f"Valid studies: {', '.join(info['studies'])}")
            sys.exit(1)
        module = importlib.import_module(f"{paper}.{study}")
        module.run()
        return

    results = {}
    for name in info["studies"]:
        module = importlib.import_module(f"{paper}.{name}")
        print(f"\n=== {paper}.{name} ===")
        results[name] = module.run()

    if info.get("combine"):
        package = importlib.import_module(paper)
        package.combine(results)


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print_usage()
        return

    paper = args[0]
    if paper not in REGISTRY:
        print(f"Unknown paper '{paper}'.\n")
        print_usage()
        sys.exit(1)

    study = args[1] if len(args) > 1 else None
    run_paper(paper, study)


if __name__ == "__main__":
    main()
