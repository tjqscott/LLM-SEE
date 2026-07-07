"""Jørgensen, Teigen & Moløkken 2002 -- Study D: Ego-free prediction intervals (new experiment)

Motivation: developers give narrow PIs partly to signal competence. Framing
estimation as a favour for a colleague removes that pressure. Compare PI width
against Study A to test whether the bias has an ego-driven component.
"""
import utils
from . import setup


def build_tasks():
    tasks = []
    for doc_name, doc_text in setup.LONG_DOC:
        prompt = f"""
A colleague has asked you to provide an independent effort estimate for their project.
You have no personal stake in the outcome — you are simply offering an outside perspective.
Provide a 90% prediction interval for how long the project is likely to take.

```requirements
{doc_text}
```

End your response with exactly:
MOST_LIKELY: <number> work-hours
MINIMUM: <number> work-hours
MAXIMUM: <number> work-hours
"""
        for model in utils.MODELS:
            tasks.append((model, prompt, {"doc": doc_name}))
    return tasks


def merge(store, model, response, meta):
    doc = meta["doc"]
    row = setup.parse_pi(response)
    store.setdefault(model, {})[doc] = row
    if row["most_likely"] is None:
        utils.record_failure("jorgensen2002_d_failures.jsonl", model, response, meta)
        print(f"  FAIL {model.split('/')[1]:20} | {doc}")
    else:
        print(f"  OK   {model.split('/')[1]:20} | {doc} | ml={row['most_likely']}")


def run():
    results = {}
    utils.fire_and_collect(build_tasks(), results, merge,
                           save_path="jorgensen2002_d_partial.json")
    utils.save("jorgensen2002_study_d_results.json", results)
    return results
