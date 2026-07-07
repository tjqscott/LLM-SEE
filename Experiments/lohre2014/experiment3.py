"""Løhre & Jørgensen 2014 -- Experiment 3: Source credibility

Four groups. Anchor is always 10 hours. Source varies: neutral framing,
low-credibility source (admin with no technical background), high-credibility
source (project manager with software background).
"""
import utils
from . import setup


def run():
    conditions = {
        "control":          "",
        "low_credibility":  "\nAn administrative person in your company, with no background in software development, is responsible for logging all work over 10 hours. Without looking at the requirements, they ask whether you think this will take less than 10 work-hours.",
        "high_credibility": "\nYour project manager, who has a background in software development, has reviewed the requirements and asks whether you think this will take more than 10 work-hours.",
        "neutral":          "\nDo you think this project will take more than 10 work-hours?",
    }
    results = {}
    utils.fire_and_collect(setup.build_tasks(conditions), results, setup.merge,
                           save_path="lohre2014_exp3_partial.json")
    return results
