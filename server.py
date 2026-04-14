from flask import Flask, request, jsonify
from datetime import date
import os

app = Flask(__name__)

# ==========================
# LICENCES AUTORISÉES
# ==========================
LICENCES = {
    "TEST": "2027-12-31"  # temporaire pour test
}

@app.route("/")
def home():
    return "OK"

@app.route("/verify")
def verify():
    machine = request.args.get("machine")
    app_name = request.args.get("app")

    if not machine or not app_name:
        return jsonify(valid=False, message="Requête invalide")

    exp = LICENCES.get(machine)
    if not exp:
        return jsonify(valid=False, message="Machine non autorisée")

    if date.today() > date.fromisoformat(exp):
        return jsonify(valid=False, message="Licence expirée")

    return jsonify(valid=True, message="Licence valide")
``
