from flask import Flask, request, jsonify
import hashlib
from datetime import date

app = Flask(__name__)

# ==========================
# CONFIG LICENCES
# ==========================
SALT = "SVT_BAC_2026"

# Licences autorisées (exemple)
# machine_hash : date_expiration
LICENCES = {
    # Exemple de machine autorisée
    # "hash_machine": "2027-12-31"
}

# ==========================
# OUTILS
# ==========================
def hash_text(txt):
    return hashlib.sha256((SALT + txt).encode()).hexdigest()

def licence_valide(machine):
    today = date.today()
    exp = LICENCES.get(machine)
    if not exp:
        return False, "Machine non autorisée"
    try:
        exp_date = date.fromisoformat(exp)
        if today > exp_date:
            return False, "Licence expirée"
        return True, "Licence valide"
    except ValueError:
        return False, "Licence corrompue"

# ==========================
# ROUTE DE VÉRIFICATION
# ==========================
@app.route("/verify")
def verify():
    machine = request.args.get("machine", "")
    app_name = request.args.get("app", "")

    if not machine or not app_name:
        return jsonify(valid=False, message="Requête invalide")

