from flask import Flask, request, jsonify
from cryptography.fernet import Fernet
import json

app = Flask(__name__)

# Generate a key for encryption and decryption (should be securely stored in real applications)
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# File to store encrypted messages
MESSAGE_FILE = "messages.txt"

# Utility function to load messages from the file
def load_messages():
    try:
        with open(MESSAGE_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

# Utility function to save messages to the file
def save_messages(messages):
    with open(MESSAGE_FILE, "w") as f:
        json.dump(messages, f)

@app.route("/send_message", methods=["POST"])
def send_message():
    try:
        # Get the raw message from the request
        data = request.json
        user_id = data.get("user_id")
        message = data.get("message")

        if not user_id or not message:
            return jsonify({"error": "User ID and message are required."}), 400

        # Encrypt the message
        encrypted_message = cipher_suite.encrypt(message.encode()).decode()

        # Load existing messages
        messages = load_messages()

        # Store the encrypted message
        messages[user_id] = encrypted_message
        save_messages(messages)
        return jsonify({"message": "Message stored securely."}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/get_message", methods=["GET"])
def get_message():
    try:
        # Get the user_id from the query parameter
        user_id = request.args.get("user_id")

        if not user_id:
            return jsonify({"error": "User ID is required."}), 400

        # Load existing messages
        messages = load_messages()

        # Retrieve and decrypt the message
        encrypted_message = messages.get(user_id)

        if not encrypted_message:
            return jsonify({"error": "No message found for the given User ID."}), 404

        decrypted_message = cipher_suite.decrypt(encrypted_message.encode()).decode()
        return jsonify({"message": decrypted_message}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000)
