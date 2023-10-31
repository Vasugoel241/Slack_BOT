from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import logging

from common_reponse_helper import CommonResponseHelper
from config import Config

Config.configure_logging()
slack_client = WebClient(token=Config.slack_token)

response = slack_client.auth_test()
class Slack_Message:
    job_name = ""
    def interactive_message(channel_id, message):
        slack_message = { "channel":channel_id,
                "text" : message,         
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": "Approval request",
                            "emoji": True
                        }
                    },
                    {
                        "type": "actions",
                        "elements": [
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "emoji": True,
                                    "text": "Approve"
                                },
                                "style": "primary",
                                # "action_id":"approve_button",
                                "value": "approve_button"
                            },
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "emoji": True,
                                    "text": "Reject"
                                },
                                "style": "danger",
                                # "action_id":"reject_button",
                                "value": "reject_button"
                            }
                        ]
                    }
                ]
        }
        return slack_message

    def post_message(event_data):
        # print(event_data)
        Slack_Message.job_name= event_data["job-name"]
        message = Slack_Message.interactive_message("bot-testing","")
        try:
            response = slack_client.chat_postMessage(**message)
            logging.info("Message sent to slack channel")
        
        except SlackApiError as e:
            logging.debug("Error Message: %s",e.response["error"])
            return CommonResponseHelper.send_error_response(str(e.response["error"]))  
        
        return CommonResponseHelper.send_success_response(message)
    

    def interactive(event_data):
        if event_data['type'] == 'url_verification':
            return {'challenge': event_data['challenge']}
        
        if event_data['type'] == 'block_actions':
            action = event_data['actions'][0]
            user = event_data['user']['id']
            channel_id = event_data['channel']['id']
            
            if action['action_id'] == 'approve_button':
                # Action on approval
                response_text = f"<@{user}> has approved the build for Jenkins job '{Slack_Message.job_name}'."
            
            elif action['action_id'] == 'reject_button':
                # Action on rejection
                response_text = f"<@{user}> has rejected the build for Jenkins job '{Slack_Message.job_name}'."

            try:
                response = slack_client.chat_postMessage(
                        channel=channel_id,
                        text=response_text
                    )
                print(response)
            except SlackApiError as e:
                print("Error sending message:", e.response['error'])
                return CommonResponseHelper.send_error_response(str(e.response["error"]))  
            
        return CommonResponseHelper.send_success_response(action['action_id'])
    

    def slack_events(event_data):
        # if event_data['type'] == 'url_verification':
        #     return {'challenge': event_data['challenge']}
        
        logging.info("entered slack event function: %s", event_data['type'])
        if event_data['type'] == 'actions':
            action = event_data['actions'][0]['value']
            user = event_data['user']['id']
            channel_id = event_data['channel']['id']
            
            if action == 'approve_button':
                # Action on approval
                response_text = f"<@{user}> has approved the build for Jenkins job '{Slack_Message.job_name}'."
            
            elif action == 'reject_button':
                # Action on rejection
                response_text = f"<@{user}> has rejected the build for Jenkins job '{Slack_Message.job_name}'."

            try:
                response = slack_client.chat_postMessage(
                        channel=channel_id,
                        text=response_text
                    )
                print(response)
            except SlackApiError as e:
                print("Error sending message:", e.response['error'])
                return CommonResponseHelper.send_error_response(str(e.response["error"]))  
            
        return CommonResponseHelper.send_success_response(action['action_id'])
