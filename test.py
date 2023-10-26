import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_sdk.web import SlackResponse
from slack_sdk.rtm import RTMClient

# Replace 'YOUR_BOT_TOKEN' with your Slack bot's OAuth access token
SLACK_BOT_TOKEN = 'xoxb-6091475121747-6114675644496-F9iyZYTwXC9uxAjifYP6vDYh'

client = WebClient(token=SLACK_BOT_TOKEN)

def respond_to_hello(event):
    channel_id = event['channel']
    user_id = event['user']
    text = event['text']

    if 'hello' in text.lower():
        try:
            response:SlackResponse = client.chat_postMessage(
                channel=channel_id,
                text=f"Hello <@{user_id}>! :wave:"
            )
            assert response["message"]["text"] == f"Hello <@{user_id}>! :wave:"
        except SlackApiError as e:
            print(f"Error sending message: {e.response['error']}")

# Listen to Slack events
@RTMClient.run_on(event='message')
def handle_message(**payload):
    data = payload['data']
    if 'text' in data:
        respond_to_hello(data)

if __name__ == "__main__":
    rtm_client = RTMClient(token=SLACK_BOT_TOKEN)
    rtm_client.start()
