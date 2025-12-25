import re

# Turkish character map for ASCII-normalization
TR_MAP = str.maketrans({"ç": "c", "ğ": "g", "ı": "i", "ö": "o", "ş": "s", "ü": "u"})

def _norm(s: str) -> str:
    """Lowercase + strip (safe for None)."""
    return (s or "").lower().strip()

def _ascii_tr(s: str) -> str:
    """Convert Turkish characters to ASCII equivalents after normalization."""
    return _norm(s).translate(TR_MAP)

def _dedupe_keep_order(xs: list[str]) -> list[str]:
    """Remove duplicates while preserving the original order."""
    seen = set()
    out = []
    for x in xs:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out

def _has_allergy_words(t: str) -> bool:
    """
    Detect allergy/avoidance intent words.
    Note: Some requests (milk-free, lactose-free, gluten-free) are handled as hard constraints.
    """
    return any(w in t for w in [
        "allergy", "allergic", "intolerance",
        "alerji", "alerjim", "alerjik",
        "yemem", "istemem", "yasak",
        "dokunuyor", "rahatsiz ediyor", "rahatsız ediyor",
    ])

def _has_root_word(atext: str, root: str) -> bool:
    """
    Check if ASCII text contains a root word with possible suffixes.
    Examples: tarcinli, elmali, cileksiz, glutensiz, etc.
    """
    return bool(re.search(rf"\b{re.escape(root)}[a-z]*\b", atext))

# -----------------------
# Label groups (should match Admin panel labels)
# -----------------------
FRUIT_LABELS = [
    "apple", "banana", "blueberry", "raspberry", "strawberry",
    "pineapple", "watermelon", "kiwi", "orange", "lemon"
]

NUT_LABELS = ["nuts", "almond", "peanut"]
DIET_LABELS = ["vegan", "low calorie", "sugar free"]
SPICE_LABELS = ["cinnamon"]

# Turkish -> English mapping for fruit words (used for allergy detection)
# Note: atext is already ASCII, so "çilek" becomes "cilek".
FRUIT_TR_MAP = {
    "elma": "apple",
    "cilek": "strawberry",
    "muz": "banana",
    "limon": "lemon",
    "portakal": "orange",
    "kivi": "kiwi",
    "ananas": "pineapple",
    "karpuz": "watermelon",
}

