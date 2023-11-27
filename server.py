import os
from config import setuplogger, logger
setuplogger()
from app import app

if __name__ == "__main__":
   
    if os.environ.get('SLACK_BOT_TOKEN') is None:
        logger.error("SLACK_BOT_TOKEN env variable is not defined")
    elif os.environ.get('SIGNING_SECRET') is None:
        logger.error("SIGNING_SECRET env variable is not defined")
    elif os.environ.get('CHANNEL_ID') is None:
        logger.error("CHANNEL_ID env variable is not defined")
   
    app.run(debug = True, host='0.0.0.0')
