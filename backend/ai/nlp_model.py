import re

def analyze_text(user_input: str) -> dict:
    text = user_input.lower().strip()

    intent = {
        "categories": [],

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
    }

    # -----------------------------------------
    # CATEGORY DETECTION (TR + EN)
    # -----------------------------------------
    if re.search(r"\b(coffee|kahve)\b", text):
        intent["categories"].append("coffee")

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
        intent["sugar_free"] = True

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
        intent["vegan"] = True

        # vegan kullanıcı için süt / yumurta otomatik yasaklanır
        for v_ing in ["milk", "egg"]:
            if v_ing not in intent["exclude_ingredients"]:
                intent["exclude_ingredients"].append(v_ing)

    if "low calorie" in text or "low-calorie" in text or "diyet" in text:
        intent["low_calorie"] = True

    if "sugar-free" in text or "no sugar" in text:
        intent["sugar_free"] = True
        if "sugar" not in intent["exclude_ingredients"]:
            intent["exclude_ingredients"].append("sugar")

    return intent
