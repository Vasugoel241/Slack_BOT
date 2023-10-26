from flask import Flask,request, jsonify
import logging 

import slack_message

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def home():
    print('hi budy')
    return 'This is the homepage'

@app.route("/slack/message_actions", methods=["POST"])
def slack_message_actions():
    event_data = request.get_json()
    # print(event_data)
    if event_data['type'] == 'url_verification':
        return jsonify({"challenge": event_data["challenge"]})
    
    if event_data['type'] == 'event_callback' and "event" in event_data:
        event = event_data["event"]
        slack_message.handle_event(event)

    return jsonify({"status": "success"}), 200
