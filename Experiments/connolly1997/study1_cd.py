"""Connolly & Dean 1997 -- Study 1, Conditions C & D: Less-than wording

Identical to A & B but fractile questions are framed in less-than format. Tests
whether wording direction affects optimism or overtightness. Does not save on its
own -- combined with study1_ab's A & B results and saved when the whole paper is
run (see connolly1997/__init__.py).
"""
from . import setup


def run():
    results_s1c = setup.run_connolly("S1C", "First estimate the WHOLE project, then each subtask.",
                                     setup.STUDY1_PREAMBLE_LT, setup.TASK_PAIRS)
    results_s1d = setup.run_connolly("S1D", "First estimate each SUBTASK, then the whole project.",
                                     setup.STUDY1_PREAMBLE_LT, setup.TASK_PAIRS)
    return {"C": results_s1c, "D": results_s1d}
