<<<<<<< HEAD
# ai/recommendation.py
||||||| parent of 53f5bb8 (Remove duplicate READ.md, keep clean structure)
def get_recommendation(intent):
=======
from ai.menu import MENU
>>>>>>> 53f5bb8 (Remove duplicate READ.md, keep clean structure)

<<<<<<< HEAD
from ai.menu import MENU
||||||| parent of 53f5bb8 (Remove duplicate READ.md, keep clean structure)
    # -----------------------------------
    # MENU WITH ALLERGEN LABELS
    # -----------------------------------
=======
def get_recommendation(intent: dict):
    results = {"coffee": [], "tea": [], "cold": [], "sweet": []}
    selected_categories = intent.get("categories") or ["coffee", "tea", "cold", "sweet"]
>>>>>>> 53f5bb8 (Remove duplicate READ.md, keep clean structure)

<<<<<<< HEAD

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

||||||| parent of 53f5bb8 (Remove duplicate READ.md, keep clean structure)
    coffees = {
        "americano": {"low_calorie": True, "lactose_free": True, "decaf": False, "milk": False, "nuts": False},
        "latte": {"milk": True},
        "cappuccino": {"milk": True},
        "flat white": {"milk": True},
        "espresso": {"low_calorie": True, "lactose_free": True},
        "mocha": {"milk": True, "chocolate": True},
        "cold brew": {"low_calorie": True, "lactose_free": True},
        "iced americano": {"low_calorie": True, "lactose_free": True},
        "decaf americano": {"low_calorie": True, "lactose_free": True, "decaf": True},
        "hazelnut latte": {"milk": True, "nuts": True},
        "caramel latte": {"milk": True}
    }

    teas = {
        "black tea": {},
        "green tea": {"low_calorie": True},
        "earl grey": {},
        "chamomile tea": {"vegan": True},
        "ginger tea": {"vegan": True},
        "mint tea": {"vegan": True},
        "sage tea": {"vegan": True},
    }

    cold_drinks = {
        "cool lime": {"vegan": True},
        "lemonade": {"vegan": True},
        "strawberry lemonade": {"vegan": True},
        "mango lemonade": {"vegan": True},
        "berry ice tea": {},
        "peach ice tea": {},
        "mint detox drink": {"vegan": True, "low_calorie": True}
    }

    sweets = {
        "cheesecake": {"milk": True},
        "brownie": {"milk": True, "chocolate": True},
        "cookie": {"milk": True, "nuts": True},
        "donut": {"milk": True},
        "tiramisu": {"milk": True},
        "magnolia": {"milk": True},

        # Vegan
        "vegan chocolate cake": {"vegan": True},
        "vegan carrot cake": {"vegan": True},

        # Diet
        "fit rice pudding": {"low_calorie": True, "milk": False},
        "chia pudding": {"low_calorie": True, "vegan": True},
        "oat bar": {"low_calorie": True, "vegan": True}
    }

    # -----------------------------------
    # FILTER LOGIC
    # -----------------------------------

    def filter_items(menu):
        results = []
        for item, props in menu.items():
=======
    for category in selected_categories:
        items = MENU.get(category, {})
        for item_name, props in items.items():
            ingredients = props.get("ingredients", [])
>>>>>>> 53f5bb8 (Remove duplicate READ.md, keep clean structure)
            ok = True

<<<<<<< HEAD
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
||||||| parent of 53f5bb8 (Remove duplicate READ.md, keep clean structure)
            # Alergies block foods directly
            if intent["nuts_allergy"] and props.get("nuts", False):
                ok = False
            if intent["milk_allergy"] and props.get("milk", False):
                ok = False
            if intent["gluten_allergy"] and props.get("gluten", False):
                ok = False
            if intent["egg_allergy"] and props.get("egg", False):
                ok = False
            if intent["chocolate_allergy"] and props.get("chocolate", False):
                ok = False
=======
            for bad in intent.get("exclude_ingredients", []):
                if bad in ingredients:
                    ok = False
                    break
>>>>>>> 53f5bb8 (Remove duplicate READ.md, keep clean structure)

<<<<<<< HEAD
            if ok and intent.get("low_calorie", False) and not props.get("low_calorie", False):
                ok = False

            if ok and intent.get("sugar_free", False):
                # Hem flag'e hem de ingredients'e bak
                has_sugar_flag = not props.get("sugar_free", False)
                has_sugar_ingredient = "sugar" in ingredients
                if has_sugar_flag or has_sugar_ingredient:
                    ok = False
||||||| parent of 53f5bb8 (Remove duplicate READ.md, keep clean structure)
            # Preference check
            for key, value in intent.items():
                if value and key in props:
                    if not props.get(key, False):
                        ok = False
=======
            include_list = intent.get("include_ingredients", [])
            if ok and include_list:
                for good in include_list:
                    if good not in ingredients:
                        ok = False
                        break

            if ok and intent.get("vegan", False) and not props.get("vegan", False):
                ok = False
            if ok and intent.get("low_calorie", False) and not props.get("low_calorie", False):
                ok = False
            if ok and intent.get("sugar_free", False):
                has_sugar_flag = not props.get("sugar_free", False)
                has_sugar_ingredient = "sugar" in ingredients
                if has_sugar_flag or has_sugar_ingredient:
                    ok = False
>>>>>>> 53f5bb8 (Remove duplicate READ.md, keep clean structure)

            if ok:
                results.setdefault(category, []).append(item_name)

<<<<<<< HEAD
    return results
||||||| parent of 53f5bb8 (Remove duplicate READ.md, keep clean structure)
        return results

    return {
        "coffee": filter_items(coffees),
        "tea": filter_items(teas),
        "cold_drinks": filter_items(cold_drinks),
        "sweet": filter_items(sweets)
    }
=======
    return results

>>>>>>> 53f5bb8 (Remove duplicate READ.md, keep clean structure)
