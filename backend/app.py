import os
import time
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from werkzeug.utils import secure_filename
from flask_cors import CORS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "frontend"))
TEMPLATE_DIR = os.path.join(FRONTEND_DIR, "templates")
STATIC_DIR = os.path.join(FRONTEND_DIR, "static")
UPLOAD_DIR = os.path.join(STATIC_DIR, "images", "uploads")

DB_PATH = os.path.join(BASE_DIR, "cafe.db")
ALLOWED_EXT = {"png", "jpg", "jpeg", "webp"}

app = Flask(
    __name__,
    template_folder=TEMPLATE_DIR,
    static_folder=STATIC_DIR,
    static_url_path="/static",
)
CORS(app)


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

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT DEFAULT '',
            image TEXT DEFAULT '',
            category TEXT NOT NULL
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS labels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS product_labels (
            product_id INTEGER NOT NULL,
            label_id INTEGER NOT NULL,
            UNIQUE(product_id, label_id),
            FOREIGN KEY(product_id) REFERENCES products(id) ON DELETE CASCADE,
            FOREIGN KEY(label_id) REFERENCES labels(id) ON DELETE CASCADE
        )
        """
    )

    conn.commit()
    conn.close()


init_db()


def fetch_labels(conn):
    return conn.execute("SELECT id, name FROM labels ORDER BY name").fetchall()


def fetch_products_for_admin(conn):
    products = conn.execute(
        "SELECT id, name, category, price, description, image FROM products ORDER BY id DESC"
    ).fetchall()

    label_map = {}
    rows = conn.execute(
        """
        SELECT pl.product_id, l.name
        FROM product_labels pl
        JOIN labels l ON l.id = pl.label_id
        ORDER BY l.name
        """
    ).fetchall()

    for r in rows:
        label_map.setdefault(r["product_id"], []).append(r["name"])

    return products, label_map


def fetch_products_json(conn):
    products = conn.execute(
        "SELECT id, name, category, price, description, image FROM products ORDER BY id DESC"
    ).fetchall()

    label_rows = conn.execute(
        """
        SELECT pl.product_id, l.name
        FROM product_labels pl
        JOIN labels l ON l.id = pl.label_id
        ORDER BY l.name
        """
    ).fetchall()

    label_map = {}
    for r in label_rows:
        label_map.setdefault(r["product_id"], []).append(r["name"])

    out = []
    for p in products:
        out.append(
            {
                "id": p["id"],
                "name": p["name"],
                "category": p["category"],
                "price": float(p["price"]),
                "description": p["description"] or "",
                "image": p["image"] or "",
                "labels": label_map.get(p["id"], []),
            }
        )
    return out


def fetch_one_product_json(conn, product_id: int):
    p = conn.execute(
        "SELECT id, name, category, price, description, image FROM products WHERE id=?",
        (product_id,),
    ).fetchone()
    if not p:
        return None

    labels = conn.execute(
        """
        SELECT l.name
        FROM product_labels pl
        JOIN labels l ON l.id = pl.label_id
        WHERE pl.product_id=?
        ORDER BY l.name
        """,
        (product_id,),
    ).fetchall()

    return {
        "id": p["id"],
        "name": p["name"],
        "category": p["category"],
        "price": float(p["price"]),
        "description": p["description"] or "",
        "image": p["image"] or "",
        "labels": [r["name"] for r in labels],
    }


# -----------------------
# Public Pages
# -----------------------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/menu")
def menu_page():
    # Menu page MUST load from /api/products using JS (no hardcoded list)
    return render_template("menu.html")


@app.route("/contact")
def contact_page():
    return render_template("contact.html")


@app.route("/product/<int:product_id>")
def product_detail_page(product_id):
    # Page fallback (if you prefer new page instead of popup)
    conn = get_conn()
    product = fetch_one_product_json(conn, product_id)
    conn.close()
    if not product:
        abort(404)
    return render_template("product_detail.html", product=product)


# -----------------------
# API
# -----------------------

@app.route("/api/products", methods=["GET"])
def api_products():
    conn = get_conn()
    data = fetch_products_json(conn)
    conn.close()
    return jsonify(data)


@app.route("/api/products/<int:product_id>", methods=["GET"])
def api_product_detail(product_id):
    conn = get_conn()
    product = fetch_one_product_json(conn, product_id)
    conn.close()
    if not product:
        return jsonify({"error": "not_found"}), 404
    return jsonify(product)


# -----------------------
# Admin - Pages
# -----------------------

CATEGORIES = ["Coffee", "Tea", "Cold Drinks", "Desserts"]


@app.route("/admin", methods=["GET"])
def admin_panel():
    conn = get_conn()
    labels = fetch_labels(conn)
    products, product_labels = fetch_products_for_admin(conn)
    conn.close()

    return render_template(
        "admin.html",
        labels=labels,
        products=products,
        product_labels=product_labels,
    )


@app.route("/admin/products/new", methods=["GET"])
def admin_new_product():
    conn = get_conn()
    labels = fetch_labels(conn)
    conn.close()
    return render_template(
        "admin_product_form.html",
        mode="create",
        product=None,
        product_labels=[],
        labels=labels,
        categories=CATEGORIES,
    )


@app.route("/admin/products/<int:product_id>/edit", methods=["GET"])
def admin_edit_product(product_id):
    conn = get_conn()
    product = conn.execute(
        "SELECT id, name, price, description, image, category FROM products WHERE id = ?",
        (product_id,),
    ).fetchone()

    if not product:
        conn.close()
        abort(404)

    labels = fetch_labels(conn)
    rows = conn.execute(
        """
        SELECT l.name
        FROM product_labels pl
        JOIN labels l ON l.id = pl.label_id
        WHERE pl.product_id = ?
        ORDER BY l.name
        """,
        (product_id,),
    ).fetchall()
    conn.close()

    product_labels = [r["name"] for r in rows]

    return render_template(
        "admin_product_form.html",
        mode="edit",
        product=product,
        product_labels=product_labels,
        labels=labels,
        categories=CATEGORIES,
    )


# -----------------------
# Admin - Actions
# -----------------------

@app.route("/admin/labels/add", methods=["POST"])
def admin_add_label():
    name = (request.form.get("label_name") or "").strip()
    if not name:
        return redirect(url_for("admin_panel"))

    conn = get_conn()
    try:
        conn.execute("INSERT INTO labels (name) VALUES (?)", (name,))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    finally:
        conn.close()

    return redirect(url_for("admin_panel"))


@app.route("/admin/labels/<int:label_id>/delete", methods=["POST"])
def admin_delete_label(label_id):
    conn = get_conn()
    conn.execute("DELETE FROM product_labels WHERE label_id = ?", (label_id,))
    conn.execute("DELETE FROM labels WHERE id = ?", (label_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("admin_panel"))


def save_uploaded_image(file_storage):
    if not file_storage or file_storage.filename == "":
        return ""

    filename = secure_filename(file_storage.filename)
    if not allowed_file(filename):
        return ""

    ext = filename.rsplit(".", 1)[1].lower()
    new_name = f"{int(time.time())}_{os.getpid()}.{ext}"
    full_path = os.path.join(UPLOAD_DIR, new_name)
    file_storage.save(full_path)

    return f"/static/images/uploads/{new_name}"


@app.route("/admin/products/create", methods=["POST"])
def admin_create_product():
    name = (request.form.get("name") or "").strip()
    price_raw = (request.form.get("price") or "").strip()
    description = (request.form.get("description") or "").strip()
    category = (request.form.get("category") or "").strip()

    if not name or not price_raw or not category:
        return redirect(url_for("admin_new_product"))

    try:
        price = float(price_raw)
    except ValueError:
        return redirect(url_for("admin_new_product"))

    image_path = ""
    if "image_file" in request.files:
        image_path = save_uploaded_image(request.files["image_file"])

    selected_labels = request.form.getlist("labels")

    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO products (name, price, description, image, category)
        VALUES (?, ?, ?, ?, ?)
        """,
        (name, price, description, image_path, category),
    )
    product_id = cur.lastrowid

    for label_name in selected_labels:
        row = cur.execute("SELECT id FROM labels WHERE name = ?", (label_name,)).fetchone()
        if row:
            cur.execute(
                "INSERT OR IGNORE INTO product_labels (product_id, label_id) VALUES (?, ?)",
                (product_id, row["id"]),
            )

    conn.commit()
    conn.close()

    return redirect(url_for("admin_panel"))


