import glob
import os

import utils

DEVS = {
    "Developer A": "a senior developer who tends toward optimistic estimates and focuses on the core implementation path",
    "Developer B": "a project manager who has seen many projects overrun and accounts carefully for integration, testing, and unexpected delays",
    "Developer C": "a junior developer who is less familiar with the codebase and tends to be uncertain about edge cases",
    "Developer D": "a QA engineer who focuses on testing, validation, and the effort required to reach production quality",
}


def make_release_pairs():
    pairs, groups = [], {}
    for p in sorted(glob.glob(f"{utils.DOC_ROOT}user stories/*.md")):
        prefix = os.path.basename(p).rsplit(" ", 1)[0]
        groups.setdefault(prefix, []).append(os.path.splitext(os.path.basename(p))[0])
    for prefix, names in groups.items():
        if len(names) < 2:
            continue
        times = [(n, sum(utils.load_completion_times(n) or [])) for n in names]
        times = [(n, t) for n, t in times if t > 0]
        times.sort(key=lambda x: x[1])
        if len(times) < 2:
            continue
        pairs.append((times[0][0], times[-1][0]))
    return pairs


RELEASE_PAIRS = make_release_pairs()


def parse_stories(doc_text):
    stories, current = [], []
    for line in doc_text.splitlines():
        if line.strip().startswith("---") and current:
            stories.append("\n".join(current).strip())
            current = []
        else:
            current.append(line)
    if current:
        stories.append("\n".join(current).strip())
    return [s for s in stories if s]


# Pre-load all story texts
story_index = {}   # {release_name: [story_text, ...]}
for easy_name, hard_name in RELEASE_PAIRS:
    for release_name in [easy_name, hard_name]:
        if release_name not in story_index:
            _, doc_text = utils.load("user stories", release_name)[0]
            story_index[release_name] = parse_stories(doc_text)
