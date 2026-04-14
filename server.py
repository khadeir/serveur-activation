from flask import Flask, request, jsonify
from datetime import date
import os

app = Flask(__name__)

# ==================================================
# LICENCES AUTORISÉES
# ==================================================
LICENCES = {
    # ✅ REMPLACE CETTE VALEUR PAR LE HASH DE TON PC
    "COLLE_ICI_LE_HASH_DE_TA_MACHINE": "2027-12-31"
}

# ==================================================
# ROUTES
# ==================================================
@app.route("/")
def home():
    return "Serveur de licence actif ✅"

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

# ==================================================
# LANCEMENT (OBLIGATOIRE POUR RAILWAY)
# ==================================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
``
