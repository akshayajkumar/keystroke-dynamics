# home.py

from app import app
from flask import render_template, request, jsonify
import csv
import random
import uuid
import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
import joblib

random_paragraphs = [
    "c write know however late each that with because that place nation only for each change form consider we would interest with world so order or run more open that large write turn never over open each over change still old take hold need give by consider line only leave while what set up",
]

user_info = {}  # Dictionary to store user IDs and usernames

def generate_unique_id():
    return str(uuid.uuid4())

def load_user_info():
    # Load existing user IDs and usernames from the CSV file
    try:
        with open('data/raw/data.csv', 'r', newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                user_info[row[0]] = row[1].lower()
    except FileNotFoundError:
        # If file does not exist, create it
        with open('data/raw/data.csv', 'w', newline='') as csvfile:
            pass

load_user_info()

@app.route('/')
def home():
    paragraph = random.choice(random_paragraphs)
    return render_template('index.html', paragraph=paragraph)

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        username = request.form['username'].lower()
        keystrokes = json.loads(request.form['keystrokes'])  # Parse JSON data

        if username in user_info.values():
            user_id = next(key for key, value in user_info.items() if value == username)
        else:
            user_id = generate_unique_id()
            user_info[user_id] = username

        with open('data/raw/data.csv', 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([user_id, username, json.dumps(keystrokes)])  # Store keystrokes as JSON string

        # Return success message
        return jsonify({
            'message': 'Data submitted successfully!',
        })