def analyze_text(user_input: str) -> dict:
    text = _norm(user_input)
    atext = _ascii_tr(user_input)

    intent = {
        "categories": [],
        "exclude_labels": [],
        "include_labels": [],
        "vegan": False,
        "low_calorie": False,
        "sugar_free": False,
        "drink_only": False,
        "food_only": False,
    }

    # Detect whether the user explicitly wants drinks vs food
    wants_drink = bool(
        re.search(r"\b(drink|beverage|iced|ice|icecek|iccek|içecek)\b", text)
        or re.search(r"\b(drink|beverage|iced|ice|icecek|iccek)\b", atext)
    )

    wants_food = bool(
        re.search(r"\b(food|snack|dessert|sweet|yiyecek|yemek|tatli|tatlı)\b", text)
        or re.search(r"\b(food|snack|dessert|sweet|yiyecek|yemek|tatli|tatlı)\b", atext)
    )

    # Explicit dessert keywords
    explicit_dessert = bool(
        re.search(
            r"\b(dessert|sweet|tatli|tatlı|cake|cookie|brownie|cheesecake|tiramisu|pudding|puding|parfait|protein\s*bar)\b",
            text,
        )
        or re.search(
            r"\b(dessert|sweet|tatli|cake|cookie|brownie|cheesecake|tiramisu|pudding|puding|parfait|protein\s*bar)\b",
            atext,
        )
    )

    # Category detection
    if re.search(r"\b(coffee|kahve|espresso|americano|latte|cappuccino|mocha|affogato|turkish\s*coffee)\b", text) or \
       re.search(r"\b(coffee|kahve|espresso|americano|latte|cappuccino|mocha|affogato|turkish\s*coffee)\b", atext):
        intent["categories"].append("coffee")

    if re.search(r"\b(tea|cay|çay|matcha)\b", text) or re.search(r"\b(tea|cay|matcha)\b", atext):
        intent["categories"].append("tea")

    if re.search(r"\b(cold|iced|ice|buzlu|soguk|soğuk|lemonade|limonata|detox|milkshake|hibiscus|juice)\b", text) or \
       re.search(r"\b(cold|iced|ice|buzlu|soguk|lemonade|limonata|detox|milkshake|hibiscus|juice)\b", atext):
        intent["categories"].append("cold")

    if explicit_dessert:
        intent["categories"].append("sweet")

    # If user wants drinks and didn't explicitly ask for dessert, drop sweets
    if wants_drink and not explicit_dessert:
        intent["categories"] = [c for c in intent["categories"] if c != "sweet"]

    # If user wants drinks but no category matched, default to all drink categories
    if wants_drink and len(intent["categories"]) == 0:
        intent["categories"] = ["coffee", "tea", "cold"]
        intent["drink_only"] = True

    # If user wants food only and no category matched, default to sweets
    if wants_food and not wants_drink and len(intent["categories"]) == 0:
        intent["categories"] = ["sweet"]
        intent["food_only"] = True

    # If nothing matched, default to all categories
    if len(intent["categories"]) == 0:
        intent["categories"] = ["coffee", "tea", "cold", "sweet"]

    intent["categories"] = _dedupe_keep_order(intent["categories"])

    # Diet flags
    if any(k in text for k in ["diet", "diyet", "diyetteyim", "diyetlik", "fit", "healthy", "light", "kalori"]) or \
       any(k in atext for k in ["diet", "diyet", "diyetteyim", "diyetlik", "fit", "healthy", "light", "kalori"]):
        intent["low_calorie"] = True

    if any(k in text for k in ["sugar-free", "no sugar", "şekersiz", "sekersiz"]) or \
       any(k in atext for k in ["sugar-free", "no sugar", "sekersiz"]):
        intent["sugar_free"] = True

    if "vegan" in text or "plant-based" in text or "vegan" in atext or "plant-based" in atext:
        intent["vegan"] = True

    # ----------------------------------------
    # HARD CONSTRAINTS (no need for allergy keywords)
    # ----------------------------------------

    # Milk-free constraints
    if (
        "no milk" in text
        or "milk free" in text
        or _has_root_word(atext, "sutsuz")   # sütsüz
        or _has_root_word(atext, "sut")      # süt (e.g., "süt istemiyorum")
    ):
        intent["exclude_labels"].append("milk")

    # Lactose-free constraints
    if (
        "lactose free" in text
        or _has_root_word(atext, "laktoz")   # laktoz / laktozsuz
    ):
        intent["exclude_labels"].append("lactose")

    # Gluten-free constraints: hard constraint (no need for allergy keywords)
    gluten_request = ("gluten" in text) or ("gluten" in atext)

    gluten_free_phrases = [
        "gluten free",
        "glutensiz",
        "gluten icermeyen",
        "gluten içermeyen",
        "gluten olmasin",
        "gluten olmasın",
        "gluten istemiyorum",
        "gluten yemem",
        "without gluten",
        "no gluten",
    ]

    # Detect common "free of" patterns in Turkish too
    gluten_free_pattern_tr = (
        _has_root_word(atext, "icermeyen")   # içermeyen -> icermeyen
        or _has_root_word(atext, "olmasin")  # olmasın -> olmasin
        or _has_root_word(atext, "yok")      # yok
        or _has_root_word(atext, "siz")      # -siz / -sız (glutensiz)
    )

    # Check both normalized text and ASCII text
    if gluten_request and (
        any(p in text for p in gluten_free_phrases) or
        any(p in atext for p in gluten_free_phrases) or
        gluten_free_pattern_tr
    ):
        intent["exclude_labels"].append("gluten")

    # ----------------------------------------
    # Allergy / avoidance intent (general)
    # ----------------------------------------
    allergy_context = text + " " + atext
    allergy_on = _has_allergy_words(allergy_context)

    # Group-level allergies
    if allergy_on:
        if "meyve" in atext or "fruit" in text:
            intent["exclude_labels"].extend(FRUIT_LABELS)

        if "kuruyemis" in atext or "nuts" in text or "nut" in text:
            intent["exclude_labels"].extend(NUT_LABELS)

    # English fruit terms (exclude only if allergy intent is on)
    for f in FRUIT_LABELS:
        if _has_root_word(atext, f) or re.search(rf"\b{re.escape(f)}\b", text):
            if allergy_on:
                intent["exclude_labels"].append(f)

    # Turkish fruit roots -> mapped English labels (exclude only if allergy intent is on)
    for tr_root, en_label in FRUIT_TR_MAP.items():
        if _has_root_word(atext, _ascii_tr(tr_root)):
            if allergy_on:
                intent["exclude_labels"].append(en_label)

    # Nuts (exclude only if allergy intent is on)
    for n in NUT_LABELS:
        if _has_root_word(atext, n) or re.search(rf"\b{re.escape(n)}\b", text):
            if allergy_on:
                intent["exclude_labels"].append(n)

    # Spices: cinnamon / tarçın (requires allergy intent words)
    if (_has_root_word(atext, "tarcin") or re.search(r"\b(cinnamon)\b", text)) and allergy_on:
        intent["exclude_labels"].append("cinnamon")

    # Include labels via simple English "with ..." pattern
    if "with" in text:
        for f in FRUIT_LABELS + NUT_LABELS + SPICE_LABELS:
            if re.search(rf"\bwith\s+{re.escape(f)}\b", text):
                intent["include_labels"].append(f)

    intent["exclude_labels"] = _dedupe_keep_order(intent["exclude_labels"])
    intent["include_labels"] = _dedupe_keep_order(intent["include_labels"])
    return intent


