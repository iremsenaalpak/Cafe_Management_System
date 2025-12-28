def _to_ai_category(db_category: str) -> str:
    """
    Maps DB category names to AI keys.
    """
    c = (db_category or "").strip().lower()
    
    if "coffee" in c: return "coffee"
    if "tea" in c: return "tea"
    if "cold" in c or "beverage" in c: return "cold"
    if "dessert" in c or "sweet" in c or "cake" in c: return "sweet"
    return "other"

def get_recommendation(intent: dict, products: list) -> list:
    """
    Main logic to filter products based on AI intent and exclusions.
    """
    recommendations = []
    exclude_list = [x.lower() for x in intent.get("exclude_labels", [])]
    target_categories = intent.get('categories', [])

    for p in products:
        # 1. Category Filter
        db_cat = p.get('category', "")
        ai_cat = _to_ai_category(db_cat)
        
        if target_categories and (ai_cat not in target_categories):
            continue
            
        # 2. Ingredient Exclusion Check
        product_labels = [l.lower() for l in p.get('labels', [])]
        if any(forbidden in product_labels for forbidden in exclude_list):
            continue
            
        # 3. Dietary Preferences Check
        if intent.get("vegan") and "vegan" not in product_labels:
            continue
            
        if intent.get("sugar_free"):
            if "sugar free" not in product_labels and "sekersiz" not in product_labels:
                continue

        if intent.get("low_calorie") and "low calorie" not in product_labels:
            continue

        recommendations.append(p)
        
    return recommendations[:5]