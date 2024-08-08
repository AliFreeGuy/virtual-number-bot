
from pyrogram.errors import UserNotParticipant
import requests 
import json







async def join_checker(cli , msg , channels ):
    my_channels = []
    not_join = []
    for channel in channels :
        data = channel.split(' ')
        if len(data) == 2 : my_channels.append({'link' : data[0] , 'chat_id' : data[1]})
    for i in my_channels : 
        try :data = await cli.get_chat_member(int(i['chat_id']), msg.from_user.id )
        except UserNotParticipant :
            not_join.append(i['link'])
        except Exception as e  : print(e)

    return not_join

    




async def alert(client ,call , msg = None ):
    try :
        if msg is None : await call.answer('خطا لطفا دوباره تلاش کنید', show_alert=True)
        else : await call.answer(msg , show_alert = True)
    except Exception as e : print('alert ' , str(e))
    



async def deleter(client , call , message_id ):
    try :
        message_id = message_id
        msg_ids = []
        for x in range(100) :
            msg_ids.append(message_id + x)
        await client.delete_messages(call.from_user.id  ,msg_ids )
    except :pass



def get_numbers(token):
    url = f'https://api.ozvinoo.xyz/web/{token}/get-prices/1'
    res = requests.get(url=url)
    if res.status_code == 200 :
        return res.json()
    return False


def get_phone_number(token, country, max_attempts=1, checker_key=None):
    url = f'https://api.ozvinoo.xyz/web/{token}/getNumber/1/{country}'
    
    
    for _ in range(max_attempts):
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            print(f"Received data: {data}")
            
            if checker_key and max_attempts > 1:
                checker_result = checker([data['number']], api_key=checker_key)
                if checker_result and checker_result[0]['status'] != 'ban':
                    print(data)
                    yield data  
                else:
                    print("Number failed checker validation.")
                    continue  
            else:
                yield data  
        else:
            yield None  



def get_code(token, request_id):
    url = f'https://api.ozvinoo.xyz/web/{token}/getCode/{str(request_id)}'
    # try:
    #     res = requests.get(url)
    #     res.raise_for_status()
    # except requests.exceptions.RequestException as e:
    #     print(f"HTTP Request failed: {e}")
    #     return False
    # data = res.json()
    # if 'code' in data:
    #     return data['code']
    # else:
    #     print(f"Error: {data.get('error_msg', 'Unknown error')}")
    #     return False

    return True






def checker(numbers, api_key):
    url = "http://ca.irbots.com"
    phone_numbers = ','.join(numbers)
    
    params = {
        "key": api_key,
        "numbers": phone_numbers,
        'target': 'checker'  # انتخاب چکر
    }
    
    # ارسال درخواست GET
    try:
        response = requests.get(url, params=params, timeout=15)
    except Exception as e:
        print(f'API error: {e}')
        return []
    
    try:
        response_json = response.json()
        print(f"Response JSON: {response_json}")  # چاپ پاسخ دریافتی برای بررسی
        
        # تبدیل پاسخ به لیست مورد نظر
        results = []
        if response_json['status'] == 'ok':
            for phone, status in response_json['data'].items():
                results.append({'phone': phone, 'status': status})
        return results
    except requests.exceptions.JSONDecodeError:
        print('Error: Invalid JSON response')
        print(response.text)
        return []
    except requests.exceptions.RequestException as e:
        print(f'Error: {e}')
        return []

