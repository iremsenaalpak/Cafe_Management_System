from flask import Flask, render_template

app = Flask(__name__)

# örnek menü verisi 
menu_items = [
    {"name": "Latte", "price": 80, "category": "kahve", "desc": "Yumuşak içim sütlü kahve", "img": "latte.jpg"},
    {"name": "Espresso", "price": 50, "category": "kahve", "desc": "Yoğun ve sert lezzet", "img": "espresso.jpg"},
    {"name": "Cheesecake", "price": 120, "category": "tatli", "desc": "Limonlu taze cheesecake", "img": "cheesecake.jpg"},
    {"name": "Çay", "price": 30, "category": "sicak", "desc": "Taze demlenmiş Türk çayı", "img": "cay.jpg"}
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/menu')
def menu():
    return render_template('menu.html', items=menu_items)

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/contact')
def contact():
    return render_template('contact.html')