# ai/recommendation.py

from ai.menu import MENU


def get_recommendation(intent: dict):
    # Sonuçları kategorilere göre döndürüyoruz
    results = {
        "coffee": [],
        "tea": [],
        "sweet": []
    }

    selected_categories = intent.get("categories") or ["coffee", "tea", "sweet"]

    for category in selected_categories:
        items = MENU.get(category, {})

        for item_name, props in items.items():
            ingredients = props.get("ingredients", [])

            ok = True

            # 1) X-free (exclude ingredients)
            for bad in intent.get("exclude_ingredients", []):
                if bad in ingredients:
                    ok = False
                    break

            # 2) X-based / include ingredients (tüm requested ingredient'ler içinde olmalı)
            include_list = intent.get("include_ingredients", [])
            if ok and len(include_list) > 0:
                for good in include_list:
                    if good not in ingredients:
                        ok = False
                        break

            # 3) Diet filters (vegan, low_calorie, sugar_free)
            if ok and intent.get("vegan", False) and not props.get("vegan", False):
                ok = False

            if ok and intent.get("low_calorie", False) and not props.get("low_calorie", False):
                ok = False

            if ok and intent.get("sugar_free", False):
                # Hem flag'e hem de ingredients'e bak
                has_sugar_flag = not props.get("sugar_free", False)
                has_sugar_ingredient = "sugar" in ingredients
                if has_sugar_flag or has_sugar_ingredient:
                    ok = False

            if ok:
                results.setdefault(category, []).append(item_name)

    return results
