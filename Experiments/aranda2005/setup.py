import json

import utils

ARANDA_PATH = "requirements documents/Aranda2005/Recreation MD files/"

instructions  = open(ARANDA_PATH + "instructions.md",  encoding="utf-8").read()
questionnaire = open(ARANDA_PATH + "questionnaire.md", encoding="utf-8").read()

conditions = {
    "control": open(ARANDA_PATH + "control.md", encoding="utf-8").read(),
    "low":     open(ARANDA_PATH + "low.md",     encoding="utf-8").read(),
    "high":    open(ARANDA_PATH + "high.md",    encoding="utf-8").read(),
}

TAWOS_DOCS    = utils.load("full specification")
TAWOS_ANCHORS = {k: v for k, v in json.load(open("results/pilot_anchors.json"))["anchors"].items()
                 if k != "aranda_original"}
