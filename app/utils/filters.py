from pyrogram import filters
from utils.connection import connection as con 
from utils.logger import logger
import config
from datetime import datetime





async def updater(_ , cli , msg ):
    try :
        
        user = con.user(chat_id=msg.from_user.id , full_name=msg.from_user.first_name )
        print(user)
    except Exception as e :
         logger.warning(e)
         
    return True



updater = filters.create(updater)

