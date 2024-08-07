# Bot Database# ===================================
# ||||||||||||(Libraries)||||||||||||
# ===================================
import asyncio
import random

from pyrogram import Client, filters, enums, errors
from pyrogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, \
    InlineKeyboardButton, CallbackQuery
from pyromod import listen
from collections import defaultdict
import database
import aiohttp
import re
import requests

# ===================================
# |||||||||||(requirements)||||||||||
# ===================================
api_id = 29928833
api_hash = "9fca526e490949ff2278b383053cfa30"
app = Client(name="mybot",
             api_id=api_id,
             api_hash=api_hash,
             bot_token="6001924985:AAGc_r19tapkoDzaBIrGyrAvmbYNKLg4zGE")  # BOT Token
link_payment = "http://mrmajazino.ir"
url_get_prices = "https://api.ozvinoo.xyz/web/785683988:BtUbJ16cZtsw78JoXk675A6ElAs5BToeQABJP5oaU3CT/get-prices/1"
url_get_account = "https://api.ozvinoo.xyz/web/785683988:BtUbJ16cZtsw78JoXk675A6ElAs5BToeQABJP5oaU3CT/getNumber/1/"
url_get_code = "https://api.ozvinoo.xyz/web/785683988:BtUbJ16cZtsw78JoXk675A6ElAs5BToeQABJP5oaU3CT/getCode/"
url_log_out = "https://api.ozvinoo.xyz/web/785683988:BtUbJ16cZtsw78JoXk675A6ElAs5BToeQABJP5oaU3CT/logout/"

vak_links = {
    "orderphone": "https://vak-sms.com/api/getNumber/?apiKey=577e38a21ff84e57bea34c34586891aa&service=tg&country=",
    "getcode": "https://vak-sms.com/api/getSmsCode/?apiKey=577e38a21ff84e57bea34c34586891aa&idNum=",
    "setorderstat": "https://vak-sms.com/api/setStatus/?apiKey=6ae430f6c0b348b5bfe0fc56c932db69&status=end&idNum=",
    "again_code": "https://vak-sms.com/api/setStatus/?apiKey=6ae430f6c0b348b5bfe0fc56c932db69&status=send&idNum="}

vak_country = {'Bulgaria': 'bg',
               'United Kingdom': 'gb',
               'Georgia': 'ge',
               'Hong Kong': 'hk',
               'Indonesia': 'id',
               'Kyrgyzstan': 'kg',
               'Kazakhstan': 'kz',
               'Laos': 'la',
               'Lithuania': 'lt',
               'Latvia': 'lv',
               'Netherlands': 'nl',
               'Phillipines': 'ph',
               'Pakistan': 'pk',
               'Poland': 'pl',
               'Russia': 'ru'}

flags = {
    "Russia": "🇷🇺",
    "Phillipines": "🇵🇭",
    "United Kingdom": "🏴󠁧󠁢󠁥󠁮󠁧󠁿",
    "Ukraine": "🇺🇦",
    "Kazakhstan": "🇰🇿",
    "Hong Kong": "🇭🇰",
    "China": "🇨🇳",
    "Philippines": "🇵🇭",
    "Myanmar": "🇲🇲",
    "Indonesia": "🇮🇩",
    "Malaysia": "🇲🇾",
    "Kenya": "🇰🇪",
    "Tanzania": "🇹🇿",
    "Vietnam": "🇻🇳",
    "Kyrgyzstan": "🇰🇬",
    "USA (virtual)": "🇺🇸",
    "USA": "🇺🇸",
    "Israel": "🇮🇱",
    "HongKong": "🇭🇰",
    "Poland": "🇵🇱",
    "England": "🏴󠁧󠁢󠁥󠁮󠁧󠁿",
    "Madagascar": "🇲🇬",
    "DCongo": "🇨🇩",
    "Nigeria": "🇳🇬",
    "Macao": "🇲🇴",
    "Egypt": "🇪🇬",
    "India": "🇮🇳",
    "Ireland": "🇮🇪",
    "Cambodia": "🇰🇭",
    "Laos": "🇱🇦",
    "Haiti": "🇭🇹",
    "Ivory": "🇨🇮",
    "Gambia": "🇬🇲",
    "Serbia": "🇷🇸",
    "Yemen": "🇾🇪",
    "Southafrica": "🇿🇦",
    "Romania": "🇷🇴",
    "Colombia": "🇨🇴",
    "Estonia": "🇪🇪",
    "Azerbaijan": "🇦🇿",
    "Canada": "🇨🇦",
    "Morocco": "🇲🇦",
    "Ghana": "🇬🇭",
    "Argentina": "🇦🇷",
    "Uzbekistan": "🇺🇿",
    "Cameroon": "🇨🇲",
    "Chad": "🇹🇩",
    "Germany": "🇩🇪",
    "Lithuania": "🇱🇹",
    "Croatia": "🇭🇷",
    "Sweden": "🇸🇪",
    "Iraq": "🇮🇶",
    "Netherlands": "🇳🇱",
    "Latvia": "🇱🇻",
    "Austria": "🇦🇹",
    "Belarus": "🇧🇾",
    "Thailand": "🇹🇭",
    "Saudiarabia": "🇸🇦",
    "Mexico": "🇲🇽",
    "Taiwan": "🇹🇼",
    "Spain": "🇪🇸",
    "Iran": "🇮🇷",
    "Algeria": "🇩🇿",
    "Slovenia": "🇸🇮",
    "Bangladesh": "🇧🇩",
    "Senegal": "🇸🇳",
    "Turkey": "🇹🇷",
    "Czech": "🇨🇿",
    "Srilanka": "🇱🇰",
    "Peru": "🇵🇪",
    "Pakistan": "🇵🇰",
    "Newzealand": "🇳🇿",
    "Guinea": "🇬🇳",
    "Mali": "🇲🇱",
    "Venezuela": "🇻🇪",
    "Ethiopia": "🇪🇹",
    "Mongolia": "🇲🇳",
    "Brazil": "🇧🇷",
    "Afghanistan": "🇦🇫",
    "Uganda": "🇺🇬",
    "Angola": "🇦🇴",
    "Cyprus": "🇨🇾",
    "France": "🇫🇷",
    "Papua": "🇵🇬",
    "Mozambique": "🇲🇿",
    "Nepal": "🇳🇵",
    "Belgium": "🇧🇪",
    "Bulgaria": "🇧🇬",
    "Hungary": "🇭🇺",
    "Moldova": "🇲🇩",
    "Italy": "🇮🇹",
    "Paraguay": "🇵🇾",
    "Honduras": "🇭🇳",
    "Tunisia": "🇹🇳",
    "Nicaragua": "🇳🇮",
    "Timorleste": "🇹🇱",
    "Bolivia": "🇧🇴",
    "Costarica": "🇨🇷",
    "Guatemala": "🇬🇹",
    "Uae": "🇦🇪",
    "Zimbabwe": "🇿🇼",
    "Puertorico": "🇵🇷",
    "Sudan": "🇸🇩",
    "Togo": "🇹🇬",
    "Kuwait": "🇰🇼",
    "Salvador": "🇸🇻",
    "Libyan": "🇱🇾",
    "Jamaica": "🇯🇲",
    "Trinidad": "🇹🇹",
    "Ecuador": "🇪🇨",
    "Swaziland": "🇸🇿",
    "Oman": "🇴🇲",
    "Bosnia": "🇧🇦",
    "Dominican": "🇩🇴",
    "Syrian": "🇸🇾",
    "Qatar": "🇶🇦",
    "Panama": "🇵🇦",
    "Cuba": "🇨🇺",
    "Mauritania": "🇲🇷",
    "Sierra Leone": "🇸🇱",
    "Jordan": "🇯🇴",
    "Portugal": "🇵🇹",
    "Barbados": "🇧🇧",
    "Burundi": "🇧🇮",
    "Benin": "🇧🇯",
    "Brunei": "🇧🇳",
    "Bahamas": "🇧🇸",
    "Botswana": "🇧🇼",
    "Belize": "🇧🇿",
    "Central African Republic": "🇨🇫",
    "Dominica": "🇩🇲",
    "Grenada": "🇬🇩",
    "Georgia": "🇬🇪",
    "Greece": "🇬🇷",
    "Guinea-Bissau": "🇬🇼",
    "Guyana": "🇬🇾",
    "Iceland": "🇮🇸",
    "Comoros": "🇰🇲",
    "Saint Kitts and Nevis": "🇰🇳",
    "Liberia": "🇱🇷",
    "Lesotho": "🇱🇸",
    "Malawi": "🇲🇼",
    "Namibia": "🇳🇦",
    "Niger": "🇳🇪",
    "Rwanda": "🇷🇼",
    "Slovakia": "🇸🇰",
    "Suriname": "🇸🇷",
    "Tajikistan": "🇹🇯",
    "Monaco": "🇲🇨",
    "Bahrain": "🇧🇭",
    "Reunion": "🇷🇪",
    "Zambia": "🇿🇲",
    "Armenia": "🇦🇲",
    "Somalia": "🇸🇴",
    "Republic of the Congo": "🇨🇬",
    "Chile": "🇨🇱",
    "Burkina Faso": "🇧🇫",
    "Lebanon": "🇱🇧",
    "Gabon": "🇬🇦",
    "Albania": "🇦🇱",
    "Uruguay": "🇺🇾",
    "Mauritius": "🇲🇺",
    "Bhutan": "🇧🇹",
    "Maldives": "🇲🇻",
    "Guadeloupe": "🇬🇵",
    "Turkmenistan": "🇹🇲",
    "French Guiana": "🇬🇫",
    "Finland": "🇫🇮",
    "Saint Lucia": "🇱🇨",
    "Luxembourg": "🇱🇺",
    "Saint Vincent and the Grenadines": "🇻🇨",
    "Equatorial Guinea": "🇬🇶",
    "Djibouti": "🇩🇯",
    "Antigua and Barbuda": "🇦🇬",
    "Cayman Islands": "🇰🇾",
    "Montenegro": "🇲🇪",
    "Denmark": "🇩🇰",
    "Norway": "🇳🇴",
    "Australia": "🇦🇺",
    "Eritrea": "🇪🇷",
    "South Sudan": "🇸🇸",
    "Sao Tome and Principe": "🇸🇹",
    "Aruba": "🇦🇼",
    "Montserrat": "🇲🇸",
    "Anguilla": "🇦🇮"
}

