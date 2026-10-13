import json
import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_cors import CORS
from db import register_user
import bcrypt
app = Flask(__name__)
CORS(app)
app.secret_key = "justmeet-secret-key"
@app.route('/')
def home():
    user = None
    if 'regno' in session:
        with open("users.json", "r") as file:
            users = json.load(file)
        regno = session['regno']
        user = users.get(regno)
    return render_template('home.html', user=user)
@app.route('/register', methods=['GET', 'POST'])
def signup_page():
    if request.method == 'POST':
        username = request.form.get('fname')
        regno = request.form.get('regno')
        password = request.form.get('password')
        success = register_user(username, regno, password)
        if success:
            session['regno'] = regno.strip().upper()
            return redirect(url_for('home'))
        return "Registration Failed. Username or Registration Number already exists."
    return render_template('reg.html')
@app.route('/choice', methods=['GET', 'POST'])
def choice():
    if 'regno' not in session:
        return redirect(url_for('login'))
    regno = session['regno'].strip().upper()
    with open("users.json", "r") as file:
        users = json.load(file)
    user = users.get(regno)
    if user is None:
        return "User not found"
    if request.method == 'POST':
        user["choice"] = request.form.get('choice')
        with open("users.json", "w") as file:
            json.dump(users, file, indent=4)
        return redirect(url_for('my_profile'))
    return redirect(url_for('my_profile'))
@app.route('/search')
def search():
    if 'regno' not in session:
        return redirect(url_for('login'))
    regno = request.args.get('q', '').strip().upper()
    if not regno:
        return render_template(
            'search.html',
            user=None,
            searched_regno=None
        )
    with open("users.json", "r") as file:
        users = json.load(file)
    user = users.get(regno)
    return render_template(
        'search.html',
        user=user,
        searched_regno=regno
    )
@app.route('/timetable')
def timetable():
    return render_template('timetable.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        regno = request.form.get('regno').strip().upper()
        password = request.form.get('password')
        with open("users.json", "r") as file:
            users = json.load(file)
        user = users.get(regno)
        if user is None:
            return "Registration number not found."
        if bcrypt.checkpw(password.encode('utf-8'),user['password_hash'].encode('utf-8')):
            session['regno'] = regno
            return redirect(url_for('home'))
        return "Incorrect Password."
    return render_template('login.html')
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))
@app.route('/profile')
def my_profile():
    if 'regno' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('view_profile', regno=session['regno']))
@app.route('/profile/<regno>')
def view_profile(regno):
    if 'regno' not in session:
        return redirect(url_for('login'))
    regno = regno.strip().upper()
    with open("users.json", "r") as file:
        users = json.load(file)
    user = users.get(regno)
    if user is None:
        return "User not found"
    logged_in_regno = session['regno'].strip().upper()
    is_owner = logged_in_regno == regno
    return render_template(
        "profile.html",
        user=user,
        profile_regno=regno,
        is_owner=is_owner
    )
@app.route('/friends')
def friends():
    if 'regno' not in session:
        return redirect(url_for('login'))
    my_regno = session['regno'].strip().upper()
    with open("users.json", "r") as file:
        users = json.load(file)
    my_user = users.get(my_regno)
    if my_user is None:
        return "User not found"
    friend_regnos = my_user.get("friends", [])
    friend_users = []
    for friend_regno in friend_regnos:
        friend = users.get(friend_regno)
        if friend:
            friend_users.append(friend)
    return render_template(
        "friends.html",
        friends=friend_users
    )
@app.route('/follow/<regno>')
def follow(regno):
    if 'regno' not in session:
        return redirect(url_for('login'))
    current_regno = session['regno']
    target_regno = regno.strip().upper()
    if current_regno == target_regno:
        return "You cannot follow yourself."
    with open("users.json", "r") as file:
        users = json.load(file)
    if target_regno not in users:
        return "User not found."
    users[current_regno].setdefault("friends", [])
    users[target_regno].setdefault("friends", [])
    if target_regno not in users[current_regno]["friends"]:
        users[current_regno]["friends"].append(target_regno)
    if current_regno not in users[target_regno]["friends"]:
        users[target_regno]["friends"].append(current_regno)
    with open("users.json", "w") as file:
        json.dump(users, file, indent=4)
    return redirect(url_for('friends'))
@app.route('/upload-profile-picture', methods=['POST'])
def upload_profile_picture():
    if 'regno' not in session:
        return jsonify({"success": False, "error": "Not logged in"}), 401
    regno = session['regno']
    if 'profile_picture' not in request.files:
        return jsonify({"success": False, "error": "No picture"}), 400
    picture = request.files['profile_picture']
    folder = os.path.join(
        app.root_path,
        "static",
        "profile_pictures"
    )
    os.makedirs(folder, exist_ok=True)
    filename = regno + ".png"
    filepath = os.path.join(folder, filename)
    picture.save(filepath)
    with open("users.json", "r") as file:
        users = json.load(file)
    user = users.get(regno)
    if user is None:
        return jsonify({"success": False, "error": "User not found"}), 404
    user["profile_picture"] = "profile_pictures/" + filename
    with open("users.json", "w") as file:
        json.dump(users, file, indent=4)
    return jsonify({"success": True})
if __name__ == '__main__':
    app.run(debug=True)
