"""Moløkken & Jørgensen 2003 -- Unstructured Group Discussion as a Method to Reduce Individual Biases"""
import re

import utils
from . import setup


def _parse_estimate(response):
    est = re.search(r"ESTIMATE:\s*([\d.]+)", response or "")
    if not est:
        nums = utils.extract_numbers(next((l for l in (response or "").splitlines() if "ESTIMATE" in l), ""))
        return int(nums[0]) if nums else None
    return int(float(est.group(1)))


def run():
    ROLES     = setup.ROLES
    DOCUMENTS = setup.DOCUMENTS

    # ── Wave 1: all roles × all models × all docs independently ──────────────────
    wave1_tasks = [
        (model,
         f"""You are a {desc} at a web development company.
Estimate the total effort needed to complete the project below.
Assume average company productivity. Project members are not yet allocated.
End with: ESTIMATE: <number> work-hours

```requirements
{doc_text}
```""",
         {"doc": doc_name, "model": model, "role": role})
        for doc_name, doc_text in DOCUMENTS
        for model in utils.MODELS
        for role, desc in ROLES.items()
    ]

    before = {}   # {doc: {model: {role: hours}}}

    def merge_wave1(store, model, response, meta):
        doc, role = meta["doc"], meta["role"]
        val = _parse_estimate(response)
        store.setdefault(doc, {}).setdefault(model, {})[role] = val
        if val is None:
            utils.record_failure("molokken2003_failures.jsonl", model, response, meta)
            print(f"  FAIL W1 {model.split('/')[1]:20} | {doc:30} | {role}")
        else:
            print(f"  OK   W1 {model.split('/')[1]:20} | {doc:30} | {role} | {val}h")

    utils.fire_and_collect(wave1_tasks, before, merge_wave1)

    # ── Wave 2: group consensus — one per (doc × model) ──────────────────────────
    wave2_tasks = [
        (model,
         f"""A four-person estimation team has shared their individual estimates and now has up to
60 minutes to discuss and agree on a single consensus estimate.
Individual estimates: {"  ".join(f"{r}: {before.get(doc_name,{}).get(model,{}).get(r,'?')}h" for r in ROLES)}
End with: ESTIMATE: <number> work-hours

```requirements
{doc_text}
```""",
         {"doc": doc_name, "model": model})
        for doc_name, doc_text in DOCUMENTS
        for model in utils.MODELS
    ]

    group_est = {}   # {doc: {model: hours}}

    def merge_wave2(store, model, response, meta):
        doc = meta["doc"]
        val = _parse_estimate(response)
        store.setdefault(doc, {})[model] = val
        if val is None:
            utils.record_failure("molokken2003_failures.jsonl", model, response, meta)
            print(f"  FAIL W2 {model.split('/')[1]:20} | {doc:30}")
        else:
            print(f"  OK   W2 {model.split('/')[1]:20} | {doc:30} | group={val}h")

    utils.fire_and_collect(wave2_tasks, group_est, merge_wave2)

    # ── Wave 3: post-discussion personal opinions — all roles × models × docs ─────
    wave3_tasks = [
        (model,
         f"""You are a {desc}. Your team has just agreed on a consensus estimate of {group_est.get(doc_name,{}).get(model,'?')} work-hours.
Individual estimates before discussion were: {"  ".join(f"{r}: {before.get(doc_name,{}).get(model,{}).get(r,'?')}h" for r in ROLES)}
What is your personal revised estimate?
End with: ESTIMATE: <number> work-hours

```requirements
{doc_text}
```""",
         {"doc": doc_name, "model": model, "role": role})
        for doc_name, doc_text in DOCUMENTS
        for model in utils.MODELS
        for role, desc in ROLES.items()
    ]

    after = {}   # {doc: {model: {role: hours}}}

    def merge_wave3(store, model, response, meta):
        doc, role = meta["doc"], meta["role"]
        val = _parse_estimate(response)
        store.setdefault(doc, {}).setdefault(model, {})[role] = val
        if val is None:
            utils.record_failure("molokken2003_failures.jsonl", model, response, meta)

    utils.fire_and_collect(wave3_tasks, after, merge_wave3)

    # ── Assemble results ──────────────────────────────────────────────────────────
    results = {}
    for doc_name, _ in DOCUMENTS:
        for model in utils.MODELS:
            b  = before.get(doc_name, {}).get(model, {})
            g  = group_est.get(doc_name, {}).get(model)
            a  = after.get(doc_name, {}).get(model, {})
            vb = [v for v in b.values() if v]
            va = [v for v in a.values() if v]
            results.setdefault(model, {})[doc_name] = {
                "before": b, "group": g, "after": a,
                "avg_before": round(sum(vb)/len(vb), 1) if vb else None,
                "avg_after":  round(sum(va)/len(va), 1) if va else None,
            }
        print(f"{doc_name}: " + "  ".join(
            f"{m.split('/')[1]} b={results[m][doc_name]['avg_before']} "
            f"g={results[m][doc_name]['group']} "
            f"a={results[m][doc_name]['avg_after']}"
            for m in utils.MODELS))

    utils.save("molokken2003_results.json", results)
    return results
