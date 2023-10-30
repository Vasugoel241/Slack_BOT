from flask import Flask,request, jsonify

from slack_message_handler import Slack_Message

import logging
logging.basicConfig(filename="logfile.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

app = Flask(__name__)

@app.route("/")
def hello():
    return"<h1>Hello From Slack BOT</h1>"

@app.route("/slack/post-message", methods=["POST"])
def slack_post_message():
    event_data = request.get_json()
    status = Slack_Message.post_message(event_data)
    return jsonify(status)
    

@app.route("/slack/events", methods=["GET","POST"])
def slack_events_message():
    event_data = request.get_json()
    status = Slack_Message.slack_events(event_data)
    return jsonify(status)

