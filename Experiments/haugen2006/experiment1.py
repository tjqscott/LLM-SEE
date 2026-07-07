"""Haugen 2006 -- An Empirical Study of Using Planning Poker for User Story Estimation

Experiment 1 -- Unstructured group estimation vs planning poker.

Each story estimated individually. Unstructured: Developer A volunteers first, each
subsequent developer sees prior estimates. Planning poker: all four estimate
simultaneously in parallel, highest and lowest justify, then consensus.
"""
import re

import utils
from . import setup


def _parse_estimate(response):
    est = re.search(r"ESTIMATE:\s*([\d.]+)", response or "")
    if not est:
        nums = utils.extract_numbers(next((l for l in (response or "").splitlines() if "ESTIMATE" in l), ""))
        return float(nums[0]) if nums else None
    return float(est.group(1))


def run():
    DEVS          = setup.DEVS
    RELEASE_PAIRS = setup.RELEASE_PAIRS
    story_index   = setup.story_index

    # Haugen runs in four waves due to sequential dependencies:
    #
    #  Wave U1: each developer estimates individually (sequential within a story,
    #           but all stories × all models fire at once via one dev-loop iteration).
    #           Because each dev sees prior estimates, we actually need 4 sub-waves
    #           per story — but we can still parallelise across all stories × models.
    #
    #  Wave U2: group consensus for unstructured (after U1).
    #  Wave P1: planning poker — all four devs estimate independently (parallel).
    #  Wave P2: high/low developer justifications (after P1, parallel).
    #  Wave P3: planning poker consensus (after P2).

    results = {
        model: {
            f"{easy}__{hard}": {"unstructured": [], "planning_poker": []}
            for easy, hard in RELEASE_PAIRS
        }
        for model in utils.MODELS
    }

    # ── Unstructured: 4 sequential sub-waves, each parallelised across story×model ──
    # Individual estimates accumulate in prior_u[model][pair_key][release_name][story_idx]
    prior_u = {}   # {model: {pair_key: {release_name: {story_idx: str}}}}  (running text)
    indiv_u = {}   # {model: {pair_key: {release_name: {story_idx: {dev: val}}}}}

    for model in utils.MODELS:
        prior_u[model] = {}
        indiv_u[model] = {}
        for easy, hard in RELEASE_PAIRS:
            pk = f"{easy}__{hard}"
            prior_u[model][pk] = {easy: {}, hard: {}}
            indiv_u[model][pk] = {easy: {i: {} for i in range(len(story_index[easy]))},
                                   hard: {i: {} for i in range(len(story_index[hard]))}}

    for dev, persona in DEVS.items():
        dev_tasks = []
        for model in utils.MODELS:
            for easy, hard in RELEASE_PAIRS:
                pk = f"{easy}__{hard}"
                for release_name in [easy, hard]:
                    for si, story_text in enumerate(story_index[release_name]):
                        prior_text = prior_u[model][pk][release_name].get(si, "")
                        dev_tasks.append((model,
                            f"""You are {dev} — {persona}.
Estimate the user story below in ideal pair-days.
The team is using an unstructured process where developers volunteer estimates one at a time.
{prior_text}
End with: ESTIMATE: <number> pair-days

```story
{story_text}
```""",
                            {"model": model, "pair_key": pk, "release": release_name,
                             "story_idx": si, "dev": dev, "story_text": story_text}))

        dev_store = {}

        def merge_dev(store, model, response, meta):
            val = _parse_estimate(response)
            pk, rel, si, dv = meta["pair_key"], meta["release"], meta["story_idx"], meta["dev"]
            indiv_u[model][pk][rel][si][dv] = val
            if val is not None:
                prior_u[model][pk][rel][si] = (
                    prior_u[model][pk][rel].get(si, "") + f"{dv} estimated {val} pair-days.\n"
                )
            else:
                utils.record_failure("haugen2006_failures.jsonl", model, response, meta)

        utils.fire_and_collect(dev_tasks, dev_store, merge_dev)
        print(f"Unstructured sub-wave done: {dev}")

    # ── Wave U2: group consensus for unstructured ─────────────────────────────────
    u2_tasks = []
    for model in utils.MODELS:
        for easy, hard in RELEASE_PAIRS:
            pk = f"{easy}__{hard}"
            for release_name in [easy, hard]:
                for si, story_text in enumerate(story_index[release_name]):
                    prior_text = prior_u[model][pk][release_name].get(si, "")
                    u2_tasks.append((model,
                        f"""The team has discussed the story below. Individual estimates: {prior_text}
End with: ESTIMATE: <number> pair-days

```story
{story_text}
```""",
                        {"model": model, "pair_key": pk, "release": release_name, "story_idx": si}))

    group_u = {}   # {model: {pk: {release: {si: val}}}}

    def merge_u2(store, model, response, meta):
        val = _parse_estimate(response)
        pk, rel, si = meta["pair_key"], meta["release"], meta["story_idx"]
        store.setdefault(model, {}).setdefault(pk, {}).setdefault(rel, {})[si] = val
        if val is None:
            utils.record_failure("haugen2006_failures.jsonl", model, response, meta)

    utils.fire_and_collect(u2_tasks, group_u, merge_u2)
    print("Unstructured group wave done")

    # ── Wave P1: planning poker — all devs independent, all stories × models ──────
    p1_tasks = []
    for model in utils.MODELS:
        for easy, hard in RELEASE_PAIRS:
            pk = f"{easy}__{hard}"
            for release_name in [easy, hard]:
                for si, story_text in enumerate(story_index[release_name]):
                    for dev, persona in DEVS.items():
                        p1_tasks.append((model,
                            f"""You are {dev} — {persona}.
Estimate the user story below in ideal pair-days using planning poker.
Estimate independently without considering what others might say.
End with: ESTIMATE: <number> pair-days

```story
{story_text}
```""",
                            {"model": model, "pair_key": pk, "release": release_name,
                             "story_idx": si, "dev": dev}))

    indiv_p = {}   # {model: {pk: {release: {si: {dev: val}}}}}

    def merge_p1(store, model, response, meta):
        val = _parse_estimate(response)
        pk, rel, si, dev = meta["pair_key"], meta["release"], meta["story_idx"], meta["dev"]
        store.setdefault(model, {}).setdefault(pk, {}).setdefault(rel, {}).setdefault(si, {})[dev] = val
        if val is None:
            utils.record_failure("haugen2006_failures.jsonl", model, response, meta)

    utils.fire_and_collect(p1_tasks, indiv_p, merge_p1)
    print("Planning poker individual wave done")

    # ── Wave P2: high/low justifications ─────────────────────────────────────────
    p2_tasks = []
    for model in utils.MODELS:
        for easy, hard in RELEASE_PAIRS:
            pk = f"{easy}__{hard}"
            for release_name in [easy, hard]:
                for si in range(len(story_index[release_name])):
                    est_map = indiv_p.get(model, {}).get(pk, {}).get(release_name, {}).get(si, {})
                    valid   = {d: v for d, v in est_map.items() if v is not None}
                    if len(valid) < 2:
                        continue
                    reveal   = "  ".join(f"{d}: {v}" for d, v in est_map.items())
                    high_dev = max(valid, key=valid.get)
                    low_dev  = min(valid, key=valid.get)
                    for dev, label in [(high_dev, "highest"), (low_dev, "lowest")]:
                        p2_tasks.append((model,
                            f"You are {dev} — {DEVS[dev]}. Estimates revealed: {reveal}. "
                            f"You gave the {label} estimate of {est_map[dev]} pair-days. "
                            f"Briefly justify your reasoning.",
                            {"model": model, "pair_key": pk, "release": release_name,
                             "story_idx": si, "dev": dev}))

    justifications = {}   # {model: {pk: {release: {si: {dev: text}}}}}

    def merge_p2(store, model, response, meta):
        pk, rel, si, dev = meta["pair_key"], meta["release"], meta["story_idx"], meta["dev"]
        store.setdefault(model, {}).setdefault(pk, {}).setdefault(rel, {}).setdefault(si, {})[dev] = response or ""

    utils.fire_and_collect(p2_tasks, justifications, merge_p2)
    print("Planning poker justifications done")

    # ── Wave P3: planning poker consensus ─────────────────────────────────────────
    p3_tasks = []
    for model in utils.MODELS:
        for easy, hard in RELEASE_PAIRS:
            pk = f"{easy}__{hard}"
            for release_name in [easy, hard]:
                for si, story_text in enumerate(story_index[release_name]):
                    est_map = indiv_p.get(model, {}).get(pk, {}).get(release_name, {}).get(si, {})
                    reveal  = "  ".join(f"{d}: {v}" for d, v in est_map.items())
                    just    = justifications.get(model, {}).get(pk, {}).get(release_name, {}).get(si, {})
                    just_text = "\n".join(f"{d}: {r}" for d, r in just.items())
                    p3_tasks.append((model,
                        f"""Planning poker for the story below. Estimates: {reveal}
Justifications: {just_text}
End with: ESTIMATE: <number> pair-days

```story
{story_text}
```""",
                        {"model": model, "pair_key": pk, "release": release_name, "story_idx": si}))

    group_p = {}   # {model: {pk: {release: {si: val}}}}

    def merge_p3(store, model, response, meta):
        val = _parse_estimate(response)
        pk, rel, si = meta["pair_key"], meta["release"], meta["story_idx"]
        store.setdefault(model, {}).setdefault(pk, {}).setdefault(rel, {})[si] = val
        if val is None:
            utils.record_failure("haugen2006_failures.jsonl", model, response, meta)

    utils.fire_and_collect(p3_tasks, group_p, merge_p3, save_path="haugen2006_partial.json")
    print("Planning poker consensus done")

    # ── Assemble final results ────────────────────────────────────────────────────
    for model in utils.MODELS:
        for easy, hard in RELEASE_PAIRS:
            pk = f"{easy}__{hard}"
            for release_name in [easy, hard]:
                stories = story_index[release_name]
                for si in range(len(stories)):
                    results[model][pk]["unstructured"].append({
                        "release":    release_name,
                        "individual": indiv_u.get(model, {}).get(pk, {}).get(release_name, {}).get(si, {}),
                        "group":      group_u.get(model, {}).get(pk, {}).get(release_name, {}).get(si),
                    })
                    results[model][pk]["planning_poker"].append({
                        "release":    release_name,
                        "individual": indiv_p.get(model, {}).get(pk, {}).get(release_name, {}).get(si, {}),
                        "group":      group_p.get(model, {}).get(pk, {}).get(release_name, {}).get(si),
                    })
                print(f"{model.split('/')[1]:20} | {release_name:35} | {len(stories)} stories done")

    utils.save("haugen2006_results.json", results)
    return results
