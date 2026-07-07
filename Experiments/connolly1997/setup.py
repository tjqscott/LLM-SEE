import glob
import os
import re

import utils


def make_task_pairs():
    pairs, groups = [], {}
    for p in sorted(glob.glob(f"{utils.DOC_ROOT}user stories/*.md")):
        prefix = os.path.basename(p).rsplit(" ", 1)[0]
        groups.setdefault(prefix, []).append(os.path.splitext(os.path.basename(p))[0])
    for prefix, names in groups.items():
        times = [(n, sum(utils.load_completion_times(n) or [])) for n in names]
        times = [(n, t) for n, t in times if t > 0]
        times.sort(key=lambda x: x[1])
        if len(times) < 2:
            continue
        for i in range(len(times) - 1):
            pairs.append((times[i][0], times[i + 1][0]))
    return pairs


TASK_PAIRS = make_task_pairs()


def make_prompt(preamble, order_instruction, doc_text, feedback=""):
    subtasks = [l.strip("- *").strip() for l in doc_text.splitlines()
                if l.strip().startswith(("-", "*")) and l.strip("- *").strip()]
    subtask_list = "\n".join(f"  {i+1}. {s}" for i, s in enumerate(subtasks))
    return f"""
{preamble}
{feedback}
{order_instruction}

The subtasks for this project are:
{subtask_list}

```requirements
{doc_text}
```

End your response with exactly:
WHOLE: <p01> <p25> <p50> <p75> <p99>
SUBTASKS: <p50 for subtask 1>, <p50 for subtask 2>, ...
"""


def parse_estimate(response, doc_text):
    subtasks = [l.strip("- *").strip() for l in doc_text.splitlines()
                if l.strip().startswith(("-", "*")) and l.strip("- *").strip()]
    whole = re.search(r"WHOLE:\s*([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)", response or "")
    subs  = re.search(r"SUBTASKS:\s*(.+)", response or "")
    w     = [float(x) for x in whole.groups()] if whole else [None] * 5
    raw_parts = re.findall(r"\b\d+(?:\.\d+)?\b(?!\.\d)", subs.group(1)) if subs else []
    parts = [float(x) for x in raw_parts][:len(subtasks)]
    return {
        "whole_fractiles": {"p01": w[0], "p25": w[1], "p50": w[2], "p75": w[3], "p99": w[4]},
        "whole_p50": w[2],
        "subtask_sum": round(sum(parts), 1) if parts else None,
        "gap": round(sum(parts) - w[2], 1) if (w[2] and parts) else None,
        "subtask_p50s": parts,
    }


def build_feedback(a1_result, completion_times):
    if not completion_times or not a1_result.get("whole_fractiles"):
        return ""
    f = a1_result["whole_fractiles"]
    lines = ["\nFeedback from your Assignment 1 estimates:\n"]
    for i, actual in enumerate(completion_times):
        est = a1_result["subtask_p50s"][i] if i < len(a1_result["subtask_p50s"]) else None
        if est:
            lines.append(f"  Subtask {i+1}: you estimated {est}h, actual was {actual}h.")
    whole_actual = sum(completion_times)
    region = ("R1 (astonishingly short)" if whole_actual < (f["p01"] or float("inf")) else
              "R2 (surprisingly short)"  if whole_actual < (f["p25"] or float("inf")) else
              "R3 (expected low)"        if whole_actual < (f["p50"] or float("inf")) else
              "R4 (expected high)"       if whole_actual < (f["p75"] or float("inf")) else
              "R5 (surprisingly long)"   if whole_actual < (f["p99"] or float("inf")) else
              "R6 (astonishingly long)")
    lines.append(f"  Whole task: you estimated {f['p50']}h (median), actual was {whole_actual}h — fell in {region}.")
    lines.append("\nYour estimates were hugely too tight. For Assignment 2, stretch out your tails — "
                 "your p01 should be much lower and your p99 much higher than feels comfortable.\n")
    return "\n".join(lines)


