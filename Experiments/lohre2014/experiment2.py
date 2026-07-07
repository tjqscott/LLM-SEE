"""Løhre & Jørgensen 2014 -- Experiment 2: Low anchor, anchor precision

Three groups. Anchor values are low (~20 hours). Precise interval (19-21 h) vs
imprecise interval (10-30 h).
"""
import utils
from . import setup


def run():
    conditions = {
        "control":            "",
        "precise_interval":   "\nBefore you begin: consider how likely it is that this project will take between 19 and 21 work-hours.",
        "imprecise_interval": "\nBefore you begin: consider how likely it is that this project will take between 10 and 30 work-hours.",
    }
    results = {}
    utils.fire_and_collect(setup.build_tasks(conditions), results, setup.merge,
                           save_path="lohre2014_exp2_partial.json")
    return results
