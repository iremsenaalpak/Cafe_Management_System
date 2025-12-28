Caffe HUB: Smart Menu & Management System
Students

İrem Sena Alpak – 210201030

Ayşe Asude Doğan – 220201044

Project Overview

Caffe HUB is a Smart Cafe Management System that optimizes customer experience with advanced AI solutions while meeting the operational needs of a modern business. The system provides business owners with the ability to manage menu contents, product tags, and customer feedback from a centralized panel. Its most notable feature is the integrated AI assistant (Caffe HUB Assistant), which offers personalized product recommendations by considering customers' specific preferences (e.g., vegan, diet, sugar-free) or sensitivities (e.g., allergen content filtering).

Project Requirements Compliance

This work meets the academic requirements of the course:

Frontend: Developed using HTML5, CSS3, and modern JavaScript, following responsive design principles.

Backend: Asynchronous API structure built with the Python-based Flask framework.

AI Integration: A Natural Language Processing (NLP) model is actively running on the backend to analyze user intent and constraints.

Source Control: The project development is managed with Git and stored on GitHub for continuous updates.

Core Features

AI-Powered Smart Assistant

Analyzes natural language commands such as "a dessert without fruits" or "lactose-free coffee" with high accuracy.

Intent Detection: Identifies what the user prefers and, particularly, what they want to avoid (exclude labels).

Personalized Recommendations: Matches user requests with product tags in the database in real-time.

Advanced Admin Dashboard

Centralized Management: Allows tracking of label management, product inventory, and notifications from a single screen.

Full CRUD Support: Provides a user-friendly interface for adding products, updating prices, changing categories, and deleting items.

Real-time Search: Offers fast search and filtering options based on product names.

Dynamic Menu & Label System

Synchronized Categories: Categories like "Coffee," "Tea," "Cold Beverages," and "Desserts" are fully synced with the backend.

Advanced Tagging: Products are tagged with labels such as Vegan, Sugar-Free, Gluten-Free, allowing the AI model to be enriched.

Technologies Used
Layers

Frontend: HTML5, CSS3, JavaScript (ES6), FontAwesome

Backend: Python, Flask, Flask-CORS, SQLite

AI / Machine Learning: Scikit-learn, Joblib, NLP (Regex & ML Logic)

Tools

Git

GitHub

How to Run the Project

Install Dependencies:

pip install flask flask-cors joblib scikit-learn


Start the Server:

python backend/app.py


Access the System:

User Interface: http://127.0.0.1:5000/

Admin Panel: http://127.0.0.1:5000/admin?key=1234