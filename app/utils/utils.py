
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