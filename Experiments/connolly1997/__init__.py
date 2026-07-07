import utils


def combine(results):
    """Called by main.py after every study for this paper has run.

    Study 1's result file needs both conditions A & B (study1_ab) and C & D
    (study1_cd) -- mirroring the original notebook, where the save happened in
    the C & D cell but depended on variables set by the earlier A & B cell.
    Study 2 saves its own file directly since it never depended on Study 1.
    """
    if "study1_ab" in results and "study1_cd" in results:
        combined = {**results["study1_ab"], **results["study1_cd"]}
        utils.save("connolly1997_study1_results.json", combined)
