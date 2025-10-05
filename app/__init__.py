from flask import Blueprint, request, jsonify
from datetime import date

api_bp = Blueprint("api_v1", __name__)

# ----------------------
# Mock Data Generators
# ----------------------
def make_product(pid: int, *, discount=None):
    images = [
        "https://picsum.photos/seed/{}/640/360".format(pid),
        "https://picsum.photos/seed/{}_b/640/360".format(pid)
    ]
    base = {
        "id": str(pid),
        "images": images,
        "location": "Porto Alegre, RS",
        "address": "Av. Ipiranga, 1000",
        "dateRange": f"{date.today().isoformat()} - {date.today().isoformat()}",
        "price": round(50 + (pid % 7) * 10, 2),
        "rating": 3.5 + (pid % 15) / 10.0,
        "currency": "BRL",
    }
    if discount is not None:
        base["discount"] = discount
    return base

SPECIAL_DISCOUNTS = [make_product(i, discount=10 + (i % 3) * 5) for i in range(101, 107)]
BEST_RATED = [make_product(i) for i in range(201, 207)]
NEAR_YOU = [make_product(i) for i in range(301, 304)]

USERS = {
    "1": {
        "id": "1",
        "name": "Usuário Demo",
        "email": "demo@canchasja.com",
        "type": "C",
        "initials": "UD",
        "isLogin": True,
        "favorites": [SPECIAL_DISCOUNTS[0], BEST_RATED[1], NEAR_YOU[0]]
    }
}

# ----------------------
# Auth
# ----------------------
@api_bp.post("/login")
def login():
    body = request.get_json(silent=True) or {}
    email = (body.get("email") or "").strip().lower()
    password = (body.get("password") or "").strip()

    if not email or not password:
        return jsonify({"detail": "email e password são obrigatórios"}), 400

    user = USERS["1"].copy()
    user["email"] = email
    return jsonify({"user": user}), 200

@api_bp.post("/signin")
def signin():
    body = request.get_json(silent=True) or {}
    name = (body.get("name") or "").strip()
    email = (body.get("email") or "").strip().lower()
    password = (body.get("password") or "").strip()
    confirm = (body.get("confirmPassword") or "").strip()
    utype = (body.get("type") or "C").strip()

    if not name or not email or not password or not confirm:
        return jsonify({"detail": "Campos obrigatórios ausentes"}), 400
    if password != confirm:
        return jsonify({"detail": "As senhas não coincidem"}), 400

    new_id = str(len(USERS) + 1)
    USERS[new_id] = {
        "id": new_id,
        "name": name,
        "email": email,
        "type": utype,
        "initials": "".join([p[0] for p in name.split()[:2]]).upper(),
        "isLogin": True,
        "favorites": []
    }
    return jsonify({
        "id": new_id,
        "name": name,
        "email": email,
        "type": utype
    }), 200

# ----------------------
# User
# ----------------------
@api_bp.get("/user/<user_id>/favorite")
def user_favorites(user_id):
    user = USERS.get(user_id)
    if not user:
        return jsonify([]), 200
    return jsonify(user.get("favorites", [])), 200

# ----------------------
# Products
# ----------------------
@api_bp.get("/product/special_discount")
def product_special_discount():
    return jsonify(SPECIAL_DISCOUNTS), 200

@api_bp.get("/product/best_rated")
def product_best_rated():
    return jsonify(BEST_RATED), 200

@api_bp.get("/product/near_you")
def product_near_you():
    return jsonify(NEAR_YOU), 200
