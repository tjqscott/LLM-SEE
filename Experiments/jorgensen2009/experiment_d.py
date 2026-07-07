"""Jørgensen 2009 -- Experiment D: Colleague's project (new experiment)

Motivation: Jørgensen's original Experiment D tested the MORE→optimism effect
when estimators have no personal stake, using a conference scenario. Here the
same LESS/MORE structure is applied to software estimation with a colleague
framing. If the effect persists, it is not driven by personal investment.
"""
import utils
from . import setup


def run():
    less_d = "briefly describe the THREE MOST IMPORTANT risk factors for your colleague's project."
    more_d = "identify as many important risk factors as you can for your colleague's project."
    colleague_framing = ("A colleague has asked you to provide an independent effort estimate for their project. "
                         "You have no personal stake in the outcome — you are simply offering an outside perspective.")

    results = {"LESS": {}, "MORE": {}}
    utils.fire_and_collect(setup.build_tasks(less_d, more_d, setup.BRIEF_DOCS, framing=colleague_framing),
                           results, setup.merge, save_path="jorgensen2009_d_partial.json")
    return results
