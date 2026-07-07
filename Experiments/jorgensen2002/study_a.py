"""Jørgensen, Teigen & Moløkken 2002 -- Study A: 90% prediction interval hit rate

LLM provides a 90% PI per document. Hit rate is computed offline against TAWOS
ground truth completion times.
"""
import utils
from . import setup


def build_tasks():
    tasks = []
    for doc_name, doc_text in setup.LONG_DOC:
        prompt = f"""
You are a software developer estimating the effort required to complete the project below.
Assume average productivity for your team using the technology stack your company knows best.

Provide a 90% confidence prediction interval: you are 90% confident the actual effort will fall
between your minimum and maximum. That is, across 100 similar projects, the actual effort should
fall within your range approximately 90 times.

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
    row["completion_times"] = utils.load_completion_times(doc)
    store.setdefault(model, {})[doc] = row
    if row["most_likely"] is None:
        utils.record_failure("jorgensen2002_a_failures.jsonl", model, response, meta)
        print(f"  FAIL {model.split('/')[1]:20} | {doc}")
    else:
        print(f"  OK   {model.split('/')[1]:20} | {doc} | ml={row['most_likely']}")


def run():
    results = {}
    utils.fire_and_collect(build_tasks(), results, merge,
                           save_path="jorgensen2002_a_partial.json")
    utils.save("jorgensen2002_study_a_results.json", results)
    return results