admin = 785683988
admins = [785683988, 1786981564]

reports_channel = -1002028706548


def detect_number_language(number):
    persian_pattern = r'^[\u0660-\u0669\u06F0-\u06F9]+$'
    latin_pattern = r'^[0-9]+$'

    if re.match(persian_pattern, number):
        return "persian"
    elif re.match(latin_pattern, number):
        return "english"
    else:
        return "error"


def countryPanel():
    code = []
    country = []
    for x in vak_country:
        country.append(x)
    for c in country:
        button = [InlineKeyboardButton(text=c + flags[c], callback_data=f"second_api\n{vak_country[c]}")]
        code.append(button)
    return code


def persian_to_english_numbers(persian_number):
    persian_to_english = {
        '۰': '0',
        '۱': '1',
        '۲': '2',
        '۳': '3',
        '۴': '4',
        '۵': '5',
        '۶': '6',
        '۷': '7',
        '۸': '8',
        '۹': '9'
    }
    english_number = ''
    for char in persian_number:
        if char in persian_to_english:
            english_number += persian_to_english[char]
        else:
            english_number += char
    return int(english_number)


loop = asyncio.get_event_loop()


async def fetch_data_checker(url, params):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            return await response.json()


async def checker_call(number):
    number = f"+{number.strip('+')}"
    url_checker = "http://checker.irbots.com:2021/check"
    api_key_checker = "785683988:ISbefnUTioexcCtrGW"
    phone_numbers_checker = number
    params_checker = {
        "key": api_key_checker,

        "numbers": phone_numbers_checker
    }
    print(number)
    response_json_checker = await fetch_data_checker(url_checker, params_checker)
    print(response_json_checker)
    if str(response_json_checker["data"][phone_numbers_checker]) == 'ban':
        return 0
    else:
        return 1


async def checker(number):
    number = f"+{number.strip('+')}"
    url_checker = "http://checker.irbots.com:2021/check"
    api_key_checker = "785683988:ISbefnUTioexcCtrGW"
    phone_numbers_checker = number
    params_checker = {
        "key": api_key_checker,

        "numbers": phone_numbers_checker
    }
    response_checker = requests.get(url_checker, params=params_checker)
    response_json_checker = response_checker.json()
    print(response_json_checker)
    if str(response_json_checker["status"]) == 'ok' and str(
            response_json_checker["data"][phone_numbers_checker]) == 'True':
        print("ok")
        return 1
    else:
        return 0


async def checker_sell(number):
    url_checker = "http://checker.irbots.com:2021/check"
    api_key_checker = "785683988:ISbefnUTioexcCtrGW"
    phone_numbers_checker = number
    params_checker = {
        "key": api_key_checker,

        "numbers": phone_numbers_checker
    }
    print(number)
    response_json_checker = await fetch_data_checker(url_checker, params_checker)
    print(response_json_checker)
    if str(response_json_checker["data"][phone_numbers_checker]) == 'ban':
        return 0
    elif str(response_json_checker["status"]) == 'ok' and str(
            response_json_checker["data"][phone_numbers_checker]) == 'True':
        return 1
    elif str(response_json_checker["status"]) == 'ok':
        return 2
    else:
        return 3


def join_checker(_, client: Client, message: Message):
    if len(database.view_join_link()) > 0:
        try:
            link = database.view_join_link()[0][0]
            chat_id = int(database.view_join_link()[0][1])
            user = client.get_chat_member(chat_id=chat_id, user_id=message.from_user.id)
            return True
        except:
            message.reply_text("برای ادامه و استفاده از ربات باید ابتدا وارد چنل زیر شوید⛔",
                               reply_markup=InlineKeyboardMarkup([
                                   [InlineKeyboardButton("عضویت در کانال", url=link)],
                                   [InlineKeyboardButton("عضو شدم✅", callback_data="joined")]
                               ]))
            return False
    else:
        return True


join_filter = filters.create(join_checker)  # filter of join_checker


def admin_checker(_, client: Client, message: Message):
    for x in database.view_admins():
        if message.from_user.id == int(x[0]):
            return True
    return False


admin_filter = filters.create(admin_checker)


