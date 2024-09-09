
import jdatetime
from datetime import datetime
import jdatetime
import jdatetime
from datetime import datetime

admin_panel = 'منو مدیریت ربات :'
recaved_support_message = 'پیام شما دریافت شد به زودی ادمین های ما پاسخ میدن !'
admin_message = 'پاسخ خود را ارسال کنید . درصورت منصرف شدن بر روی /cancel بزنید'
admin_message_cancel = 'با موفقیت کنسل شد !'
admin_message_sended = 'با موفقیت پیام شما ارسال شد !'
timedout_get_code = 'زمان دریافت کد گذشته است.'

healthy_number = '✅ این شماره سالم و بن نمیباشد !'
broken_number = '❌ این شماره سالم نیست و بن شده است !'


user_is_logout = 'شما قبلا از این حساب خارج شده اید !'


def logout_text(text):

    text = f'''ربات از اکانت خارج شد 
➖➖➖➖➖➖➖➖➖➖➖
{text}'''
    return text

logout_text_q = 'با خروج ربات از اکانت دیگر امکان دریافت کد نیست ایا اطمینان دارید ربات از اکانت خارج شود ؟'




def send_number_to_user_text(number_data , admin_text, code=None ):

    if code :
        code_text = f'کد دریافتی : `{str(code)}`\n➖➖➖➖➖➖➖➖➖➖➖'
  
    text = f'''
{code_text if code else ''}
کشور : `{number_data['countery']}`
قیمت : `{number_data['price']}`
شماره : `{number_data['number']}`

{admin_text}

'''
    return text


def send_code_to_user_text(number_data , admin_text, code=None):
    if code :
        code_text = f'کد دریافتی : `{str(code)}`\n➖➖➖➖➖➖➖➖➖➖➖'
  
    text = f'''
{code_text if code else ''}
کشور : `{number_data['countery']}`
قیمت : `{number_data['price']}`
شماره : `{number_data['number']}`

'''
    return text


def inventory_transfer_confirmation(sender ,recever , amount ):
    text = f'''ایا انتقال {amount} تومان به کاربر {recever} موافقت میکنید ؟'''
    return text



def success_transfer(text , status_code):
    if status_code['status'] == 200 :
        text = f'{text}\n\n✅ عملیات با موفقیت انجام شد ! کد پیگیری : {status_code[str("code")]}'
        return text 

    else :
        text = f'{text}\n\n❌ خطا در پردازش اطلاعات'
        return text 
    


err_inventory_increase = 'خطا لطفا دوباره تلاش کنید !'
err_limit_amount = 'خطا مبلغ وارد شده معتبر نیست لطفا دوباره تلاش کنید !'



def log_transfer(sender_username, receiver_username, amount, code):
    sender_link = f"tg://openmessage?user_id={sender_username.chat_id}"
    receiver_link = f"tg://openmessage?user_id={receiver_username.chat_id}"
    now_date_time  = jdatetime.datetime.now().strftime("%Y/%m/%d %H:%M")
    text = f'''
💸 انتقال موجودی 

دریفات  کننده : [ {sender_username.chat_id} ]({sender_link})
موجودی دریفات کننده : {sender_username.wallet}
ارسال کننده : [ {receiver_username.chat_id} ]({receiver_link})
موجودی ارسال کننده : {receiver_username.wallet}
مقدار انتقالی : {amount}
کد پیگیری : {code}

⏰ {now_date_time}
'''
    return text

not_found = 'اینجا چیزی نیست :('

number_not_found = 'موجودی این کشور به اتمام رسیده !'


def profile_data_text(user):


    user_data = user.data if hasattr(user, 'data') else user
    
    now = datetime.now()
    jalali_now = jdatetime.datetime.fromgregorian(datetime=now)
    formatted_date_now = jalali_now.strftime('%Y/%m/%d - %H:%M:%S')
    
    creation_date = datetime.fromisoformat(user_data['creation'])
    jalali_creation_date = jdatetime.datetime.fromgregorian(datetime=creation_date)
    formatted_date_creation = jalali_creation_date.strftime('%Y/%m/%d')
    
    total_payments_amount = sum(payment['amount'] for payment in user_data['payments'] if payment['status'])
    total_transfers_count = len(user_data['transfers'])
    orders = 1  
    
    text = f'''
👤 شناسه کاربری : `{str(user_data['chat_id'])}`
📆 تاریخ عضویت : `{formatted_date_creation}`
💰 موجودی حساب : `{user_data['wallet']} تومان`
🛍 تعداد سفارشات : `{str(len(user.orders))} سفارش`
💳 مجموع واریزی‌ها : `{total_payments_amount} تومان`
💸 مجموع انتقالی‌ها : `{total_transfers_count} انتقال`

⏰ {formatted_date_now}
'''
    return text




user_is_auth = 'شما احراز هویت شدی :)'
send_user_auth = f'لطفا مدارک خود را ارسال کنید :'




def payment_text(text, amount):
    # متن پرداخت با استفاده از مبلغ
    payment_message = f'💳 برای ورود به درگاه زرین پال و پرداخت {amount} تومن می‌توانید از کلید زیر استفاده کنید :'
    # ترکیب متن ورودی با پیام پرداخت و پیغام دکمه
    return f'{text}\n\n{payment_message}'



def success_transfer_text(amoutn ,user_wallet ):
    now_date_time  = jdatetime.datetime.now().strftime("%Y/%m/%d %H:%M")
    text = f'''
💸 واریز به حساب
💰 مبلغ : {str(amoutn)}
💰 موجودی : {str(user_wallet)}

⏰ {now_date_time}
'''
    return text





def backup_buy_number(chat_id , number , country  , price   , wallet   , old_amount , new_amount ):

    now_date_time  = jdatetime.datetime.now().strftime("%Y/%m/%d %H:%M")

    text = f'''
💰خرید موفق

توسط کاربر : {chat_id}
شماره : {number}
کشور : {country}
قیمت : {price}
موجودی کاربر : {wallet}

موجودی قبلی کالینو : {str(old_amount)}
موجودی جدید کالینو : {str(new_amount)}


⏰ {now_date_time}'''
    
    return text




def get_code(code ):

    text = f'کد شما : {str(code)}'
    return text