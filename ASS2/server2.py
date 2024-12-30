from flask import Flask, render_template, request, redirect, url_for, flash
import subprocess
import json

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Helper function to execute cURL commands
def execute_curl(curl_command):
    try:
        print("Executing cURL command:", curl_command)  # Debugging
        result = subprocess.check_output(curl_command, shell=True)
        return json.loads(result)
    except subprocess.CalledProcessError as e:
        print("cURL error:", e.output.decode())  # Debugging
        return {'error': e.output.decode()}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_user', methods=['POST'])
def add_user():
    # Retrieve form data
    user_id = request.form['id']
    name = request.form['name']
    email = request.form['email']
    age = request.form['age']
    phone = request.form['phone']
    
    # Construct the JSON payload
    data = {
        'id': user_id,
        'name': name,
        'email': email,
        'age': int(age),
        'phone': phone
    }

    # Print the data for debugging
    print("Sending data to Server 1:", data)

    # Construct the cURL command with escaped double quotes for Windows compatibility
    json_payload = json.dumps(data).replace('"', '\\"')  # Escape quotes for Windows
    curl_command = f'curl -X POST -H "Content-Type: application/json" -d "{json_payload}" http://127.0.0.1:5000/user'
    
    # Execute the cURL command
    result = execute_curl(curl_command)

    # Flash success or error message
    flash(result.get('message') or result.get('error'))
    
    # Redirect back to the index page
    return redirect(url_for('index'))

@app.route('/get_user', methods=['POST'])
def get_user():
    user_id = request.form['id']
    curl_command = f"curl -X GET http://127.0.0.1:5000/user/{user_id}"
    result = execute_curl(curl_command)
    flash(result)
    return redirect(url_for('index'))

@app.route('/update_user', methods=['POST'])
def update_user():
    user_id = request.form['id']
    name = request.form['name']
    email = request.form['email']
    age = request.form['age']
    phone = request.form['phone']
    data = {'name': name, 'email': email, 'age': int(age), 'phone': phone}
    json_payload = json.dumps(data).replace('"', '\\"')  # Escape quotes for Windows
    curl_command = f'curl -X PUT -H "Content-Type: application/json" -d "{json_payload}" http://127.0.0.1:5000/user/{user_id}'
    result = execute_curl(curl_command)
    flash(result.get('message') or result.get('error'))
    return redirect(url_for('index'))

@app.route('/delete_user', methods=['POST'])
def delete_user():
    user_id = request.form['id']
    curl_command = f"curl -X DELETE http://127.0.0.1:5000/user/{user_id}"
    result = execute_curl(curl_command)
    flash(result.get('message') or result.get('error'))
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port=5001)
