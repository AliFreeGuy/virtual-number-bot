import redis
import time
import json
import requests
import config
from utils.logger import logger


REDIS_HOST = config.REDIS_HOST
REDIS_PORT = config.REDIS_PORT
REDIS_DB = config.REDIS_DB

API_URL = config.API_URL
API_KEY = config.API_KEY
BOT_USERNAME = config.BOT_USERNAME
CACHE_TTL = config.CACHE_TTL


class Connection:
    def __init__(self , api_key , url , bot_username) -> None:
        self.api_key = api_key
        self.url = url
        self.username = bot_username
        self.headers = {'Authorization' : f'token {self.api_key}'}
        self.redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB) 

            


    @property
    def setting(self):
            last_request_time = self.redis_client.get('last_request_time')  
            current_time = time.time()
            if last_request_time is None or current_time - float(last_request_time) > CACHE_TTL:
                pattern = 'setting'
                url = self.link_generator(pattern=pattern)
                res = self.get(url)
                if res and res.status_code == 200:
                    res_data = res.json()
                    self.redis_client.set('setting_data', json.dumps(res_data))
                    self.redis_client.set('last_request_time', current_time)
                    return Response(res.json())
            else:
                return Response(json.loads(self.redis_client.get('setting_data')))
        

    



    def user(self, chat_id, full_name):
      
        try:
            password = str(hash(chat_id))
            last_request_time = self.redis_client.get(f'last_user_request_time:{str(chat_id)}')
            current_time = time.time()
            if last_request_time is None or current_time - float(last_request_time) > CACHE_TTL:

                pattern = 'user_update'
                data = {}
                url = self.link_generator(pattern)
                data['url'] = url
                data['chat_id'] = chat_id
                data['full_name'] = full_name
                data['password'] = password
           
                res = self.post(url=url, chat_id=chat_id, data=data)
                res_raw = res
                if res and res.status_code == 200:
                    res = Response(res.json())
                    self.redis_client.set(f'user_data:{str(chat_id)}', json.dumps(res_raw.json()))
                    self.redis_client.set(f'last_user_request_time:{str(chat_id)}', current_time)
                    return res
            else:
                return Response(json.loads(self.redis_client.get(f'user_data:{str(chat_id)}')))
            return None
        except Exception as e:
            logger.error(e)


    def transfer(self , sender , receiver , amount ):
        pattern = f'transfer'
        url = self.link_generator(pattern)
        data = {'sender' : sender , 'receiver' : receiver , 'amount' :amount}
        res = requests.post(url = url , data=data , headers=self.headers)
        response = {}
        response['status'] = res.status_code
        if res.status_code == 200 :response['code'] = res.json()['tracking_code']
        else :response['code'] = 0
        return response
    

    def update_phone(self , chat_id , phone):
         pattern = 'update_phone'
         url = self.link_generator(pattern)
         data = {'chat_id' : chat_id , 'phone' : phone}
         res = requests.post(url = url , data = data , headers=self.headers)
         return res.status_code

    
    def get_user(self , chat_id):
            pattern  = 'user_update'
            url = self.link_generator(pattern)
            res = self.post(url , chat_id )
            if res and res.status_code == 200 :
                res = Response(res.json())
                return res
            return None  
        

    def link_generator(self  , pattern = None):
            if pattern is not None :
                end_point = self.url.rstrip('/') + f'/api/{pattern}/'
                return end_point
            return None
        

    def payment_url(self , chat_id , amount ):
         
        pattern = 'request'
        url = self.link_generator(pattern )
        data = {'chat_id' : chat_id , 'amount' : amount}
        res = requests.post(url= url , data=data , headers=self.headers)
        if res.status_code == 200 : 
            return res.json()
        return None


    def get(self , url):
            res = requests.get(url , headers=self.headers)
            return res

    

    def post(self ,url , chat_id , data = None    ):
            if data != None :

                    res = requests.post(url , headers=self.headers , data  = data )
                    return res
            else :
                res = requests.post(url , headers=self.headers , data = {'chat_id' : chat_id })
                return res



         

class Response:
    
    def __init__(self, data):
            self.data = data
            if type(data) is dict:
                for key, value in data.items():
                    if isinstance(value, dict):
                        setattr(self, key, Response(value))
                    else:
                        setattr(self, key, value)
        

    def __str__(self) -> str:
            return str(self.data) 
        

    def __getattr__(self, attr):
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{attr}'")
        



connection = Connection(api_key=API_KEY , url=API_URL , bot_username=BOT_USERNAME)