def block_checker(_, client: Client, message: Message):
    if len(database.search_block_user(message.from_user.id)) == 0:
        return True
    else:
        message.reply_text("شما توسط ادمین مسدود شده اید❌")
        return False


block_filter = filters.create(block_checker)


def Tree():
    return defaultdict(Tree)


async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


listCancel = []


async def auto_code(orderId, phone, user_id):
    count = 0
    while count < 650:
        result = await fetch_data(vak_links["getcode"] + orderId)
        if result.get("smsCode"):
            result = result['smsCode']
            await fetch_data(vak_links["again_code"] + orderId)
            await app.send_message(chat_id=user_id,text=f"شماره :\n +`{phone}`\n\nکد دریافتی :\n `{result}`",
                                        reply_markup=InlineKeyboardMarkup([
                                            [InlineKeyboardButton(text="دریافت کد مجدد",
                                                                  callback_data=f"vak-getcode-a\n{orderId}\n{phone}")]
                                        ]))
            break
        else:
            count += 1
            await asyncio.sleep(1)
            # await callback.answer("کدی دریافت نشده!")


async def cancelTheNumber(orderId, price, userid, message_id):
    try:
        await asyncio.sleep(600)
        if orderId in listCancel:
            database.update_status_buy(userid, "T")
            pass
        else:
            result = await fetch_data(vak_links["setorderstat"] + orderId)
            if result['status'] == "update":
                try:
                    await app.delete_messages(userid, message_id)
                except:
                    pass
                inv = int(database.inf_user(user_id=userid)[0][1])
                inv = inv + price
                database.update_inv_user(userid, inv)
                database.update_status_buy(userid, "T")
                await app.send_message(chat_id=userid, text="شماره سفارش داده شده منقضی شد")
                await app.send_message(chat_id=reports_channel,
                                       text=f"مقدار {price} به حساب کاربر {userid} برگشت داده شد.\nموجودی کاربر : {inv}")
                listCancel.append(orderId)
            else:
                database.update_status_buy(userid, "T")
    except Exception as e:
        print(e)
        pass


user_pocket = Tree()


# ===================================
# |||||||||||||(Buttons)|||||||||||||
# ===================================

def home_btn(user_id):
    if len(database.search_admins(user_id)) > 0:
        home = ReplyKeyboardMarkup([
            ["خرید شماره مجازی"],
            ["👤 حساب کاربری", "افزایش موجودی"],
            ["☎ پشتیبانی", "چکر شماره🔍"],
            ["📍 پنل ادمین"]
        ], resize_keyboard=True)
        return home
    else:
        home = ReplyKeyboardMarkup([
            ["خرید شماره مجازی"],
            ["👤 حساب کاربری", "افزایش موجودی"],
            ["☎ پشتیبانی", "چکر شماره🔍"]
        ], resize_keyboard=True)
        return home


@app.on_message(filters.private & filters.command("start") & join_filter & block_filter)
async def start_handler(client: Client, message: Message):
    if len(database.inf_user(message.from_user.id)) == 0:
        database.insert_users(message.from_user.id, "0", "0")
    else:
        pass
    start_text = database.view_start_text()[0][0]
    await message.reply_text(text=start_text,
                             reply_markup=home_btn(message.from_user.id))
    user_pocket[message.from_user.id]['step'] = 0


@app.on_message(filters.private & filters.regex("🔙 بازگشت به منو اصلی") & join_filter & block_filter)
async def start_handler(client: Client, message: Message):
    if len(database.inf_user(message.from_user.id)) == 0:
        database.insert_users(message.from_user.id, "0", "0")
    else:
        pass
    await message.reply_text("🏠 به منو اصلی بازگشتید", reply_markup=home_btn(message.from_user.id))
    user_pocket[message.from_user.id]['step'] = 0


@app.on_message(filters.private & filters.regex("☎ پشتیبانی") & join_filter & block_filter)
async def start_handler(client: Client, message: Message):
    await message.reply_text("""
    📞 به بخش ارتباط با پشتیبانی خوش آمدید !

🆔 ارتباط مستقیم : @ARC021A

💡 متن توضیحات خود را با رعایت قوانین ارسال کنید :
    """)
    user_pocket[message.from_user.id]['step'] = "support_message"


@app.on_message(filters.private & filters.regex("👤 حساب کاربری") & join_filter & block_filter)
async def start_handler(client: Client, message: Message):
    if len(database.inf_user(message.from_user.id)) == 0:
        database.insert_users(message.from_user.id, "0", "0")
    else:
        pass
    user_data = database.inf_user(message.from_user.id)[0]
    await message.reply_text(
        f"👤 شناسه کاربری : {user_data[0]}\n🛍 تعداد سفارشات : {user_data[2]}\n\n💰موجودی حساب : {user_data[1]} تومان")


@app.on_message(filters.private & filters.regex("افزایش موجودی") & join_filter & block_filter)
async def start_handler(client: Client, message: Message):
    await message.reply_text(f"💶 جهت افزایش موجودی حساب مبلغ مورد نظرخود را به تومان وارد نمایید:")
    user_pocket[message.from_user.id]['step'] = "amount_payment"


@app.on_message(filters.private & filters.regex("چکر شماره🔍") & join_filter & block_filter)
async def start_handler(client: Client, message: Message):
    check_price = database.view_checker_price()[0][0]
    await message.reply_text(
        f"🔍 لطفا شماره هایی که میخواهید چک شود را به صورت زیر ارسال کنید\nقیمت چک کردن هر شماره : {check_price} تومان\n\n+123456789\n+98123456789")
    user_pocket[message.from_user.id]['step'] = "check_number"


@app.on_message(filters.private & filters.regex("خرید شماره مجازی") & join_filter & block_filter)
async def start_handler(client: Client, message: Message):
    await message.reply_text("💠 پنل خود را انتخاب کنید :", reply_markup=ReplyKeyboardMarkup([
        ["شماره های بدون ریپورت", "شماره های خام"],
        ["🔙 بازگشت به منو اصلی"]
    ], resize_keyboard=True))


@app.on_message(filters.private & filters.regex("شماره های خام") & join_filter & block_filter)
async def start_handler(client: Client, message: Message):
    data = database.view_vak_panel()
    if len(data) > 0:
        if len(data) <= 7:
            code = []
            first_btn = [InlineKeyboardButton(text="🌍 نام کشور", callback_data="test"),
                         InlineKeyboardButton(text="💰 قیمت", callback_data="test")]
            code.append(first_btn)
            for d in data:
                button = [InlineKeyboardButton(text=d[0], callback_data=f'vak\n{d[1]}'),
                          InlineKeyboardButton(text=d[2], callback_data=f'vak\n{d[1]}')]
                code.append(button)
            await message.reply_text(f"👈 جهت خرید شماره مجازی روی نام کشور مورد نظر خود کلیک نمایید:",
                                     reply_markup=InlineKeyboardMarkup(code))
        else:
            code = []
            first_btn = [InlineKeyboardButton(text="🌍 نام کشور", callback_data="test"),
                         InlineKeyboardButton(text="💰 قیمت", callback_data="test")]
            code.append(first_btn)
            count = 0
            for d in data:
                if count < 7:
                    button = [InlineKeyboardButton(text=d[0], callback_data=f'vak\n{d[1]}'),
                              InlineKeyboardButton(text=d[2], callback_data=f'vak\n{d[1]}')]
                    code.append(button)
                else:
                    break
            but = [InlineKeyboardButton(text="➡ صفحه بعدی", callback_data=f"next_page_vak")]
            code.append(but)
            await message.reply_text(f"👈 جهت خرید شماره مجازی روی نام کشور مورد نظر خود کلیک نمایید:",
                                     reply_markup=InlineKeyboardMarkup(code))
    else:
        await message.reply_text("❗ در حال حاضر شماره ای موجود نمیباشد")


