import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_cors import CORS
from ai.nlp_model import analyze_text
from ai.recommendation import get_recommendation

# Path configurations
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "frontend"))
TEMPLATE_DIR = os.path.join(FRONTEND_DIR, "templates")
STATIC_DIR = os.path.join(FRONTEND_DIR, "static")
DB_PATH = os.path.join(BASE_DIR, "cafe.db")

# Admin security and constants
ADMIN_KEY = "1234"
# Categories updated to match frontend menu buttons
CATEGORIES = ["Coffee", "Tea", "Cold Beverages", "Desserts"]

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
# Enable CORS for frontend-backend communication (Fixes Chatbot connection issues)
CORS(app)

def get_conn():
    """Establish a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# --- AI ASSISTANT API ---
@app.route("/api/ai-assistant", methods=["POST"])
def ai_assistant():
    """Handle chatbot requests and provide AI-based product recommendations."""
    try:
        data = request.json
        user_message = data.get("message", "")
        
        # Analyze user message intent
        intent = analyze_text(user_message)
        
        # Fetch all products and their associated labels from DB
        conn = get_conn()
        products_raw = conn.execute("SELECT * FROM products").fetchall()
        products_list = []
        for p in products_raw:
            p_dict = dict(p)
            label_rows = conn.execute(
                "SELECT l.name FROM product_labels pl JOIN labels l ON l.id = pl.label_id WHERE pl.product_id = ?",
                (p_dict['id'],)
            ).fetchall()
            p_dict['labels'] = [row['name'] for row in label_rows]
            products_list.append(p_dict)
        conn.close()

        # Get filtered recommendations based on AI analysis
        recommendations = get_recommendation(intent, products_list)
        
        return jsonify({
            "status": "success",
            "recommendations": recommendations
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# --- ADMIN DASHBOARD ---
@app.route("/admin")
def admin_panel():
    """Render the main admin panel with labels, products, and notifications."""
    key = request.args.get("key")
    if key != ADMIN_KEY: abort(403)
    conn = get_conn()
    labels = conn.execute("SELECT * FROM labels ORDER BY name").fetchall()
    products = conn.execute("SELECT * FROM products ORDER BY id DESC").fetchall()
    notifications = conn.execute("SELECT * FROM notifications ORDER BY created_at DESC").fetchall()
    conn.close()
    return render_template("admin.html", labels=labels, products=products, notifications=notifications, admin_key=ADMIN_KEY)

# --- PRODUCT CRUD OPERATIONS ---
@app.route("/admin/products/new")
def admin_new_product():
    """Display the form to create a new product."""
    key = request.args.get("key")
    if key != ADMIN_KEY: abort(403)
    conn = get_conn()
    labels = conn.execute("SELECT * FROM labels ORDER BY name").fetchall()
    conn.close()
    return render_template("admin_product_form.html", mode="new", labels=labels, categories=CATEGORIES, admin_key=ADMIN_KEY)

@app.route("/admin/products/create", methods=["POST"])
def admin_create_product():
    """Save a new product and its labels to the database."""
    key = request.form.get("key")
    if key != ADMIN_KEY: abort(403)
    conn = get_conn()
    cursor = conn.execute("INSERT INTO products (name, price, category, description) VALUES (?, ?, ?, ?)",
                         (request.form.get("name"), request.form.get("price"), request.form.get("category"), request.form.get("description")))
    product_id = cursor.lastrowid
    # Link selected labels to the new product
    for lname in request.form.getlist("labels"):
        lrow = conn.execute("SELECT id FROM labels WHERE name = ?", (lname,)).fetchone()
        if lrow: conn.execute("INSERT INTO product_labels (product_id, label_id) VALUES (?, ?)", (product_id, lrow['id']))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_panel', key=ADMIN_KEY))

@app.route("/admin/products/edit/<int:product_id>")
def admin_edit_product(product_id):
    """Fetch product data and display the edit form."""
    key = request.args.get("key")
    if key != ADMIN_KEY: abort(403)
    conn = get_conn()
    product = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
    labels = conn.execute("SELECT * FROM labels ORDER BY name").fetchall()
    p_labels = conn.execute("SELECT l.name FROM product_labels pl JOIN labels l ON l.id = pl.label_id WHERE pl.product_id = ?", (product_id,)).fetchall()
    conn.close()
    return render_template("admin_product_form.html", mode="edit", product=product, labels=labels, product_labels=[x['name'] for x in p_labels], categories=CATEGORIES, admin_key=ADMIN_KEY)

@app.route("/admin/products/update/<int:product_id>", methods=["POST"])
def admin_update_product(product_id):
    """Update existing product details and refresh label associations."""
    key = request.form.get("key")
    if key != ADMIN_KEY: abort(403)
    conn = get_conn()
    conn.execute("UPDATE products SET name=?, price=?, category=?, description=? WHERE id=?",
                (request.form.get("name"), request.form.get("price"), request.form.get("category"), request.form.get("description"), product_id))
    # Delete old labels and insert new ones
    conn.execute("DELETE FROM product_labels WHERE product_id = ?", (product_id,))
    for lname in request.form.getlist("labels"):
        lrow = conn.execute("SELECT id FROM labels WHERE name = ?", (lname,)).fetchone()
        if lrow: conn.execute("INSERT INTO product_labels (product_id, label_id) VALUES (?, ?)", (product_id, lrow['id']))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_panel', key=ADMIN_KEY))

@app.route("/admin/products/delete/<int:product_id>", methods=["POST"])
def admin_delete_product(product_id):
    """Remove a product and its label associations from the database."""
    key = request.args.get("key")
    if key != ADMIN_KEY: abort(403)
    conn = get_conn()
    conn.execute("DELETE FROM product_labels WHERE product_id = ?", (product_id,))
    conn.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_panel', key=ADMIN_KEY))

# --- SYSTEM ACTIONS ---
@app.route("/admin/add_label", methods=["POST"])
def admin_add_label():
    """Add a new global tag/label for products."""
    key = request.args.get("key")
    if key != ADMIN_KEY: abort(403)
    conn = get_conn()
    conn.execute("INSERT OR IGNORE INTO labels (name) VALUES (?)", (request.form.get("label_name"),))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_panel', key=ADMIN_KEY))

@app.route("/admin/resolve_notification/<int:msg_id>", methods=["POST"])
def admin_resolve_notification(msg_id):
    """Delete a customer message/notification once handled."""
    key = request.args.get("key")
    if key != ADMIN_KEY: abort(403)
    conn = get_conn()
    conn.execute("DELETE FROM notifications WHERE id = ?", (msg_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_panel', key=ADMIN_KEY))

# --- FRONTEND ROUTES ---
@app.route("/contact", methods=["GET", "POST"])
def contact_page():
    """Display contact page and handle form submissions for notifications."""
    if request.method == "POST":
        conn = get_conn()
        conn.execute("INSERT INTO notifications (full_name, email, category, message) VALUES (?, ?, ?, ?)",
                     (request.form.get("name"), request.form.get("email"), request.form.get("category"), request.form.get("message")))
        conn.commit()
        conn.close()
        return redirect(url_for('contact_page'))
    return render_template("contact.html")

@app.route("/")
def home():
    """Render landing page."""
    return render_template("index.html")

@app.route("/menu")
def menu_page():
    """Render menu display page."""
    return render_template("menu.html")

@app.route("/api/products")
def api_products():
    """API endpoint to fetch all products for the frontend menu."""
    conn = get_conn()
    products = [dict(p) for p in conn.execute("SELECT * FROM products").fetchall()]
    for p in products:
        labels = conn.execute("SELECT l.name FROM product_labels pl JOIN labels l ON l.id = pl.label_id WHERE pl.product_id = ?", (p['id'],)).fetchall()
        p['labels'] = [row['name'] for row in labels]
    conn.close()
    return jsonify(products)

if __name__ == "__main__":
    # Start the Flask development server on port 5000
    app.run(debug=True, port=5000)