import json
from flask import Flask, request
import logging
from slack_sdk import WebClient
import os
from dotenv import load_dotenv

env_path = ".env"
load_dotenv(env_path)

SLACK_TOKEN = os.environ['SLACK_BOT_TOKEN']


app = Flask(__name__)


@app.route('/post-data', methods=['POST'])
def post_data():
    app.logger.info('Received POST request')
    data = request.get_json()
    app.logger.info('Received data: %s', data)

    message = data.get('message', 'No message found in the data')

    client = WebClient(token=SLACK_TOKEN)
    channel = '#bot-testing'
    response = client.chat_postMessage(channel=channel, text=message)

    return 'Data received and posted to Slack channel!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port= 5000)

