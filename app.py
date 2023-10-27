from flask import Flask,request, jsonify
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

import os
from dotenv import load_dotenv
import logging
logging.basicConfig(filename="newfile.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


env_path = ".env"
load_dotenv(env_path)

slack_token = os.environ['SLACK_BOT_TOKEN']
signing_secret = os.environ['SIGNING_SECRET']
webhook_url = os.environ['SLACK_WEBHOOK_URL']

slack_client = WebClient(token=slack_token)

app = Flask(__name__)


@app.route("/slack/post-message", methods=["POST"])
def slack_message_actions():
    event_data = request.get_json()
    message = event_data["message"]
    try:
        response = slack_client.chat_postMessage(
            channel="bot-testing",
            text=message
            )
    except SlackApiError as e:
        assert e.response["error"] 
    return jsonify({"status": "success"}), 200


@app.route("/slack/get-message", methods=["GET"])
def slack_message_actions():
    event_data = request.get_json()
    message = event_data["message"]
    try:
        response = slack_client.chat_postMessage(
            channel="bot-testing",
            text=message
            )
    except SlackApiError as e:
        assert e.response["error"] 
    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
   
    if os.environ.get('SLACK_BOT_TOKEN') is None:
        print ("SLACK_BOT_TOKEN env variable is not defined")
    elif os.environ.get('CHATBOT_NAME') is None:
        print ("CHATBOT_NAME env variable is not defined")
    elif os.environ.get('SLACK_WEBHOOK_URL') is None:
        print ("SLACK_WEBHOOK_URL env variable is not defined")
   
    app.run(debug = True, host='0.0.0.0')