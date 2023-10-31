import os
import logging
from dotenv import load_dotenv
env_path = ".env"
load_dotenv(env_path)

class Config:
    slack_token = os.environ['SLACK_BOT_TOKEN']
    signing_secret = os.environ['SIGNING_SECRET']
    webhook_url = os.environ['SLACK_WEBHOOK_URL']

    def configure_logging():
        logging.basicConfig(filename="logfile.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
