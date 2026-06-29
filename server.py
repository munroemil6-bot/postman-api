from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///events.db"
db = SQLAlchemy(app)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()

events = [
    {"id": 1, "title": "Yoga in the Park"},
    {"id": 2, "title": "Lake 5K Run"},
]

attendees = []

@app.route("/events/<int:event_id>/attendees", methods=["GET"])
def get_attendees(event_id):
    event_attendees = [a for a in attendees if a["event_id"] == event_id]
    return jsonify(event_attendees), 200

@app.route("/events/<int:event_id>/attendees", methods=["POST"])
def add_attendee(event_id):
    data = request.get_json(silent=True)

    if not isinstance(data, dict) or "name" not in data:
        return jsonify({"error": "Name is required"}), 400

    # Check event exists
    event = next((e for e in events if e["id"] == event_id), None)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    new_attendee = {
        "id": len(attendees) + 1,
        "event_id": event_id,
        "name": data["name"]
    }
    attendees.append(new_attendee)
    return jsonify(new_attendee), 201

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
    new_event = {
        "id": new_id,
        "title": str(data["title"]).strip(),
        "date": data.get("date", ""),
        "location": data.get("location", ""),
        "capacity": data.get("capacity", 0),
    }
    events.append(new_event)
    return jsonify(new_event), 201

@app.route("/events/<int:event_id>", methods=["GET"])
def get_event(event_id):
    for event in events:
        if event["id"] == event_id:
            return jsonify(event), 200
    return jsonify({"error": "Event not found"}), 404

@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    data = request.get_json(silent=True)

    if not isinstance(data, dict) or "title" not in data or not str(data["title"]).strip():
        return jsonify({"error": "Title is required"}), 400

    for event in events:
        if event["id"] == event_id:
            event["title"] = str(data["title"]).strip()
            return jsonify(event), 200

    return jsonify({"error": "Event not found"}), 404


@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    for idx, event in enumerate(events):
        if event["id"] == event_id:
            events.pop(idx)
            return jsonify({"message": "Event deleted"}), 200

    return jsonify({"error": "Event not found"}), 404


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404

@app.route("/events/search", methods=["GET"])
def search_events():
    query = request.args.get("q", "").lower()
    results = [e for e in events if query in e["title"].lower()]
    return jsonify(results), 200


if __name__ == "__main__":
    app.run(debug=False)
