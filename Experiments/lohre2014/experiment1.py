"""Løhre & Jørgensen 2014 -- Experiment 1: High anchor, anchor precision

Five groups. Anchor values cluster around 1000 hours (implausibly high).
Precision varies: precise single (998 h), round single (1000 h), precise
interval (900-1100 h), imprecise interval (500-1500 h).
"""
import utils
from . import setup


def run():
    conditions = {
        "control":            "",
        "precise_single":     "\nBefore you begin: consider how likely it is that this project will take less than 998 work-hours.",
        "round_single":       "\nBefore you begin: consider how likely it is that this project will take less than 1000 work-hours.",
        "precise_interval":   "\nBefore you begin: consider how likely it is that this project will take between 900 and 1100 work-hours.",
        "imprecise_interval": "\nBefore you begin: consider how likely it is that this project will take between 500 and 1500 work-hours.",
    }
    results = {}
    utils.fire_and_collect(setup.build_tasks(conditions), results, setup.merge,
                           save_path="lohre2014_exp1_partial.json")
    return results
