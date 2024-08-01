from pyrogram import Client, filters
from utils import logger , cache  , btn , txt
from utils import filters as f
from utils.connection import connection as con
import requests
from utils.utils import alert , deleter
from utils.utils import join_checker
from utils import utils
import config
import jdatetime
from datetime import datetime

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


        elif msg.text in ['افزایش موجودی'] :
            await inventoryـincrease(bot , msg )
            
        elif msg.text == 'برگشت به منو قبل 🔙':
            await start_manager(bot , msg )
        
        elif msg.text == 'انتقال موجودی' : 
            await inventory_transfer(bot , msg )
        
        elif msg.text in ['/profile' , 'حساب کاربری']:
            await profile_manager(bot , msg )
        

    elif msg.contact :
        setting = con.setting
        user_phone = str(msg.contact.phone_number)
        user = con.update_phone(chat_id=msg.from_user.id , phone=user_phone)
        if user == 200 :
            await bot.send_message(msg.from_user.id , text = setting.inventory_increase_text , reply_markup = btn.inventory_increase_btn())


        










async def profile_manager(bot , msg ):
    user = con.get_user(msg.from_user.id)
    await bot.send_message(chat_id = msg.from_user.id , text = txt.profile_data_text(user) , reply_markup  = btn.profile_data_btn(user) , reply_to_message_id = msg.id)


    

async def  inventoryـincrease(bot , msg ) :
    setting = con.setting
    user = con.get_user(msg.from_user.id)
    await bot.send_message(msg.from_user.id , text = setting.inventory_increase_text , reply_markup = btn.inventory_increase_btn())
    if setting.auth_phone and user.phone == 'none' :
                await bot.send_message(msg.from_user.id , text = setting.auth_phone_text , reply_markup = btn.get_user_contact())




async def inventory_transfer(bot , msg ):
    setting = con.setting
    user = con.get_user(msg.from_user.id)
    user_chat_id = await bot.ask(msg.from_user.id , setting.inventory_transfer_text , reply_to_message_id = msg.id )

    if user_chat_id and user_chat_id.text and user_chat_id.text.isdigit():
        user_transfer = con.get_user(int(user_chat_id.text))
        
        if user_transfer :
            inventory = await bot.ask(msg.from_user.id  , setting.inventory_transfer_amount_text , reply_to_message_id = user_chat_id.id)
            if inventory and inventory.text and inventory.text.isdigit():
                print(user.wallet)
                if int(inventory.text)<= user.wallet and user.wallet > 0 and msg.from_user.id != user_chat_id.text:
                    sender = msg.from_user.id
                    recever = user_chat_id.text
                    amount = inventory.text
                    await bot.send_message(chat_id  = msg.from_user.id ,
                                            text = txt.inventory_transfer_confirmation(sender , recever , amount)  , 
                                            reply_markup = btn.inventory_transfer(sender , recever , amount) ,
                                            reply_to_message_id = inventory.id)
                
                else :await bot.send_message(msg.from_user.id , setting.inventory_transfer_error_text)
            else :await bot.send_message(msg.from_user.id , setting.inventory_transfer_error_text)
        else :await bot.send_message(msg.from_user.id , setting.inventory_transfer_error_text)
    else :await bot.send_message(msg.from_user.id , setting.inventory_transfer_error_text)
    






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
    
    elif status == 'transfer' :
        await inventory_transfer_call(bot , call )
    
    elif status == 'cancel_transfer' :
        await bot.delete_messages(call.from_user.id , call.message.id)
        await alert(bot  , call , msg='عملیات با موفقیت کنسل شد !')
        await start_manager(bot , call )
    
    elif status == 'inventory_increase' :
        await inventory_increase_manager(bot , call )

    
    elif status == 'deposits' :
        await deposits_manager(bot , call )
    
    elif status == 'back_profile' :
        await back_profile_manager(bot , call )
    
    elif status == 'transitions' :
        await transitions_manager(bot , call )
    
    elif status == 'authentication' :
        await  authentication_manager(bot , call )
    
    elif status == 'send_auth_data' :
        await send_auth_data_manager(bot , call )
    
    elif status == 'get_number_list' :
        await get_number_list_manager(bot , call )
        

    



async def get_number_list_manager(bot , call ):
    setting = con.setting
    token  = setting.callino_key
    data  = utils.get_numbers(token)
    if data :
        file_path = "countries_info.txt"
        with open(file_path, 'w', encoding='utf-8') as file:
            for entry in data:
                file.write(f"کشور: {entry['country']}  -  قیمت: {entry['price']}  -  رنج: {entry['range']}  -  وضعیت: {entry['count']}  -  ایموجی: {entry['emoji']}\n\n")
        await bot.send_document(call.from_user.id , document = file_path)





async def send_auth_data_manager(bot , call ):
    user= con.get_user(call.from_user.id)
    if user.is_auth is False : 
        setting = con.setting
        user_auth = await bot.ask(chat_id = call.from_user.id , text = txt.send_user_auth , reply_to_message_id = call.message.id )
        await user_auth.copy(chat_id = int(setting.backup_channel) ,reply_markup = btn.user_auth_btn(user =user  ) )
        await bot.send_message(chat_id = call.from_user.id , text = setting.received_auth_text )

    else :
        await alert(bot , call , txt.user_is_auth)
    



