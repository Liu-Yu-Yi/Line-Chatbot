import os
import json
import datetime

WISHLIST_DIR = "data/wishlists"

def load_wishlist(user_id):
    path = os.path.join(WISHLIST_DIR, f"{user_id}.json")
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_wishlist(user_id, wishlist):
    os.makedirs(WISHLIST_DIR, exist_ok=True)
    path = os.path.join(WISHLIST_DIR, f"{user_id}.json")
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(wishlist, f, ensure_ascii=False, indent=2)

def add_to_wishlist(user_id, product_name):
    wishlist = load_wishlist(user_id)
    wishlist.append({
        'name': product_name,
        'added_at': datetime.datetime.now().isoformat()
    })
    save_wishlist(user_id, wishlist)
    return f"已將 {product_name} 加入您的願望清單。"

def view_wishlist(user_id):
    wishlist = load_wishlist(user_id)
    if not wishlist:
        return "您的願望清單是空的。"
    text = "您的願望清單:\n"
    for i, item in enumerate(wishlist, 1):
        text += f"{i}. {item['name']}\n"
    return text
