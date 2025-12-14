<<<<<<< HEAD
import re

def analyze_text(user_input: str) -> dict:
    text = user_input.lower().strip()
||||||| parent of 53f5bb8 (Remove duplicate READ.md, keep clean structure)
def analyze_text(user_input):
    user_input = user_input.lower()
=======
import re

TR_MAP = str.maketrans({
    "ç": "c", "ğ": "g", "ı": "i", "ö": "o", "ş": "s", "ü": "u",
})

def _norm(s: str) -> str:
    return (s or "").lower().strip()

def _ascii_tr(s: str) -> str:
    return _norm(s).translate(TR_MAP)

def _dedupe_keep_order(items: list[str]) -> list[str]:
    seen = set()
    out = []
    for x in items:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out

def _has_allergy_words(t: str) -> bool:
    return any(w in t for w in [
        "allergy", "allergic", "intolerance",
        "alerji", "alerjim", "yemem", "istemem", "yasak"
    ])

def _has_root_word(atext: str, root: str) -> bool:
    """
    Matches Turkish-root words with suffixes:
    limon, limona, limonu, limonlu, limonsuz ...
    kuruyemis, kuruyemise ...
    """
    return bool(re.search(rf"\b{re.escape(root)}[a-z]*\b", atext))

def analyze_text(user_input: str) -> dict:
    text = _norm(user_input)
    atext = _ascii_tr(user_input)
>>>>>>> 53f5bb8 (Remove duplicate READ.md, keep clean structure)

    intent = {
        "categories": [],

<<<<<<< HEAD
        # filters
        "exclude_ingredients": [],
        "include_ingredients": [],

        # diet flags
        "vegan": False,
        "low_calorie": False,
        "sugar_free": False,

        # allergy flags
        "milk": False,
        "lactose": False,
        "gluten": False,
        "egg": False,
        "nuts": False,
        "peanut": False,
        "chocolate": False,
        "strawberry": False,
||||||| parent of 53f5bb8 (Remove duplicate READ.md, keep clean structure)
        # Allergies
        "nuts_allergy": False,
        "gluten_allergy": False,
        "egg_allergy": False,
        "milk_allergy": False,
        "chocolate_allergy": False
=======
        "exclude_ingredients": [],
        "include_ingredients": [],

        "vegan": False,
        "low_calorie": False,
        "sugar_free": False,

        "drink_only": False,
        "food_only": False,

        # debug flags
        "milk": False,
        "lactose": False,
        "gluten": False,
        "egg": False,
        "nuts": False,
        "peanut": False,
        "chocolate": False,
        "strawberry": False,
        "lemon": False,
        "sugar": False,
>>>>>>> 53f5bb8 (Remove duplicate READ.md, keep clean structure)
    }

<<<<<<< HEAD
    # -----------------------------------------
    # CATEGORY DETECTION (TR + EN)
    # -----------------------------------------
    if re.search(r"\b(coffee|kahve)\b", text):
        intent["categories"].append("coffee")
||||||| parent of 53f5bb8 (Remove duplicate READ.md, keep clean structure)
    # DIET
    if "diet" in user_input or "low calorie" in user_input or "light" in user_input:
        intent["low_calorie"] = True
