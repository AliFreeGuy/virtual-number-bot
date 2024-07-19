
from pyrogram.errors import UserNotParticipant







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
    