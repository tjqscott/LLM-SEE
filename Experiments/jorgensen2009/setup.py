import re

import utils

BRIEF_DOCS = utils.load("project brief")
STORY_DOCS = utils.load("user stories")


def build_tasks(less_instruction, more_instruction, documents, framing="",
                success_question="the probability of project success (defined as: "
                                 "less than 25% estimation error and a client satisfied "
                                 "with quality and usability)"):
    tasks = []
    for condition, risk_instruction in [("LESS", less_instruction), ("MORE", more_instruction)]:
        for doc_name, doc_text in documents:
            prompt = f"""
You are a software developer asked to estimate the effort required to develop the system below.
{framing}
Note: this risk analysis is input to your effort estimate only — it is not the only risk
management activity that will take place on this project.

As a first step, {risk_instruction}

Then estimate the most likely effort required to develop and test the system, and assess
{success_question}.

```requirements
{doc_text}
```

End your response with exactly:
RISKS: <comma-separated list>
EFFORT: <number> work-hours
SUCCESS: <number>%
"""
            for model in utils.MODELS:
                tasks.append((model, prompt,
                              {"condition": condition, "doc": doc_name}))
    return tasks


def merge(store, model, response, meta):
    condition, doc = meta["condition"], meta["doc"]
    effort  = re.search(r"EFFORT:\s*(\d+)",  response or "")
    success = re.search(r"SUCCESS:\s*(\d+)", response or "")
    risks   = re.search(r"RISKS:\s*(.+)",    response or "")
    # Fallback: try extract_numbers if direct parse fails
    if not effort:
        eline = next((l for l in (response or "").splitlines() if "EFFORT" in l), "")
        nums = utils.extract_numbers(eline)
        effort_val = int(nums[0]) if nums else None
    else:
        effort_val = int(effort.group(1))
    row = {
        "effort":    effort_val,
        "success":   int(success.group(1))          if success else None,
        "num_risks": len(risks.group(1).split(",")) if risks   else None,
    }
    store.setdefault(condition, {}).setdefault(model, {})[doc] = row
    if row["effort"] is None:
        utils.record_failure("jorgensen2009_failures.jsonl", model, response, meta)
        print(f"  FAIL {condition} | {model.split('/')[1]:20} | {doc}")
    else:
        print(f"  OK   {condition} | {model.split('/')[1]:20} | {doc} | effort={row['effort']}")
