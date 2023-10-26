from flask import Flask,request, jsonify
# import logging 
import os
import os
from dotenv import load_dotenv
# import logging
# logging.basicConfig(level=logging.DEBUG)

from slack_sdk import WebClient
from slack_sdk.signature import SignatureVerifier
from slack_sdk.web import SlackResponse
from slack_sdk.errors import SlackApiError

env_path = ".env"
load_dotenv(env_path)

slack_token = os.environ['SLACK_BOT_TOKEN']
signing_secret = os.environ['SIGNING_SECRET']

slack_client = WebClient(token=slack_token)
signature_verifier = SignatureVerifier(signing_secret)

import slack_message

app = Flask(__name__)
# logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def home():
    print('hi budy')
    return 'This is the homepage'

@app.route("/slack/message_actions", methods=["POST"])
def slack_message_actions():
    event_data = request.get_json()
   
    if event_data['type'] == 'url_verification':
        return jsonify({"challenge": event_data["challenge"]})
    
    # if event_data['type'] == 'event_callback' and "event" in event_data:
    #     event = event_data["event"]
    #     slack_message.handle_event(event)

    try:
        response = slack_client.chat_postMessage(
            channel="bot-testing",
            text="Hello from your app! :tada:"
            )
    except SlackApiError as e:
    # You will get a SlackApiError if "ok" is False
        assert e.response["error"] 
    return jsonify({"status": "success"}), 200


if __name__ == "__main__":
   
    if os.environ.get('SLACK_BOT_TOKEN') is None:
        print ("SLACK_BOT_TOKEN env variable is not defined")
    elif os.environ.get('CHATBOT_NAME') is None:
        print ("CHATBOT_NAME env variable is not defined")
   
    app.run(debug = True, host='0.0.0.0')