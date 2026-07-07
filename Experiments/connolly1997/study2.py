"""Connolly & Dean 1997 -- Study 2: Extreme limit-setting

Before estimating, participants identify the most extreme plausible bounds.
Assignment 2 is preceded by personalised feedback showing where Assignment 1
outcomes fell in the estimated distribution.
"""
import utils
from . import setup


def run():
    results_s2a = setup.run_connolly("S2A", "First estimate the WHOLE project, then each subtask.",
                                     setup.STUDY2_PREAMBLE, setup.TASK_PAIRS, with_feedback=True)
    results_s2b = setup.run_connolly("S2B", "First estimate each SUBTASK, then the whole project.",
                                     setup.STUDY2_PREAMBLE, setup.TASK_PAIRS, with_feedback=True)

    results = {"A": results_s2a, "B": results_s2b}
    utils.save("connolly1997_study2_results.json", results)
    return results
