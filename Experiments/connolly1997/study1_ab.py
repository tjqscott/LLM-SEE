"""Connolly & Dean 1997 -- Study 1, Conditions A & B: Greater-than wording

Order is the manipulation. A: whole task first, then subtasks. B: subtasks first,
then whole task. Does not save on its own -- combined with study1_cd's C & D
results and saved when the whole paper is run (see connolly1997/__init__.py).
"""
from . import setup


def run():
    results_s1a = setup.run_connolly("S1A", "First estimate the WHOLE project, then each subtask.",
                                     setup.STUDY1_PREAMBLE_GT, setup.TASK_PAIRS)
    results_s1b = setup.run_connolly("S1B", "First estimate each SUBTASK, then the whole project.",
                                     setup.STUDY1_PREAMBLE_GT, setup.TASK_PAIRS)
    return {"A": results_s1a, "B": results_s1b}
