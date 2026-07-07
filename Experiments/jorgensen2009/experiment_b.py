"""Jørgensen 2009 -- Experiment B: 1 risk vs structured retrospective analysis

MORE group spends at least 5 minutes recalling similar past projects and what
went wrong, then identifies all risk factors with support from a checklist of
common risk categories.
"""
import utils
from . import setup


def run():
    less_b = "briefly describe the SINGLE MOST IMPORTANT risk factor for this project."
    more_b = ("spend at least 5 minutes thinking back on similar development tasks you have worked on "
              "and what went wrong when completing those tasks. Consider risks such as: unclear or changing "
              "requirements, technical problems, personnel issues, integration difficulties, testing challenges, "
              "and scope creep. Then identify all important risk factors you can for this project.")

    results = {"LESS": {}, "MORE": {}}
    utils.fire_and_collect(setup.build_tasks(less_b, more_b, setup.BRIEF_DOCS),
                           results, setup.merge, save_path="jorgensen2009_b_partial.json")
    return results
