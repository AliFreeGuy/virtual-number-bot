from pyrogram.types import (ReplyKeyboardMarkup, InlineKeyboardMarkup,InlineKeyboardButton , KeyboardButton , WebAppInfo)
import config
import jdatetime
from utils.connection import connection  as con






def inventory_increase_btn():
    buttons = []
    buttons.append([InlineKeyboardButton(text='افزایش موجودی',callback_data='inventory_increase'),])
    return InlineKeyboardMarkup(buttons)



def get_user_contact():
    marks = [
                    
                    [KeyboardButton('تایید شماره' , request_contact=True)],
                    ['برگشت به منو قبل 🔙 ' ],
            ]
    return ReplyKeyboardMarkup(marks , resize_keyboard=True)



def payment_btn(data):
    return InlineKeyboardMarkup([[InlineKeyboardButton(text='ورود به درگاه پرداخت',url=data['url']),]])


def inventory_transfer(sender , recever , amount):
    buttons = []
    transfer_key = f'transfer:{str(sender)}_{str(recever)}_{str(amount)}'
    buttons.append([InlineKeyboardButton(text='تایید و انتقال موجودی',callback_data=transfer_key),])
    buttons.append([InlineKeyboardButton(text='کنسل',callback_data='cancel_transfer'),])
    return InlineKeyboardMarkup(buttons)





def user_auth_btn(user ):
    buttons = []
    now_date_time  = jdatetime.datetime.now().strftime("%Y/%m/%d %H:%M")
    buttons.append([InlineKeyboardButton(text=now_date_time,callback_data='date_time'),])
    buttons.append([
                    InlineKeyboardButton(text='پروفایل 👤',url= f"tg://openmessage?user_id={user.chat_id}"),
                    InlineKeyboardButton(text='اطلاعات 📇',url= f"{config.ADMIN_PANEL}accounts/user/{str(user.id)}/change/"),
                    ])


      
        
       

    return InlineKeyboardMarkup(buttons)




def profile_data_btn(user , back = False , auth = False ):
    is_auth = user.is_auth
    
    buttons = []
    
    if not back :
        buttons.append([InlineKeyboardButton(text='احراز هویت',callback_data='authentication'),InlineKeyboardButton(text='انتقال موجودی',callback_data='inventory_transfer')])
        buttons.append([InlineKeyboardButton(text='واریز ها',callback_data='deposits'),
                        InlineKeyboardButton(text='انتقالی ها',callback_data='transitions'),
                        InlineKeyboardButton(text='سفارش ها',callback_data='orders')])
    
    else : 

        if not auth :
            buttons.append([
                        InlineKeyboardButton(text='🔙',callback_data='back_profile'),
                        InlineKeyboardButton(text='احراز هویت',callback_data='authentication'),])
        else :
            buttons.append([
                        InlineKeyboardButton(text='🔙',callback_data='back_profile'),
                        InlineKeyboardButton(text='ارسال مدارک',callback_data='send_auth_data'),])

        
        buttons.append([InlineKeyboardButton(text='واریز ها',callback_data='deposits'),
                        InlineKeyboardButton(text='انتقالی ها',callback_data='transitions'),
                        InlineKeyboardButton(text='سفارش ها',callback_data='orders')])

    return InlineKeyboardMarkup(buttons)







def join_channels_url(channels):
    persian_numbers = ['اول', 'دوم', 'سوم', 'چهارم', 'پنجم']  
    buttons = []
    for idx, channel in enumerate(channels):
        text = f"کانال {persian_numbers[idx]}"
        buttons.append([InlineKeyboardButton(text=text, url=channel)])
    buttons.append([InlineKeyboardButton(text='عضو شدم',callback_data='join:joined')])
    return InlineKeyboardMarkup(buttons)




def admin_panel_btn():
    buttons = []
    buttons.append([InlineKeyboardButton(text='ورود به ادمین پنل',url=config.ADMIN_PANEL),])
    buttons.append([InlineKeyboardButton(text='موجودی حساب کالینو',callback_data=f'callino_amount'),])
    buttons.append([InlineKeyboardButton(text='دریافت آپدیت کشور ها',callback_data=f'get_number_list'),])
    buttons.append([InlineKeyboardButton(text='دریافت سشن استرینگ',callback_data=f'get_sesstion_string'),])

    return InlineKeyboardMarkup(buttons)
    
