from flask import Flask, request, jsonify
from datetime import date
import os

app = Flask(__name__)

# ==================================================
# BASE DE DONNÉES SIMPLIFIÉE (CLÉS)
# (plus tard : vraie DB)
# ==================================================
LICENCES = {
    # clé : {"exp": "YYYY-MM-DD", "machine": None}
    "SVT-2026-TEST-0001": {"exp": "2027-12-31", "machine": None},
    "SVT-2026-TEST-0002": {"exp": "2027-12-31", "machine": None},
}

# ==================================================
@app.route("/")
def home():
    return "Serveur d’activation actif ✅"

# ==================================================
@app.route("/activate", methods=["POST"])
def activate():
    data = request.get_json()
    key = data.get("key")
    machine = data.get("machine")

    if not key or not machine:
        return jsonify(ok=False, message="Requête invalide")

    licence = LICENCES.get(key)
    if not licence:
        return jsonify(ok=False, message="Clé invalide")

    if date.today() > date.fromisoformat(licence["exp"]):
        return jsonify(ok=False, message="Clé expirée")

    if licence["machine"] is None:
        licence["machine"] = machine
        return jsonify(ok=True, message="Activation réussie ✅")

    if licence["machine"] != machine:
        return jsonify(ok=False, message="Clé déjà utilisée sur un autre PC")

    return jsonify(ok=True, message="Licence déjà activée sur ce PC")

# ==================================================
@app.route("/verify")
def verify():
    key = request.args.get("key")
    machine = request.args.get("machine")

    licence = LICENCES.get(key)
    if not licence:
        return jsonify(valid=False)

    if licence["machine"] != machine:
        return jsonify(valid=False)

    if date.today() > date.fromisoformat(licence["exp"]):
        return jsonify(valid=False)

    return jsonify(valid=True)

# ==================================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
