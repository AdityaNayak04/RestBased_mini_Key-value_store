# node_a.py
from flask import Flask, request, jsonify
import requests

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
replication_status = {}
REPLICA_BASE_URL = "http://localhost:5001"

def log(msg):
    print(f"[Node A] {msg}")

@app.route("/key/<key>", methods=["PUT"])
def put_key(key):
    data = request.get_json(silent=True) or {}
    if "value" not in data:
        log(f"PUT /key/{key} missing value")
        return jsonify(error="missing 'value' in JSON body"), 400

    value = data["value"]

    # 1) Local update
    log(f"PUT /key/{key}")
    store[key] = value
    log(f"Local store updated: {key} = {value}")

    # 2) Replicate to Node B
    log(f"Attempting replication → Node B...")
    try:
        resp = requests.put(
            f"{REPLICA_BASE_URL}/key/{key}",
            json={"value": value},
            timeout=2
        )

        if 200 <= resp.status_code < 300:
            log(f"Replica response: {resp.status_code} OK")
            log(f"Replication SUCCESS for {key}")

            replication_status[key] = {
                "status": "replicated",
                "detail": f"replica returned {resp.status_code}"
            }

            return jsonify(
                node="A",
                key=key,
                value=value,
                replication="replicated"
            ), 200

        else:
            log(f"Replica returned {resp.status_code}: FAILURE")
            replication_status[key] = {
                "status": "replication_failed",
                "detail": f"replica returned {resp.status_code}: {resp.text}"
            }

            return jsonify(
                node="A",
                key=key,
                value=value,
                replication="replication_failed",
                error="replica responded with error"
            ), 502

    except requests.RequestException as e:
        # handle timeout / connection refused
        log(f"Replication ERROR: {e}")
        log(f"Replication FAILED for {key}")

        replication_status[key] = {
            "status": "replication_failed",
            "detail": str(e)
        }

        return jsonify(
            node="A",
            key=key,
            value=value,
            replication="replication_failed",
            error="could not reach replica"
        ), 502

@app.route("/key/<key>", methods=["GET"])
def get_key(key):
    if key not in store:
        log(f"GET /key/{key} → NOT FOUND")
        return jsonify(error="not found on Node A"), 404

    log(f"GET /key/{key} → {store[key]}")
    return jsonify(node="A", key=key, value=store[key]), 200

@app.route("/status/<key>", methods=["GET"])
def get_status(key):
    info = replication_status.get(key)
    if not info:
        log(f"STATUS /{key} → no replication info")
        return jsonify(error="no replication info for this key"), 404

    log(f"STATUS /{key} → {info['status']}")
    return jsonify(key=key, status=info["status"], detail=info["detail"]), 200

@app.route("/health", methods=["GET"])
def health():
    return jsonify(node="A", status="up"), 200

if __name__ == "__main__":
    log("Starting Node A on port 5000")
    app.run(host="0.0.0.0", port=5000)
