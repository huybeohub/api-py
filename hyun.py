from flask import Flask, request, jsonify
import time

app = Flask(__name__)
boss_data = []

@app.route("/add", methods=["POST"])
def add():
    data = request.json

    boss = {
        "boss": data["boss"],
        "jobId": data["jobId"],
        "placeId": data["placeId"],
        "time": time.time()
    }

    # tránh trùng server
    for b in boss_data:
        if b["jobId"] == boss["jobId"]:
            return {"status": "duplicate"}

    boss_data.append(boss)
    return {"status": "ok"}

@app.route("/get", methods=["GET"])
def get():
    now = time.time()

    valid = [
        b for b in boss_data
        if now - b["time"] < 600
    ]

    return jsonify(valid)

app.run(host="0.0.0.0", port=5000)
