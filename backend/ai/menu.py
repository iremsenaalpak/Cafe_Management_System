# backend/ai/menu.py

# Ingredient keys used across the system:
# coffee, tea, matcha, milk, lactose, egg, gluten, nuts, almond, peanut, chocolate,
# strawberry, lemon, orange, apple, cinnamon, banana, blueberry, raspberry, pineapple,
# watermelon, kiwi, sugar, oats, yogurt, water, hibiscus, ginger, ice_cream, oat_milk, oreo, rice

MENU = {
    "coffee": {
        "americano": {"ingredients": ["coffee"], "vegan": True, "low_calorie": True, "sugar_free": True},
        "espresso": {"ingredients": ["coffee"], "vegan": True, "low_calorie": True, "sugar_free": True},
        "latte": {"ingredients": ["coffee", "milk", "lactose"], "vegan": False, "low_calorie": False, "sugar_free": True},
        "cappuccino": {"ingredients": ["coffee", "milk", "lactose"], "vegan": False, "low_calorie": False, "sugar_free": True},
        "mocha": {"ingredients": ["coffee", "milk", "lactose", "chocolate"], "vegan": False, "low_calorie": False, "sugar_free": True},

        "oat milk latte": {"ingredients": ["coffee", "oat_milk"], "vegan": True, "low_calorie": True, "sugar_free": True},
        "affogato": {"ingredients": ["coffee", "ice_cream", "milk", "lactose"], "vegan": False, "low_calorie": False, "sugar_free": True},
    },

    "tea": {
        "matcha tea": {"ingredients": ["matcha"], "vegan": True, "low_calorie": True, "sugar_free": True},
        "ginger lemon tea": {"ingredients": ["tea", "ginger", "lemon"], "vegan": True, "low_calorie": True, "sugar_free": True},
        "herbal tea": {"ingredients": ["tea"], "vegan": True, "low_calorie": True, "sugar_free": True},
        "black tea": {"ingredients": ["tea"], "vegan": True, "low_calorie": True, "sugar_free": True},
        "green tea": {"ingredients": ["tea"], "vegan": True, "low_calorie": True, "sugar_free": True},
    },

    "cold": {
        "banana milkshake": {"ingredients": ["milk", "lactose", "banana", "sugar"], "vegan": False, "low_calorie": False, "sugar_free": False},
        "strawberry milkshake": {"ingredients": ["milk", "lactose", "strawberry", "sugar"], "vegan": False, "low_calorie": False, "sugar_free": False},
        "oreo milkshake": {"ingredients": ["milk", "lactose", "chocolate", "oreo", "sugar"], "vegan": False, "low_calorie": False, "sugar_free": False},

        "detox water": {"ingredients": ["water", "lemon"], "vegan": True, "low_calorie": True, "sugar_free": True},
        "hibiscus": {"ingredients": ["hibiscus"], "vegan": True, "low_calorie": True, "sugar_free": True},
        "lemonade": {"ingredients": ["lemon", "sugar"], "vegan": True, "low_calorie": False, "sugar_free": False},

        "orange juice": {"ingredients": ["orange"], "vegan": True, "low_calorie": True, "sugar_free": True},
    },

    "sweet": {
        # admin: Milk + Lactose
        "sutlac (rice pudding)": {"ingredients": ["milk", "lactose", "rice", "sugar"], "vegan": False, "low_calorie": False, "sugar_free": False},

        # admin: Chocolate + Egg + Gluten + Nuts
        "nutella pancake stack": {"ingredients": ["gluten", "egg", "chocolate", "nuts", "sugar"], "vegan": False, "low_calorie": False, "sugar_free": False},

        # admin: Banana + Vegan
        "vegan banana bread": {"ingredients": ["banana", "oats", "sugar"], "vegan": True, "low_calorie": False, "sugar_free": False},

        # admin: Low Calorie + Sugar Free (yogurt tabanlı varsaydık)
        "apple cinnamon yogurt cup": {"ingredients": ["yogurt", "milk", "lactose", "apple", "cinnamon"], "vegan": False, "low_calorie": True, "sugar_free": True},

        # admin: Low Calorie + Sugar Free
        "chia pudding": {"ingredients": ["oats"], "vegan": True, "low_calorie": True, "sugar_free": True},

        # mevcutlar (ekran görüntüsüne göre)
        "tiramisu": {"ingredients": ["milk", "lactose", "egg", "gluten", "coffee", "chocolate", "sugar"], "vegan": False, "low_calorie": False, "sugar_free": False},

        "fruit & yogurt parfait": {"ingredients": ["yogurt", "milk", "lactose", "strawberry", "blueberry"], "vegan": False, "low_calorie": True, "sugar_free": True},

        "protein bar": {"ingredients": ["nuts", "oats", "blueberry", "raspberry", "sugar"], "vegan": True, "low_calorie": True, "sugar_free": False},

        "peanut brownie": {"ingredients": ["gluten", "peanut", "chocolate", "egg", "sugar"], "vegan": False, "low_calorie": False, "sugar_free": False},

        "fruit bowl": {"ingredients": ["strawberry", "blueberry", "raspberry", "pineapple", "watermelon", "kiwi"], "vegan": True, "low_calorie": True, "sugar_free": True},

        "vegan cookie": {"ingredients": ["almond", "chocolate", "sugar"], "vegan": True, "low_calorie": False, "sugar_free": False},
        "cheesecake": {"ingredients": ["egg", "milk", "lactose", "sugar"], "vegan": False, "low_calorie": False, "sugar_free": False},
        "brownie": {"ingredients": ["chocolate", "egg", "gluten", "sugar"], "vegan": False, "low_calorie": False, "sugar_free": False},
    }
}

