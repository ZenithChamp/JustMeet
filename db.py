import json
import os
import bcrypt
JSON_FILE="users.json"
def load_users():
    if not os.path.exists(JSON_FILE):
        return {}
    try:
        with open(JSON_FILE, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        return {}
def register_user(username, regno, plain_password):
    username = username.strip()
    regno = regno.strip().upper()
    all_users = load_users()
    for existing_uid, details in all_users.items():
        if details['username'] == username or details['regno'] == regno:
            print("❌ Error: Username or Registration number is already registered.")
            return False
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
    hashed_password_str = hashed_password.decode('utf-8')
    new_user_data = {
        "username": username,
        "regno": regno,
        "password_hash": hashed_password_str
    }
    all_users[regno] = new_user_data
    with open(JSON_FILE, 'w') as file:
        json.dump(all_users, file, indent=4)
        
    print(f"🎉 Success! User '{username}' has been stored securely in JSON.")
    return True