def run_connolly(label, order_instruction, preamble, pairs, with_feedback=False):
    """
    Two-wave: fire all Assignment 1 prompts simultaneously across all
    models and all pairs, then fire all Assignment 2 prompts simultaneously.
    """
    # Pre-load texts
    texts = {}
    for short_name, long_name in pairs:
        if short_name not in texts:
            _, t = utils.load("user stories", short_name)[0]
            texts[short_name] = t
        if long_name not in texts:
            _, t = utils.load("user stories", long_name)[0]
            texts[long_name] = t

    # ── Wave 1: Assignment 1 (short task) ────────────────────────────────────
    a1_tasks = [
        (model,
         make_prompt(preamble, order_instruction, texts[short_name]),
         {"model": model, "short": short_name, "long": long_name})
        for short_name, long_name in pairs
        for model in utils.MODELS
    ]
    a1_raw = {}   # {short_name: {model: parsed_result}}

    def merge_a1(store, model, response, meta):
        short, long = meta["short"], meta["long"]
        store.setdefault(short, {})[model] = parse_estimate(response, texts[short])
        print(f"  A1 {model.split('/')[1]:20} | {short}")

    utils.fire_and_collect(a1_tasks, a1_raw, merge_a1)
    print(f"[{label}] Assignment 1 complete")
    for short_name, long_name in pairs:
        print(f"  {short_name}: " + "  ".join(
            f"{m.split('/')[1]}={a1_raw.get(short_name,{}).get(m,{}).get('whole_p50')}"
            for m in utils.MODELS))

    # ── Wave 2: Assignment 2 (long task, optionally with feedback) ────────────
    a2_tasks = []
    for short_name, long_name in pairs:
        times = utils.load_completion_times(short_name)
        for model in utils.MODELS:
            a1 = a1_raw.get(short_name, {}).get(model, {})
            fb = build_feedback(a1, times) if with_feedback else ""
            a2_tasks.append((model,
                             make_prompt(preamble, order_instruction, texts[long_name], feedback=fb),
                             {"model": model, "short": short_name, "long": long_name}))

    a2_raw = {}   # {long_name: {model: parsed_result}}

    def merge_a2(store, model, response, meta):
        short, long = meta["short"], meta["long"]
        store.setdefault(long, {})[model] = parse_estimate(response, texts[long])
        print(f"  A2 {model.split('/')[1]:20} | {long}")

    utils.fire_and_collect(a2_tasks, a2_raw, merge_a2)
    print(f"[{label}] Assignment 2 complete")
    for short_name, long_name in pairs:
        print(f"  {long_name}: " + "  ".join(
            f"{m.split('/')[1]}={a2_raw.get(long_name,{}).get(m,{}).get('whole_p50')}"
            for m in utils.MODELS))

    # ── Assemble ──────────────────────────────────────────────────────────────
    results = {}
    for short_name, long_name in pairs:
        pk = f"{short_name}__{long_name}"
        for model in utils.MODELS:
            results.setdefault(model, {})[pk] = {
                short_name: a1_raw.get(short_name, {}).get(model, {}),
                long_name:  a2_raw.get(long_name,  {}).get(model, {}),
            }
    return results


STUDY1_PREAMBLE_GT = """You are a software developer estimating how long the project below will take.
For each estimate, provide five values dividing the range of possible outcomes:
  p01: 1% chance the task takes less time than this
  p25: lower quartile (25% chance of taking less)
  p50: your best estimate
  p75: upper quartile (75% chance of taking less)
  p99: 1% chance the task takes more time than this"""

STUDY1_PREAMBLE_LT = """You are a software developer estimating how long the project below will take.
For each estimate, provide five values using the less-than format:
  p01: 99% chance the task takes less time than this
  p25: 75% chance the task takes less time than this
  p50: your best estimate
  p75: 25% chance the task takes less time than this
  p99: 1% chance the task takes less time than this"""

STUDY2_PREAMBLE = """You are a software developer estimating how long the project below will take.
Before estimating, first identify the absolute minimum time if everything went perfectly and the
absolute maximum time if everything went wrong. Use these extreme limits to anchor your distribution:
  p01: near your minimum limit (1% chance of being shorter)
  p25: lower quartile
  p50: your best estimate
  p75: upper quartile
  p99: near your maximum limit (1% chance of being longer)"""
