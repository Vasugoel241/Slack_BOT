from flask import Flask,request, jsonify
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

import os
from dotenv import load_dotenv
import logging
logging.basicConfig(filename="logfile.log",
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

@app.route("/")
def hello():
    return"<h1>Hello World</h1>"

@app.route("/slack/post-message", methods=["POST"])
def slack_post_message():
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

# slack_message = ""
@app.route("/slack/events", methods=["POST"])
def slack_events():
    event_data = request.get_json()

    # Verify the request to make sure it's from Slack
    if "challenge" in event_data:
        # Respond to the URL verification challenge during app installation
        return jsonify({"challenge": event_data["challenge"]}), 200
    
  
    if "event" in event_data:
        event = event_data["event"]
        slack_message = event["text"]
        print(slack_message)

        # Check if the event is an "app_mention" event
        if event["type"] == "app_mention":
            # Check if the message mentions the bot
            if f"<@{slack_client.api_call('auth.test')['user_id']}>" in event["text"]:
                # Respond to the mention with a message
                channel_id = event["channel"]
                try:
                    response = slack_client.chat_postMessage(
                        channel=channel_id,
                        text="Hello! I received your mention!"
                    )
                    print("Message sent successfully:", response["message"]["text"])
                except SlackApiError as e:
                    print("Error sending message:", e.response["error"])
    
    return jsonify({"status": "success",}), 200

# @app.route("/slack/get-message", methods=["GET"])
# def slack_get_message():
#     return jsonify({"message": slack_message}), 200


if __name__ == "__main__":
   
    if os.environ.get('SLACK_BOT_TOKEN') is None:
        print ("SLACK_BOT_TOKEN env variable is not defined")
    elif os.environ.get('CHATBOT_NAME') is None:
        print ("CHATBOT_NAME env variable is not defined")
    elif os.environ.get('SLACK_WEBHOOK_URL') is None:
        print ("SLACK_WEBHOOK_URL env variable is not defined")
   
    app.run(debug = True, host='0.0.0.0')