def user_panel():
    marks = [
                    ['خرید شماره مجازی'],
                    ['حساب کاربری' , 'افزایش موجودی',],
                    ['راهنما و قوانین' , 'پشتیبانی' , 'چکر شماره']
            ]
    return ReplyKeyboardMarkup(marks , resize_keyboard=True )




def help_and_rule_btn():
    buttons = []
    buttons.append([InlineKeyboardButton(text='راهنما',callback_data='help_text'),InlineKeyboardButton(text='قوانین',callback_data=f'rule_text')])
    return InlineKeyboardMarkup(buttons)


def support_btn(msg_id , chat_id , url  , user_name):

    buttons = []
    buttons.append([
        InlineKeyboardButton(text='پاسخ',callback_data=f'answer:{chat_id}:{msg_id}'),
        InlineKeyboardButton(text=user_name,url=url)
        ])
    return InlineKeyboardMarkup(buttons)



def get_code_menu(request_id , setting ):
    
    buttons = []

    one_list  = [
        InlineKeyboardButton(text='بررسی کیفیت',callback_data=f'get_code:quality:{request_id}'),
        ]
    
    if setting.checker_status :
        one_list.append(InlineKeyboardButton(text='چکر شماره',callback_data=f'get_code:checker:{request_id}'),)
    buttons.append(one_list)
    
    buttons.append([
        InlineKeyboardButton(text='کنسل',callback_data=f'get_code:cancel:{request_id}'),
        InlineKeyboardButton(text='دریافت کد',callback_data=f'get_code:getcode:{request_id}'),
        
        ])
    return InlineKeyboardMarkup(buttons)





def get_twice_code(request_id , setting ):
    
    buttons = []

    one_list  = [
        InlineKeyboardButton(text='بررسی کیفیت',callback_data=f'get_code:quality:{request_id}'),
        ]
    
    if setting.checker_status :
        one_list.append(InlineKeyboardButton(text='چکر شماره',callback_data=f'get_code:checker:{request_id}'),)
    buttons.append(one_list)
    
    buttons.append([
        InlineKeyboardButton(text='خروج ربات',callback_data=f'get_code:logoutbot:{request_id}'),
        InlineKeyboardButton(text='دریافت کد مجدد',callback_data=f'get_code:getcode:{request_id}'),
        
        ])
    return InlineKeyboardMarkup(buttons)




def logout_q(request_id) : 
    buttons = []
    buttons.append([

        InlineKeyboardButton(text='لغو',callback_data=f'get_code:logoutbot_no:{request_id}'),
        InlineKeyboardButton(text='تایید',callback_data=f'get_code:logoutbot_ok:{request_id}'),

        ])
    return InlineKeyboardMarkup(buttons)



def get_admin_code(request_id ):
    buttons = []
    buttons.append([
        InlineKeyboardButton(text='دریافت کد',callback_data=f'get_code:getcode_admin:{request_id}'),
        InlineKeyboardButton(text='خروج ربات',callback_data=f'get_code:logoutbot_admin:{request_id}'),
        ])
    return InlineKeyboardMarkup(buttons)




def numbers_list_btn(current_page=1):
    setting = con.setting
    buttons = []
    buttons.append([
        InlineKeyboardButton(text='🌎 نام کشور', callback_data='note'),
        InlineKeyboardButton(text='📊 وضعیت', callback_data='note'),
        InlineKeyboardButton(text='💰 قیمت', callback_data='note'),
    ])

    # Filter numbers based on the show_numbers setting
    if setting.show_numbers == 'active':
        filtered_numbers = [number for number in setting.numbers if number['status']]
    elif setting.show_numbers == 'inactive':
        filtered_numbers = [number for number in setting.numbers if not number['status']]
    else:  # 'all'
        filtered_numbers = setting.numbers

    # Calculate the start and end indices for the current page
    start_index = (current_page - 1) * setting.number_rows
    end_index = start_index + setting.number_rows
    paginated_numbers = filtered_numbers[start_index:end_index]

    for number in paginated_numbers:
        status_text = '✅ موجود' if number['status'] else '❌ ناموجود'
        buttons.append([
            InlineKeyboardButton(text=number["name"], callback_data=f'get_number:{number["id"]}'),
            InlineKeyboardButton(text=status_text, callback_data=f'get_number:{number["id"]}'),
            InlineKeyboardButton(text=number['price'], callback_data=f'get_number:{number["id"]}'),
        ])

    # Add navigation buttons if necessary
    navigation_buttons = []
    if current_page > 1:
        navigation_buttons.append(InlineKeyboardButton(text='صفحه قبل', callback_data=f'change_page:{current_page - 1}'))
    if end_index < len(filtered_numbers):
        navigation_buttons.append(InlineKeyboardButton(text='صفحه بعد', callback_data=f'change_page:{current_page + 1}'))

    if navigation_buttons:
        buttons.append(navigation_buttons)

    return InlineKeyboardMarkup(buttons)













