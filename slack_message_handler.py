from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import logging

from common_reponse_helper import CommonResponseHelper
from config import Config

Config.configure_logging()
slack_client = WebClient(token=Config.slack_token)

response = slack_client.auth_test()
class Slack_Message:
    
    def post_message(event_data):
        print(event_data)
        message = event_data["message"]
        
        try:
            response = slack_client.chat_postMessage(
                    channel="bot-testing",
                    text=message
                    )
            # logging.info("Message sent to slack channel")
        
        except SlackApiError as e:
            # logging.debug("Error Message: %s",e.response["error"])
            return CommonResponseHelper.send_error_response(str(e.response["error"]))  
        
        return CommonResponseHelper.send_success_response(message)
    

    def slack_events(event_data):
          
        if "event" in event_data:
            event = event_data["event"]
            slack_message = event["text"]

            logging.info("Message recieved form slack : %s",slack_message)

            if event["type"] == "app_mention":

                BOT_ID = slack_client.api_call('auth.test')['user_id']

                if f"<@{BOT_ID}>" in event["text"]:
                    
                    channel_id = event["channel"]

                    logging.info("Bot id is %d and channel id is %d",BOT_ID,channel_id)

                    try:
                        response = slack_client.chat_postMessage(
                            channel=channel_id,
                            text="Hello! I received your mention!"
                        )

                        logging.info("Message sent successfully: %s", response["message"]["text"])
                    
                    except SlackApiError as e:

                        logging.info("Error sending message: %s", e.response["error"])
                        
                        return CommonResponseHelper.send_error_response(str(e.response["error"]))  
        
        return CommonResponseHelper.send_success_response(slack_message)