async def authentication_manager(bot , call ):
    setting = con.setting
    user = con.get_user(call.from_user.id)
    await bot.edit_message_text(chat_id = call.from_user.id ,
                                text = setting.send_auth_data_text ,
                                message_id = call.message.id ,
                                reply_markup = btn.profile_data_btn(user = user , back=True , auth=True))




async def back_profile_manager(bot , call ):
    user = con.get_user(call.from_user.id)
    await bot.edit_message_text(chat_id = call.from_user.id , text = txt.profile_data_text(user) , reply_markup  = btn.profile_data_btn(user=user) , message_id = call.message.id)



async def transitions_manager(bot, call):
    user = con.get_user(call.from_user.id)
    print(user.transfers)  # این خط برای دیباگ نگه داشته شده است
    text = []
    user.transfers.sort(key=lambda x: x['creation_date'], reverse=True)
    recent_transfers = user.transfers[:5][::-1]
    for transfer in recent_transfers:
        creation_date = datetime.strptime(transfer['creation_date'][:19], '%Y-%m-%dT%H:%M:%S')
        shamsi_date = jdatetime.datetime.fromgregorian(datetime=creation_date).strftime('%Y/%m/%d %H:%M:%S')
        sender_id = transfer['sender_chat_id']
        receiver_id = transfer['receiver_chat_id']
        text.append(f"تاریخ: {shamsi_date}\nفرستنده: {sender_id}\nگیرنده: {receiver_id}\nمقدار: {transfer['amount']} تومان")
    
    if text :
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.id, text='\n\n'.join(text), reply_markup=btn.profile_data_btn(user = user , back=True))
    else :
        await alert(bot , call , msg=txt.not_found)


async def deposits_manager(bot, call):


    user = con.get_user(call.from_user.id)
    text = []
    user.payments.sort(key=lambda x: x['creation'], reverse=True)
    recent_payments = user.payments[:10][::-1]
    for payment in recent_payments:
        creation_date = datetime.strptime(payment['creation'][:19], '%Y-%m-%dT%H:%M:%S')
        shamsi_date = jdatetime.datetime.fromgregorian(datetime=creation_date).strftime('%Y/%m/%d %H:%M:%S')
        status_text = '✅ پرداخت موفق' if payment['status'] else '❌ پرداخت ناموفق'
        text.append(f"تاریخ: {shamsi_date}\n{status_text} | {payment['amount']} تومان")
    
    if text :
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.id, text='\n\n'.join(text), reply_markup=btn.profile_data_btn(user = user , back=True))
    else :
        await alert(bot , call , msg=txt.not_found)






async def inventory_increase_manager(bot , call):
    user = con.get_user(call.from_user.id)
    setting = con.setting
    validates = []

    if setting.auth_status and not user.is_auth:
        validates.append(setting.auth_text)
    
    if setting.auth_phone and user.phone == 'none':
        validates.append(setting.auth_phone_text)

    if setting.ir_phone_only and not (user.phone.startswith('+98') or user.phone.startswith('98')):
        validates.append(setting.ir_phone_only_text)

    if not validates:

        await deleter(bot , call , call.message.id +1 )
        amount =await  bot.ask(chat_id = call.from_user.id , text = setting.inventory_increase_text  , reply_to_message_id = call.message.id)

        if amount and amount.text and amount.text.isdigit() :
            
            user_amount = int(amount.text)

            if user_amount <= setting.user_limit_pay :

                paymnet_data = con.payment_url(chat_id=call.from_user.id , amount=user_amount)
                print(paymnet_data)
                if paymnet_data :
                    await bot.edit_message_text(chat_id = call.from_user.id ,
                                                text = txt.payment_text(call.message.text) ,
                                                message_id = call.message.id ,
                                                reply_markup = btn.payment_btn(paymnet_data) 
                                                )
            
            else :await alert(bot , call ,msg=txt.err_limit_amount)







        else : await alert(bot , call , msg=txt.err_inventory_increase)
        await deleter(bot , call , call.message.id +1 )
    else :await alert(bot , call , msg=validates[0])

    







    

async def inventory_transfer_call(bot , call ):
    setting = con.setting
    data = call.data.split(':')[1]
    sender = int(data.split('_')[0])
    receiver = int(data.split('_')[1])
    amount = int(data.split('_')[2])
    data = con.transfer(sender , receiver , amount)
    if data['status'] == 200 :
        await bot.edit_message_text(chat_id = call.from_user.id ,
                                    text = txt.success_transfer(text = call.message.text , status_code=data),
                                    message_id = call.message.id
                                    )
        
        await bot.send_message(chat_id = setting.backup_channel , text = txt.log_transfer(sender , receiver  , amount , data['code']))
        user_wallet = con.get_user(int(receiver))
        await bot.send_message(chat_id = int(receiver) , text = txt.success_transfer_text(amount , user_wallet.wallet))






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

