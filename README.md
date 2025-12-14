# Cafe Management System (Flask + HTML/CSS/JS + AI Assistant)

## Project Overview
This project is a cafe website with a menu page and an AI Menu Assistant.
- Frontend: HTML, CSS, JavaScript
- Backend: Python (Flask)
- AI Module: rule-based NLP intent detection + recommendation engine

## Folder Structure
- `frontend/templates/` : HTML templates (Jinja2)
- `frontend/static/` : CSS / JS / images
- `backend/app.py` : Flask backend (routes + API)
- `backend/ai/` : AI modules (`nlp_model.py`, `recommendation.py`, `menu.py`)

## Features
- Menu listing with categories
- Client-side filtering (Coffee / Tea / Cold Drinks / Desserts)
- AI Menu Assistant:
  - diet / low calorie suggestions
  - vegan suggestions
  - sugar-free suggestions
  - allergy filtering (e.g., no milk, no lemon, no nuts)

## How to Run (Windows PowerShell)
1. Go to backend folder:
   ```powershell
   cd .\backend
   python app.py