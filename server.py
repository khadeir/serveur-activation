from flask import Flask, request, jsonify

app = Flask(__name__)

# 🔑 Base de données simple
valid_keys = {
    "ABC123": False,
    "SVT-2026-001": False,
    "PROF-SVT-999": False
}

@app.route('/activate', methods=['POST'])
def activate():
    data = request.json
    key = data.get("key")

    if key in valid_keys:
        if not valid_keys[key]:
            valid_keys[key] = True  # clé utilisée
            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "error", "message": "Clé déjà utilisée"})
    
    return jsonify({"status": "error", "message": "Clé invalide"})

@app.route('/')
def home():
    return "Serveur actif ✔"

if __name__ == "__main__":
    app.run()