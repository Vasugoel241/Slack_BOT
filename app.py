from flask import Flask,request, jsonify
import logging
import json

from slack_message_handler import Slack_Message
from config import Config

Config.configure_logging()
app = Flask(__name__)

@app.route("/")

def hello():
    return"<h1>Hello From Slack BOT</h1>"


@app.route("/slack/post-message", methods=["POST"])

def slack_post_message():
    event_data = request.get_json()
    logging.info("Entering post message function")
    slack_data = Slack_Message.post_message(event_data)
    logging.info("Executed post message function")
    return slack_data

# @app.route("/slack/events", methods=["GET","POST"])
# def slack_events_message():
#     event_data = request.get_json()
#     logging.info("Entering slack event message function")
#     slack_data = Slack_Message.slack_events(event_data)
#     logging.info("Executed slack event message function")
#     return jsonify(slack_data)


@app.route("/slack/interactivity", methods=["GET","POST"])
def slack_interactive_message():
    payload = request.form['payload']
    data = json.loads(payload)
    logging.info("Entering slack event message function")
    slack_data = Slack_Message.interactive_message(data)
    logging.info("Executed slack event message function")
    return jsonify(slack_data)