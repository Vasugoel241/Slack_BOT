import os
from app import app

if __name__ == "__main__":
   
    if os.environ.get('SLACK_BOT_TOKEN') is None:
        print ("SLACK_BOT_TOKEN env variable is not defined")
    elif os.environ.get('CHATBOT_NAME') is None:
        print ("CHATBOT_NAME env variable is not defined")
    elif os.environ.get('SLACK_WEBHOOK_URL') is None:
        print ("SLACK_WEBHOOK_URL env variable is not defined")
   
    app.run(debug = True, host='0.0.0.0')
