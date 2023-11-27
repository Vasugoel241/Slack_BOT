from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import json
import requests
import time
import hmac
import hashlib

from slackbot_db_handler import SlackbotDB
from common_reponse_helper import CommonResponseHelper
from config import Config
from config import setuplogger, logger
setuplogger()

slack_client = WebClient(token=Config.slack_token)
response = slack_client.auth_test()
json_data = json.load(Config.file)

class Slack_Message:

    def interactive_message(channel_id, message, job_name):
        slack_message = { "channel":channel_id,
                "text" : "Jenkins Job Approval Request",       
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": message,
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
                                    "text": "Approve"
                                },
                                "style": "primary",
                                "action_id":"approve_button",
                                "value": job_name
                            },
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "Reject"
                                },
                                "style": "danger",
                                "action_id":"reject_button",
                                "value": job_name
                            }
                        ]
                    }
                ],
                "timout":30
        }
        return slack_message


    def post_message(event_data):
        
        logger.info(f"Post Message event data => {event_data}")
        
        job_name = event_data["job-name"]
        channel_id = Config.channel_id
        message = f'Approval Request for Job : {job_name}'
        response_text = Slack_Message.interactive_message(channel_id,message,job_name)
        
        logger.info(f"Job name => {job_name}")
        
        try:
            
            job_count = SlackbotDB.get_jobcount(job_name)
            if job_count > 0:
                SlackbotDB.update_job_status(job_name)
            else:
                SlackbotDB.add_jobname(job_name)
           
            response = slack_client.chat_postMessage(**response_text)
            logger.info(f"Message sent to slack channel : {response}")
        
        except SlackApiError as e:
            logger.exception(f"Error : {e}")
            return CommonResponseHelper.send_error_response(str(e.response["error"]))  
        
        return CommonResponseHelper.send_success_response(response_text)
    

    def check_user(name, user_id, data):
        for user in data:
            if user["username"] == name and user["memberid"] == user_id:
                return True
        return False


    def delete_message(channel_id,message_ts):
        try:
            slack_client.chat_delete(
                    channel=channel_id,
                    ts=message_ts
                )
            logger.info("Request Message Deleted")
        except:
            logger.exception("Message Not Found")
            # return CommonResponseHelper.send_error_response("Message Not Found") 


    def get_action_status(payload):

        logger.info("="*40)
        logger.info(f"payload ===  {payload}")
       
        if payload['type'] == 'block_actions':
            action = payload['actions'][0]
            user = payload['user']['id']
            username = payload['user']['name']
            channel_id = payload['channel']['id']
            job_name = action['value']
            message_ts = payload['message']['ts']
            response_text = ""
            
            # Verify User
            auth_user = Slack_Message.check_user(username, user, json_data)

            if auth_user == False:
                logger.info(f"Permission Denied: {username}")
                response_text = f"<@{user}> Permission denied. You do not have access to perform this task."

            elif auth_user == True:
                
                # Deleting message if Time Limit exceeds
                message_time = float(message_ts)
                if float(time.time()-message_time) > float(60*60*24):
                    logger.info("Approval Request Time Limit Exceeded")
                    response_text = f"<@{user}> Approval Request Time Limit Exceeded for Job {job_name}"
                    Slack_Message.delete_message(channel_id, message_ts)
                
                # Action on approval
                elif action['action_id'] == 'approve_button':
                    choice = "approved"  
                    SlackbotDB.update_action(job_name,choice,username,user)  
                    Slack_Message.delete_message(channel_id, message_ts)        
                    response_text = f"<@{user}> has approved the build for Jenkins job : {job_name}."
                    
                    logger.info(f'{username} approved {job_name}')
        
                # Action on rejection
                elif action['action_id'] == 'reject_button':
                    choice = "rejected"
                    SlackbotDB.update_action(job_name,choice,username,user)  
                    Slack_Message.delete_message(channel_id, message_ts)
                    response_text = f"<@{user}> has rejected the build for Jenkins job : {job_name}."
                    
                    logger.info(f'{username} rejected {job_name}')

            try:
                response = slack_client.chat_postMessage(
                        channel=channel_id,
                        text=response_text,
                        timeout=30
                    )
                logger.info(response)
            except SlackApiError as e:
                logger.exception(f"Error sending message: {e}")
                return CommonResponseHelper.send_error_response(str(e.response["error"]))  
            
        return CommonResponseHelper.send_success_response(action['value'])
    

    def get_status(job_name):
        choice = ""
        
        if len(job_name) == 0:
            logger.error("No job name found")
            return CommonResponseHelper.send_error_response("Job Not Found")
    
        try:
            data = SlackbotDB.get_action(job_name)
            
            if data:
                choice = data[0]
            else:
                logger.error(f"Job {job_name} Not Found")
                return CommonResponseHelper.send_error_response("Job not found") 
        
        except Exception as e:
            logger.exception(f"Error sending message: {e}")
            return CommonResponseHelper.send_error_response(str(e.response["error"])) 
        logger.info(choice)
        return choice