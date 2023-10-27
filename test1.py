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


# Convert the payload to JSON format
# payload_json = json.dumps(payload)

# # Set the headers for the request
# headers = {
#     "Content-type": "application/json"
# }

# Send a POST request to the Slack Webhook URL with the payload
# response = requests.post(webhook_url, data=payload_json, headers=headers)

# Check the response
# if response.status_code == 200:
#     print("Message sent successfully to Slack!")
# else:
#     print("Failed to send message to Slack. Status code:", response.status_code)
#     print("Response:", response.text)
