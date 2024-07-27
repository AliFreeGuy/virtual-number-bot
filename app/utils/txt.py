



admin_panel = 'منو مدیریت ربات :'
recaved_support_message = 'پیام شما دریافت شد به زودی ادمین های ما پاسخ میدن !'
admin_message = 'پاسخ خود را ارسال کنید . درصورت منصرف شدن بر روی /cancel بزنید'
admin_message_cancel = 'با موفقیت کنسل شد !'
admin_message_sended = 'با موفقیت پیام شما ارسال شد !'



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
    sender_link = f"tg://openmessage?user_id={sender_username}"
    receiver_link = f"tg://openmessage?user_id={receiver_username}"
    text = f'''
💸 انتقال موجودی 

ارسال کننده : [ {sender_username} ]({sender_link})
دریافت کننده : [ {receiver_username} ]({receiver_link})
مقدار انتقالی : {amount}
کد پیگیری : {code}
'''
    return text





def payment_text(text):
    return f'{text}\n\n✅ برای ورود به درگاه بر روی دکمه زیر بزنید'




def success_transfer_text(amoutn ,user_wallet ):
    text = f'''
💸 واریز به حساب
💰 مبلغ : {str(amoutn)}
💰 موجودی : {str(user_wallet)}
'''
    return text