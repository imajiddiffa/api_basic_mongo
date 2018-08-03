import os

from datetime import timedelta
from dotenv import load_dotenv, find_dotenv
from urllib.parse import quote_plus

from pymongo.read_preferences import ReadPreference

# Load environment
load_dotenv(find_dotenv())


class Configuration(object):

    # PYMONGO NEW DB CONFIGURATION
    MONGO_URI = os.getenv("MONGO_URI", "MONGO_URI")

    # JWT
    JWT_ALGORITHM = "HS256"
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_AUTH_URL_RULE = None
    JWT_EXPIRATION_DELTA = timedelta(days=7)  # token expired in 1 weeks