"""Helpers for building Irish vocabulary and expression suggestions."""

import re

TERM_ENTRIES = {
    "an": "the",
    "baile": "town, home place",
    "béal": "mouth, river mouth",
    "bearna": "gap, pass",
    "bóthar": "road",
    "bun": "bottom, mouth of a river",
    "charraig": "rock",
    "cill": "church",
    "clár": "plain, board",
    "cluain": "meadow, pasture",
    "cnoc": "hill",
    "doire": "oak grove",
    "droichead": "bridge",
    "dumha": "mound, ridge",
    "dún": "fort",
    "feirste": "sandbank, estuary",
    "gaeltacht": "Irish-speaking region",
    "gaorthaidh": "rough field or enclosed green place",
    "gleann": "glen, valley",
    "inis": "island",
    "iúir": "yew",
    "leaca": "hillside, slope",
    "loch": "lake",
    "maigh": "plain",
    "mór": "big, great",
    "na": "of the",
    "nua": "new",
    "rann": "division, headland, section",
    "sean": "old",
    "sliabh": "mountain",
    "sráid": "street",
    "teach": "house",
    "tír": "land, country",
    "thuama": "burial mound, tomb",
}

TERM_ALIASES = {
    "mhic": "mac, son of",
    "mic": "mac, son of",
    "uí": "descendant of",
}

USEFUL_EXPRESSIONS = [
    ("Dia dhuit", "Hello"),
    ("Conas atá tú?", "How are you?"),
    ("Go raibh maith agat", "Thank you"),
    ("Slán", "Goodbye"),
    ("Le do thoil", "Please"),
    ("An bhfuil Gaeilge agat?", "Do you speak Irish?"),
]

TOKEN_PATTERN = re.compile(r"[A-Za-zÁÉÍÓÚáéíóú']+")


def normalize_word(text):
    return text.strip().lower()


def tokenize_irish(text):
    """Split Irish place names into normalized word tokens."""
    if not text:
        return []
    return [normalize_word(token) for token in TOKEN_PATTERN.findall(text)]


def build_term_list_from_town_names(town_names):
    """Build ordered Irish vocabulary entries from nearby town names."""
    terms = []
    seen = set()

    for name in town_names:
        for token in tokenize_irish(name):
            if token in TERM_ENTRIES and token not in seen:
                terms.append((token, TERM_ENTRIES[token]))
                seen.add(token)
            elif token in TERM_ALIASES and token not in seen:
                terms.append((token, TERM_ALIASES[token]))
                seen.add(token)

    if not terms:
        terms = [
            ("gaeltacht", TERM_ENTRIES["gaeltacht"]),
            ("baile", TERM_ENTRIES["baile"]),
        ]

    return terms[:8]


def select_useful_expressions():
    """Return a short set of beginner-friendly Irish expressions."""
    return USEFUL_EXPRESSIONS[:4]


def generate_glossary(nearest_towns):
    """Generate a small Irish learning pack from nearby towns."""
    town_names = [town["name"] for town in nearest_towns]
    return {
        "terms": build_term_list_from_town_names(town_names),
        "expressions": select_useful_expressions(),
    }
