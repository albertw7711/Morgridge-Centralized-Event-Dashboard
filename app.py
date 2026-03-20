from flask import Flask, request, jsonify
from database_controller import database_controller

app = Flask(__name__)
db = database_controller()
db.init_event_db()
db.init_channel_db()

REQUIRED_FIELDS = {"name", "description", "location", "start", "duration", "food", "media"}

@app.post("/insert")
def insert_event():
    body = request.get_json()

    missing = REQUIRED_FIELDS - body.keys()
    if missing:
        return jsonify({"error": "Missing required fields", "missing": list(missing)}), 400

    if len(body.keys()) != len(REQUIRED_FIELDS):
        return jsonify({"error": "Too many fields in body", "received": list(body.keys())}), 400

    try:
        db.insert_event(
            name=body["name"],
            description=body["description"],
            location=body["location"],
            start=body["start"],
            duration=body["duration"],
            food=body["food"],
            media=body["media"],
        )
        return jsonify({"message": "Event inserted"}), 201

    except Exception as e:
        print(e)
        return jsonify({"message": "Something went wrong while trying to write, try again later"}), 500


@app.get("/retrieve")
def retrieve_events():
    try:
        events = db.retrieve_events()
        return jsonify(events), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Something went wrong while trying to retrieve, try again later"}), 500


@app.get("/retrieve/<int:event_id>")
def retrieve_event(event_id):
    try:
        event = db.retrieve_event(event_id)
        if event is None:
            return jsonify({"message": "Event not found"}), 404
        return jsonify(event), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Something went wrong while trying to retrieve, try again later"}), 500



@app.post("/channels")
def add_channel():
    """Register a channel for a server.
    Body: { "server_id": "...", "channel_id": "..." }
    """
    body = request.get_json()
    missing = {"server_id", "channel_id"} - body.keys()
    if missing:
        return jsonify({"error": "Missing required fields", "missing": list(missing)}), 400

    try:
        db.insert_channel(body["server_id"], body["channel_id"])
        return jsonify({"message": "Channel registered"}), 201
    except Exception as e:
        print(e)
        return jsonify({"message": "Something went wrong, try again later"}), 500


@app.get("/channels/<server_id>")
def get_channels(server_id):
    """Return all channel IDs for a server as a flat list.
    The bot can load this directly into a set: set(response.json())
    """
    try:
        channels = db.retrieve_channels(server_id)
        return jsonify(channels), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Something went wrong, try again later"}), 500

@app.delete("/events/<int:event_id>")
def delete_event(event_id):
    try:
        deleted = db.delete_event(event_id)
        if not deleted:
            return jsonify({"message": "Event not found"}), 404
        return jsonify({"message": "Event deleted"}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Something went wrong"}), 500

@app.delete("/channels")
def remove_channel():
    """Remove a specific channel from a server.
    Body: { "server_id": "...", "channel_id": "..." }
    """
    body = request.get_json()
    missing = {"server_id", "channel_id"} - body.keys()
    if missing:
        return jsonify({"error": "Missing required fields", "missing": list(missing)}), 400

    try:
        deleted = db.delete_channel(body["server_id"], body["channel_id"])
        if not deleted:
            return jsonify({"message": "Channel not found"}), 404
        return jsonify({"message": "Channel removed"}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Something went wrong, try again later"}), 500


@app.get("/sample-data")
def sample():
    payload = {
        "name": "UPL Research Talk 📚",
        "description": "The UPL is hosting a talk on getting into research as an undergrad for the first time! I'll be sharing what I've personally learned about reaching out to labs, finding advisors, and making the most of your time once you're in. Whether you're interested in research for grad school, industry, or pure curiosity, feel free to stop by.",
        "location": "Morgridge Hall Rm. 1524",
        "start": "6:00 PM",
        "duration": "1 hour",
        "food": True,
        "media": [
            "https://cdn.discordapp.com/attachments/1423716763711045705/1473462011881848842/flyer.jpg?ex=69a180af&is=69a02f2f&hm=48183abc7d49de6070f133fa6ca6c1f18490fe424c85be3624f3b840ae8c2347&"
        ],
    }
    return jsonify(payload), 200