@app.on_message(filters.private & filters.regex("شماره های بدون ریپورت") & join_filter & block_filter)
async def start_handler(client: Client, message: Message):
    mess = await message.reply_text("درحال پردازش...", reply_markup=ReplyKeyboardMarkup([
        ["🔙 بازگشت به منو اصلی"]
    ]))
    data = await fetch_data(url=url_get_prices)
    code = []
    count = 0
    first_btn = [InlineKeyboardButton(text="🌍 نام کشور", callback_data="test"),
                 InlineKeyboardButton(text="📊 وضعیت", callback_data="test"),
                 InlineKeyboardButton(text="💰 قیمت", callback_data="test")]
    code.append(first_btn)
    for x in data:
        if count < 13:
            price = int(x["price"])
            percent = float(database.view_percent()[0][0])
            per = price * percent
            price = price + per
            if x["country"] != "لهستان 🇵🇱":
                c_count = x["count"]
            else:
                c_count = "❌ ناموجود"
            number = int(price)
            formatted_number = f'{number:,}'
            button = [InlineKeyboardButton(text=x["country"],
                                           callback_data=f'c\n{x["country"]}\n{str(int(price)).replace(".0", "")}'),
                      InlineKeyboardButton(text=c_count,
                                           callback_data=f'c\n{x["country"]}\n{str(int(price)).replace(".0", "")}'),
                      InlineKeyboardButton(text=formatted_number,
                                           callback_data=f'c\n{x["country"]}\n{str(int(price)).replace(".0", "")}')]
            code.append(button)
            count += 1
        else:
            break
    but = [InlineKeyboardButton(text="➡ صفحه بعدی", callback_data=f"next_page-{count}")]
    code.append(but)
    await mess.delete()
    await message.reply_text(f"👈 جهت خرید شماره مجازی روی نام کشور مورد نظر خود کلیک نمایید:",
                             reply_markup=InlineKeyboardMarkup(code))


#######################################admin############################################

admin_btn = ReplyKeyboardMarkup([
    ["افزودن موجودی کاربر", "مشخصات فرد"],
    ["تنظیم سود", "مسدود کردن کاربر"],
    ["تنظیم متن خوشامد گویی", "تنظیم جوین اجباری"],
    ["ارسال پیام تکی", "ارسال همگانی"],
    ["افزودن ادمین", "تعیین نرخ چکر"],
    ["تعیین کشور پنل vak", "حذف کشور پنل vak"],
    ["🔙 بازگشت به منو اصلی"]
], resize_keyboard=True)


@app.on_message(filters.private & filters.regex("📍 پنل ادمین") & admin_filter)
async def start_handler(client: Client, message: Message):
    await message.reply_text("به پنل مدیریت خوش امدید", reply_markup=admin_btn)


@app.on_message(filters.private & filters.regex("افزودن موجودی کاربر") & admin_filter)
async def start_handler(client: Client, message: Message):
    await message.reply_text(
        "لطفا ایدی عددی و موجودی که میخواهید به آن اضافه کنید را به صورت زیر وارد کنید :\nuserid&amount\n123456789&50000")
    user_pocket[message.from_user.id]['step'] = "add_amount"


@app.on_message(filters.private & filters.regex("تنظیم سود") & admin_filter)
async def start_handler(client: Client, message: Message):
    await message.reply_text(
        "لطفا میزان سودی که میخواهید رو به صورت مثال زیر بفرستید!\nمثال :\n0.1\nسود : 20000 * 0.1 = 2000 -> 22000")
    user_pocket[message.from_user.id]['step'] = "percent"


@app.on_message(filters.private & filters.regex("تعیین نرخ چکر") & admin_filter)
async def start_handler(client: Client, message: Message):
    await message.reply_text(
        "لطفا نرخ مورد نظر خود را ارسال نمایید:")
    user_pocket[message.from_user.id]['step'] = "set_checker_price"


@app.on_message(filters.private & filters.regex("مشخصات فرد") & admin_filter)
async def start_handler(client: Client, message: Message):
    await message.reply_text(
        "لطفا ایدی عددی فرد مورد نظر را ارسال نمایید:")
    user_pocket[message.from_user.id]['step'] = "check_user"


@app.on_message(filters.private & filters.regex("ارسال پیام تکی") & admin_filter)
async def start_handler(client: Client, message: Message):
    await message.reply_text(
        "لطفا متن مورد نظر را ارسال نمایید")
    user_pocket[message.from_user.id]['step'] = "user_send"


@app.on_message(filters.private & filters.regex("تنظیم متن خوشامد گویی") & admin_filter)
async def start_handler(client: Client, message: Message):
    await message.reply_text("لطفا متن مورد نظر خود را بفرستید:")
    user_pocket[message.from_user.id]['step'] = "start_text"


@app.on_message(filters.private & filters.regex("تعیین کشور پنل vak") & admin_filter)
async def start_handler(client: Client, message: Message):
    await message.reply_text("لطفا کشور مورد نظر خود را وارد نمایید:",
                             reply_markup=InlineKeyboardMarkup(countryPanel()))


@app.on_message(filters.private & filters.regex("حذف کشور پنل vak") & admin_filter)
async def start_handler(client: Client, message: Message):
    data = database.view_vak_panel()
    code = []
    if len(data) > 0:
        for d in data:
            button = [InlineKeyboardButton(text=d[0], callback_data=f'delete_vak\n{d[1]}')]
            code.append(button)
        await message.reply_text("لطفا کشور مورد نظر خود را وارد نمایید:",
                                 reply_markup=InlineKeyboardMarkup(code))
    else:
        await message.reply_text("هیچ کشوری برای انتخاب وجود ندارد")


@app.on_message(filters.private & filters.regex("تنظیم جوین اجباری") & admin_filter)
async def start_handler(client: Client, message: Message):
    await message.reply_text(
        "لطفا ابتدا ربات را ادمین چنل کرده و سپس لینک و ایدی عددی چنل را به صورت زیر ارسال کنید:\nlink#chatid\nhttps://t.me/testtest#-100123456789")
    user_pocket[message.from_user.id]['step'] = "join_link"


@app.on_message(filters.private & filters.regex("مسدود کردن کاربر") & admin_filter)
async def start_handler(client: Client, message: Message):
    await message.reply_text("لطفا ایدی عددی شخصی که میخواهید مسدود شود را ارسال کنید :")
    user_pocket[message.from_user.id]['step'] = "block_user"


@app.on_message(filters.private & filters.regex("ارسال همگانی") & admin_filter)
async def start_handler(client: Client, message: Message):
    await message.reply_text("لطفا پیام مورد نظر خود را ارسال نمایید :")
    user_pocket[message.from_user.id]['step'] = "all_send"


