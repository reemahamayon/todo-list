# TaskFlow: Python To-Do List

Project 1 of the DecodeLabs Python Programming training (Batch 2026).

This repository has two versions of the same to-do list:

## 1. Terminal app (`todo_list.py`)

A menu-driven to-do list that uses Python lists and dictionaries. Tasks are saved to `tasks.json` so they survive restarts.

Features: add a task, view tasks, delete a task, exit.

Run it with `python todo_list.py`.

## 2. Website (`app.py`)

A web version built with Flask, with sign up and login through Firebase Authentication and private tasks per user stored in Firestore.

To run it you need your own Firebase project and a service account key saved as `firebase-key.json` in this folder (never upload this file). Then:

1. Install the requirements with `pip install -r requirements.txt`
2. Run `python app.py`
3. Open `http://localhost:5000`

## Tools used

Python, Flask, Firebase (free plan), HTML and CSS. All free and open source.