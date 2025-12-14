# backend/ai/menu.py

# Ingredient keys used across the system:
# coffee, tea, matcha, milk, lactose, egg, gluten, nuts, peanut, chocolate,
# strawberry, lemon, sugar, oats, berry, yogurt, water, hibiscus, ginger, ice_cream, oat_milk

MENU = {
    "coffee": {
        "americano": {"ingredients": ["coffee"], "vegan": True, "low_calorie": True, "sugar_free": True},
        "espresso": {"ingredients": ["coffee"], "vegan": True, "low_calorie": True, "sugar_free": True},
        "latte": {"ingredients": ["coffee", "milk", "lactose"], "vegan": False, "low_calorie": False, "sugar_free": True},
        "cappuccino": {"ingredients": ["coffee", "milk", "lactose"], "vegan": False, "low_calorie": False, "sugar_free": True},
        "mocha": {"ingredients": ["coffee", "milk", "lactose", "chocolate", "sugar"], "vegan": False, "low_calorie": False, "sugar_free": False},

        # Diet-friendly coffee
        "cold brew": {"ingredients": ["coffee"], "vegan": True, "low_calorie": True, "sugar_free": True},

        # Vegan alternative
        "oat milk latte": {"ingredients": ["coffee", "oat_milk"], "vegan": True, "low_calorie": True, "sugar_free": True},

        # Dessert-style coffee
        "affogato": {"ingredients": ["coffee", "ice_cream", "milk", "lactose", "sugar"], "vegan": False, "low_calorie": False, "sugar_free": False},
    },

    "tea": {
        "green tea": {"ingredients": ["tea"], "vegan": True, "low_calorie": True, "sugar_free": True},
        "black tea": {"ingredients": ["tea"], "vegan": True, "low_calorie": True, "sugar_free": True},
        "herbal tea": {"ingredients": ["tea"], "vegan": True, "low_calorie": True, "sugar_free": True},
        "ginger lemon tea": {"ingredients": ["tea", "ginger", "lemon"], "vegan": True, "low_calorie": True, "sugar_free": True},
        "matcha tea": {"ingredients": ["matcha"], "vegan": True, "low_calorie": True, "sugar_free": True},
    },

    "cold": {
        "lemonade": {"ingredients": ["lemon", "sugar"], "vegan": True, "low_calorie": False, "sugar_free": False},
        "hibiscus": {"ingredients": ["hibiscus"], "vegan": True, "low_calorie": True, "sugar_free": True},
        "detox water": {"ingredients": ["water", "lemon"], "vegan": True, "low_calorie": True, "sugar_free": True},
        "milkshake": {"ingredients": ["milk", "lactose", "sugar"], "vegan": False, "low_calorie": False, "sugar_free": False},

        # Cold brew should also appear in cold drinks when user asks for cold beverages
        "cold brew": {"ingredients": ["coffee"], "vegan": True, "low_calorie": True, "sugar_free": True},
    },

    "sweet": {
        "brownie": {"ingredients": ["gluten", "chocolate", "egg", "sugar"], "vegan": False, "low_calorie": False, "sugar_free": False},
        "cheesecake": {"ingredients": ["milk", "lactose", "egg", "sugar"], "vegan": False, "low_calorie": False, "sugar_free": False},
        "vegan cookie": {"ingredients": ["nuts", "sugar"], "vegan": True, "low_calorie": False, "sugar_free": False},
        "fruit bowl": {"ingredients": ["strawberry"], "vegan": True, "low_calorie": True, "sugar_free": True},
        "peanut brownie": {"ingredients": ["gluten", "peanut", "chocolate", "egg", "sugar"], "vegan": False, "low_calorie": False, "sugar_free": False},

        # Diet-friendly snack (nuts/oats/berries)
        # Note: contains nuts -> should be excluded for nut allergy
        "protein bar": {
            "ingredients": ["nuts", "oats", "berry", "sugar"],
            "vegan": True,
            "low_calorie": True,
            "sugar_free": False
        },

        "fruit & yogurt parfait": {
            "ingredients": ["yogurt", "milk", "lactose", "strawberry"],
            "vegan": False,
            "low_calorie": True,
            "sugar_free": True
        },

        "tiramisu": {
            "ingredients": ["milk", "lactose", "egg", "gluten", "coffee", "sugar", "chocolate"],
            "vegan": False,
            "low_calorie": False,
            "sugar_free": False
        },
    }
}

