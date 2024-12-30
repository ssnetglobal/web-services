from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Database file
DB_FILE = "user.txt"

# Utility function to load users from the file
def load_users():
    users = {}
    try:
        with open(DB_FILE, "r") as f:
            for line in f:
                user = eval(line.strip())  # Convert string back to dictionary
                users[user["id"]] = user
    except FileNotFoundError:
        pass
    return users

# Utility function to save users to the file
def save_users(users):
    with open(DB_FILE, "w") as f:
        for user in users.values():
            f.write(str(user) + "\n")

@app.route('/')
def welcome():
    return "<h1>Welcome to Server 1</h1><p>Use the API to manage user data.</p>"

@app.route('/user', methods=['POST'])
def add_user():
    data = request.json
    print("Received data at Server 1:", data)  # Debugging
    users = load_users()
    user_id = data.get('id')
    if not user_id or user_id in users:
        return jsonify({'error': 'Invalid or duplicate user ID'}), 400

    required_fields = ['id', 'name', 'email', 'age', 'phone']
    if not all(field in data for field in required_fields):
        return jsonify({'error': f"Missing required fields: {', '.join(required_fields)}"}), 400

    users[user_id] = data
    save_users(users)
    return jsonify({'message': 'User added successfully'}), 201

@app.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    users = load_users()
    user = users.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user), 200

@app.route('/user/<user_id>', methods=['PUT'])
def update_user(user_id):
    users = load_users()
    if user_id not in users:
        return jsonify({'error': 'User not found'}), 404
    data = request.json
    users[user_id].update(data)
    save_users(users)
    return jsonify({'message': 'User updated successfully'}), 200

@app.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    users = load_users()
    if user_id not in users:
        return jsonify({'error': 'User not found'}), 404
    del users[user_id]
    save_users(users)
    return jsonify({'message': 'User deleted successfully'}), 200

if __name__ == '__main__':
    app.run(port=5000)