# def vid_editor_quality(user_lang , vid_key ):

#     buttons = []
#     if user_lang == 'fa' : 
#         q1= 'کیفیت خوب'
#         q2='کیفیت متوسط'
#         q3= 'کیفیت کم'
#         quality_btn = [
#             InlineKeyboardButton(text=q1,callback_data=f'editor_q1:{vid_key}'),
#             InlineKeyboardButton(text=q2,callback_data=f'editor_q2:{vid_key}'),
#             InlineKeyboardButton(text=q3,callback_data=f'editor_q3:{vid_key}'),
#             ] 
#         buttons.append(quality_btn)
    

#     elif user_lang == 'en' : 
#         q1= 'good quality'
#         q2=  'mid quality'
#         q3= 'low quality'
#         quality_btn = [
#             InlineKeyboardButton(text=q1,callback_data=f'editor_q1:{vid_key}'),
#             InlineKeyboardButton(text=q2,callback_data=f'editor_q2:{vid_key}'),
#             InlineKeyboardButton(text=q3,callback_data=f'editor_q3:{vid_key}'),
#             ] 
#         buttons.append(quality_btn)
    
#     return InlineKeyboardMarkup(buttons)









# def vid_editor_btn(vid_data , user_lang  ):
    
#     buttons = []
#     if user_lang == 'en'  : 
#         buttons.append([
#             InlineKeyboardButton(text='❌ Cancel',callback_data=f'cancel-editor:{vid_data}'),
#             InlineKeyboardButton(text='♻️ Status',callback_data=f'status-editor:{vid_data}') , 
#                         ])
        
#     elif user_lang == 'fa' : 
#         buttons.append([
#             InlineKeyboardButton(text='❌ کنسل',callback_data=f'cancel-editor:{vid_data}'),
#             InlineKeyboardButton(text='♻️ وضعیت',callback_data=f'status-editor:{vid_data}') ,
#                         ])
#     return InlineKeyboardMarkup(buttons)






# def user_panel_menu(user_lang  , placeholder):
#     setting_text = '⚙️ setting' if user_lang== 'en' else '⚙️ تنظیمات'
#     help_text = '🆘 help' if user_lang == 'en' else '🆘 راهنما'
#     support_text = '🧑‍✈️ support' if user_lang == 'en' else '🧑‍✈️ پشتیبانی'
#     profile_text = '🎫 profile' if user_lang == 'en' else '🎫 پروفایل'
#     plans_text = '🎖 plans' if user_lang == 'en' else '🎖 اشتراک'

#     marks = [
#                     [setting_text , profile_text],
#                     [support_text,help_text,plans_text]
#             ]
#     return ReplyKeyboardMarkup(marks , resize_keyboard=True , placeholder=placeholder)












# def admin_inline_query(sub_code):
#     reply_markup=InlineKeyboardMarkup(
#                     [
#                         [InlineKeyboardButton(
#                             " فعالسازی اشتراک | Activate subscription",
#                             url=f"https://t.me/{config.BOT_USERNAME}?start=sub_{sub_code}",
#                         )]
#                     ]
#                 )
#     return reply_markup




# def join_channel(lang , url ):
#     buttons = []
#     if lang == 'en'  : 
#         buttons.append([InlineKeyboardButton(text='Join Channel',url=url)])
#         buttons.append([InlineKeyboardButton(text='I became a member',callback_data='joined')])
#     elif lang == 'fa' : 
#         buttons.append([InlineKeyboardButton(text='عضویت در کانال',url=url)])
#         buttons.append([InlineKeyboardButton(text='عضو شدم',callback_data='joined')])
#     return InlineKeyboardMarkup(buttons)



