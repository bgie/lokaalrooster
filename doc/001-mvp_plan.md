## 📄 Project: Minimalist Class Schedule Webpage

### 🎯 **Objective**

Create a simple web application using Flask that:

* Displays a large live clock
* Shows the daily class schedule for a specific room
* Uses minimal, clean design
* Loads class schedule data from a JSON file

---

## ✅ **Functional Requirements**

1. Display a live digital clock prominently.
2. Show a list/table of classes scheduled in a specific room.
3. Use a JSON file to store class information.
4. The webpage should auto-update or refresh class info periodically.

---

## 🗂️ **Data Structure**

### JSON file: `schedule.json`

```json
[
  {
    "name": "Math 101",
    "room": "A101",
    "start_time": "09:00",
    "end_time": "10:30"
  },
  {
    "name": "Physics 202",
    "room": "A101",
    "start_time": "11:00",
    "end_time": "12:30"
  }
]
```

---

## 🛠️ **Development Steps**

### 1. **Project Setup**

* Create project folder
* Create virtual environment and install Flask
* Create required files:

  * `app.py` (Flask app)
  * `schedule.json` (class data)
  * `templates/index.html` (HTML template)
  * `static/` (CSS, optional JavaScript)

### 2. **Backend (Flask)**

* Read `schedule.json` on app start or on request
* Filter classes for a specific room (e.g., "A101")
* Pass filtered data to the template

### 3. **Frontend (HTML/CSS)**

* Use a minimalist layout (e.g., centered clock and list)
* Display live clock using JavaScript
* Show current and upcoming classes

### 4. **Optional Enhancements**

* Auto-refresh the schedule every few minutes
* Highlight the current class based on time

---

## 📦 **File Structure**

```
/project-root
│
├── app.py
├── schedule.json
├── /templates
│   └── index.html
└── /static
    ├── style.css
    └── clock.js
```
