import os
from slack_sdk import WebClient
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = ".env"
load_dotenv(env_path)

# Get Slack webhook URL from environment variable
# webhook_url = os.getenv('SLACK_WEBHOOK_URL')
webhook_url = 'https://hooks.slack.com/services/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'

env_path = ".env"
load_dotenv(env_path)
slack_token = os.environ['SLACK_BOT_TOKEN']
client = WebClient(token=slack_token)

def send_slack_message(message):
    try:
        response = client.chat_postMessage(
            channel='#bot-testing', 
            text=message
        )
        if response['ok']:
            print("Message sent successfully!")
        else:
            print("Failed to send message. Error:", response['error'])
    except Exception as e:
        print("An error occurred:", e)

def main():
    # Get message from user input or set a default message
    message = input("Enter the message you want to send to Slack: ")
    if not message:
        message = "Hello from the Python script using Slack webhook!"
    
    # Send the message using Slack webhook
    send_slack_message(message)

if __name__ == "__main__":
    main()