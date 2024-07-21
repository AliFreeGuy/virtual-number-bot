from pyrogram import Client
from os import environ as env


PROXY = {"scheme": env.get("PROXY_SCHEME"),
         "hostname": env.get("PROXY_HOSTNAME"),
         "port": int(env.get("PROXY_PORT"))}
BOT_SESSION = env.get('BOT_SESSION') or env.get('BOT_NAME')
API_ID = env.get('API_ID')
API_HASH = env.get('API_HASH')
BOT_TOKEN = env.get('BOT_TOKEN')


bot = Client('test' , api_id=API_ID , api_hash=API_HASH , bot_token=BOT_TOKEN , proxy=PROXY)

with bot :
    data = bot.export_session_string()
    print(data)