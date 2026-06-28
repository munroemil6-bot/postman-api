from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

events = [
    {"id": 1, "title": "Yoga in the Park"},
    {"id": 2, "title": "Lake 5K Run"},
]


@app.route("/", methods=["GET"])
def welcome():
    return jsonify({"message": "Welcome!"}), 200


@app.route("/events", methods=["GET"])
def get_events():
    return jsonify(events), 200


@app.route("/events", methods=["POST"])
def add_event():
    data = request.get_json(silent=True)

    if not isinstance(data, dict) or "title" not in data or not str(data["title"]).strip():
        return jsonify({"error": "Title is required"}), 400

    new_id = max((event["id"] for event in events), default=0) + 1
    new_event = {"id": new_id, "title": str(data["title"]).strip()}
    events.append(new_event)

    return jsonify(new_event), 201


if __name__ == "__main__":
    app.run(debug=True)