@app.on_message(filters.private & filters.regex("افزودن ادمین") & admin_filter)
async def start_handler(client: Client, message: Message):
    ad = ""
    for x in database.view_admins():
        ad = ad + f"{x[0]}\n"
    await message.reply_text(f"ادمین های فعلی :\n{ad}\nبرای ادد کردن ادمین جدید لطفا ایدی عددی فرد را وارد کنید!")
    user_pocket[message.from_user.id]['step'] = "add_admin"


@app.on_message(filters.private)
async def text_message(client: Client, message: Message):
    if user_pocket[message.from_user.id]['step'] == "amount_payment":
        detect_number = detect_number_language(message.text)
        if detect_number == "persian":
            amount = persian_to_english_numbers(message.text)
            await message.reply_text(
                f"💳 فاکتور افزایش موجودی به مبلغ {amount} تومان صادر گردید .\n\nدرصورت تایید فاکتور میتوانید آن را از طریق دکمه درگاه پرداخت خرید خود را تکمیل کنید .",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("💳 درگاه پرداخت",
                                          url=f"{link_payment}/data/?user_id={message.from_user.id}&amount={amount}")]
                ]))
        elif detect_number == "english":
            amount = message.text
            await message.reply_text(
                f"💳 فاکتور افزایش موجودی به مبلغ {amount} تومان صادر گردید .\n\nدرصورت تایید فاکتور میتوانید آن را از طریق دکمه درگاه پرداخت خرید خود را تکمیل کنید .",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("💳 درگاه پرداخت",
                                          url=f"{link_payment}/data/?user_id={message.from_user.id}&amount={amount}")]
                ]))
        else:
            await message.reply_text("خطا")
    elif user_pocket[message.from_user.id]['step'] == "percent":
        try:
            if len(database.view_percent()) > 0:
                database.update_percent(float(message.text))
            else:
                database.insert_percent(float(message.text))
            await message.reply_text("درصد سود مورد نظر با موفقیت ثبت شد✅")
            user_pocket[message.from_user.id]['step'] = 0
        except Exception as e:
            print(e)
            await message.reply_text("خطا\nلطفا به صورت عدد بفرستید!")
    elif user_pocket[message.from_user.id]['step'] == "support_message":
        mess = message.text
        await app.send_message(chat_id=admin, text=f"✉ یک پیام از طرف کاربر {message.from_user.id} :\n\n{mess}",
                               reply_markup=InlineKeyboardMarkup([
                                   [InlineKeyboardButton("پاسخ دادن به کاربر",
                                                         callback_data=f"answer\n{message.from_user.id}")]
                               ]))
        await message.reply_text("✏ پیام شما برای ادمین ارسال شد و منتظر پاسخ از طرف ادمین باشید✅")
        user_pocket[message.from_user.id]['step'] = 0
    elif user_pocket[message.from_user.id]['step'] == "join_link":
        try:
            link = message.text.split("#")[0]
            chat_id = int(message.text.split("#")[1])
            if len(database.view_join_link()) > 0:
                database.update_join_link(link, chat_id)
            else:
                database.insert_join_link(link, chat_id)
            await message.reply_text("کانال مورد نظر در بخش جوین اجباری با موفقیت ثبت شد✅")
            user_pocket[message.from_user.id]['step'] = 0
        except:
            await message.reply_text("خطا")
            user_pocket[message.from_user.id]['step'] = 0
    elif user_pocket[message.from_user.id]['step'] == "add_amount":
        try:
            user_id = message.text.split("&")[0]
            str_amount = message.text.split("&")[1]
            amount = int(message.text.split("&")[1])
            last_amount = int(database.inf_user(user_id)[0][1])
            database.update_inv_user(user_id, amount + last_amount)
            await message.reply_text(f"موجودی کاربر به {amount + last_amount} با موفقیت اپدیت شد✅")
            if str_amount[0] == "-":
                await app.send_message(chat_id=int(user_id),
                                       text=f"🎉 موجودی شما توسط ادمین به {amount} تومان کسر شد\nموجودی جدید شما : {amount + last_amount}")
                await app.send_message(chat_id=-1002028706548,
                                       text=f"🎉 موجودی {user_id} توسط ادمین به {amount} تومان کسر شد\nموجودی جدید شما : {amount + last_amount}")
            else:
                await app.send_message(chat_id=int(user_id),
                                       text=f"🎉 موجودی شما توسط ادمین به {amount} تومان اضافه شد\nموجودی جدید شما : {amount + last_amount}")
                await app.send_message(chat_id=-1002028706548,
                                       text=f"🎉 موجودی {user_id} توسط ادمین به {amount} تومان اضافه شد\nموجودی جدید شما : {amount + last_amount}")
            user_pocket[message.from_user.id]['step'] = 0
        except Exception as e:
            print(e)
            await message.reply_text("خطایی پیش آمده")
            user_pocket[message.from_user.id]['step'] = 0
    elif user_pocket[message.from_user.id]['step'] == "block_user":
        try:
            user_id = int(message.text)
            database.insert_block_user(user_id)
            await message.reply_text("کاربر مورد نظر با موفقیت مسدود شد✅")
            user_pocket[message.from_user.id]['step'] = 0
        except:
            await message.reply_text("خطایی رخ داده")
            user_pocket[message.from_user.id]['step'] = 0
    elif user_pocket[message.from_user.id]['step'] == "start_text":
        if len(database.view_start_text()) > 0:
            database.update_start_text(message.text)
        else:
            database.insert_start_text(message.text)
        await message.reply_text("متن استارت با موفقیت اضافه شد✅")
        user_pocket[message.from_user.id]['step'] = 0
    elif user_pocket[message.from_user.id]['step'] == "user_send":
        user_id = await message.chat.ask("لطفا ایدی عددی شخص مورد نظر را ارسال نمایید :")
        try:
            user_id = int(user_id.text)
            await message.forward(chat_id=user_id)
            await message.reply_text("با موفقیت انجام شد✅")
            user_pocket[message.from_user.id]['step'] = 0
        except:
            await message.reply_text("مشکلی پیش امده")
            user_pocket[message.from_user.id]['step'] = 0
    elif user_pocket[message.from_user.id]['step'] == "all_send":
        for x in database.all_user():
            user_id = int(x[0])
            await message.forward(user_id)
        await message.reply_text("با موفقیت برای همه اعضا ارسال شد✅")
        user_pocket[message.from_user.id]['step'] = 0
    elif user_pocket[message.from_user.id]['step'] == "add_admin":
        try:
            user_id = int(message.text)
            database.insert_admins(user_id)
            await message.reply_text("با موفقیت انجام شد✅")
            user_pocket[message.from_user.id]['step'] = 0
        except:
            await message.reply_text("خطا❌")
            user_pocket[message.from_user.id]['step'] = 0
    elif user_pocket[message.from_user.id]['step'] == "set_checker_price":
        try:
            price = int(message.text)
            if len(database.view_checker_price()) > 0:
                database.update_checker_price(price)
            else:
                database.insert_checker_price(price)
            await message.reply_text("با موفقیت انجام شد✅")
            user_pocket[message.from_user.id]['step'] = 0
        except Exception as e:
            print(e)
            await message.reply_text("خطا❌")
            user_pocket[message.from_user.id]['step'] = 0
    elif user_pocket[message.from_user.id]['step'].splitlines()[0] == "price_vak":
        try:
            price = int(message.text.split("|")[1])
            name = message.text.split("|")[0]
            id = user_pocket[message.from_user.id]['step'].splitlines()[1]
            database.insert_vak_panel(name, id, price)
            await message.reply_text(f"کشور مورد نظر خود ثبت شد🎉")
            user_pocket[message.from_user.id]['step'] = 0
        except Exception as e:
            print(e)
            await message.reply_text("مشکلی پیش امده")
            user_pocket[message.from_user.id]['step'] = 0
    elif user_pocket[message.from_user.id]['step'] == "check_user":
        try:
            user_id = int(message.text)
            data = database.inf_user(user_id)[0]
            await message.reply_text(f"کاربر : {data[0]}\nموجودی : {data[1]}")
        except:
            await message.reply_text("کاربر مورد نظر پیدا نشد")
    elif user_pocket[message.from_user.id]['step'] == "check_number":
        try:
            numbers = message.text.splitlines()
            pr = len(numbers) * int(database.view_checker_price()[0][0])
            if int(database.inf_user(message.from_user.id)[0][1]) >= pr:
                database.update_inv_user(message.from_user.id, int(database.inf_user(message.from_user.id)[0][1]) - pr)
                text = ""
                for number in numbers:
                    x = await checker_sell(number)
                    if x == 0:
                        text = text + f"{number} ❌\n"
                    elif x == 1:
                        text = text + f"{number} ✅\n"
                    else:
                        text = text + f"{number} 🔒\n"
                text = text + "🔒 شماره نشست دارد\n✅ شماره سالم است\n❌ شماره بن شده"
                await message.reply_text(text)
                user_pocket[message.from_user.id]['step'] = 0
            else:
                await message.reply_text("موجودی حساب شما کافی نمیباشد")
                user_pocket[message.from_user.id]['step'] = 0
        except Exception as e:
            print(e)
            await message.reply_text("خطایی پیش امده")
            user_pocket[message.from_user.id]['step'] = 0


