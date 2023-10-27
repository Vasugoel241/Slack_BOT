import json
from flask import Flask, request
from slack_sdk import WebClient
import os
from dotenv import load_dotenv

env_path = ".env"
load_dotenv(env_path)

SLACK_TOKEN = os.environ['SLACK_BOT_TOKEN']


app = Flask(__name__)

# Route to handle incoming POST requests
@app.route('/post-data', methods=['POST'])
def post_data():
    # Get data sent in the POST request
    data = request.get_json()

    # Extract relevant information from the data (customize this based on your data structure)
    message = data.get('message', 'No message found in the data')

    # Post the message to a Slack channel
    client = WebClient(token=SLACK_TOKEN)
    channel = '#bot-testing'
    client.chat_postMessage(channel=channel, text=message)

    return 'Data received and posted to Slack channel!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

