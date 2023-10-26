from flask import Flask,request, jsonify
# import logging 
import os
import os
from dotenv import load_dotenv
# import logging
# logging.basicConfig(level=logging.DEBUG)

from slack_sdk import WebClient
# from slack_sdk.signature import SignatureVerifier
# from slack_sdk.web import SlackResponse
from slack_sdk.errors import SlackApiError

env_path = ".env"
load_dotenv(env_path)

slack_token = os.environ['SLACK_BOT_TOKEN']
signing_secret = os.environ['SIGNING_SECRET']

slack_client = WebClient(token=slack_token)

app = Flask(__name__)
# logging.basicConfig(level=logging.DEBUG)

@app.route("/slack/message_actions", methods=["POST"])
def slack_message_actions():
    event_data = request.get_json()
    try:
        response = slack_client.chat_postMessage(
            channel="bot-testing",
            text="Hello from your app! :tada:"
            )
    except SlackApiError as e:
        assert e.response["error"] 
    return jsonify({"status": "success"}), 200


if __name__ == "__main__":
   
    if os.environ.get('SLACK_BOT_TOKEN') is None:
        print ("SLACK_BOT_TOKEN env variable is not defined")
    elif os.environ.get('CHATBOT_NAME') is None:
        print ("CHATBOT_NAME env variable is not defined")
   
    app.run(debug = True, host='0.0.0.0')