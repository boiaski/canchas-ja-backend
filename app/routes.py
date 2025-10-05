from flask import Blueprint, request, jsonify
import re

main = Blueprint('main', __name__)

# Armazenamento em memória para itens (exemplo mock)
items = []

@main.route("/")
def home():
    return "Backend funcionando!"

def validar_email_senha(email, senha):
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(email_regex, email):
        return False, "Email inválido."
    if not senha or len(senha) < 6:
        return False, "A senha deve ter pelo menos 6 caracteres."
    return True, ""

# === AUTH ENDPOINTS ===
@main.route("/api/v1/login", methods=["POST"])
def login():
    data = request.json
    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Email e senha são obrigatórios"}), 400

    valido, mensagem = validar_email_senha(data["email"], data["password"])
    if not valido:
        return jsonify({"error": mensagem}), 400

    # Simulação de autenticação
    return jsonify({"message": "Login válido!", "user": {"email": data["email"]}})

@main.route("/api/v1/signin", methods=["POST"])
def signin():
    data = request.json
    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Email e senha são obrigatórios"}), 400

    valido, mensagem = validar_email_senha(data["email"], data["password"])
    if not valido:
        return jsonify({"error": mensagem}), 400

    # Simulação de cadastro
    return jsonify({"message": "Usuário cadastrado com sucesso!", "user": {"email": data["email"]}})

# === USER ENDPOINTS ===
@main.route("/api/v1/user", methods=["GET"])
def get_user():
    # Simulação de usuário autenticado
    return jsonify({"user": {"id": 1, "email": "usuario@teste.com", "name": "Usuário Teste"}})

# === PRODUCT ENDPOINTS ===
@main.route("/api/v1/product", methods=["GET"])
def get_products():
    produtos_mock = [
        {
            "id": 1,
            "title": "Quadra Society Central",
            "location": "Centro",
            "price": 120,
            "image": "https://exemplo.com/imagem1.jpg",
            "rating": 4.8,
            "reviews": 32,
            "discount": 10
        },
        {
            "id": 2,
            "title": "Quadra Coberta Sul",
            "location": "Zona Sul",
            "price": 150,
            "image": "https://exemplo.com/imagem2.jpg",
            "rating": 4.5,
            "reviews": 21,
            "discount": 0
        }
    ]
    return jsonify(produtos_mock)

# === CRUD DE ITENS MOCK (PADRÃO /api/v1/) ===
@main.route("/api/v1/items", methods=["POST"])
def create_item():
    try:
        data = request.get_json()
        name = data.get("name")
        description = data.get("description")

        if not name or not description:
            return jsonify({"error": "Nome e descrição são obrigatórios"}), 400

        item = {
            "id": len(items) + 1,
            "name": name,
            "description": description
        }
        items.append(item)

        return jsonify(item), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route("/api/v1/items", methods=["GET"])
def get_items():
    return jsonify(items)

@main.route("/api/v1/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    data = request.get_json()
    item = next((item for item in items if item["id"] == item_id), None)
    
    if item is None:
        return jsonify({"error": "Item não encontrado"}), 404

    item["name"] = data.get("name", item["name"])
    item["description"] = data.get("description", item["description"])
    
    return jsonify(item)

@main.route("/api/v1/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    global items
    items = [item for item in items if item["id"] != item_id]
    return jsonify({"message": "Item deletado"}), 200