import re


FILLERS = [
    "um",
    "uh",
    "like",
    "you know",
    "actually",
    "basically",
    "so"
]


def detect_fillers(text):

    text = text.lower()

    filler_count = 0

    filler_words = {}

    for filler in FILLERS:

        matches = re.findall(rf"\b{re.escape(filler)}\b", text)

        if matches:

            filler_words[filler] = len(matches)

            filler_count += len(matches)

    return filler_count, filler_words