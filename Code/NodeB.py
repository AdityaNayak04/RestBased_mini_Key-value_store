# node_b.py
from flask import Flask, request, jsonify

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET,PUT,POST,OPTIONS"
    return response


store = {}

def log(msg):
    print(f"[Node B] {msg}")

@app.route("/key/<key>", methods=["PUT"])
def put_key(key):
    data = request.get_json(silent=True) or {}
    if "value" not in data:
        log(f"PUT /key/{key} missing value")
        return jsonify(error="missing 'value' in JSON body"), 400

    value = data["value"]
    log(f"PUT /key/{key} value={value}")

    # Simulate failure
    if value == "__fail__":
        log(f"Simulating failure for key={key}")
        return jsonify(error="simulated failure on Node B"), 500

    store[key] = value
    log(f"Stored key={key} value={value}")

    return jsonify(status="ok", node="B", key=key, value=value), 200

@app.route("/key/<key>", methods=["GET"])
def get_key(key):
    if key not in store:
        log(f"GET /key/{key} → NOT FOUND")
        return jsonify(error="not found on Node B"), 404

    log(f"GET /key/{key} → {store[key]}")
    return jsonify(node="B", key=key, value=store[key]), 200

@app.route("/health", methods=["GET"])
def health():
    return jsonify(node="B", status="up"), 200

if __name__ == "__main__":
    log("Starting Node B on port 5001")
    app.run(host="0.0.0.0", port=5001)
