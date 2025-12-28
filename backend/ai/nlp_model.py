import re
import joblib
import os

# -----------------------
# PATH CONFIGURATIONS
# -----------------------
# Ensure the model is loaded from the correct directory relative to this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'menu_ai_model.pkl')

# -----------------------
# MODEL INITIALIZATION
# -----------------------
# Load the pre-trained AI model once at startup for performance
AI_MODEL = None
if os.path.exists(MODEL_PATH):
    try:
        AI_MODEL = joblib.load(MODEL_PATH)
        print("NLP System: AI Model loaded successfully.")
    except Exception as e:
        print(f"NLP System Error: Could not load model - {e}")

# -----------------------
# NORMALIZATION TOOLS
# -----------------------
# Map for converting Turkish specific characters to ASCII equivalents
TR_MAP = str.maketrans({"ç": "c", "ğ": "g", "ı": "i", "ö": "o", "ş": "s", "ü": "u"})

def _norm(s: str) -> str:
    """Standardize input string: lowercase and remove leading/trailing spaces."""
    return (s or "").lower().strip()

def _ascii_tr(s: str) -> str:
    """Normalize text by removing Turkish specific characters."""
    return _norm(s).translate(TR_MAP)

def _has_negation(text: str, ascii_text: str) -> bool:
    """Detects if the user is asking for an exclusion (e.g., 'no', 'without')."""
    return any(k in ascii_text for k in ["siz", "suz", "olmasin", "yok"]) or \
           any(k in text for k in ["no ", "without", "free", "not "])

# -----------------------
# DATA DEFINITIONS
# -----------------------
FRUIT_LABELS = ["apple", "banana", "blueberry", "strawberry", "pineapple", "watermelon", "kiwi", "orange", "lemon"]
NUT_LABELS = ["nuts", "almond", "peanut"]
FRUIT_TR_MAP = {"elma": "apple", "cilek": "strawberry", "muz": "banana", "kivi": "kiwi", "ananas": "pineapple"}

# -----------------------
# MAIN ANALYSIS FUNCTION
# -----------------------
def analyze_text(user_input: str) -> dict:
    """
    Analyzes user message to detect dietary intents and exclusions.
    """
    text = _norm(user_input)
    atext = _ascii_tr(user_input)

    # 1. AI Prediction (Machine Learning)
    ai_label = None
    if AI_MODEL:
        try:
            # Predict intent using the trained model
            ai_label = AI_MODEL.predict([user_input.lower()])[0]
        except:
            pass

    # 2. Build Intent Object
    intent = {
        "categories": [],
        "exclude_labels": [],
        "vegan": (ai_label == "vegan") or ("vegan" in text),
        "low_calorie": (ai_label == "diet") or (any(k in text for k in ["diet", "diyet", "light", "fit"])),
        "sugar_free": any(k in text for k in ["sugar-free", "sekersiz", "no sugar"]),
    }

    # 3. Category Detection (Rule-based)
    if re.search(r"\b(coffee|kahve|espresso|latte|americano|cappuccino)\b", text): 
        intent["categories"].append("coffee")
    if re.search(r"\b(tea|cay|çay|matcha)\b", text): 
        intent["categories"].append("tea")
    if re.search(r"\b(dessert|sweet|tatli|cake|kek|pastry|cookie)\b", text): 
        intent["categories"].append("sweet")
    if re.search(r"\b(cold|iced|soguk|lemonade|milkshake|smoothie)\b", text): 
        intent["categories"].append("cold")

    # Default to all categories if no specific one is mentioned
    if not intent["categories"]:
        intent["categories"] = ["coffee", "tea", "cold", "sweet"]

    # 4. Exclusion & Allergy Logic
    is_negation = _has_negation(text, atext)
    is_allergy = (ai_label == "allergy") or ("alerji" in atext or "allergy" in text)
    
    if is_negation or is_allergy:
        if "fruit" in text or "meyve" in atext:
            intent["exclude_labels"].extend(FRUIT_LABELS)
        
        for tr_root, en_label in FRUIT_TR_MAP.items():
            if tr_root in atext:
                intent["exclude_labels"].append(en_label)

        if any(k in atext for k in ["nuts", "nut", "kuruyemis", "peanut"]):
            intent["exclude_labels"].extend(NUT_LABELS)
        
        if any(k in atext for k in ["milk", "sut", "dairy", "laktoz"]):
            intent["exclude_labels"].append("milk")

    # Ensure unique values
    intent["exclude_labels"] = list(set(intent["exclude_labels"]))
    return intent