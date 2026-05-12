import os
import json

DATA_DIR = 'data/wishlists'

def add_to_wishlist(user_id, product_name):
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    path = f"{DATA_DIR}/{user_id}.json"
    wishlist = []
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            wishlist = json.load(f)
    
    wishlist.append(product_name)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(wishlist, f, ensure_ascii=False)
    return f"已將 {product_name} 加入您的願望清單！"

def view_wishlist(user_id):
    path = f"{DATA_DIR}/{user_id}.json"
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            wishlist = json.load(f)
        return "您的願望清單：\n" + "\n".join(wishlist)
    return "您的願望清單目前是空的。"