@app.route("/admin/products/<int:product_id>/update", methods=["POST"])
def admin_update_product(product_id):
    name = (request.form.get("name") or "").strip()
    price_raw = (request.form.get("price") or "").strip()
    description = (request.form.get("description") or "").strip()
    category = (request.form.get("category") or "").strip()

    if not name or not price_raw or not category:
        return redirect(url_for("admin_edit_product", product_id=product_id))

    try:
        price = float(price_raw)
    except ValueError:
        return redirect(url_for("admin_edit_product", product_id=product_id))

    selected_labels = request.form.getlist("labels")

    conn = get_conn()
    cur = conn.cursor()

    existing = cur.execute(
        "SELECT id, image FROM products WHERE id = ?",
        (product_id,),
    ).fetchone()
    if not existing:
        conn.close()
        abort(404)

    image_path = existing["image"] or ""
    if "image_file" in request.files and request.files["image_file"].filename:
        new_path = save_uploaded_image(request.files["image_file"])
        if new_path:
            image_path = new_path

    cur.execute(
        """
        UPDATE products
        SET name = ?, price = ?, description = ?, image = ?, category = ?
        WHERE id = ?
        """,
        (name, price, description, image_path, category, product_id),
    )

    cur.execute("DELETE FROM product_labels WHERE product_id = ?", (product_id,))
    for label_name in selected_labels:
        row = cur.execute("SELECT id FROM labels WHERE name = ?", (label_name,)).fetchone()
        if row:
            cur.execute(
                "INSERT OR IGNORE INTO product_labels (product_id, label_id) VALUES (?, ?)",
                (product_id, row["id"]),
            )

    conn.commit()
    conn.close()

    return redirect(url_for("admin_panel"))


@app.route("/admin/products/<int:product_id>/delete", methods=["POST"])
def admin_delete_product(product_id):
    conn = get_conn()
    conn.execute("DELETE FROM product_labels WHERE product_id = ?", (product_id,))
    conn.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("admin_panel"))


if __name__ == "__main__":
    app.run(debug=True)
