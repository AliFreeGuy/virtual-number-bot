from pyrogram import Client, filters
from utils import logger , cache 
from utils import filters as f
from utils.connection import connection as con
import requests
from utils.utils import alert



@Client.on_message(f.updater &f.bot_is_on & f.user_is_active, group=2)
async def command_manager(bot, msg):
    

    if msg and msg.text :


        if msg.text == '/privacy' :
            setting  = con.setting
            await bot.send_message(msg.from_user.id , setting.privacy_text)

        
        






@Client.on_callback_query(f.updater &f.bot_is_on & f.user_is_active, group=0)
async def callback_manager(bot, call):
    

    status = call.data.split(':')[0]


    if status == 'callino_amount' : 
        await callino_amount_manager(bot ,call )
        

async def callino_amount_manager(bot , call ):
    try : 
        setting = con.setting
        data = requests.get(f'http://api.ozvinoo.xyz/web/{setting.callino_key}/get-balance')
        if data.status_code == 200 :
            data = data.json()
            await alert(bot , call , msg=f'موجودی حساب کالینو : {data["balance"]}')
    except Exception as e :
        await alert(bot , call , msg= str(e))