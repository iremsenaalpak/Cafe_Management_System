import re

def _to_ai_category(db_category: str) -> str:
    # DB categories: "Coffee", "Tea", "Cold Drinks", "Desserts"
    c = (db_category or "").strip().lower()
    if c == "coffee":
        return "coffee"
    if c == "tea":
        return "tea"
    if c in ["cold drinks", "cold", "cold drink"]:
        return "cold"
    if c in ["desserts", "dessert", "sweet"]:
        return "sweet"
    return "sweet"

def _norm(s: str) -> str:
    return (s or "").strip().lower()

def _tokenize_text_fields(p: dict) -> set[str]:
    """
    Build a token set from:
    - labels (primary)
    - product name + description (fallback)
    This helps filtering even when labels are missing.
    """
    tokens = set()

    # labels
    for x in (p.get("labels") or []):
        tokens.add(_norm(str(x)))

    name = _norm(p.get("name", ""))
    desc = _norm(p.get("description", ""))

    full = f"{name} {desc}".strip()
    if full:
        # word tokens (simple)
        for w in re.findall(r"[a-z0-9]+", full):
            tokens.add(w)
        # keep full text too for phrase checks
        tokens.add(full)

    return tokens

def _has_phrase(tokens: set[str], phrase: str) -> bool:
    """
    True if phrase exists in tokens.
    - single word: direct match
    - multi-word: all words present
    """
    phrase = _norm(phrase)
    if not phrase:
        return False

    if phrase in tokens:
        return True

    parts = phrase.split()
    if len(parts) == 1:
        return parts[0] in tokens

    return all(p in tokens for p in parts)

def get_recommendation(intent: dict, products: list[dict]):
    results = {"coffee": [], "tea": [], "cold": [], "sweet": []}
    selected_categories = intent.get("categories") or ["coffee", "tea", "cold", "sweet"]

    # Exclude/include label lists
    excl = set(_norm(x) for x in intent.get("exclude_labels", []) if str(x).strip())
    incl = set(_norm(x) for x in intent.get("include_labels", []) if str(x).strip())

    for p in products:
        ai_cat = _to_ai_category(p.get("category"))
        if ai_cat not in selected_categories:
            continue

        tokens = _tokenize_text_fields(p)

        # Exclude: if any excluded term matches labels OR appears in name/description tokens
        if excl:
            blocked = False
            for bad in excl:
                if bad in tokens or _has_phrase(tokens, bad):
                    blocked = True
                    break
            if blocked:
                continue

        # Include: if include list exists, require at least one match (OR logic)
        if incl:
            ok = False
            for good in incl:
                if good in tokens or _has_phrase(tokens, good):
                    ok = True
                    break
            if not ok:
                continue

        # Diet flags via tokens (labels preferred, fallback also works)
        if intent.get("vegan") and not _has_phrase(tokens, "vegan"):
            continue
        if intent.get("low_calorie") and not _has_phrase(tokens, "low calorie"):
            continue
        if intent.get("sugar_free") and not _has_phrase(tokens, "sugar free"):
            continue

        results[ai_cat].append(p)

    return results


