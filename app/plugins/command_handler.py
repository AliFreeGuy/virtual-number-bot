from pyrogram import Client, filters
from utils import logger , cache  , btn , txt
from utils import filters as f
from utils.connection import connection as con
import requests
from utils.utils import alert
from utils.utils import join_checker


@Client.on_message(f.updater &f.bot_is_on & f.user_is_active & f.user_is_join, group=2)
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

    elif status == 'join' :
        await joined_handler(bot , call )

        

async def callino_amount_manager(bot , call ):
    try : 
        setting = con.setting
        data = requests.get(f'http://api.ozvinoo.xyz/web/{setting.callino_key}/get-balance')
        if data.status_code == 200 :
            data = data.json()
            await alert(bot , call , msg=f'موجودی حساب کالینو : {data["balance"]}')
    except Exception as e :
        await alert(bot , call , msg= str(e))


async def joined_handler(bot , call ):
    if con :

        channels = con.setting.channels
        not_join_channels = await join_checker(bot , call ,channels)
        if not_join_channels :
            await bot.send_message(call.from_user.id   , text = con.setting.join_text  , reply_markup = btn.join_channels_url(not_join_channels))
            await alert(bot , call , 'هنوز که تو کانالا جوین نشدی !')
            logger.info(f'user not join channel : {str(call.from_user.id)}')
        else :
            await bot.delete_messages(call.from_user.id , call.message.id)
            await bot.send_message(call.from_user.id , text = con.setting.start_text)
            logger.info(f'user is join channel : {str(call.from_user.id)}')

