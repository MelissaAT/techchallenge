import os
from dotenv import load_dotenv

load_dotenv() 

class Config(object):
    SITE_URL = os.environ["SITE_URL"]
    APP_SECRET = os.environ["APP_SECRET_KEY"]