=======
    # -------------------------
    # drink vs food intent
    # -------------------------
    wants_drink = bool(re.search(r"\b(drink|beverage|iced|ice|icecek|iccek|içecek)\b", text) or
                       re.search(r"\b(drink|beverage|iced|ice|icecek|iccek)\b", atext))

    wants_food = bool(re.search(r"\b(food|snack|dessert|sweet|yiyecek|yemek|tatli|tatlı)\b", text) or
                      re.search(r"\b(food|snack|dessert|sweet|yiyecek|yemek|tatli)\b", atext))

    explicit_dessert = bool(re.search(r"\b(dessert|sweet|tatli|tatlı|cake|cookie|brownie|cheesecake|tiramisu|pudding|puding|parfait|protein\s*bar)\b", text) or
                            re.search(r"\b(dessert|sweet|tatli|cake|cookie|brownie|cheesecake|tiramisu|pudding|puding|parfait|protein\s*bar)\b", atext))

    # -------------------------
    # CATEGORY DETECTION
    # -------------------------
    if re.search(r"\b(coffee|kahve|espresso|americano|latte|cappuccino|mocha)\b", text) or \
       re.search(r"\b(coffee|kahve|espresso|americano|latte|cappuccino|mocha)\b", atext):
        intent["categories"].append("coffee")

    if re.search(r"\b(tea|cay|çay|matcha)\b", text) or re.search(r"\b(tea|cay|matcha)\b", atext):
        intent["categories"].append("tea")

    # cold drinks (cold brew can be treated as cold too)
    if re.search(r"\b(cold|iced|ice|buzlu|soguk|soğuk|lemonade|limonata|detox|smoothie|milkshake|hibiscus|cold\s*brew|coldbrew)\b", text) or \
       re.search(r"\b(cold|iced|ice|buzlu|soguk|lemonade|limonata|detox|smoothie|milkshake|hibiscus|cold\s*brew|coldbrew)\b", atext):
        intent["categories"].append("cold")

    if explicit_dessert:
        intent["categories"].append("sweet")

    # If user said “drink” but not dessert -> remove sweet
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
    # DIET DETECTION
    # -------------------------
    if any(k in text for k in ["diet", "diyet", "diyetteyim", "diyetlik", "fit", "healthy", "light"]) or \
       any(k in atext for k in ["diet", "diyet", "diyetteyim", "diyetlik", "fit", "healthy", "light"]):
        intent["low_calorie"] = True
>>>>>>> 53f5bb8 (Remove duplicate READ.md, keep clean structure)

<<<<<<< HEAD
    if re.search(r"\b(tea|çay|cay)\b", text):
        intent["categories"].append("tea")

    if re.search(r"\b(tatlı|tatli|sweet|dessert)\b", text):
        intent["categories"].append("sweet")

    # If none specified → default to all
    if len(intent["categories"]) == 0:
        intent["categories"] = ["coffee", "tea", "sweet"]

    # -----------------------------------------
    # GENERIC ALLERGY DETECTION (X-free / no X)
    # -----------------------------------------
    allergens = ["milk", "lactose", "gluten", "egg",
                 "nuts", "peanut", "chocolate", "strawberry", "sugar"]

    # X-free detection (EN)
    for a in allergens:
        patterns = [
            f"{a}-free",
            f"{a} free",
            f"no {a}",
        ]
        if any(p in text for p in patterns):
            if a not in intent["exclude_ingredients"]:
                intent["exclude_ingredients"].append(a)
            intent[a] = True

    # Turkish -siz (sütsüz)
    if "sütsüz" in text or "sutsuz" in text:
        intent["exclude_ingredients"].append("milk")
        intent["milk"] = True

    # şekersiz
    if "şekersiz" in text or "sekersiz" in text:
        if "sugar" not in intent["exclude_ingredients"]:
            intent["exclude_ingredients"].append("sugar")
||||||| parent of 53f5bb8 (Remove duplicate READ.md, keep clean structure)
    if "lactose-free" in user_input or "milk allergy" in user_input:
        intent["lactose_free"] = True
        intent["milk_allergy"] = True

    if "sugar-free" in user_input or "no sugar" in user_input:
=======
    if any(k in text for k in ["sugar-free", "no sugar", "şekersiz", "sekersiz"]) or \
       any(k in atext for k in ["sugar-free", "no sugar", "sekersiz"]):
>>>>>>> 53f5bb8 (Remove duplicate READ.md, keep clean structure)
        intent["sugar_free"] = True
        if "sugar" not in intent["exclude_ingredients"]:
            intent["exclude_ingredients"].append("sugar")
        intent["sugar"] = True

