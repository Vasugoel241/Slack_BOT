import os
from dotenv import load_dotenv
env_path = ".env"
load_dotenv(env_path)

slack_token = os.environ['SLACK_BOT_TOKEN']
signing_secret = os.environ['SIGNING_SECRET']
webhook_url = os.environ['SLACK_WEBHOOK_URL']