@app.on_callback_query()
async def callbacks(client, callback: CallbackQuery):
    if callback.data.split("-")[0] == "next_page":
        data = await fetch_data(url=url_get_prices)
        code = []
        count_last = int(callback.data.split("-")[1])
        count = int(callback.data.split("-")[1])
        new_count = count + 13
        first_btn = [InlineKeyboardButton(text="🌍 نام کشور", callback_data="test"),
                     InlineKeyboardButton(text="📊 وضعیت", callback_data="test"),
                     InlineKeyboardButton(text="💰 قیمت", callback_data="test")]
        code.append(first_btn)
        for x in data[count:]:
            if count < new_count:
                price = int(x["price"])
                percent = float(database.view_percent()[0][0])
                per = price * percent
                price = price + per
                if x["country"] != "لهستان 🇵🇱":
                    c_count = x["count"]
                else:
                    c_count = "❌ ناموجود"
                number = int(price)
                formatted_number = f'{number:,}'
                button = [InlineKeyboardButton(text=x["country"],
                                               callback_data=f'c\n{x["country"]}\n{str(int(price)).replace(".0", "")}'),
                          InlineKeyboardButton(text=c_count,
                                               callback_data=f'c\n{x["country"]}\n{str(int(price)).replace(".0", "")}'),
                          InlineKeyboardButton(text=formatted_number,
                                               callback_data=f'c\n{x["country"]}\n{str(int(price)).replace(".0", "")}')]
                code.append(button)
                count += 1
            else:
                break
        if len(data[count:]) > 0:
            but = [InlineKeyboardButton(text="⬅ صفحه قبلی", callback_data=f"last_page-{count}"),
                   InlineKeyboardButton(text="➡ صفحه بعدی", callback_data=f"next_page-{count}")]
        else:
            but = [InlineKeyboardButton(text="⬅ صفحه قبلی", callback_data=f"last_page-{count}")]
        code.append(but)
        await callback.message.edit(f"👈 جهت خرید شماره مجازی روی نام کشور مورد نظر خود کلیک نمایید:",
                                    reply_markup=InlineKeyboardMarkup(code))
    elif callback.data == "joined":
        try:
            chat_id = int(database.view_join_link()[0][1])
            user = await client.get_chat_member(chat_id=chat_id, user_id=callback.from_user.id)
            if len(database.inf_user(callback.from_user.id)) == 0:
                database.insert_users(callback.from_user.id, "0", "0")
            else:
                pass
            start_text = database.view_start_text()[0][0]
            await callback.message.delete()
            await callback.message.reply_text(text=start_text,
                                              reply_markup=home_btn(callback.from_user.id))
        except:
            await callback.answer(text="شما هنوز جوین کانال نشده اید❌", show_alert=True)
    elif callback.data.split("-")[0] == "last_page":
        data = await fetch_data(url=url_get_prices)
        code = []
        count_last = int(callback.data.split("-")[1])
        count = int(callback.data.split("-")[1])
        if len(data[count:]) > 0:
            count -= 13
            new_count = count - 13
        else:
            count -= 3
            new_count = count - 13
        first_btn = [InlineKeyboardButton(text="🌍 نام کشور", callback_data="test"),
                     InlineKeyboardButton(text="📊 وضعیت", callback_data="test"),
                     InlineKeyboardButton(text="💰 قیمت", callback_data="test")]
        code.append(first_btn)
        for x in data[new_count:]:
            if new_count < count:
                price = int(x["price"])
                percent = float(database.view_percent()[0][0])
                per = price * percent
                price = price + per
                if x["country"] != "لهستان 🇵🇱":
                    c_count = x["count"]
                else:
                    c_count = "❌ ناموجود"
                number = int(price)
                formatted_number = f'{number:,}'
                button = [InlineKeyboardButton(text=x["country"],
                                               callback_data=f'c\n{x["country"]}\n{str(int(price)).replace(".0", "")}'),
                          InlineKeyboardButton(text=c_count,
                                               callback_data=f'c\n{x["country"]}\n{str(int(price)).replace(".0", "")}'),
                          InlineKeyboardButton(text=formatted_number,
                                               callback_data=f'c\n{x["country"]}\n{str(int(price)).replace(".0", "")}')]
                code.append(button)
                new_count += 1
            else:
                break
        if new_count > 0:
            but = [InlineKeyboardButton(text="⬅ صفحه قبلی", callback_data=f"last_page-{count}"),
                   InlineKeyboardButton(text="➡ صفحه بعدی", callback_data=f"next_page-{count}")]
            code.append(but)
        else:
            but = [InlineKeyboardButton(text="➡ صفحه بعدی", callback_data=f"next_page-{count}")]
            code.append(but)
        await callback.message.edit(f"👈 جهت خرید شماره مجازی روی نام کشور مورد نظر خود کلیک نمایید:",
                                    reply_markup=InlineKeyboardMarkup(code))
    elif callback.data == "cancel":
        await callback.message.edit("پنل با موفقیت بسته شد✅", reply_markup=home_btn(callback.from_user.id))
    elif callback.data.splitlines()[0] == "c":
        country = callback.data.splitlines()[1]
        price = int(callback.data.splitlines()[2])
        inv = int(database.inf_user(callback.from_user.id)[0][1])
        if inv >= price:
            if country != "لهستان 🇵🇱":
                await callback.message.reply_text(f"از خرید شماره مجازی {country} اطمینان دارید؟",
                                                  reply_markup=InlineKeyboardMarkup([
                                                      [InlineKeyboardButton("خرید شماره",
                                                                            callback_data=f"number\n{country}")],
                                                      [InlineKeyboardButton("انصراف", callback_data="cancel")]
                                                  ]))
            else:
                await callback.answer("درحال حاضر این کشور در دسترس نمیباشد")
        else:
            await callback.answer("موجودی شما کافی نیست!")
    elif callback.data == "last_page_vak":
        data = database.view_vak_panel()
        code = []
        first_btn = [InlineKeyboardButton(text="🌍 نام کشور", callback_data="test"),
                     InlineKeyboardButton(text="💰 قیمت", callback_data="test")]
        code.append(first_btn)
        count = 0
        for d in data:
            if count < 7:
                button = [InlineKeyboardButton(text=d[0], callback_data=f'vak\n{d[1]}'),
                          InlineKeyboardButton(text=d[2], callback_data=f'vak\n{d[1]}')]
                code.append(button)
            else:
                break
        but = [InlineKeyboardButton(text="➡ صفحه بعدی", callback_data=f"next_page_vak")]
        code.append(but)
        await callback.message.edit(f"👈 جهت خرید شماره مجازی روی نام کشور مورد نظر خود کلیک نمایید:",
                                    reply_markup=InlineKeyboardMarkup(code))
    elif callback.data == "next_page_vak":
        data = database.view_vak_panel()
        code = []
        first_btn = [InlineKeyboardButton(text="🌍 نام کشور", callback_data="test"),
                     InlineKeyboardButton(text="💰 قیمت", callback_data="test")]
        code.append(first_btn)
        count = 0
        for d in data[7:]:
            button = [InlineKeyboardButton(text=d[0], callback_data=f'vak\n{d[1]}'),
                      InlineKeyboardButton(text=d[2], callback_data=f'vak\n{d[1]}')]
            code.append(button)
        but = [InlineKeyboardButton(text="⬅ صفحه قبلی", callback_data=f"last_page_vak")]
        code.append(but)
        await callback.message.edit(f"👈 جهت خرید شماره مجازی روی نام کشور مورد نظر خود کلیک نمایید:",
                                    reply_markup=InlineKeyboardMarkup(code))
    elif callback.data.splitlines()[0] == "vak":
        await callback.message.delete()
        id = callback.data.splitlines()[1]
        await asyncio.sleep(random.randrange(0, 2))
        data = database.view_vak_country(id)[0]
        if len(database.view_status_buy(callback.from_user.id)) == 0:
            database.insert_status_buy(callback.from_user.id, "T")
        else:
            pass
        price = int(data[2])
        inv = int(database.inf_user(callback.from_user.id)[0][1])
        if inv >= price:
            if database.view_status_buy(callback.from_user.id)[0][1] == "T":
                database.update_status_buy(callback.from_user.id, "F")
                count_check = 0
                while True:
                    if count_check < 7:
                        link = vak_links["orderphone"] + id
                        result = await fetch_data(link)
                        if result == "NO_NUMBERS":
                            await callback.message.edit("در حال حاضر شماره ای موجود نیست")
                            database.update_status_buy(callback.from_user.id, "T")
                        elif result == "NO_BALANCE":
                            await client.send_message(admin, "موجودی سایت vak به اتمام رسیده.")
                            await callback.message.edit("در حال حاضر شماره ای موجود نیست")
                            database.update_status_buy(callback.from_user.id, "T")
                        elif len(result) < 2:
                            await callback.message.edit("در حال حاضر شماره ای موجود نیست")
                            database.update_status_buy(callback.from_user.id, "T")
                        elif result == "ERROR":
                            await callback.message.edit("در حال حاضر شماره ای موجود نیست")
                            database.update_status_buy(callback.from_user.id, "T")
                        else:
                            phone = str(result["tel"])
                            orderId = result["idNum"]
                            check = await checker(number=phone)
                            if check == 1:

                                await callback.message.delete()
                                x = await callback.message.reply_text(
                                    f"شماره با موفقیت دریافت شد✅\n\nشماره : `{phone}`+\n\nلطفا شماره را در تلگرام وارد کنید تا ربات کد را برایتان ارسال کند.",
                                    reply_markup=InlineKeyboardMarkup([
                                        # [InlineKeyboardButton(text="دریافت کد",
                                        #                       callback_data=f"vak-getcode\n{orderId}\n{phone}")],
                                        [InlineKeyboardButton(text="لغو شماره ❌",
                                                              callback_data=f"vak-cancel\n{orderId}\n{phone}\n{price}")]
                                    ]))
                                price_end = inv - price
                                database.update_inv_user(callback.from_user.id, price_end)
                                await app.send_message(chat_id=reports_channel,
                                                       text=f"کاربر `{callback.from_user.id}` شماره {phone} به قیمت {price} تومان را از پنل vak دریافت کرد.\nموجودی کاربر : {price_end}")
                                loop.create_task(auto_code(orderId=orderId, phone=phone, user_id=callback.from_user.id))
                                loop.create_task(cancelTheNumber(orderId, price, callback.from_user.id, x.id))
                                break

                            elif check == 0:
                                await fetch_data(vak_links["setorderstat"] + orderId)
                                count_check += 1
                                continue
                            elif check == 2:
                                await fetch_data(vak_links["setorderstat"] + orderId)
                                continue
                            elif check == 3:
                                await fetch_data(vak_links["setorderstat"] + orderId)
                                continue
                    else:
                        await callback.message.delete()
                        await callback.message.reply_text("شماره ای موجود نیست دوباره امتحان گنید")
                        database.update_status_buy(callback.from_user.id, "T")
                        break
            else:
                await callback.answer("در حال حاضر شما در حال خرید شماره دیگری میباشید!")
        else:
            await callback.message.edit("موجودی کاقی نیست")
    elif callback.data.splitlines()[0] == "vak-getcode":
        orderId = callback.data.splitlines()[1]
        phone = callback.data.splitlines()[2]
        result = await fetch_data(vak_links["getcode"] + orderId)
        if result.get("smsCode"):
            result = result['smsCode']
            await fetch_data(vak_links["again_code"] + orderId)
            await callback.message.edit(text=f"شماره :\n +`{phone}`\n\nکد دریافتی :\n `{result}`",
                                        reply_markup=InlineKeyboardMarkup([
                                            [InlineKeyboardButton(text="دریافت کد مجدد",
                                                                  callback_data=f"vak-getcode-a\n{orderId}\n{phone}")]
                                        ]))
        else:
            await callback.answer("کدی دریافت نشده!")
    elif callback.data.splitlines()[0] == "vak-getcode-a":
        orderId = callback.data.splitlines()[1]
        phone = callback.data.splitlines()[2]
        result = await fetch_data(vak_links["getcode"] + orderId)
        if result.get("smsCode"):
            result = result['smsCode']
            await fetch_data(vak_links["again_code"] + orderId)
            await callback.message.edit(text=f"شماره :\n +`{phone}`\n\nکد دریافتی :\n `{result}`")
            database.update_status_buy(callback.from_user.id, "T")
        else:
            await callback.answer("کدی دریافت نشده!")
    elif callback.data.splitlines()[0] == "vak-cancel":
        await callback.message.delete()
        await asyncio.sleep(0.2)
        orderId = callback.data.splitlines()[1]
        phone = callback.data.splitlines()[2]
        price = int(callback.data.splitlines()[3])
        userid = callback.from_user.id
        if orderId not in listCancel:
            listCancel.append(orderId)
            result = await fetch_data(vak_links["setorderstat"] + orderId)
            if result['status'] == "update":
                inv = int(database.inf_user(user_id=userid)[0][1])
                inv = inv + price
                database.update_inv_user(userid, inv)
                database.update_status_buy(userid, "T")
                await callback.message.reply_text("با موفقیت شماره شما لغو شد❌")
                await app.send_message(chat_id=reports_channel,
                                       text=f"مقدار {price} به حساب کاربر {userid} برگشت داده شد.\nموحودی کاربر : {inv}")
            else:
                await callback.message.delete()
                await callback.message.reply_text("امکان لغو وجود ندارد!")
        else:
            await callback.message.delete()
            await callback.message.reply_text("امکان لغو وجود ندارد!")
    elif callback.data.splitlines()[0] == "number":
        await callback.answer("درحال پردازش...")
        country = callback.data.splitlines()[1]
        data = await fetch_data(url=url_get_prices)
        inv = int(database.inf_user(callback.from_user.id)[0][1])
        for x in data:
            if x["country"] == country:
                price = int(x["price"])
                percent = float(database.view_percent()[0][0])
                per = price * percent
                price = price + per
                count = x["count"]
            else:
                pass
        if inv >= price:
            if count == "\u2705 \u0645\u0648\u062c\u0648\u062f":
                c = 0
                while True:
                    if c < 10:
                        sec_data = await fetch_data(url=url_get_account + country)
                        if "error_msg" not in sec_data.keys():
                            check = await checker_call(sec_data["number"])
                            if check == 1:
                                number = sec_data["number"]
                                request_id = sec_data["request_id"]
                                quality = sec_data["quality"]
                                await callback.message.edit(
                                    f"شماره مورد نظر با موفقیت پیدا شد✅\n\nشماره : `{number}`\nکیفیت اکانت : {quality}\n\n💢 لطفا ابتدا شماره را در تلگرام خود زده و سپس روی دکمه دریافت کد کلیک نمایید!",
                                    reply_markup=InlineKeyboardMarkup([
                                        [InlineKeyboardButton("دریافت کد",
                                                              callback_data=f"code\n{request_id}\n{int(price)}")],
                                        [InlineKeyboardButton("لغو", callback_data="cancel")]
                                    ]))
                                break
                            else:
                                c += 1
                                pass
                        else:
                            if sec_data["error_msg"] == "not enough price!":
                                await app.send_message(chat_id=admin,
                                                       text="موجودی توکن به اتمام رسیده لطفا آن را شارژ کنید!")
                                await callback.answer("مشکلی پیش آمده لطفا چند دقیقه دیگر دوباره امتحان کنید!")
                                break
                            break
                    else:
                        await callback.message.edit("♻️ مجدد تلاش کنید شماره سالمی پیدا نشد")
                        break
            else:
                await callback.answer("این شماره در ربات موجود نمیباشد")
        else:
            await callback.message.edit(
                "موجودی حساب شما کافی نمیباشد لطفا از طریق دکمه افزایش موجودی اقدام به افزایش اعتبار خود کنید❗",
                reply_markup=home_btn(callback.from_user.id))
    elif callback.data.splitlines()[0] == "code":
        request_id = callback.data.splitlines()[1]
        price = int(callback.data.splitlines()[2])
        data = await fetch_data(url_get_code + request_id)
        inv = int(database.inf_user(callback.from_user.id)[0][1])
        if inv >= price:
            if "error_msg" not in data.keys():
                code = data["code"]
                await callback.message.edit(
                    f"🎉کد ارسال تلگرام : `{code}`\n☎ شماره مجازی : {data['number']}\n📍در صورت خواستن خروج ربات از اکانت از دکمه خارج شدن از اکانت استفاده نمایید",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("کد مجدد", callback_data=f"r_code\n{request_id}\n{int(price)}")],
                        [InlineKeyboardButton("خارج شدن", callback_data=f"exit\n{request_id}")],
                        [InlineKeyboardButton("بازگشت به منو اصلی", callback_data="cancel")]
                    ]))
                await app.send_message(chat_id=reports_channel,
                                       text=f"""✔کاربر [{callback.from_user.id}](tg://user?id={callback.from_user.id}) از کشور {data['country']} شماره {data['number']} را خریداری کرد""")
                database.update_inv_user(callback.from_user.id, inv - price)
            else:
                if data["error_msg"] == "Still waiting...":
                    await callback.answer("هنوز کدی دریافت نشده منتظر بمانید...!")
        else:
            await callback.answer("کاربر گرامی موجودی شما کافی نمیباشد...!")
    elif callback.data.splitlines()[0] == "r_code":
        request_id = callback.data.splitlines()[1]
        price = int(callback.data.splitlines()[2])
        data = await fetch_data(url_get_code + request_id)
        inv = int(database.inf_user(callback.from_user.id)[0][1])
        if "error_msg" not in data.keys():
            code = data["code"]
            await callback.message.reply_text(
                f"🎉کد ارسال تلگرام : `{code}`\n☎ شماره مجازی : {data['number']}\n📍در صورت خواستن خروج ربات از اکانت از دکمه خارج شدن از اکانت استفاده نمایید",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("کد مجدد", callback_data=f"r_code\n{request_id}\n{int(price)}")],
                    [InlineKeyboardButton("خارج شدن", callback_data=f"exit\n{request_id}")],
                    [InlineKeyboardButton("بازگشت به منو اصلی", callback_data="cancel")]
                ]))
        else:
            if data["error_msg"] == "Still waiting...":
                await callback.answer("هنوز کدی دریافت نشده منتظر بمانید...!")
            else:
                await callback.answer("کد دریافت نشده است...")
    elif callback.data.splitlines()[0] == "exit":
        request_id = callback.data.splitlines()[1]
        data = await fetch_data(url_log_out + request_id)
        if "error_msg" not in data.keys():
            await callback.message.edit("✅ ربات با موفقیت از اکانت خارج شد")
        else:
            await callback.answer("خطا")
    elif callback.data.splitlines()[0] == "delete_vak":
        try:
            id = callback.data.splitlines()[1]
            database.delete_vak_panel(id)
            await callback.message.delete()
            await callback.message.reply_text("کشور مورد نظر با موفقیت حذف شد")
        except Exception as e:
            print(e)
            await callback.message.reply_text("خطایی رخ داده")

    elif callback.data.splitlines()[0] == "answer":
        user_id = int(callback.data.splitlines()[1])
        mess = await callback.message.chat.ask("💠 لطفا پیام مورد نظر را در قالب یک پیام ارسال نمایید:")
        await app.send_message(chat_id=user_id, text=f"✉یک پیام از طرف ادمین :\n\n{mess.text}")
        await callback.message.reply_text("پیام مورد نظر ارسال شد✅")
    elif callback.data.splitlines()[0] == "second_api":
        country = callback.data.splitlines()[1]
        if len(database.view_vak_country(country)) > 0:
            await callback.message.reply_text("کشور انتخابی تکراری است")
        else:
            await callback.message.reply_text(
                "لطفا نام کشور که میخواهید قابل نمایش باشد به همراه قیمت مورد نظر خود را ارسال کنید :\nمثال :\nآمریکا|10000")
            user_pocket[callback.from_user.id]['step'] = f"price_vak\n{country}"


app.run()