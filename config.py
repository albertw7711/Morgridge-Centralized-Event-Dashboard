"""
This file contains the constants and preconfigurations for the bot
"""


import time
import os
from dotenv import load_dotenv
load_dotenv()

# Load current .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Bot Prefix (e.g. !help, !get_announcements)
PREFIX = "!"

# Bot owner
OWNERS = []

# Database configuration
DATABASE_NAME = ""

# Beta Channel ID to scrape from:
CHANNEL_ID = set()


BACKEND_URL = "127.0.0.1"
BACKEND_PORT = 5000
BACKEND_ROUTE = "insert"
BACKEND_ROUTE_ADDCHANNEL = "channels"
BACKEND_ROUTE_DELCHANNEL = "channels"
BACKEND_ROUTE_CURCHANNEL = "curchannel"