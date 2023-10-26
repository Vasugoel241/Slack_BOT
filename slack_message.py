import os
from dotenv import load_dotenv

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

response = slack_client.auth_test()
BOT_ID = response['user_id']


def handle_event(event : dict):
    print(event)
    event_type = event["type"]

    if event_type == "message":
        channel_id = event["channel"]
        user_id = event["user"]
        message_text = event["text"]

    if 'hello bot' in message_text.lower():
        try:
            response: SlackResponse = slack_client.chat_postMessage(
                channel=channel_id,
                text=f"Hello <@{user_id}>! :wave:"
            )
            assert response["message"]["text"] == f"Hello <@{user_id}>! :wave:"
        except SlackApiError as e:
            print(f"Error sending message: {e.response['error']}")
