import json
from datetime import datetime, timedelta
from flask import Flask, render_template, abort

app = Flask(__name__)


def load_config():
    """Loads configuration from config.json or falls back to config.example.json."""
    try:
        with open("data/config.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        with open("data/config.example.json", "r", encoding="utf-8") as f:
            return json.load(f)


config = load_config()


@app.context_processor
def inject_config():
    """Injects config into templates."""
    return dict(config=config)


def load_schedule():
    """Loads the schedule from the JSON file."""
    with open("data/schedule.json", "r", encoding="utf-8") as f:
        return json.load(f)


def load_shared_schedule():
    """Loads the shared break schedule from the JSON file."""
    try:
        with open("data/shared_schedule.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def get_text_color_for_bg(hex_color):
    """Determines if text should be black or white based on background color luminance."""
    hex_color = hex_color.lstrip("#")
    if len(hex_color) != 6:
        return "#000000"  # Default to black for invalid hex codes

    r_s, g_s, b_s = (int(hex_color[i:i + 2], 16) / 255.0 for i in (0, 2, 4))

    def srgb_to_linear(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    luminance = (0.2126 * srgb_to_linear(r_s) +
                 0.7152 * srgb_to_linear(g_s) +
                 0.0722 * srgb_to_linear(b_s))

    return "#FFFFFF" if luminance < 0.4 else "#000000"


def get_all_rooms():
    """Gets a list of all rooms with their colors from rooms.json."""
    try:
        with open("data/rooms.json", "r", encoding="utf-8") as f:
            rooms = json.load(f)
    except FileNotFoundError:
        return []

    for room in rooms:
        room["text_color"] = get_text_color_for_bg(room["color"])

    return rooms


def get_schedule_for_room(room_id):
    """
    Gets the combined schedule for a specific room, including shared breaks.
    """
    room_classes = [
        item for item in load_schedule() if item.get("room") == room_id
    ]
    for item in room_classes:
        item["type"] = "class"

    shared_breaks = load_shared_schedule()
    for item in shared_breaks:
        item["type"] = "break"

    combined_schedule = room_classes + shared_breaks
    combined_schedule.sort(key=lambda x: datetime.strptime(x["start_time"], "%H:%M"))
    return combined_schedule


@app.route("/")
def index():
    """Serves the home page with a list of all rooms."""
    rooms = get_all_rooms()
    return render_template("index.html", rooms=rooms)


@app.route("/room/<room_id>")
def room_schedule(room_id):
    """Serves the page with the schedule for a specific room."""
    schedule = get_schedule_for_room(room_id)
    all_rooms = get_all_rooms()
    room = next((r for r in all_rooms if r.get("name") == room_id), None)

    if not room:
        abort(404, description=f"Room '{room_id}' not found.")

    now = datetime.now()
    now_time = now.time()
    current_class = None
    show_gif = False

    for item in schedule:
        try:
            start_time = datetime.strptime(item["start_time"], "%H:%M").time()
            end_time = datetime.strptime(item["end_time"], "%H:%M").time()

            if start_time <= now_time < end_time:
                current_class = item
                if item.get("type") == "break":
                    break_start_dt = datetime.combine(now.date(), start_time)
                    if now < break_start_dt + timedelta(minutes=1):
                        show_gif = True
                break
        except (ValueError, KeyError):
            # Ignore malformed or incomplete schedule items
            continue

    return render_template(
        "room_schedule.html",
        schedule=schedule,
        room=room,
        current_class=current_class,
        show_gif=show_gif,
    )


if __name__ == "__main__":
    app.run(debug=True)
