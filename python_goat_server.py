import base64
from flask import Flask, request, render_template_string
import pickle
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client['my_database']

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')

    if username and password:
        db.users.insert_one({"username": username, "password": password})
        return 'User registered successfully!'
    else:
        return 'Please provide username and password!'

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = db.users.find_one({"username": username, "password": password}) 
    if user:
        return f'Logged in as {username}!'
    else:
        return 'Invalid credentials!'

@app.route('/note', methods=['POST'])
def add_note():
    username = request.form.get('username')
    note = request.form.get('note')
    print(username, note)
    user = db.users.find_one({"username": username})
    print(user)
    if user and note:
        db.notes.insert_one({"user": username, "note": note})
        return 'Note added!'
    else:
        return 'Invalid username or note!'

@app.route('/mynotes', methods=['GET'])
def view_notes():
    username = request.args.get('username')

    if username:
        user_notes = db.notes.find({"user": username})
        notes = [note.get("note") for note in user_notes]
        template = f'<h2>Here are your notes, {username}:</h2>' 
        template += '<ul>'
        for note in notes:
            template += f'<li>{note}</li>'
        template += '</ul>'
        return render_template_string(template)
    else:
        return 'Please provide a valid username!'

@app.route('/prefs', methods=['POST'])
def prefs():
    prefs_data = request.form.get('prefs')
    if prefs_data:
        prefs = pickle.loads(base64.urlsafe_b64decode(prefs_data)) 
        return f'Preferences for user: {prefs}'
    else:
        return 'No preferences provided!'


if __name__ == "__main__":
    app.run(debug=True, port=1234)