<<<<<<< HEAD
    # -----------------------------------------
    # TURKISH DIRECT ALLERGY EXPRESSIONS
    # -----------------------------------------
    # fıstığa alerjim var → peanut
    if ("fıstık" in text or "fistik" in text) and \
       ("alerji" in text or "alerjim" in text or "yemem" in text or "istemem" in text or "yasak" in text):

        if "peanut" not in intent["exclude_ingredients"]:
            intent["exclude_ingredients"].append("peanut")
        intent["peanut"] = True

    # fındık alerjisi → nuts
    if ("fındık" in text or "findik" in text) and \
       ("alerji" in text or "alerjim" in text or "yemem" in text or "istemem" in text or "yasak" in text):

        if "nuts" not in intent["exclude_ingredients"]:
            intent["exclude_ingredients"].append("nuts")
        intent["nuts"] = True

    # süt alerjisi
    if ("süt" in text or "sut" in text) and ("alerji" in text or "alerjim" in text):
        if "milk" not in intent["exclude_ingredients"]:
            intent["exclude_ingredients"].append("milk")
        intent["milk"] = True

    # yumurta alerjisi
    if ("yumurta" in text) and ("alerji" in text or "alerjim" in text):
        if "egg" not in intent["exclude_ingredients"]:
            intent["exclude_ingredients"].append("egg")
        intent["egg"] = True

    # -----------------------------------------
    # INGREDIENT PREFERENCE (X-based / X'li)
    # -----------------------------------------
    for a in allergens:
        patterns = [
            f"{a}-based",
            f"with {a}",
            f"{a} dessert"
        ]
        if any(p in text for p in patterns):
            if a not in intent["include_ingredients"]:
                intent["include_ingredients"].append(a)

    # Turkish içerikli (çilekli, çikolatalı)
    contains_map = {
        "sütlü": "milk",
        "sutlu": "milk",
        "çilekli": "strawberry",
        "cilekli": "strawberry",
        "fındıklı": "nuts",
        "findikli": "nuts",
        "fıstıklı": "peanut",
        "fistikli": "peanut",
        "çikolatalı": "chocolate",
        "cikolatali": "chocolate",
    }

    for turkish_word, eng in contains_map.items():
        if turkish_word in text:
            if eng not in intent["include_ingredients"]:
                intent["include_ingredients"].append(eng)

    # -----------------------------------------
    # DIET DETECTION
    # -----------------------------------------
    if "vegan" in text:
||||||| parent of 53f5bb8 (Remove duplicate READ.md, keep clean structure)
    if "vegan" in user_input:
=======
    if "vegan" in text or "plant-based" in text or "vegan" in atext or "plant-based" in atext:
>>>>>>> 53f5bb8 (Remove duplicate READ.md, keep clean structure)
        intent["vegan"] = True
        # vegan -> auto exclude milk & egg
        for v_ing in ["milk", "egg"]:
            if v_ing not in intent["exclude_ingredients"]:
                intent["exclude_ingredients"].append(v_ing)
            intent[v_ing] = True

<<<<<<< HEAD
        # vegan kullanıcı için süt / yumurta otomatik yasaklanır
        for v_ing in ["milk", "egg"]:
            if v_ing not in intent["exclude_ingredients"]:
                intent["exclude_ingredients"].append(v_ing)
||||||| parent of 53f5bb8 (Remove duplicate READ.md, keep clean structure)
    # SWEET / CHOCOLATE
    if "sweet" in user_input or "dessert" in user_input:
        intent["sweet"] = True
