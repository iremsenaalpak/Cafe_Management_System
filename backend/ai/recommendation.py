from ai.menu import MENU

def get_recommendation(intent: dict):
    results = {"coffee": [], "tea": [], "cold": [], "sweet": []}
    selected_categories = intent.get("categories") or ["coffee", "tea", "cold", "sweet"]

    for category in selected_categories:
        items = MENU.get(category, {})
        for item_name, props in items.items():
            ingredients = props.get("ingredients", [])
            ok = True

            # Exclude (allergy / -siz / no X)
            for bad in intent.get("exclude_ingredients", []):
                if bad in ingredients:
                    ok = False
                    break

            # Include (with X / -li)
            include_list = intent.get("include_ingredients", [])
            if ok and include_list:
                for good in include_list:
                    if good not in ingredients:
                        ok = False
                        break

            # Diet flags
            if ok and intent.get("vegan", False) and not props.get("vegan", False):
                ok = False
            if ok and intent.get("low_calorie", False) and not props.get("low_calorie", False):
                ok = False
            if ok and intent.get("sugar_free", False):
                has_sugar_flag = not props.get("sugar_free", False)
                has_sugar_ingredient = "sugar" in ingredients
                if has_sugar_flag or has_sugar_ingredient:
                    ok = False

            if ok:
                results[category].append(item_name)

    return results
