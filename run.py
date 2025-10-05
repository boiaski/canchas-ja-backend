from app import create_app
from flask_cors import CORS  # Importando CORS

app = create_app()

# Configuração do CORS (permitindo todas as origens)
CORS(app)

if __name__ == "__main__":
    app.run(debug=True)
