import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib
import os

# 1. Prepare Training Data using Pandas
# Adding various English and Turkish phrases to make the model robust
data = {
    "text": [
        "i am on a diet", "low calorie options", "i want to lose weight", "fit and healthy meals",
        "i am vegan", "no animal products", "plant-based milk please", "vegan friendly",
        "i have an allergy", "allergic to fruits", "strawberry allergy", "no nuts please",
        "diyetteyim", "zayıflamak istiyorum", "kalorisiz olsun", "vegan besleniyorum",
        "alerjim var", "meyve yemiyorum", "fıstığa alerjim var", "sugar free"
    ],
    "label": ["diet", "diet", "diet", "diet", "vegan", "vegan", "vegan", "vegan", "allergy", "allergy", "allergy", "allergy", "diet", "diet", "diet", "vegan", "allergy", "allergy", "allergy", "diet"]
}

df = pd.DataFrame(data)

# 2. Build Scikit-learn Pipeline
# Tfidf: Converts text into numerical vectors (NumPy arrays)
# LogisticRegression: Classifies the intent
model_pipeline = Pipeline([
    ('vectorizer', TfidfVectorizer()),
    ('classifier', LogisticRegression())
])

# 3. Train the Model
model_pipeline.fit(df['text'], df['label'])

# 4. Export the Model (The AI 'Brain' file for backend)
model_path = os.path.join(os.path.dirname(__file__), 'menu_ai_model.pkl')
joblib.dump(model_pipeline, model_path)

print(f"SUCCESS: AI Model trained and saved at '{model_path}'")