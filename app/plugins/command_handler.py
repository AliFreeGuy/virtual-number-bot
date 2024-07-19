from pyrogram import Client, filters
from utils import logger , cache  , btn , txt
from utils import filters as f
from utils.connection import connection as con
import requests
from utils.utils import alert
from utils.utils import join_checker
import config


@Client.on_message(f.updater &f.bot_is_on & f.user_is_active & f.user_is_join, group=2)
async def command_manager(bot, msg):
    

    if msg and msg.text :


        if msg.text == '/privacy' :
            setting  = con.setting
            await bot.send_message(msg.from_user.id , setting.privacy_text)
        
        elif msg.text in ['/start' ,]:
            await start_manager(bot , msg )
        
        elif msg.text in ['راهنما و قوانین']:
            await help_and_rule_manager(bot ,msg )
        
        elif msg.text == '/help' :
            setting = con.setting
            await bot.send_message(msg.from_user.id , setting.help_text)
        
        elif msg.text == '/rule' :
            setting = con.setting
            await bot.send_message(msg.from_user.id , setting.rule_text)
        

        elif msg.text in ['/support'  , 'پشتیبانی']:
            await support_manager(bot , msg )
            



async def support_manager(bot ,msg ):
    setting = con.setting
    message = await bot.ask(chat_id = msg.from_user.id , text = setting.support_text , reply_to_message_id = msg.id )

    if message :

        if message.text and message.text == '/cancel' :
            await bot.ask(chat_id = msg.from_user.id , text = setting.start_text , reply_markup = btn.user_panel() )
            
        else :
            user_profile = f'tg://openmessage?user_id={message.from_user.id}'
            await message.copy(config.ADMIN , reply_markup =btn.support_btn(
                                                                            msg_id=message.id , 
                                                                            chat_id=message.from_user.id ,
                                                                            url=user_profile ,
                                                                            user_name = message.from_user.first_name) )
            await message.reply_text(txt.recaved_support_message , quote=True)

        



                
    
            

        
        



async def start_manager(bot ,msg ):
    setting = con.setting
    await bot.send_message(msg.from_user.id ,  setting.start_text , reply_markup = btn.user_panel())



async def help_and_rule_manager(bot , msg ):
    setting = con.setting
    await bot.send_message(msg.from_user.id , setting.help_text , reply_markup= btn.help_and_rule_btn())





































@Client.on_callback_query(f.updater &f.bot_is_on & f.user_is_active, group=0)
async def callback_manager(bot, call):

    logger.warning(call.data)
    status = call.data.split(':')[0]


    if status == 'callino_amount' : 
        await callino_amount_manager(bot ,call )

    elif status == 'join' :
        await joined_handler(bot , call )
    
    elif status in ['help_text' , 'rule_text']:
        await help_and_rule_call(bot , call )
    
    elif status == 'answer' :
        await support_answer(bot , call )

    


async def support_answer(bot , call ):
    user_chat_id = call.data.split(':')[1]
    user_message_id = call.data.split(':')[2]

    admin_msg = await bot.ask(chat_id = call.from_user.id , text = txt.admin_message , reply_to_message_id = call.message.id )

    if admin_msg :

        
        if admin_msg.text and admin_msg.text == '/cancel' :
            await alert(bot , call , msg = txt.admin_message_cancel)
            
        else :
            await admin_msg.copy(int(user_chat_id)  , reply_to_message_id = int(user_message_id) )
            await alert(bot , call , msg = txt.admin_message_sended)


        



        



async def help_and_rule_call(bot , call ):
    setting = con.setting
    try :
        if call.data == 'help_text' : 
            await bot.edit_message_text(chat_id  = call.from_user.id , text = setting.help_text ,message_id = call.message.id , reply_markup = btn.help_and_rule_btn())
        elif call.data == 'rule_text' : 
            await bot.edit_message_text(chat_id  = call.from_user.id , text = setting.rule_text ,message_id = call.message.id , reply_markup = btn.help_and_rule_btn())
    except :pass




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

