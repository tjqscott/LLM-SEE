import re, json, glob, os, asyncio
from concurrent.futures import ThreadPoolExecutor
from openrouter import OpenRouter

MODELS = [
    "google/gemini-3-flash-preview",
    "anthropic/claude-opus-4.6",
    "openai/gpt-5.2-codex",
    "deepseek/deepseek-v3.2",
    "moonshotai/kimi-k2.5",
]

PRICES = {
    "google/gemini-3-flash-preview": (0.50,  3.00),
    "anthropic/claude-opus-4.6":     (5.00, 25.00),
    "openai/gpt-5.2-codex":          (1.75, 14.00),
    "deepseek/deepseek-v3.2":        (0.28,  0.42),
    "moonshotai/kimi-k2.5":          (0.40,  2.20),
}

MAX_TOKENS = {
    "anthropic/claude-opus-4.6": 6000,
    "deepseek/deepseek-v3.2":    8000,
    "moonshotai/kimi-k2.5":      10000,
}
DEFAULT_MAX_TOKENS = 2000

DOC_ROOT = "requirements documents/"
os.makedirs("results", exist_ok=True)

# OpenRouter's SDK is synchronous. We offload each call to a thread so the
# event loop stays free and all requests genuinely run in parallel.
_semaphore      = asyncio.Semaphore(100)
_thread_pool    = ThreadPoolExecutor(max_workers=100)
_api_key        = os.getenv("open-router")
REQUEST_TIMEOUT = 300   


def _blocking_call(model, prompt):
    """Pure synchronous HTTP call — safe to run in a thread."""
    client = OpenRouter(api_key=_api_key)
    return client.chat.send(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=MAX_TOKENS.get(model, DEFAULT_MAX_TOKENS),
        temperature=0,
    )


# ── Core async primitive ──────────────────────────────────────────────────────

async def _query_async(model, prompt, metadata=None):
    """
    Offload the blocking HTTP call to a thread; cancel it after REQUEST_TIMEOUT.
    Returns (model, content_or_None, metadata).
    Timed-out tasks return the sentinel string "TIMEOUT" so merge functions
    can record them distinctly from genuine None/parse failures.
    """
    async with _semaphore:
        loop = asyncio.get_event_loop()
        try:
            response = await asyncio.wait_for(
                loop.run_in_executor(_thread_pool, _blocking_call, model, prompt),
                timeout=REQUEST_TIMEOUT,
            )
            choice  = response.choices[0]
            content = choice.message.content or choice.message.reasoning or ""
            if choice.finish_reason == "length":
                print(f"  WARNING: {model} hit token limit")
                return model, None, metadata
            return model, content, metadata
        except asyncio.TimeoutError:
            short = model.split("/")[1]
            print(f"  TIMEOUT ({REQUEST_TIMEOUT}s): {short}")
            return model, "TIMEOUT", metadata
        except Exception as e:
            print(f"  ERROR {model}: {e}")
            return model, None, metadata


# ── Jupyter-safe event-loop runner ───────────────────────────────────────────

def _run(coro):
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import nest_asyncio
            nest_asyncio.apply()
            return loop.run_until_complete(coro)
        return loop.run_until_complete(coro)
    except RuntimeError:
        return asyncio.run(coro)


# ── Public API ────────────────────────────────────────────────────────────────

def query(model, prompt):
    """Blocking single query. Returns response string, 'TIMEOUT', or None."""
    _, content, _ = _run(_query_async(model, prompt))
    return content


def query_parallel(model_prompt_map):
    """
    Fire {model: prompt} concurrently. Returns {model: response_or_None}.
    """
    async def _all():
        tasks   = [_query_async(m, p) for m, p in model_prompt_map.items()]
        results = await asyncio.gather(*tasks)
        return {model: content for model, content, _ in results}
    return _run(_all())


def fire_and_collect(tasks, result_store, merge_fn, save_path=None, save_every=10):
    """
    The full streaming paralleliser. Fire every task simultaneously;
    handle results the instant they arrive; checkpoint to disk regularly.

    Parameters
    ----------
    tasks        : list of (model, prompt, metadata)
    result_store : dict — mutated in-place by merge_fn
    merge_fn     : callable(result_store, model, response, metadata) -> None
                   response is a string, "TIMEOUT", or None
    save_path    : str or None — checkpoint filename inside results/
    save_every   : int — checkpoint after every N completions
    """
    async def _stream():
        total      = len(tasks)
        done       = 0
        coroutines = [_query_async(m, p, meta) for m, p, meta in tasks]
        for finished in asyncio.as_completed(coroutines):
            model, response, meta = await finished
            merge_fn(result_store, model, response, meta)
            done += 1
            if save_path and done % save_every == 0:
                _checkpoint(save_path, result_store)
                print(f"  [{done}/{total}] checkpoint -> results/{save_path}")
        if save_path:
            _checkpoint(save_path, result_store)
    _run(_stream())


# ── File helpers ──────────────────────────────────────────────────────────────

def load(folder, name=None):
    """Return [(doc_name, text), ...] for all .md files in DOC_ROOT/folder/."""
    pattern = (f"{DOC_ROOT}{folder}/{name}.md" if name
               else f"{DOC_ROOT}{folder}/*.md")
    return [(os.path.splitext(os.path.basename(p))[0],
             open(p, encoding="utf-8").read())
            for p in sorted(glob.glob(pattern))]


def load_completion_times(name):
    """Return list of floats from DOC_ROOT/completion times/<n>.md, or None."""
    path = f"{DOC_ROOT}completion times/{name}.md"
    if not os.path.exists(path):
        return None
    return [float(x) for x in open(path, encoding="utf-8-sig").read().splitlines()
            if x.strip()]


def save(filename, data):
    path = f"results/{filename}"
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Saved -> {path}")


def _checkpoint(filename, data):
    path = f"results/{filename}"
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


# ── Failure recording ─────────────────────────────────────────────────────────

def record_failure(filename, model, response, metadata):
    """
    Append a failed response to a JSONL file in results/.
    One JSON object per line — safe to append mid-run without loading the file.
    Call this inside merge functions when parsing yields no usable value.

    Parameters
    ----------
    filename : str  — e.g. "haugen2006_failures.jsonl"
    model    : str  — model string as returned by fire_and_collect
    response : str or None — raw response text, "TIMEOUT", or None
    metadata : dict — the task metadata dict passed through fire_and_collect
    """
    path   = f"results/{filename}"
    record = {"model": model, "response": response, **metadata}
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


# ── Unit-stripping number extraction ─────────────────────────────────────────

def extract_numbers(text):
    """
    Extract all numeric values from a string, handling common model formatting:
      - unit suffixes:  42h  30d  -> 42  30
      - less-than format: <15 <20  -> 15  20
      - plain floats and integers
    Returns a list of floats. Version strings (1.2.3) are excluded.
    """
    cleaned = re.sub(r"(\d+\.?\d*)\s*[hd]\b", r"\1", text)
    cleaned = re.sub(r"<\s*(\d+\.?\d*)", r"\1", cleaned)
    return [float(x) for x in re.findall(r"\b\d+(?:\.\d+)?\b(?!\.\d)", cleaned)]
