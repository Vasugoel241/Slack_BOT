from flask import Flask, request, jsonify
import os
import requests
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables from .env file
env_path = ".env"
load_dotenv(env_path)

# Get Slack webhook URL from environment variable
webhook_url = os.getenv('SLACK_WEBHOOK_URL')

# Endpoint to send a message to Slack
@app.route('/send-message', methods=['POST'])
def send_message():
    try:
        data = request.get_json()
        message = data.get('message', 'Hello from the Flask app using Slack webhook!')

        payload = {
            'channel': '#general',  # Specify the Slack channel where you want to send the message
            'text': message
        }

        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()  # Raise an exception if the request was not successful
        return jsonify({"status": "success", "message": "Message sent successfully!"}), 200
    except requests.exceptions.HTTPError as errh:
        return jsonify({"status": "error", "message": f"HTTP Error: {errh}"}), 500
    except requests.exceptions.ConnectionError as errc:
        return jsonify({"status": "error", "message": f"Error Connecting: {errc}"}), 500
    except requests.exceptions.Timeout as errt:
        return jsonify({"status": "error", "message": f"Timeout Error: {errt}"}), 500
    except requests.exceptions.RequestException as err:
        return jsonify({"status": "error", "message": f"OOps: Something Else {err}"}), 500

# Main function to run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