# def admin_chat_id(user_lang , chat_id ):
#     if user_lang == 'fa' : 
#         return InlineKeyboardMarkup([[InlineKeyboardButton(f'خرید از پشتیبانی'  , url=f'tg://openmessage?user_id={str(chat_id)}')]])
#     elif user_lang == 'en' :
#         return InlineKeyboardMarkup([[InlineKeyboardButton(f'Buy from support'  , url=f'tg://openmessage?user_id={str(chat_id)}')]])
        

# def setting_btn(user_lang , user_quality):
#     buttons = []


#     fa_text = f'✔️ 🇮🇷 فارسی' if user_lang == 'fa' else '🇮🇷 فارسی'
#     en_text = f'✔️ 🇺🇸 English' if user_lang == 'en' else '🇺🇸 English'
#     lang_btn = [
#             InlineKeyboardButton(text=fa_text,callback_data=f'setting:lang_fa'),
#             InlineKeyboardButton(text=en_text,callback_data=f'setting:lang_en'),
#             ] 
#     buttons.append(lang_btn)


#     if user_lang == 'fa' : 
#         q1= f'✔️ کیفیت خوب' if user_quality == 'q1' else 'کیفیت خوب'
#         q2= f'✔️ کیفیت متوسط' if user_quality == 'q2' else 'کیفیت متوسط'
#         q3= f'✔️ کیفیت کم' if user_quality == 'q3' else 'کیفیت کم'
#         quality_btn = [
#             InlineKeyboardButton(text=q1,callback_data=f'setting:quality_q1'),
#             InlineKeyboardButton(text=q2,callback_data=f'setting:quality_q2'),
#             InlineKeyboardButton(text=q3,callback_data=f'setting:quality_q3'),
#             ] 
#         buttons.append(quality_btn)
    

#     elif user_lang == 'en' : 
#         q1= f'✔️ good quality' if user_quality == 'q1' else 'good quality'
#         q2= f'✔️ mid quality' if user_quality == 'q2' else 'mid quality'
#         q3= f'✔️ low quality' if user_quality == 'q3' else 'low quality'
#         quality_btn = [
#             InlineKeyboardButton(text=q1,callback_data=f'setting:quality_q1'),
#             InlineKeyboardButton(text=q2,callback_data=f'setting:quality_q2'),
#             InlineKeyboardButton(text=q3,callback_data=f'setting:quality_q3'),
#             ] 
#         buttons.append(quality_btn)
    
#     return InlineKeyboardMarkup(buttons)


    
# def join_channels_url(channels):
#     persian_numbers = ['اول', 'دوم', 'سوم', 'چهارم', 'پنجم']  
#     buttons = []
#     for idx, channel in enumerate(channels):
#         text = f"کانال {persian_numbers[idx]}"
#         buttons.append([InlineKeyboardButton(text=text, url=channel)])
#     buttons.append([InlineKeyboardButton(text='عضو شدم',callback_data='join:joined')])
#     return InlineKeyboardMarkup(buttons)




# def cancel_task(data ):
#     buttons = []
#     buttons.append([InlineKeyboardButton(text='لغو عملیات',callback_data=data)])
#     return InlineKeyboardMarkup(buttons)
    
# def plans_btn(plans , support_id=None ):
#     buttoons = []
#     for plan in plans :
#         plan_tag = plan['tag']
#         buttoons.append(InlineKeyboardButton(text=plan['name'], callback_data=f'plans:{plan_tag}'))
#     chunked_buttons = [buttoons[i:i + 3] for i in range(0, len(buttoons), 3)]
#     if  support_id : 
#         chunked_buttons.append([InlineKeyboardButton(text='خرید اشتراک' , url=f'https://t.me/{support_id}')])
#     return InlineKeyboardMarkup(chunked_buttons)

    
# def get_file(call_data):
#     buttons = [[InlineKeyboardButton(text='دریافت فایل',callback_data=call_data)]]
#     return InlineKeyboardMarkup(buttons)



































































































