from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pathlib import Path
import copy

from ai.nlp_model import analyze_text
from ai.recommendation import get_recommendation

# Menü importu (hata olursa ekrana yazsın)
try:
    from ai.menu import MENU, MENU_META
except Exception as e:
    print("MENU import error:", e)
    MENU, MENU_META = None, None


# -------------------------
# Frontend klasör yolunu ayarla
# -------------------------
BASE_DIR = Path(__file__).resolve().parent          # .../backend
PROJECT_ROOT = BASE_DIR.parent                      # proje kökü

TEMPLATES_DIR = PROJECT_ROOT / "frontend" / "templates"
STATIC_DIR = PROJECT_ROOT / "frontend" / "static"

app = Flask(
    __name__,
    template_folder=str(TEMPLATES_DIR),
    static_folder=str(STATIC_DIR),
)

# CORS sadece API için
CORS(app, resources={r"/api/*": {"origins": "*"}})


# -------------------------
# Helpers (UI-ready item builder)
# -------------------------
def _norm(s: str) -> str:
    return (s or "").strip().lower()

def build_item(category: str, key: str):
    """
    Returns a full item dict for UI:
    name, img, price, desc, ingredients, flags...
    """
    if not MENU:
        return None

    k = _norm(key)

    attrs = MENU.get(category, {}).get(k)
    if not attrs:
        return None

    meta = (MENU_META or {}).get(k, {})
    return {
        "id": k,
        "category": category,  # coffee/tea/sweet
        "name": meta.get("name", k.title()),
        "price": meta.get("price"),
        "desc": meta.get("desc", ""),
        "img": meta.get("img"),
        "ingredients": attrs.get("ingredients", []),
        "vegan": bool(attrs.get("vegan", False)),
        "low_calorie": bool(attrs.get("low_calorie", False)),
        "sugar_free": bool(attrs.get("sugar_free", False)),
    }


# -------------------------
# Frontend Routes (Pages)
# -------------------------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/menu")
def menu_page():
    items = []

    if MENU:
        for category, products in MENU.items():
            for key, attrs in products.items():
                meta = (MENU_META or {}).get(key, {})
                items.append({
                    "id": key,
                    "name": meta.get("name", key.title()),
                    "category": category,  # coffee / tea / sweet
                    "price": meta.get("price"),
                    "desc": meta.get("desc", ""),
                    "img": meta.get("img"),
                    "ingredients": attrs.get("ingredients", []),
                    "vegan": attrs.get("vegan", False),
                    "low_calorie": attrs.get("low_calorie", False),
                    "sugar_free": attrs.get("sugar_free", False),
                })

    return render_template("menu.html", items=items, menu_loaded=bool(MENU))


@app.route("/contact")
def contact():
    return render_template("contact.html")


# -------------------------
# API Routes
# -------------------------
@app.route("/api/health")
def health():
    return jsonify({"ok": True, "message": "Backend is working"}), 200


@app.route("/api/ai-suggest", methods=["POST"])
def ai_suggest():
    data = request.json

    if not data:
        return jsonify({"error": "No JSON body provided"}), 400

    user_msg = (data.get("message") or "").strip()
    if not user_msg:
        return jsonify({"error": "Message cannot be empty"}), 400

    intent = analyze_text(user_msg)
    recommendations = get_recommendation(intent)

    # recommendations -> UI-ready (name/img/price/flags)
    detailed = {}
    if isinstance(recommendations, dict):
        for category, items in recommendations.items():
            if not isinstance(items, list):
                continue

            detailed_list = []
            for it in items:
                if isinstance(it, str):
                    key = it
                elif isinstance(it, dict):
                    key = it.get("id") or it.get("key") or it.get("name")
                else:
                    continue

                obj = build_item(category, key)
                if obj:
                    detailed_list.append(obj)

            detailed[category] = detailed_list

    has_results = any(isinstance(v, list) and len(v) > 0 for v in detailed.values())

    info_message = None
    if not has_results:
        info_message = (
            "Seçtiğin kriterlere uygun bir ürün bulamadım. "
            "İstersen filtreleri (örneğin 'vegan', 'şekersiz' veya 'diyet') biraz esnetebilirsin."
        )

    intent_serializable = copy.deepcopy(intent)

    return jsonify({
        "user_message": user_msg,
        "detected_intent": intent_serializable,
        "recommendations": detailed,   # <-- UI-ready
        "has_results": has_results,
        "info_message": info_message
    }), 200


if __name__ == "__main__":
    app.run(debug=True)
