import utils


def combine(results):
    """Called by main.py after every experiment for this paper has run."""
    utils.save("jorgensen2009_results.json", {
        "exp_a": results["experiment_a"],
        "exp_b": results["experiment_b"],
        "exp_c": results["experiment_c"],
        "exp_d": results["experiment_d"],
    })
