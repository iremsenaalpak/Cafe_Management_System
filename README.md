# Cafe Management System (AI-Powered)

İrem Sena Alpak & Asude Doğan

A modern, full-stack cafe management website featuring a dynamic menu, an admin dashboard for product management, and a smart AI Assistant integrated with OpenAI's GPT-3.5 to provide personalized recommendations.

##  Features

### AI Menu Assistant
-   **Smart Recommendations**: Chat with the AI to get suggestions based on your mood or preferences.
-   **Dietary Awareness**: Intelligently handles requests for Vegan, Sugar-free, or specific allergen-free items (e.g., "No nuts").
-   **Contextual**: Uses real-time menu data to ensure recommendations are always in stock.
-   **Powered by GPT**: Integrated using the OpenAI API for natural, conversational interactions.

### Admin Dashboard
-   **Secure Access**: Protected by an Admin Key.
-   **Product Management**: Add, Edit, and Delete menu items.
-   **Label Management**: Create and manage dietary labels (e.g., Vegan, Gluten-Free).
-   **Notifications**: View and resolve customer messages sent via the Contact page.
-   **Image Uploads**: Upload product images directly from the dashboard.

### Dynamic Menu
-   **Real-time Updates**: Menu items fetched directly from the SQLite database.
-   **Categorization**: Browsable categories (Coffee, Tea, Cold Beverages, Desserts).
-   **Visuals**: Rich display with images, prices, and dietary labels.

##  Tech Stack

-   **Backend**: Python (Flask)
-   **Database**: SQLite
-   **AI Engine**: OpenAI API (GPT-3.5 Turbo)
-   **Frontend**: HTML5, CSS3, JavaScript (Vanilla)

```

## Installation & Setup

### Prerequisites
-   Python 3.8+
-   An OpenAI API Key

### 1. Clone & Setup Directory
```bash
git clone <repository-url>
cd <repository-folder>
```

### 2. Install Dependencies
Navigate to the root directory where `requirements.txt` is located:
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
Create a `.env` file in the root directory (or inside `backend/` depending on where you run it) and add your OpenAI API Key:
```
OPENAI_API_KEY=sk-your-api-key-here
```

### 4. Run the Application
Navigate to the backend folder and start the Flask server:
```bash
cd backend
python app.py
```


##  Usage

-   **Home**: Landing page with cafe ambience.
-   **Menu**: View products and chat with the AI Assistant (`Ask AI` button).
-   **Admin Panel**: Access via `/admin?key=1234` (Default Key: `1234`).
-   **Contact**: Send messages to the admin.

