import requests
from pprint import pprint
import json
import math
app_id = 's11125131-2cf17eb7-3f8e-41c0'
app_key = 'ac899a07-5b2e-4ce1-a2d7-199415be9966'

auth_url="https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token"
url = "https://tdx.transportdata.tw/api/basic/v3/Rail/TRA/Station?%24format=JSON"

class Auth():

    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key

    def get_auth_header(self):
        content_type = 'application/x-www-form-urlencoded'
        grant_type = 'client_credentials'

        return{
            'content-type' : content_type,
            'grant_type' : grant_type,
            'client_id' : self.app_id,
            'client_secret' : self.app_key
        }

class data():

    def __init__(self, app_id, app_key, auth_response):
        self.app_id = app_id
        self.app_key = app_key
        self.auth_response = auth_response

    def get_data_header(self):
        auth_JSON = json.loads(self.auth_response.text)
        access_token = auth_JSON.get('access_token')

        return{
            'authorization': 'Bearer ' + access_token,
            'Accept-Encoding': 'gzip'
        }

if __name__ == '__main__':
    try:
        d = data(app_id, app_key, auth_response)
        data_response = requests.get(url, headers=d.get_data_header())
    except:
        a = Auth(app_id, app_key)
        auth_response = requests.post(auth_url, a.get_auth_header())
        d = data(app_id, app_key, auth_response)
        data_response = requests.get(url, headers=d.get_data_header())

data = json.loads(data_response.text)
print(data)
my_lat = 25.1
my_lon = 121.5
min_result = 9999
result_name = '台北'
for station in data['Stations']:
    lat = station['StationPosition']['PositionLat']
    lon = station['StationPosition']['PositionLon']
    result = math.sqrt(math.pow((lat - my_lat), 2) + math.pow((lon - my_lon), 2))
    
    # 更新最小值和車站名稱
    if result < min_result:
        min_result = result
        result_name = station['StationName']

# 列印出最小的 result 值和對應的車站名稱
print(f"距離25.1,121.5最近的車站是: {result_name}, 距離: {min_result}")