# UI metadata (name/price/img/desc)
# img file names MUST match frontend/static/images/
MENU_META = {
    # Coffee
    "americano": {"name": "Americano", "price": 85.0, "img": "americano.jpg", "desc": "Smooth espresso diluted with hot water for a rich, clean taste."},
    "espresso": {"name": "Espresso", "price": 75.0, "img": "espresso.jpg", "desc": "A strong and concentrated coffee shot with bold flavor."},
    "latte": {"name": "Latte", "price": 95.0, "img": "latte.jpg", "desc": "Creamy espresso blended with steamed milk."},
    "cappuccino": {"name": "Cappuccino", "price": 100.0, "img": "cappuccino.jpg", "desc": "Classic espresso topped with rich milk foam."},
    "mocha": {"name": "Mocha", "price": 110.0, "img": "mocha.jpg", "desc": "Espresso mixed with chocolate and steamed milk."},
    "cold brew": {"name": "Cold Brew", "price": 105.0, "img": "cold_brew.jpg", "desc": "Slow-brewed cold coffee with a smooth and refreshing taste."},
    "oat milk latte": {"name": "Oat Milk Latte", "price": 115.0, "img": "oat_milk_latte.jpg", "desc": "Light espresso combined with creamy oat milk."},
    "affogato": {"name": "Affogato", "price": 130.0, "img": "affogato.jpg", "desc": "Hot espresso poured over vanilla ice cream."},

    # Tea
    "matcha tea": {"name": "Matcha Tea", "price": 80.0, "img": "matcha_tea.jpg", "desc": "Finely ground green tea with a smooth, earthy flavor."},
    "ginger lemon tea": {"name": "Ginger Lemon Tea", "price": 65.0, "img": "ginger_lemon_tea.jpg", "desc": "Warming ginger combined with fresh lemon."},
    "herbal tea": {"name": "Herbal Tea", "price": 60.0, "img": "herbal_tea.jpg", "desc": "A calming blend of natural herbs."},
    "black tea": {"name": "Black Tea", "price": 50.0, "img": "black_tea.jpg", "desc": "Classic black tea with a strong aroma."},
    "green tea": {"name": "Green Tea", "price": 55.0, "img": "green_tea.jpg", "desc": "Light and refreshing tea with natural antioxidants."},

    # Cold drinks
    "banana milkshake": {"name": "Banana Milkshake", "price": 120.0, "img": "banana_milkshake.jpg", "desc": "Classic creamy milkshake made with fresh milk and banana."},
    "strawberry milkshake": {"name": "Strawberry Milkshake", "price": 120.0, "img": "strawberry_milkshake.jpg", "desc": "Classic creamy milkshake made with fresh milk and strawberry."},
    "oreo milkshake": {"name": "Oreo Milkshake", "price": 120.0, "img": "oreo_milkshake.jpg", "desc": "Classic creamy milkshake made with fresh milk and chocolate cookies."},
    "detox water": {"name": "Detox Water", "price": 65.0, "img": "detox_water.jpg", "desc": "Infused water with lemon for a clean, refreshing taste."},
    "hibiscus": {"name": "Hibiscus", "price": 80.0, "img": "hibiscus_tea.jpg", "desc": "Floral hibiscus drink served cold and refreshing."},
    "lemonade": {"name": "Lemonade", "price": 75.0, "img": "lemonade.jpg", "desc": "Freshly squeezed lemon drink with a sweet and sour balance."},
    "orange juice": {"name": "Orange Juice", "price": 110.0, "img": "orange_juice.jpg", "desc": "Freshly squeezed orange juice served cold."},

    # Desserts / Sweet
    "sutlac (rice pudding)": {"name": "Sütlaç (Rice Pudding)", "price": 160.0, "img": "sutlac.jpg", "desc": "Traditional Turkish rice pudding made with milk."},
    "nutella pancake stack": {"name": "Nutella Pancake Stack", "price": 150.0, "img": "nutella_pancake.jpg", "desc": "Stack of pancakes served with chocolate spread and nuts."},
    "vegan banana bread": {"name": "Vegan Banana Bread", "price": 135.0, "img": "vegan_banana_bread.jpg", "desc": "Soft vegan banana bread made with bananas and oats."},
    "apple cinnamon yogurt cup": {"name": "Apple Cinnamon Yogurt Cup", "price": 145.0, "img": "apple_cinnamon_yogurt.jpg", "desc": "Light yogurt dessert with apple and cinnamon."},
    "chia pudding": {"name": "Chia Pudding", "price": 125.0, "img": "chia_pudding.jpg", "desc": "Light chia pudding with a clean, simple taste."},

    "tiramisu": {"name": "Tiramisu", "price": 170.0, "img": "tiramisu.jpg", "desc": "Classic Italian dessert with coffee and cocoa flavors."},
    "fruit & yogurt parfait": {"name": "Fruit & Yogurt Parfait", "price": 135.0, "img": "fruit_&_yogurt_parfait.jpg", "desc": "Light yogurt dessert layered with fresh fruits."},
    "protein bar": {"name": "Protein Bar", "price": 125.0, "img": "protein_bar.jpg", "desc": "Energy bar made with oats, nuts, and berries."},
    "peanut brownie": {"name": "Peanut Brownie", "price": 150.0, "img": "peanut_brownie.jpg", "desc": "Chocolate brownie topped with crunchy peanuts."},
    "fruit bowl": {"name": "Fruit Bowl", "price": 120.0, "img": "fruit_bowl.jpg", "desc": "Fresh seasonal fruits served chilled."},
    "vegan cookie": {"name": "Vegan Cookie", "price": 95.0, "img": "vegan_cookie.jpg", "desc": "Plant-based cookie with a soft and chewy bite."},
    "cheesecake": {"name": "Cheesecake", "price": 155.0, "img": "cheesecake.jpg", "desc": "Creamy cheesecake with a smooth texture."},
    "brownie": {"name": "Brownie", "price": 140.0, "img": "brownie.jpg", "desc": "Rich and moist chocolate brownie."},
}
