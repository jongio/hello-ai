from flask import Flask, render_template, jsonify
import os
import requests
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)

@app.route('/')
def home():
    # This route renders the HTML page initially
    return render_template('index.html')

@app.route('/quote', methods=['GET'])
def quote():
    # Assuming you have an API_URL environment variable for your quote API
    api_url = os.getenv('API_URL', 'http://api:3100')
    
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            return jsonify(data)  # Return the JSON data received from the API
        else:
            return jsonify({"error": "Failed to fetch data from API", "status_code": response.status_code})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error making request to API: {e}"})

if __name__ == '__main__':
    app.run(debug=True, port=3000)
