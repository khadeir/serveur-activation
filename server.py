from flask import Flask, request, jsonify
from datetime import date
import os
import sys

app = Flask(__name__)

# =========================
# LICENCES AUTORISÉES
# =========================
LICENCES = {
    # ⚠️ remplace cette valeur par le hash machine
    "TEST": "2027-12-31"
}

@app.route("/")
def home():
    return "OK", 200

@app.route("/verify")
def verify():
    machine = request.args.get("machine")
    app_name = request.args.get("app")

    if not machine:
        return jsonify(valid=False, message="machine manquante")

    exp = LICENCES.get(machine)
    if not exp:
        return jsonify(valid=False, message="machine non autorisée")

    if date.today() > date.fromisoformat(exp):
        return jsonify(valid=False, message="licence expirée")

    return jsonify(valid=True, message="licence valide")

# =========================
# POINT CRITIQUE RAILWAY
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print(f"Listening on port {port}", flush=True)
    app.run(host="0.0.0.0", port=port)
``
