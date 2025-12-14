import re

TR_MAP = str.maketrans({"ç":"c","ğ":"g","ı":"i","ö":"o","ş":"s","ü":"u"})

def _norm(s: str) -> str:
    return (s or "").lower().strip()

def _ascii_tr(s: str) -> str:
    return _norm(s).translate(TR_MAP)

def _dedupe_keep_order(xs: list[str]) -> list[str]:
    seen = set()
    out = []
    for x in xs:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out

def _has_allergy_words(t: str) -> bool:
    return any(w in t for w in [
        "allergy","allergic","intolerance",
        "alerji","alerjim","yemem","istemem","yasak"
    ])

def _has_root_word(atext: str, root: str) -> bool:
    # limon, limona, limonlu, limonsuz...
    return bool(re.search(rf"\b{re.escape(root)}[a-z]*\b", atext))

def analyze_text(user_input: str) -> dict:
    text = _norm(user_input)
    atext = _ascii_tr(user_input)

    intent = {
        "categories": [],
        "exclude_ingredients": [],
        "include_ingredients": [],
        "vegan": False,
        "low_calorie": False,
        "sugar_free": False,
        "drink_only": False,
        "food_only": False,

        # debug flags (optional)
        "milk": False, "lactose": False, "gluten": False, "egg": False,
        "nuts": False, "peanut": False, "chocolate": False,
        "strawberry": False, "lemon": False, "sugar": False,
    }

    # -------------------------
    # drink vs food intent
    # -------------------------
    wants_drink = bool(re.search(r"\b(drink|beverage|iced|ice|icecek|iccek|içecek)\b", text) or
                       re.search(r"\b(drink|beverage|iced|ice|icecek|iccek)\b", atext))

    wants_food = bool(re.search(r"\b(food|snack|dessert|sweet|yiyecek|yemek|tatli|tatlı)\b", text) or
                      re.search(r"\b(food|snack|dessert|sweet|yiyecek|yemek|tatli)\b", atext))

    explicit_dessert = bool(re.search(
        r"\b(dessert|sweet|tatli|tatlı|cake|cookie|brownie|cheesecake|tiramisu|pudding|puding|parfait|protein\s*bar)\b",
        text
    ) or re.search(
        r"\b(dessert|sweet|tatli|cake|cookie|brownie|cheesecake|tiramisu|pudding|puding|parfait|protein\s*bar)\b",
        atext
    ))

    # -------------------------
    # CATEGORY detection
    # -------------------------
    if re.search(r"\b(coffee|kahve|espresso|americano|latte|cappuccino|mocha|affogato|cold\s*brew|coldbrew)\b", text) or \
       re.search(r"\b(coffee|kahve|espresso|americano|latte|cappuccino|mocha|affogato|cold\s*brew|coldbrew)\b", atext):
        intent["categories"].append("coffee")

    if re.search(r"\b(tea|cay|çay|matcha)\b", text) or re.search(r"\b(tea|cay|matcha)\b", atext):
        intent["categories"].append("tea")

    if re.search(r"\b(cold|iced|ice|buzlu|soguk|soğuk|lemonade|limonata|detox|milkshake|hibiscus|cold\s*brew|coldbrew)\b", text) or \
       re.search(r"\b(cold|iced|ice|buzlu|soguk|lemonade|limonata|detox|milkshake|hibiscus|cold\s*brew|coldbrew)\b", atext):
        intent["categories"].append("cold")

    if explicit_dessert:
        intent["categories"].append("sweet")

    # If user asked drink but not dessert => do not return sweet
    if wants_drink and not explicit_dessert:
        intent["categories"] = [c for c in intent["categories"] if c != "sweet"]

    if wants_drink and len(intent["categories"]) == 0:
        intent["categories"] = ["coffee", "tea", "cold"]
        intent["drink_only"] = True

    if wants_food and not wants_drink and len(intent["categories"]) == 0:
        intent["categories"] = ["sweet"]
        intent["food_only"] = True

    if len(intent["categories"]) == 0:
        intent["categories"] = ["coffee", "tea", "cold", "sweet"]

    intent["categories"] = _dedupe_keep_order(intent["categories"])

    # -------------------------
    # DIET
    # -------------------------
    if any(k in text for k in ["diet","diyet","diyetteyim","diyetlik","fit","healthy","light","kalori"]) or \
       any(k in atext for k in ["diet","diyet","diyetteyim","diyetlik","fit","healthy","light","kalori"]):
        intent["low_calorie"] = True

    if any(k in text for k in ["sugar-free","no sugar","şekersiz","sekersiz"]) or \
       any(k in atext for k in ["sugar-free","no sugar","sekersiz"]):
        intent["sugar_free"] = True
        if "sugar" not in intent["exclude_ingredients"]:
            intent["exclude_ingredients"].append("sugar")
        intent["sugar"] = True

    if "vegan" in text or "plant-based" in text or "vegan" in atext or "plant-based" in atext:
        intent["vegan"] = True
        for k in ["milk", "egg"]:
            if k not in intent["exclude_ingredients"]:
                intent["exclude_ingredients"].append(k)
            intent[k] = True

    # -------------------------
    # TR “-siz” excludes
    # -------------------------
    tr_free_map = {
        "sutsuz":"milk","sütsüz":"milk",
        "laktozsuz":"lactose",
        "glutensiz":"gluten",
        "yumurtasiz":"egg","yumurtasız":"egg",
        "findiksiz":"nuts","fındıksız":"nuts",
        "fistiksiz":"peanut","fıstıksız":"peanut",
        "cikolatasiz":"chocolate","çikolatasız":"chocolate",
        "cileksiz":"strawberry","çileksiz":"strawberry",
        "limonsuz":"lemon",
        "sekersiz":"sugar","şekersiz":"sugar",
        "kuruyemissiz":"nuts","kuruyemişsiz":"nuts",
    }
    for tr_word, key in tr_free_map.items():
        if tr_word in atext or tr_word in text:
            if key not in intent["exclude_ingredients"]:
                intent["exclude_ingredients"].append(key)
            if key in intent:
                intent[key] = True
            if key == "sugar":
                intent["sugar_free"] = True

    # -------------------------
    # Allergy sentences (ROOT matching) ✅ limona / limonlu yakalar
    # -------------------------
    if _has_allergy_words(text + " " + atext):
        if _has_root_word(atext, "limon"):
            if "lemon" not in intent["exclude_ingredients"]:
                intent["exclude_ingredients"].append("lemon")
            intent["lemon"] = True

        if _has_root_word(atext, "cilek"):
            if "strawberry" not in intent["exclude_ingredients"]:
                intent["exclude_ingredients"].append("strawberry")
            intent["strawberry"] = True

        if _has_root_word(atext, "sut"):
            if "milk" not in intent["exclude_ingredients"]:
                intent["exclude_ingredients"].append("milk")
            intent["milk"] = True

        if _has_root_word(atext, "laktoz"):
            if "lactose" not in intent["exclude_ingredients"]:
                intent["exclude_ingredients"].append("lactose")
            intent["lactose"] = True

        if _has_root_word(atext, "yumurta"):
            if "egg" not in intent["exclude_ingredients"]:
                intent["exclude_ingredients"].append("egg")
            intent["egg"] = True

        if _has_root_word(atext, "gluten"):
            if "gluten" not in intent["exclude_ingredients"]:
                intent["exclude_ingredients"].append("gluten")
            intent["gluten"] = True

        # kuruyemiş / fındık -> nuts (+peanut da ekleyelim)
        if _has_root_word(atext, "findik") or _has_root_word(atext, "kuruyemis"):
            if "nuts" not in intent["exclude_ingredients"]:
                intent["exclude_ingredients"].append("nuts")
            intent["nuts"] = True
            if "peanut" not in intent["exclude_ingredients"]:
                intent["exclude_ingredients"].append("peanut")
            intent["peanut"] = True

        if _has_root_word(atext, "fistik"):
            if "peanut" not in intent["exclude_ingredients"]:
                intent["exclude_ingredients"].append("peanut")
            intent["peanut"] = True

    # EN quick “no/without/x-free”
    en_keys = ["milk","lactose","gluten","egg","nuts","peanut","chocolate","strawberry","lemon","sugar"]
    for k in en_keys:
        if re.search(rf"\b(no|without)\s+{re.escape(k)}\b", text) or re.search(rf"\b{re.escape(k)}\s*free\b", text):
            if k not in intent["exclude_ingredients"]:
                intent["exclude_ingredients"].append(k)
            if k in intent:
                intent[k] = True
            if k == "sugar":
                intent["sugar_free"] = True

    # -------------------------
    # INCLUDE ingredient (TR -li / EN with)
    # -------------------------
    tr_include_map = {
        "limonlu": "lemon",
        "cilekli": "strawberry", "çilekli": "strawberry",
        "cikolatali": "chocolate", "çikolatalı": "chocolate",
        "sutlu": "milk", "sütlü": "milk",
        "findikli": "nuts", "fındıklı": "nuts",
        "fistikli": "peanut", "fıstıklı": "peanut",
    }
    for tr_word, key in tr_include_map.items():
        if tr_word in atext or tr_word in text:
            if key not in intent["include_ingredients"]:
                intent["include_ingredients"].append(key)

    for k in en_keys:
        if re.search(rf"\bwith\s+{re.escape(k)}\b", text):
            if k not in intent["include_ingredients"]:
                intent["include_ingredients"].append(k)

    intent["exclude_ingredients"] = _dedupe_keep_order(intent["exclude_ingredients"])
    intent["include_ingredients"] = _dedupe_keep_order(intent["include_ingredients"])

    # protect drink-only intent
    if wants_drink and not explicit_dessert:
        intent["categories"] = [c for c in intent["categories"] if c != "sweet"] or ["coffee","tea","cold"]

    return intent
