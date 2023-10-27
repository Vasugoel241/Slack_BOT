import os
import requests
# from dotenv import load_dotenv

# env_path = ".env"
# load_dotenv(env_path)

# Get Slack webhook URL from environment variable
# webhook_url = os.getenv('SLACK_WEBHOOK_URL')
webhook_url = 'https://hooks.slack.com/services/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'


# Function to send a message using Slack webhook
def send_slack_message(message):
    payload = {
        'channel': '#bot-testing',  
        'text': message
    }
    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()  # Raise an exception if the request was not successful
        print("Message sent successfully!")
    except requests.exceptions.HTTPError as errh:
        print("HTTP Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", err)

def main():
    
    message = input("Enter the message you want to send to Slack: ")
    if not message:
        message = "Hello from the Python script using Slack webhook!"

    
    send_slack_message(message)

if __name__ == "__main__":
    main()
