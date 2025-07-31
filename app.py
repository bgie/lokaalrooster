import json
from flask import Flask, render_template

app = Flask(__name__)


def load_config():
    """Loads configuration from config.json or falls back to config.example.json."""
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        with open("config.example.json", "r", encoding="utf-8") as f:
            return json.load(f)


config = load_config()


@app.context_processor
def inject_config():
    """Injects config into templates."""
    return dict(config=config)


def load_schedule():
    """Loads the schedule from the JSON file."""
    with open("schedule.json", "r", encoding="utf-8") as f:
        return json.load(f)


def get_all_rooms():
    """Gets a unique, sorted list of all rooms."""
    full_schedule = load_schedule()
    rooms = {item["room"] for item in full_schedule}
    return sorted(list(rooms))


def get_schedule_for_room(room_id):
    """Filters the schedule for a specific room."""
    full_schedule = load_schedule()
    return [item for item in full_schedule if item["room"] == room_id]


@app.route("/")
def index():
    """Serves the home page with a list of all rooms."""
    rooms = get_all_rooms()
    return render_template("index.html", rooms=rooms)


@app.route("/room/<room_id>")
def room_schedule(room_id):
    """Serves the page with the schedule for a specific room."""
    schedule = get_schedule_for_room(room_id)
    return render_template("room_schedule.html", schedule=schedule, room=room_id)


if __name__ == "__main__":
    app.run(debug=True)
