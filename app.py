import os
import json
from functools import wraps

import firebase_admin
from firebase_admin import credentials, firestore, auth
from google.cloud.firestore_v1.base_query import FieldFilter
from flask import Flask, render_template, request, redirect, session, jsonify

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-change-me")

# Connect to Firebase (key file locally, environment variable when deployed)
key_json = os.environ.get("FIREBASE_KEY_JSON")
if key_json:
    cred = credentials.Certificate(json.loads(key_json))
else:
    cred = credentials.Certificate("firebase-key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


def login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if "uid" not in session:
            return redirect("/login")
        return view(*args, **kwargs)
    return wrapper


@app.context_processor
def inject_user():
    return {"user_email": session.get("email")}


# ---------- Public pages ----------
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/signup")
def signup():
    return render_template("signup.html")


# ---------- Auth ----------
@app.route("/session-login", methods=["POST"])
def session_login():
    id_token = request.json.get("idToken")
    try:
        decoded = auth.verify_id_token(id_token, clock_skew_seconds=10)
    except Exception:
        return jsonify({"error": "Invalid login"}), 401
    session["uid"] = decoded["uid"]
    session["email"] = decoded.get("email", "")
    return jsonify({"ok": True})


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ---------- Tasks (private to each user) ----------
@app.route("/tasks")
@login_required
def tasks():
    docs = db.collection("tasks").where(
        filter=FieldFilter("uid", "==", session["uid"])
    ).stream()
    my_tasks = []
    for doc in docs:
        task = doc.to_dict()
        task["id"] = doc.id
        my_tasks.append(task)
    my_tasks.sort(key=lambda t: t["created_at"])
    return render_template("tasks.html", tasks=my_tasks)


@app.route("/add", methods=["POST"])
@login_required
def add_task():
    title = request.form["task"].strip()[:200]
    if title:
        db.collection("tasks").add({
            "uid": session["uid"],
            "title": title,
            "done": False,
            "created_at": firestore.SERVER_TIMESTAMP,
        })
    return redirect("/tasks")


@app.route("/toggle/<task_id>", methods=["POST"])
@login_required
def toggle_task(task_id):
    ref = db.collection("tasks").document(task_id)
    doc = ref.get()
    if doc.exists and doc.to_dict()["uid"] == session["uid"]:
        ref.update({"done": not doc.to_dict()["done"]})
    return redirect("/tasks")


@app.route("/delete/<task_id>", methods=["POST"])
@login_required
def delete_task(task_id):
    ref = db.collection("tasks").document(task_id)
    doc = ref.get()
    if doc.exists and doc.to_dict()["uid"] == session["uid"]:
        ref.delete()
    return redirect("/tasks")


if __name__ == "__main__":
    app.run(debug=True)