# UI metadata (name/price/img/desc)
# img file names MUST match frontend/static/images/
MENU_META = {
    # Coffee
    "americano": {"name": "Americano", "price": 70, "img": "americano.jpg", "desc": "Simple and strong coffee."},
    "espresso": {"name": "Espresso", "price": 60, "img": "espresso.jpg", "desc": "Small but intense espresso shot."},
    "latte": {"name": "Latte", "price": 80, "img": "latte.jpg", "desc": "Milky and smooth."},
    "cappuccino": {"name": "Cappuccino", "price": 85, "img": "cappuccino.jpg", "desc": "Espresso with foamy milk."},
    "mocha": {"name": "Mocha", "price": 90, "img": "mocha.jpg", "desc": "Coffee with chocolate."},
    "cold brew": {"name": "Cold Brew", "price": 85, "img": "cold_brew.jpg", "desc": "Cold-brewed coffee with a smooth taste."},
    "oat milk latte": {"name": "Oat Milk Latte", "price": 95, "img": "oat_milk_latte.jpg", "desc": "Light latte made with oat milk."},
    "affogato": {"name": "Affogato", "price": 110, "img": "affogato.jpg", "desc": "Espresso poured over ice cream."},

    # Tea
    "green tea": {"name": "Green Tea", "price": 35, "img": "green_tea.jpg", "desc": "Light and refreshing."},
    "black tea": {"name": "Black Tea", "price": 30, "img": "black_tea.jpg", "desc": "Classic black tea."},
    "herbal tea": {"name": "Herbal Tea", "price": 40, "img": "herbal_tea.jpg", "desc": "A soothing herbal blend."},
    "ginger lemon tea": {"name": "Ginger Lemon Tea", "price": 45, "img": "ginger_lemon_tea.jpg", "desc": "Ginger-lemon blend."},
    "matcha tea": {"name": "Matcha Tea", "price": 55, "img": "matcha_tea.jpg", "desc": "Fresh matcha flavor."},

    # Cold drinks
    "lemonade": {"name": "Lemonade", "price": 55, "img": "lemonade.jpg", "desc": "Homemade lemonade."},
    "hibiscus": {"name": "Hibiscus", "price": 60, "img": "hibiscus_tea.jpg", "desc": "Hibiscus-based cold drink."},
    "detox water": {"name": "Detox Water", "price": 45, "img": "detox_water.jpg", "desc": "Lemon detox water (no sugar)."},
    "milkshake": {"name": "Milkshake", "price": 95, "img": "milkshake.jpg", "desc": "Classic creamy milkshake."},

    # Sweets
    "brownie": {"name": "Brownie", "price": 110, "img": "brownie.jpg", "desc": "Rich chocolate brownie."},
    "cheesecake": {"name": "Cheesecake", "price": 120, "img": "cheesecake.jpg", "desc": "Creamy cheesecake slice."},
    "vegan cookie": {"name": "Vegan Cookie", "price": 75, "img": "vegan_cookie.jpg", "desc": "A delicious vegan cookie."},
    "fruit bowl": {"name": "Fruit Bowl", "price": 90, "img": "fruit_bowl.jpg", "desc": "Fresh fruit bowl."},
    "peanut brownie": {"name": "Peanut Brownie", "price": 125, "img": "peanut_brownie.jpg", "desc": "Brownie with peanuts."},

    "protein bar": {"name": "Protein Bar", "price": 105, "img": "protein_bar.jpg", "desc": "Oats, nuts and mixed berries energy bar."},
    "fruit & yogurt parfait": {"name": "Fruit & Yogurt Parfait", "price": 115, "img": "fruit_&_yogurt_parfait.jpg", "desc": "Light parfait with yogurt and fruit."},
    "tiramisu": {"name": "Tiramisu", "price": 135, "img": "tiramisu.jpg", "desc": "Classic Italian dessert with coffee and cocoa."},
}
