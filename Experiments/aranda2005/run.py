"""Aranda & Easterbrook 2005 -- Anchoring and Adjustment in Software Estimation"""
import re

import utils
from . import setup


def build_tasks():
    tasks = []

    for doc_name, doc_text in setup.TAWOS_DOCS:
        anchors = setup.TAWOS_ANCHORS.get(doc_name, {})
        condition_list = [
            ("control", "I'd like to give an estimate for this project myself, but I admit "
                        "I have no experience estimating. We'll wait for your calculations for an estimate."),
        ]
        if doc_name in setup.TAWOS_ANCHORS:
            condition_list += [
                ("low",  f"I admit I have no experience with software projects, but I guess this will "
                         f"take about {anchors['low']} months to finish. I may be wrong of course."),
                ("high", f"I have taken a look at the requirements and I think this will take about "
                         f"{anchors['high']} months to finish. I may be wrong of course."),
            ]
        for condition_name, anchor_sentence in condition_list:
            prompt = f"""
You are a software developer asked to estimate the effort required to complete the project below.
Read the requirements carefully, perform any calculations you wish, and provide your estimate.

The project manager has said: "{anchor_sentence}"
```requirements
{doc_text}
```

End your response with exactly:
I ESTIMATE THE PROJECT WILL TAKE <number> MONTHS TO DELIVER.
CONFIDENCE: <number>%
"""
            for model in utils.MODELS:
                tasks.append((model, prompt, {"key": f"{doc_name}_{condition_name}"}))
    return tasks


def merge(store, model, response, meta):
    months = re.search(r"WILL TAKE\s*\*{0,2}\s*(\d+)", response or "", re.IGNORECASE)
    conf   = re.search(r"CONFIDENCE:\s*(\d+)", response or "")
    store.setdefault(model, {})[meta["key"]] = {
        "months":     int(months.group(1)) if months else None,
        "confidence": int(conf.group(1))   if conf   else None,
    }
    print(f"  {model.split('/')[1]:20} | {meta['key']}")


def run():
    results = {}
    utils.fire_and_collect(build_tasks(), results, merge,
                           save_path="aranda2005_partial.json")
    utils.save("aranda2005_results.json", results)
    return results
