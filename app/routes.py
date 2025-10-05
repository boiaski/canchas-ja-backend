from flask import Blueprint, request, jsonify
import re

main = Blueprint('main', __name__)

# Armazenamento em memória para itens (exemplo mock)
items = []

@main.route("/")
def home():
    return "Backend funcionando!"

def validar_email_senha(email, senha):
    # Regex simples para validar email
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

    # ... lógica de autenticação ...
    return jsonify({"message": "Login válido!"})

@main.route("/api/v1/signin", methods=["POST"])
def signin():
    # Aqui você vai receber os dados de cadastro
    data = request.json
    return jsonify({"message": "Signin endpoint", "data": data})

# === USER ENDPOINTS ===
@main.route("/api/v1/user", methods=["GET"])
def get_user():
    # Aqui você retorna os dados do usuário
    return jsonify({"message": "User endpoint"})

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

# === EXEMPLO DE ENDPOINT PARA CRIAÇÃO DE ITEM MOCK ===
@main.route("/api/items", methods=["POST"])
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

# Endpoint para listar todos os itens
@main.route("/api/items", methods=["GET"])
def get_items():
    return jsonify(items)

# Endpoint para atualizar um item
@main.route("/api/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    data = request.get_json()
    item = next((item for item in items if item["id"] == item_id), None)
    
    if item is None:
        return jsonify({"error": "Item não encontrado"}), 404

    item["name"] = data.get("name", item["name"])
    item["description"] = data.get("description", item["description"])
    
    return jsonify(item)

# Endpoint para deletar um item
@main.route("/api/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    global items
    items = [item for item in items if item["id"] != item_id]
    return jsonify({"message": "Item deletado"}), 200