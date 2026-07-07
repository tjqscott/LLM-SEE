"""Jørgensen, Teigen & Moløkken 2002 -- Study C: Confidence level sensitivity

The same project brief is estimated at four confidence levels. PI width should
increase markedly with confidence level if the LLM is well-calibrated.
"""
import utils
from . import setup


def build_tasks():
    tasks = []
    for doc_name, doc_text in setup.BRIEF_DOC:
        for confidence in [50, 75, 90, 99]:
            prompt = f"""
You are a software developer estimating the effort required to complete the project below.
Assume average productivity for your team using the technology stack your company knows best.

Provide a {confidence}% prediction interval: you are {confidence}% confident the actual
effort will fall between your minimum and maximum.

```requirements
{doc_text}
```

End your response with exactly:
MOST_LIKELY: <number> work-hours
MINIMUM: <number> work-hours
MAXIMUM: <number> work-hours
"""
            for model in utils.MODELS:
                tasks.append((model, prompt, {"doc": doc_name, "confidence": confidence}))
    return tasks


def merge(store, model, response, meta):
    doc, conf = meta["doc"], meta["confidence"]
    row = setup.parse_pi(response)
    store.setdefault(model, {}).setdefault(doc, {})[conf] = row
    if row["most_likely"] is None:
        utils.record_failure("jorgensen2002_c_failures.jsonl", model, response, meta)
        print(f"  FAIL {model.split('/')[1]:20} | {doc:30} | {conf}%")
    else:
        print(f"  OK   {model.split('/')[1]:20} | {doc:30} | {conf}% | ml={row['most_likely']}")


def run():
    results = {}
    utils.fire_and_collect(build_tasks(), results, merge,
                           save_path="jorgensen2002_c_partial.json")
    utils.save("jorgensen2002_study_c_results.json", results)
    return results
