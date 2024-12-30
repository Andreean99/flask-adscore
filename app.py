from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# Load users data from JSON file
with open('users.json', 'r') as f:
    users = json.load(f)

# Load provider data from JSON file
with open('adscore.json', 'r') as f:
    data = json.load(f)

# Root route
@app.route('/')
def index():
    return "Welcome to Adscore Provider API!"

# Login route
@app.route('/login', methods=['POST'])
def login():
    data = request.form  # Mengambil data dari form POST
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400  # Jika username atau password kosong

    # Cek apakah username dan password sesuai dengan yang ada di JSON file
    for user in users:
        if user['username'] == username and user['password'] == password:
            return jsonify({"message": "Login successful"}), 200

    return jsonify({"error": "Invalid username or password"}), 401

# Define a route to fetch provider data by code
@app.route('/get_provider', methods=['GET'])
def get_provider():
    provider_code = request.args.get('provider_code')
    
    if not provider_code:
        return jsonify({"error": "No provider code provided"}), 400  # Handle case where no code is provided

    for provider in data:
        if provider.get("new_code_provider") == provider_code.strip():  # Use strip() to remove any extra spaces
            return jsonify(provider), 200  # Return provider data if found
    
    return jsonify({"error": "Provider not found"}), 404  # Return error if provider not found

# Define a route to fetch the score type
@app.route('/get_score', methods=['GET'])
def get_score():
    provider_code = request.args.get('provider_code')

    if not provider_code:
        return jsonify({"error": "No provider code provided"}), 400  # Handle case where no code is provided

    for provider in data:
        if provider.get("new_code_provider") == provider_code.strip():  # Use strip() to remove any extra spaces
            total_score = provider.get("total_score", 0)  # Default to 0 if total_score is not present

            # Determine the score type based on total_score
            if total_score <= 9:
                score_type = "Bad Score"
            elif 10 <= total_score <= 14:
                score_type = "Moderate Score"
            else:
                score_type = "Good Score"

            return jsonify({"total_score": total_score, "score_type": score_type}), 200  # Return score info

    return jsonify({"error": "Provider not found"}), 404  # Return error if provider not found

if __name__ == '__main__':
     # app.run(debug=True)
    app.run()
