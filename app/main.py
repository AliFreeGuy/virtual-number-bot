
from pyrogram import Client , filters 
from pyromod import listen
import config

if config.DEBUG == 'True' :


    bot = Client(
            name = "bot",
                api_id=config.API_ID , 
                api_hash=config.API_HASH , 
                bot_token=config.BOT_TOKEN , 
                proxy=config.PROXY ,
                plugins=dict(root="plugins"))
else :
    bot = Client(
                name = "bot",
                api_id=config.API_ID , 
                api_hash=config.API_HASH , 
                bot_token=config.BOT_TOKEN , 
                plugins=dict(root="plugins"))

if __name__ == '__main__' : 
    bot.run()

