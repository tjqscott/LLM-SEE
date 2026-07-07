"""Jørgensen 2009 -- Experiment C: 1 risk vs risk table with probability and severity

Different specification from A and B (user story documents). MORE group records
probability and severity for each risk in a structured table. Success question
asks about overrun probability rather than success probability.
"""
import utils
from . import setup


def run():
    less_c = "briefly describe the SINGLE MOST IMPORTANT risk factor for this project."
    more_c = ("identify all important risk factors you can. For each risk, complete a table with: "
              "(1) description, (2) probability of occurrence (low / medium / high), "
              "(3) severity of impact (low / medium / high).")

    results = {"LESS": {}, "MORE": {}}
    utils.fire_and_collect(
        setup.build_tasks(less_c, more_c, setup.STORY_DOCS,
                          success_question="the probability of experiencing more than 25% effort overrun"),
        results, setup.merge, save_path="jorgensen2009_c_partial.json")
    return results
