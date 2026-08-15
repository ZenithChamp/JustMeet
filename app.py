import json
from flask import Flask, render_template, request, redirect, url_for, session
from db import register_user
import bcrypt
app = Flask(__name__)
app.secret_key = "justmeet-secret-key"
@app.route('/')
def home():
    return render_template('home.html')
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
@app.route('/profile')
def profile():
    if 'regno' not in session:
        return redirect(url_for('login'))
    with open("users.json", "r") as file:
        users = json.load(file)
    regno = session['regno']
    user = users.get(regno)
    if user is None:
        return "User not found"
    return render_template("profile.html", user=user)
if __name__ == '__main__':
    app.run(debug=True)