"""Jørgensen, Teigen & Moløkken 2002 -- Study B: Role-based individual estimates and group consensus

Four roles estimate independently in parallel, then the group agrees on a
consensus. Tests whether technical roles are more overconfident.
"""
import utils
from . import setup

ROLE_PROMPT = """You are a {desc}, estimating the total effort required to complete the project below.
Assume average productivity for your team. Provide a 90% prediction interval.
Note: although your role focuses on one area, you are estimating the total project effort.

```requirements
{doc_text}
```

End your response with exactly:
MOST_LIKELY: <number> work-hours
MINIMUM: <number> work-hours
MAXIMUM: <number> work-hours
"""


def run():
    # Study B requires two waves: all role estimates must finish before the group
    # prompt can be built. We run wave 1 (roles), then wave 2 (group) via
    # fire_and_collect.

    # ── Wave 1: all (doc × role × model) role estimates ──────────────────────────
    wave1_tasks = [
        (model, ROLE_PROMPT.format(desc=desc, doc_text=doc_text),
         {"doc": doc_name, "role": role, "model": model})
        for doc_name, doc_text in setup.LONG_DOC
        for role, desc in setup.ROLES.items()
        for model in utils.MODELS
    ]

    role_results = {}   # {doc_name: {model: {role: {ml,mn,mx,pi_width}}}}

    def merge_wave1(store, model, response, meta):
        doc, role = meta["doc"], meta["role"]
        row = setup.parse_pi(response)
        store.setdefault(doc, {}).setdefault(model, {})[role] = row
        if row["most_likely"] is None:
            utils.record_failure("jorgensen2002_b_failures.jsonl", model, response, meta)
            print(f"  FAIL W1 {model.split('/')[1]:20} | {doc:30} | {role}")
        else:
            print(f"  OK   W1 {model.split('/')[1]:20} | {doc:30} | {role} | ml={row['most_likely']}")

    utils.fire_and_collect(wave1_tasks, role_results, merge_wave1)

    # ── Wave 2: group consensus, one per (doc × model) ───────────────────────────
    def build_wave2_tasks():
        tasks = []
        for doc_name, doc_text in setup.LONG_DOC:
            for model in utils.MODELS:
                row    = role_results.get(doc_name, {}).get(model, {})
                reveal = "  ".join(
                    f"{k}: ML={row.get(k,{}).get('most_likely','?')}h "
                    f"PI=[{row.get(k,{}).get('minimum','?')}, {row.get(k,{}).get('maximum','?')}]"
                    for k in setup.ROLES)
                prompt = f"""
A four-person estimation team has independently estimated the project below and now discusses
to agree on a consensus. Individual estimates: {reveal}

```requirements
{doc_text}
```

End your response with exactly:
MOST_LIKELY: <number> work-hours
MINIMUM: <number> work-hours
MAXIMUM: <number> work-hours
"""
                tasks.append((model, prompt, {"doc": doc_name, "model": model}))
        return tasks

    results_b = {}

    def merge_wave2(store, model, response, meta):
        doc = meta["doc"]
        row = dict(role_results.get(doc, {}).get(model, {}))
        row["GROUP"] = setup.parse_pi(response)
        store.setdefault(model, {})[doc] = row
        g = row["GROUP"]
        if g["most_likely"] is None:
            utils.record_failure("jorgensen2002_b_failures.jsonl", model, response, meta)
            print(f"  FAIL W2 {model.split('/')[1]:20} | {doc:30}")
        else:
            print(f"  OK   W2 {model.split('/')[1]:20} | {doc:30} → group={g['most_likely']}h  width={g['pi_width']}")

    utils.fire_and_collect(build_wave2_tasks(), results_b, merge_wave2,
                           save_path="jorgensen2002_b_partial.json")
    utils.save("jorgensen2002_study_b_results.json", results_b)
    return results_b
