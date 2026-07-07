import re

import utils

DOCUMENTS = utils.load("project brief")


def build_tasks(conditions):
    """Return a list of (model, prompt, metadata) tasks ready for fire_and_collect."""
    tasks = []
    for doc_name, doc_text in DOCUMENTS:
        for condition, anchor_sentence in conditions.items():
            prompt = f"""
You are a software developer asked to estimate the effort required to complete the
project below. Assume you will carry out the development work yourself, using the
programming language, tools, and database you know best.
{anchor_sentence}

```requirements
{doc_text}
```

End your response with exactly:
MOST_LIKELY: <number> work-hours
MINIMUM: <number> work-hours
MAXIMUM: <number> work-hours
"""
            for model in utils.MODELS:
                tasks.append((model, prompt, {"doc": doc_name, "condition": condition}))
    return tasks


def merge(store, model, response, meta):
    doc, condition = meta["doc"], meta["condition"]
    ml = re.search(r"MOST_LIKELY:\s*(\d+)", response or "")
    mn = re.search(r"MINIMUM:\s*(\d+)",     response or "")
    mx = re.search(r"MAXIMUM:\s*(\d+)",     response or "")
    ml, mn, mx = (int(m.group(1)) if m else None for m in (ml, mn, mx))
    store.setdefault(model, {}).setdefault(doc, {})[condition] = {
        "most_likely": ml, "minimum": mn, "maximum": mx,
        "pi_width": round((mx - mn) / ml, 3) if (ml and mn and mx and ml > 0) else None,
    }
    print(f"  {model.split('/')[1]:20} | {doc:30} | {condition}")
