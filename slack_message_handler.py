from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import logging

from common_reponse_helper import CommonResponseHelper
from config import Config

Config.configure_logging()
slack_client = WebClient(token=Config.slack_token)

response = slack_client.auth_test()
class Slack_Message:
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
                                "value": "approve"
                            },
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "emoji": True,
                                    "text": "Reject"
                                },
                                "style": "danger",
                                "value": "reject"
                            }
                        ]
                    }
                ]
        }
        return slack_message

    def post_message(event_data):
        # print(event_data)
        # message = event_data["message"]
        message = Slack_Message.interactive_message("bot-testing","")
        try:
            response = slack_client.chat_postMessage(**message)
            logging.info("Message sent to slack channel")
        
        except SlackApiError as e:
            logging.debug("Error Message: %s",e.response["error"])
            return CommonResponseHelper.send_error_response(str(e.response["error"]))  
        
        return CommonResponseHelper.send_success_response(message)
    

    # def interactive():
    # # Verify the request signature
    #     if not signature_verifier.is_valid_request(request.get_data(), request.headers):
    #         return "Invalid Request", 403

    #     # Parse the interactive message payload
    #     payload = request.form['payload']
    #     payload_dict = json.loads(payload)

    #     # Handle the interactive message actions
    #     if payload_dict['type'] == 'block_actions':
    #         action = payload_dict['actions'][0]  # Assuming only one action for simplicity
    #         if action['action_id'] == 'approve_button':
    #             # Handle "Approve" button action
    #             client.chat_postMessage(
    #                 channel=payload_dict['channel']['id'],
    #                 text='You clicked the Approve button!'
    #             )
    #         elif action['action_id'] == 'reject_button':
    #             # Handle "Reject" button action
    #             client.chat_postMessage(
    #                 channel=payload_dict['channel']['id'],
    #                 text='You clicked the Reject button!'
    #             )

    #     return '', 200


    def slack_events(event_data):
          
        if event_data['type'] == 'url_verification':
            return {'challenge': event_data['challenge']}

        if event_data['type'] == 'interactive_message':
            callback_data = event_data['callback_id']
            if callback_data == 'approval_buttons':
                action = event_data['actions'][0]['value']
                user = event_data['user']['id']
                username = event_data['user']['username']
                channel = event_data['channel']['id']
                job_name = event_data['message']['attachments'][0]['text'].split('Job: ')[1].strip()

                if action == 'approve':
                    # Handle approval logic (e.g., proceed with the build)
                    # You can add your logic here

                    response_text = f"<@{user}> has approved the build for Jenkins job '{job_name}'. Proceeding with the build."
                elif action == 'reject':
                    # Handle rejection logic (e.g., stop the build)
                    # You can add your logic here

                    response_text = f"<@{user}> has rejected the build for Jenkins job '{job_name}'. Stopping the build."

                # Send the response back to Slack
                try:
                    response = slack_client.chat_postMessage(
                        channel=channel,
                        text=response_text
                    )
                    print(response)
                except SlackApiError as e:
                    print("Error sending message:", e.response['error'])
                    return CommonResponseHelper.send_error_response(str(e.response["error"]))  
        
        return CommonResponseHelper.send_success_response(action)

