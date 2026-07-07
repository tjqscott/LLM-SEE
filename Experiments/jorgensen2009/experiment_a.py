"""Jørgensen 2009 -- Experiment A: 3 most important risks vs as many as possible

Brief documents. LESS: identify the 3 most important risks. MORE: identify as
many as possible.
"""
import utils
from . import setup


def run():
    less_a = "briefly describe the THREE MOST IMPORTANT risk factors for this project."
    more_a = "identify as many important risk factors as you can for this project."

    results = {"LESS": {}, "MORE": {}}
    utils.fire_and_collect(setup.build_tasks(less_a, more_a, setup.BRIEF_DOCS),
                           results, setup.merge, save_path="jorgensen2009_a_partial.json")
    return results
