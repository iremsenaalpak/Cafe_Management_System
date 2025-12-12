# backend/ai/menu.py

MENU = {
    "coffee": {
        "americano": {"ingredients": ["coffee"], "vegan": True, "low_calorie": True, "sugar_free": True},
        "latte": {"ingredients": ["coffee", "milk"], "vegan": False, "low_calorie": False, "sugar_free": True},
        "cappuccino": {"ingredients": ["coffee", "milk"], "vegan": False, "low_calorie": False, "sugar_free": True},
        "mocha": {"ingredients": ["coffee", "milk", "chocolate", "sugar"], "vegan": False, "low_calorie": False, "sugar_free": False}
    },

    "tea": {
        "green tea": {"ingredients": ["tea"], "vegan": True, "low_calorie": True, "sugar_free": True},
        "black tea": {"ingredients": ["tea"], "vegan": True, "low_calorie": True, "sugar_free": True},
        "herbal tea": {"ingredients": ["tea"], "vegan": True, "low_calorie": True, "sugar_free": True}
    },

    "sweet": {
        "brownie": {"ingredients": ["chocolate", "egg", "sugar"], "vegan": False, "low_calorie": False, "sugar_free": False},
        "cheesecake": {"ingredients": ["milk", "egg", "sugar"], "vegan": False, "low_calorie": False, "sugar_free": False},
        "vegan cookie": {"ingredients": ["nuts", "sugar"], "vegan": True, "low_calorie": False, "sugar_free": False},
        "fruit bowl": {"ingredients": ["strawberry"], "vegan": True, "low_calorie": True, "sugar_free": True},
        "peanut brownie": {"ingredients": ["peanut", "chocolate", "egg", "sugar"], "vegan": False, "low_calorie": False, "sugar_free": False}
    }
}

# Web'de kartlarda gözüksün diye (isim/fiyat/resim/açıklama)
# img dosyaları: frontend/static/images içindeki isimlerle aynı olmalı
MENU_META = {
    "americano":      {"name": "Americano",      "price": 70,  "img": "americano.jpg",   "desc": "Sade ve yoğun kahve."},
    "latte":          {"name": "Latte",          "price": 80,  "img": "latte.jpg",      "desc": "Sütlü, yumuşak içim."},
    "cappuccino":     {"name": "Cappuccino",     "price": 85,  "img": "cappuccino.jpg",      "desc": "Köpüklü süt ve espresso."},
    "mocha":          {"name": "Mocha",          "price": 90,  "img": "mocha.jpg",   "desc": "Çikolatalı kahve."},

    "green tea":      {"name": "Green Tea",      "price": 35,  "img": "green_tea.jpg",        "desc": "Hafif ve ferah."},
    "black tea":      {"name": "Black Tea",      "price": 30,  "img": "black_tea.jpg",        "desc": "Klasik siyah çay."},
    "herbal tea":     {"name": "Herbal Tea",     "price": 40,  "img": "herbal_tea.jpg",        "desc": "Bitki çayı karışımı."},

    "brownie":        {"name": "Brownie",        "price": 110, "img": "brownie.jpg", "desc": "Yoğun çikolatalı."},
    "cheesecake":     {"name": "Cheesecake",     "price": 120, "img": "cheesecake.jpg", "desc": "Kremamsı tatlı."},
    "vegan cookie":   {"name": "Vegan Cookie",   "price": 75,  "img": "vegan_cookie.jpg", "desc": "Vegan kurabiye."},
    "fruit bowl":     {"name": "Fruit Bowl",     "price": 90,  "img": "fruit_bowl.jpg", "desc": "Meyve kasesi."},
    "peanut brownie": {"name": "Peanut Brownie", "price": 125, "img": "peanut_brownie.jpg", "desc": "Fıstıklı brownie."},
}
