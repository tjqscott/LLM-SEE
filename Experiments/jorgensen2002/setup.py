import re

import utils

LONG_DOC  = utils.load("full specification")
BRIEF_DOC = utils.load("project brief")

ROLES = {
    "EM":  "Engagement Manager — client relations; limited technical background",
    "PM":  "Project Manager — technical background; planning and delivery",
    "UD":  "User Interaction Designer — UX focus; not a core programmer",
    "DEV": "Software Developer — implementation",
}


def parse_pi(response):
    # Use extract_numbers to handle h/d suffixes and < separators
    def _get(label):
        m = re.search(rf"{label}:\s*([^\n]+)", response or "")
        if not m:
            return None
        nums = utils.extract_numbers(m.group(1))
        return int(nums[0]) if nums else None
    ml, mn, mx = _get("MOST_LIKELY"), _get("MINIMUM"), _get("MAXIMUM")
    return {"most_likely": ml, "minimum": mn, "maximum": mx,
            "pi_width": round((mx - mn) / ml, 3) if (ml and mn and mx and ml > 0) else None}
