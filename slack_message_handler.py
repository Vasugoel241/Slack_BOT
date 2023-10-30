from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from config import slack_token

slack_client = WebClient(token=slack_token)

response = slack_client.auth_test()
# BOT_ID = response['user_id']

class Slack_Message:
    
    def post_message(event_data):
        message = event_data["message"]
        try:
            response = slack_client.chat_postMessage(
                channel="bot-testing",
                text=message
                )
        except SlackApiError as e:
            return e.response["error"] 
        return {"status": "success"}, 200
    

    def slack_events(event_data):
          
        if "event" in event_data:
            event = event_data["event"]
            slack_message = event["text"]
            print(slack_message)

            if event["type"] == "app_mention":
                # Check if the message mentions the bot
                BOT_ID = slack_client.api_call('auth.test')['user_id']
                if f"<@{BOT_ID}>" in event["text"]:
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
        
        return {"message": slack_message}, 200
