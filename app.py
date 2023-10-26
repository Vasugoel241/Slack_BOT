from flask import Flask,request, jsonify
# import logging 
import os

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
    print("Before")
    slack_message.hello()
    print("After")
    return jsonify({"status": "success"}), 200


if __name__ == "__main__":
   
    if os.environ.get('SLACK_BOT_TOKEN') is None:
        print ("SLACK_BOT_TOKEN env variable is not defined")
    elif os.environ.get('CHATBOT_NAME') is None:
        print ("CHATBOT_NAME env variable is not defined")
   
    app.run(debug = True, host='0.0.0.0')