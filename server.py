from flask import Flask, request, jsonify
from datetime import date
import os

app = Flask(__name__)

# ==================================================
# BASE DE LICENCES (exemple)
# ==================================================
LICENCES = {
    "SVT-2026-TEST-0001": {"exp": "2027-12-31", "machine": None},
    "SVT-2026-TEST-0002": {"exp": "2027-12-31", "machine": None}
}

# ==================================================
@app.route("/")
def home():
    return "Activation server running"

# ==================================================
@app.route("/activate", methods=["POST"])
def activate():
    data = request.get_json(silent=True)
    if not data:
        return jsonify(ok=False, message="Invalid request")

    key = data.get("key")
    machine = data.get("machine")

    if not key or not machine:
        return jsonify(ok=False, message="Missing key or machine")

    licence = LICENCES.get(key)
    if not licence:
        return jsonify(ok=False, message="Invalid license key")

    if date.today() > date.fromisoformat(licence["exp"]):
        return jsonify(ok=False, message="License expired")

    if licence["machine"] is None:
        licence["machine"] = machine
        return jsonify(ok=True, message="Activation successful")

    if licence["machine"] != machine:
        return jsonify(ok=False, message="Key already used on another machine")

    return jsonify(ok=True, message="License already active on this machine")

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
