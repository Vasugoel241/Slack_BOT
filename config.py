import os
import logging
import logging.config
import yaml
import mysql.connector
from dotenv import load_dotenv

env_path = ".env"
load_dotenv(env_path)


def setuplogger():
        with open('logging_config.yaml', 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
logger = logging.getLogger('app')
class Config:
    
    slack_token = os.environ['SLACK_BOT_OAUTH_TOKEN']
    signing_secret = os.environ['SIGNING_SECRET']
    channel_id = os.environ['CHANNEL_ID']

    mysql_host = os.environ['MYSQL_HOST']
    mysql_username = os.environ['MYSQL_USERNAME']
    mysql_password = os.environ['MYSQL_PASSWORD']
    mysql_database = os.environ['MYSQL_DATABASE']

    file =  open('./auth_users.json', 'r')

    def connect_to_database():
        connection = mysql.connector.connect(
            host=Config.mysql_host,
            user=Config.mysql_username,
            passwd=Config.mysql_password,
            db=Config.mysql_database
            )
        
        return connection
