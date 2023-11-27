from flask import Flask,request, jsonify
import json
from slack_message_handler import Slack_Message
from config import Config
from config import setuplogger, logger
from common_reponse_helper import CommonResponseHelper

setuplogger()
app = Flask(__name__)

@app.route("/")
def hello():
    return"<h1>Hello From Slack BOT</h1>"


@app.route("/slack/post-message", methods=["POST"])
def slack_post_message():
    event_data = request.get_json()
    logger.info("Entering post message function")
    slack_data = Slack_Message.post_message(event_data)
    logger.info("Executed post message function")
    return slack_data


@app.route("/slack/interactivity", methods=["POST"])
def slack_interactive_message():  
    payload = request.form.get('payload')
    payload_dict = json.loads(payload)
    logger.info(f"Payload == {payload_dict}")

    return Slack_Message.get_action_status(payload_dict)

    
@app.route("/slack/jenkins-webhook", methods=["GET"])
def send_status():
    job_name = request.args.get('job_name', default="", type=str)
    action = Slack_Message.get_status(job_name)
    return action