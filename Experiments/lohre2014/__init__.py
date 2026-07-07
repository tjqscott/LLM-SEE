import utils


def combine(results):
    """Called by main.py after every experiment for this paper has run."""
    utils.save("lohre2014_results.json", {
        "exp1": results["experiment1"],
        "exp2": results["experiment2"],
        "exp3": results["experiment3"],
    })
