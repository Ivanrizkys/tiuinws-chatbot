import os
from dotenv import load_dotenv

load_dotenv()
CHATBOT_TOKEN = os.getenv('CHATBOT_TOKEN')
SERVER_URL = os.getenv('SERVER_URL')
STRAPI_CLIENT_TOKEN = os.getenv('STRAPI_CLIENT_TOKEN')

HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {STRAPI_CLIENT_TOKEN}'
}