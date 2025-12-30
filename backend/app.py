import os
import sqlite3
import json
import openai
from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

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
CORS(app)

def get_conn():
    """Establish a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# --- AI ASSISTANT API (GPT Integration) ---
@app.route("/api/ai-suggest", methods=["POST"])
def ai_suggest():
    """Handle chatbot requests using OpenAI GPT."""
    try:
        data = request.json
        user_message = data.get("message", "")
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        # Fetch all products to give context to GPT
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

        # Construct System Prompt
        system_prompt = f"""
You are the AI Assistant for 'Caffe HUB'. 
You are friendly, helpful, and knowledgeable about the menu.
Your goal is to recommend products based on user preferences.
If a product does not have a specific label but you know it matches the user's request (e.g. 'Coffee' usually has caffeine, 'Fruit' is vegan), you can infer it.

MENU DATA:
{json.dumps(products_list, ensure_ascii=False)}

INSTRUCTIONS:
1. Analyze the user's message.
2. Recommend items from the MENU DATA that match the request.
3. If the user has restrictions (e.g. vegan, sugar-free), STRICTLY respect them. Check 'labels' first. If labels are missing, use your general knowledge to infer safety (e.g. Black Tea is vegan).
4. Return the response in strictly Valid JSON format with this structure:
{{
  "reply": "Your conversational response here...",
  "recommendations": {{
      "coffee": [List of match objects...],
      "tea": [...],
      "cold": [...],
      "sweet": [...]
  }}
}}
The 'recommendations' object keys must map to your best categorization.
Only include products that actually exist in the MENU DATA.
"""

        # New OpenAI API (v1.0+)
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7
        )

        content = response.choices[0].message.content
        
        # Attempt to parse JSON from GPT response
        try:
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]
            
            parsed_response = json.loads(content.strip())
            return jsonify(parsed_response)
        except json.JSONDecodeError:
            return jsonify({
                "reply": content,
                "recommendations": {}
            })

    except Exception as e:
        print(f"AI Error: {e}")
        return jsonify({"error": str(e)}), 500

# --- ADMIN DASHBOARD ---
@app.route("/admin")
def admin_panel():
    """Render the main admin panel with labels, products, and notifications."""
    key = request.args.get("key")
    if key != ADMIN_KEY: abort(403)
    conn = get_conn()
    labels = conn.execute("SELECT * FROM labels ORDER BY name").fetchall()
    products = conn.execute("SELECT * FROM products ORDER BY id DESC").fetchall()
    notifications = conn.execute("SELECT * FROM notifications ORDER BY id DESC").fetchall()
    
    # We also need product_labels for the view
    product_labels = {}
    all_pl = conn.execute("SELECT p.name as p_name, p.id as p_id, l.name as l_name FROM product_labels pl JOIN products p ON p.id = pl.product_id JOIN labels l ON l.id = pl.label_id").fetchall()
    
    # Organize labels by product id for easier template rendering
    # The template uses product_labels.get(p["id"], [])
    product_labels_map = {}
    for row in all_pl:
        pid = row['p_id']
        if pid not in product_labels_map:
            product_labels_map[pid] = []
        product_labels_map[pid].append(row['l_name'])
        
    conn.close()
    conn.close()
    return render_template("admin.html", labels=labels, products=products, notifications=notifications, product_labels=product_labels_map, admin_key=ADMIN_KEY)

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
    
    # Handle Image Upload (basic implementation)
    image_file = request.files.get("image_file")
    image_path = ""
    if image_file and image_file.filename:
        filename = image_file.filename
        save_path = os.path.join(STATIC_DIR, "images", "uploads", filename)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        image_file.save(save_path)
        image_path = f"/static/images/uploads/{filename}"

    cursor = conn.execute("INSERT INTO products (name, price, category, description, image) VALUES (?, ?, ?, ?, ?)",
                         (request.form.get("name"), request.form.get("price"), request.form.get("category"), request.form.get("description"), image_path))
    product_id = cursor.lastrowid
    
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
    
    # Handle Image Upload
    image_file = request.files.get("image_file")
    if image_file and image_file.filename:
        filename = image_file.filename
        save_path = os.path.join(STATIC_DIR, "images", "uploads", filename)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        image_file.save(save_path)
        image_path = f"/static/images/uploads/{filename}"
        conn.execute("UPDATE products SET name=?, price=?, category=?, description=?, image=? WHERE id=?",
                    (request.form.get("name"), request.form.get("price"), request.form.get("category"), request.form.get("description"), image_path, product_id))
    else:
        conn.execute("UPDATE products SET name=?, price=?, category=?, description=? WHERE id=?",
                    (request.form.get("name"), request.form.get("price"), request.form.get("category"), request.form.get("description"), product_id))

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
    label_name = request.form.get("label_name")
    if label_name:
        conn = get_conn()
        conn.execute("INSERT OR IGNORE INTO labels (name) VALUES (?)", (label_name,))
        conn.commit()
        conn.close()
    return redirect(url_for('admin_panel', key=ADMIN_KEY))

@app.route("/admin/delete_label/<int:label_id>", methods=["POST"])
def admin_delete_label(label_id):
    """Delete a global label."""
    key = request.args.get("key")
    if key != ADMIN_KEY: abort(403)
    conn = get_conn()
    conn.execute("DELETE FROM labels WHERE id = ?", (label_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_panel', key=ADMIN_KEY))

# --- FRONTEND ROUTES ---
@app.route("/contact", methods=["GET", "POST"])
def contact_page():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        category = request.form.get("category")
        message = request.form.get("message")
        
        if name and message:
            conn = get_conn()
            conn.execute("INSERT INTO notifications (full_name, email, category, message) VALUES (?, ?, ?, ?)",
                         (name, email, category, message))
            conn.commit()
            conn.close()
            # Redirect to home or show success (simple redirect for now)
            return redirect(url_for('home'))
            
    return render_template("contact.html")
    
@app.route("/admin/notifications/resolve/<int:msg_id>", methods=["POST"])
def admin_resolve_notification(msg_id):
    """Delete a notification."""
    key = request.args.get("key")
    if key != ADMIN_KEY: abort(403)
    conn = get_conn()
    conn.execute("DELETE FROM notifications WHERE id = ?", (msg_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_panel', key=ADMIN_KEY))

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
    app.run(debug=True, port=5001)
