import os
import time
import sqlite3

from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from werkzeug.utils import secure_filename

# Eğer kurulu değilse: python -m pip install flask-cors
from flask_cors import CORS

# -----------------------
# AI Module Imports
# -----------------------
try:
    from ai.nlp_model import analyze_text
    from ai.recommendation import get_recommendation
except Exception as e:
    
    analyze_text = None
    get_recommendation = None
    _AI_IMPORT_ERROR = str(e)
else:
    _AI_IMPORT_ERROR = None

# -----------------------
# Path configs
# -----------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "frontend"))
TEMPLATE_DIR = os.path.join(FRONTEND_DIR, "templates")
STATIC_DIR = os.path.join(FRONTEND_DIR, "static")
UPLOAD_DIR = os.path.join(STATIC_DIR, "images", "uploads")

DB_PATH = os.path.join(BASE_DIR, "cafe.db")
ALLOWED_EXT = {"png", "jpg", "jpeg", "webp"}

CATEGORIES = ["Coffee", "Tea", "Cold Drinks", "Desserts"]
ADMIN_KEY = "1234"  

app = Flask(
    __name__,
    template_folder=TEMPLATE_DIR,
    static_folder=STATIC_DIR,
    static_url_path="/static",
)
CORS(app)

# -----------------------
# Helpers
# -----------------------
def allowed_file(filename: str) -> bool:
    if not filename or "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in ALLOWED_EXT


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT DEFAULT '',
            image TEXT DEFAULT '',
            category TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS labels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS product_labels (
            product_id INTEGER NOT NULL,
            label_id INTEGER NOT NULL,
            UNIQUE(product_id, label_id),
            FOREIGN KEY(product_id) REFERENCES products(id) ON DELETE CASCADE,
            FOREIGN KEY(label_id) REFERENCES labels(id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()


def require_admin_key():
    # hem URL query (?key=1234) 
    key = request.args.get("key") or request.form.get("key") or ""
    if key != ADMIN_KEY:
        abort(403)


def save_uploaded_image(file_storage):
    """
    returns: '/static/images/uploads/<filename>'
    """
    if not file_storage or not file_storage.filename:
        return ""

    if not allowed_file(file_storage.filename):
        return ""

    filename = secure_filename(file_storage.filename)
    ext = filename.rsplit(".", 1)[1].lower()
    new_name = f"{int(time.time())}_{os.getpid()}.{ext}"

    full_path = os.path.join(UPLOAD_DIR, new_name)
    file_storage.save(full_path)

    return f"/static/images/uploads/{new_name}"


# -----------------------
# DB Fetch Helpers
# -----------------------
def fetch_labels(conn):
    return conn.execute("SELECT id, name FROM labels ORDER BY name").fetchall()


def fetch_products_json(conn):
    products = conn.execute(
        "SELECT id, name, category, price, description, image FROM products ORDER BY id DESC"
    ).fetchall()

    label_rows = conn.execute("""
        SELECT pl.product_id, l.name
        FROM product_labels pl
        JOIN labels l ON l.id = pl.label_id
        ORDER BY l.name
    """).fetchall()

    label_map = {}
    for r in label_rows:
        label_map.setdefault(r["product_id"], []).append(r["name"])

    out = []
    for p in products:
        out.append({
            "id": p["id"],
            "name": p["name"],
            "category": p["category"],
            "price": float(p["price"]),
            "description": p["description"] or "",
            "image": p["image"] or "",
            "labels": label_map.get(p["id"], []),
        })
    return out


def fetch_one_product_by_name(conn, name):
    
    if isinstance(name, dict):
        name = name.get("name") or name.get("title") or name.get("product") or ""

    name = str(name).strip()
    if not name:
        return None

    p = conn.execute(
        "SELECT id, name, category, price, description, image FROM products WHERE name = ? COLLATE NOCASE",
        (name,)
    ).fetchone()

    if not p:
        return None

    labels = conn.execute("""
        SELECT l.name
        FROM product_labels pl
        JOIN labels l ON l.id = pl.label_id
        WHERE pl.product_id = ?
        ORDER BY l.name
    """, (p["id"],)).fetchall()

    return {
        "name": p["name"],
        "price": float(p["price"]),
        "image": p["image"] or "",
        "labels": [r["name"] for r in labels]
    }



init_db()

# -----------------------
# Public Routes
# -----------------------
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/menu")
def menu_page():
    return render_template("menu.html")


@app.route("/contact")
def contact_page():
    return render_template("contact.html")


@app.route("/api/products", methods=["GET"])
def api_products():
    conn = get_conn()
    data = fetch_products_json(conn)
    conn.close()
    return jsonify(data)


# -----------------------
# AI Suggest API (FIXED)
# -----------------------
@app.route("/api/ai-suggest", methods=["POST"])
def api_ai_suggest():
    if analyze_text is None or get_recommendation is None:
        return jsonify({"error": "AI modules failed to load", "detail": _AI_IMPORT_ERROR}), 500

    payload = request.get_json(silent=True) or {}
    msg = (payload.get("message") or "").strip()
    if not msg:
        return jsonify({"error": "empty_message"}), 400

    intent = analyze_text(msg)

    conn = get_conn()
    all_products = fetch_products_json(conn)

    raw = get_recommendation(intent, all_products) or {}

    out = {"coffee": [], "tea": [], "cold": [], "sweet": []}

    for category in out.keys():
        items = raw.get(category, []) or []
        for item in items:
            # ✅
            if isinstance(item, dict):
                item_name = item.get("name") or item.get("title") or item.get("product") or ""
            else:
                item_name = str(item)

            item_name = item_name.strip()
            if not item_name:
                continue

            product_data = fetch_one_product_by_name(conn, item_name)
            if product_data:
                out[category].append(product_data)

    conn.close()

    total_found = sum(len(out[k]) for k in out)
    if total_found == 0:
        return jsonify({
            "recommendations": out,
            "info_message": "No matching items found. Try another request!"
        })

    return jsonify({"recommendations": out})


# -----------------------
# Admin Routes 
# -----------------------
@app.route("/admin")
def admin_panel():
    require_admin_key()

    conn = get_conn()
    labels = fetch_labels(conn)
    products = conn.execute(
        "SELECT id, name, category, price, description, image FROM products ORDER BY id DESC"
    ).fetchall()

    # product_id -> [label names]
    rows = conn.execute("""
        SELECT pl.product_id, l.name
        FROM product_labels pl
        JOIN labels l ON l.id = pl.label_id
        ORDER BY l.name
    """).fetchall()
    conn.close()

    product_labels = {}
    for r in rows:
        product_labels.setdefault(r["product_id"], []).append(r["name"])

    return render_template(
        "admin.html",
        labels=labels,
        products=products,
        product_labels=product_labels
    )


# Label add/delete (admin.html bunları çağırıyor)
@app.route("/admin/labels/add", methods=["POST"])
def admin_add_label():
    require_admin_key()

    name = (request.form.get("label_name") or "").strip()
    if not name:
        return redirect(url_for("admin_panel", key=ADMIN_KEY))

    conn = get_conn()
    try:
        conn.execute("INSERT INTO labels (name) VALUES (?)", (name,))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    finally:
        conn.close()

    return redirect(url_for("admin_panel", key=ADMIN_KEY))


@app.route("/admin/labels/<int:label_id>/delete", methods=["POST"])
def admin_delete_label(label_id):
    require_admin_key()

    conn = get_conn()
    conn.execute("DELETE FROM labels WHERE id = ?", (label_id,))
    conn.commit()
    conn.close()

    return redirect(url_for("admin_panel", key=ADMIN_KEY))


# Product form pages (admin.html bunları çağırıyor)
@app.route("/admin/products/new")
def admin_new_product():
    require_admin_key()

    conn = get_conn()
    labels = fetch_labels(conn)
    conn.close()

    return render_template(
        "admin_product_form.html",
        mode="new",
        product=None,
        labels=labels,
        product_labels=[],
        categories=CATEGORIES
    )


@app.route("/admin/products/<int:product_id>/edit")
def admin_edit_product(product_id):
    require_admin_key()

    conn = get_conn()
    product = conn.execute(
        "SELECT id, name, category, price, description, image FROM products WHERE id = ?",
        (product_id,)
    ).fetchone()

    labels = fetch_labels(conn)

    rows = conn.execute("""
        SELECT l.name
        FROM product_labels pl
        JOIN labels l ON l.id = pl.label_id
        WHERE pl.product_id = ?
        ORDER BY l.name
    """, (product_id,)).fetchall()

    conn.close()

    product_labels = [r["name"] for r in rows]

    return render_template(
        "admin_product_form.html",
        mode="edit",
        product=product,
        labels=labels,
        product_labels=product_labels,
        categories=CATEGORIES
    )


# Create / Update / Delete (admin_product_form.html bunları çağırıyor)
@app.route("/admin/products/create", methods=["POST"])
def admin_create_product():
    require_admin_key()

    name = (request.form.get("name") or "").strip()
    category = (request.form.get("category") or "").strip()
    price_raw = (request.form.get("price") or "").strip()
    description = (request.form.get("description") or "").strip()
    selected_labels = request.form.getlist("labels")

    if not name or not category or not price_raw:
        return redirect(url_for("admin_new_product", key=ADMIN_KEY))

    try:
        price = float(price_raw)
    except ValueError:
        return redirect(url_for("admin_new_product", key=ADMIN_KEY))

    image_path = ""
    if "image_file" in request.files and request.files["image_file"].filename:
        image_path = save_uploaded_image(request.files["image_file"])

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO products (name, price, description, image, category) VALUES (?, ?, ?, ?, ?)",
        (name, price, description, image_path, category)
    )
    product_id = cur.lastrowid

    for lbl in selected_labels:
        row = conn.execute("SELECT id FROM labels WHERE name = ?", (lbl,)).fetchone()
        if row:
            try:
                conn.execute(
                    "INSERT INTO product_labels (product_id, label_id) VALUES (?, ?)",
                    (product_id, row["id"])
                )
            except sqlite3.IntegrityError:
                pass

    conn.commit()
    conn.close()

    return redirect(url_for("admin_panel", key=ADMIN_KEY))


@app.route("/admin/products/<int:product_id>/update", methods=["POST"])
def admin_update_product(product_id):
    require_admin_key()

    name = (request.form.get("name") or "").strip()
    category = (request.form.get("category") or "").strip()
    price_raw = (request.form.get("price") or "").strip()
    description = (request.form.get("description") or "").strip()
    selected_labels = request.form.getlist("labels")

    if not name or not category or not price_raw:
        return redirect(url_for("admin_edit_product", product_id=product_id, key=ADMIN_KEY))

    try:
        price = float(price_raw)
    except ValueError:
        return redirect(url_for("admin_edit_product", product_id=product_id, key=ADMIN_KEY))

    conn = get_conn()

    # image optional
    image_path = None
    if "image_file" in request.files and request.files["image_file"].filename:
        image_path = save_uploaded_image(request.files["image_file"])

    if image_path:
        conn.execute(
            "UPDATE products SET name=?, price=?, description=?, image=?, category=? WHERE id=?",
            (name, price, description, image_path, category, product_id)
        )
    else:
        conn.execute(
            "UPDATE products SET name=?, price=?, description=?, category=? WHERE id=?",
            (name, price, description, category, product_id)
        )

    # refresh labels
    conn.execute("DELETE FROM product_labels WHERE product_id=?", (product_id,))
    for lbl in selected_labels:
        row = conn.execute("SELECT id FROM labels WHERE name = ?", (lbl,)).fetchone()
        if row:
            try:
                conn.execute(
                    "INSERT INTO product_labels (product_id, label_id) VALUES (?, ?)",
                    (product_id, row["id"])
                )
            except sqlite3.IntegrityError:
                pass

    conn.commit()
    conn.close()

    return redirect(url_for("admin_panel", key=ADMIN_KEY))


@app.route("/admin/products/<int:product_id>/delete", methods=["POST"])
def admin_delete_product(product_id):
    require_admin_key()

    conn = get_conn()
    conn.execute("DELETE FROM products WHERE id=?", (product_id,))
    conn.commit()
    conn.close()

    return redirect(url_for("admin_panel", key=ADMIN_KEY))


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