=======
    # -------------------------
    # TURKISH -SIZ detections
    # -------------------------
    tr_free_map = {
        "sutsuz": "milk", "sütsüz": "milk",
        "laktozsuz": "lactose",
        "glutensiz": "gluten",
        "yumurtasiz": "egg", "yumurtasız": "egg",
        "findiksiz": "nuts", "fındıksız": "nuts",
        "fistiksiz": "peanut", "fıstıksız": "peanut",
        "cikolatasiz": "chocolate", "çikolatasız": "chocolate",
        "cileksiz": "strawberry", "çileksiz": "strawberry",
        "limonsuz": "lemon",
        "sekersiz": "sugar", "şekersiz": "sugar",
    }
    for tr_word, key in tr_free_map.items():
        if tr_word in atext or tr_word in text:
            if key not in intent["exclude_ingredients"]:
                intent["exclude_ingredients"].append(key)
            if key in intent:
                intent[key] = True
            if key == "sugar":
                intent["sugar_free"] = True
>>>>>>> 53f5bb8 (Remove duplicate READ.md, keep clean structure)

<<<<<<< HEAD
    if "low calorie" in text or "low-calorie" in text or "diyet" in text:
        intent["low_calorie"] = True
||||||| parent of 53f5bb8 (Remove duplicate READ.md, keep clean structure)
    if "chocolate" in user_input:
        intent["chocolate"] = True
=======
    # -------------------------
    # ALLERGY detections (TR roots + EN)
    # -------------------------
    if _has_allergy_words(text + " " + atext):
        # TR roots with suffixes
        if _has_root_word(atext, "limon"):
            intent["exclude_ingredients"].append("lemon")
            intent["lemon"] = True
>>>>>>> 53f5bb8 (Remove duplicate READ.md, keep clean structure)

<<<<<<< HEAD
    if "sugar-free" in text or "no sugar" in text:
        intent["sugar_free"] = True
        if "sugar" not in intent["exclude_ingredients"]:
            intent["exclude_ingredients"].append("sugar")
||||||| parent of 53f5bb8 (Remove duplicate READ.md, keep clean structure)
    # DECAF
    if "decaf" in user_input or "caffeine-free" in user_input:
        intent["decaf"] = True

    # ALLERGIES
    if "nut" in user_input or "nuts" in user_input:
        intent["nuts_allergy"] = True

    if "gluten" in user_input or "gluten-free" in user_input:
        intent["gluten_allergy"] = True

    if "egg allergy" in user_input or "cannot eat egg" in user_input:
        intent["egg_allergy"] = True

    if "chocolate allergy" in user_input:
        intent["chocolate_allergy"] = True
=======
        if _has_root_word(atext, "sut") or _has_root_word(atext, "sut") or _has_root_word(atext, "sut"):
            # (ascii already "sut")
            intent["exclude_ingredients"].append("milk")
            intent["milk"] = True

        if _has_root_word(atext, "cilek"):
            intent["exclude_ingredients"].append("strawberry")
            intent["strawberry"] = True

        if _has_root_word(atext, "findik"):
            intent["exclude_ingredients"].append("nuts")
            intent["nuts"] = True
            # many people mean peanuts too
            if "peanut" not in intent["exclude_ingredients"]:
                intent["exclude_ingredients"].append("peanut")
            intent["peanut"] = True

        if _has_root_word(atext, "fistik"):
            intent["exclude_ingredients"].append("peanut")
            intent["peanut"] = True

        # “kuruyemiş” = nuts (and often peanuts)
        if _has_root_word(atext, "kuruyemis"):
            intent["exclude_ingredients"].append("nuts")
            intent["nuts"] = True
            if "peanut" not in intent["exclude_ingredients"]:
                intent["exclude_ingredients"].append("peanut")
            intent["peanut"] = True

        if _has_root_word(atext, "yumurta"):
            intent["exclude_ingredients"].append("egg")
            intent["egg"] = True

    # English "no/without/x-free" quick checks (kept simple)
    en_keys = ["milk", "lactose", "gluten", "egg", "nuts", "peanut", "chocolate", "strawberry", "lemon", "sugar"]
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
        intent["categories"] = [c for c in intent["categories"] if c != "sweet"] or ["coffee", "tea", "cold"]
>>>>>>> 53f5bb8 (Remove duplicate READ.md, keep clean structure)

    return intent



