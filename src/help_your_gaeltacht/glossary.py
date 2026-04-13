IRISH_GLOSSARY = {
    "gaeltacht": "Irish-speaking region",
    "baile": "town, village",
    "móra": "big",
    "nua": "new",
    "sean": "old",
    "tír": "land",
    "cluain": "meadow",
    "dún": "fort",
    "loch": "lake",
    "cnoc": "hill",
    "sráid": "street",
    "eaglais": "church",
    "siopa": "shop",
    "ionad": "centre",
    "club": "club",
}


def normalize_word(text):
    return text.strip().lower()


def extract_terms_from_text(text):
    if not text:
        return []
    words = [normalize_word(word) for word in text.replace("-", " ").split()]
    return [word for word in words if word in IRISH_GLOSSARY]


def build_glossary_from_town_names(town_names):
    terms = {}
    for name in town_names:
        for term in extract_terms_from_text(name):
            terms[term] = IRISH_GLOSSARY[term]
    return terms


def generate_glossary(nearest_towns):
    town_names = [town["name"] for town in nearest_towns]
    glossary = build_glossary_from_town_names(town_names)
    if not glossary:
        glossary = {
            "gaeltacht": IRISH_GLOSSARY["gaeltacht"],
            "baile": IRISH_GLOSSARY["baile"],
        }
    return glossary
