from flask import Flask, render_template, request, jsonify
import requests
import json
from pprint import pprint

app = Flask(__name__)

# 讀取 TDX API 認證資訊
with open(r"1131_BME_information\1114_11125119\setting\setting.json", 'r', encoding='utf8') as file:
    jf = file.read()
CLIENT_ID = json.loads(jf)["CLIENT_ID"]
CLIENT_SECRET = json.loads(jf)["CLIENT_SECRET"]

# 獲取 TDX API 的 Access Token
def get_access_token():
    auth_url = 'https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token'
    auth_data = {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    response = requests.post(auth_url, data=auth_data)
    
    if response.status_code != 200:
        print("Failed to get access token:", response.text)
        return None

    token_data = response.json()
    return token_data.get('access_token')

# 獲取所有台鐵路線
def get_rail_routes():
    access_token = get_access_token()
    if access_token is None:
        print("No access token available.")
        return []

    url = 'https://tdx.transportdata.tw/api/basic/v2/Rail/TRA/Line?%24format=JSON'
    headers = {
        'authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Failed to retrieve rail routes:", response.text)
        return []

    routes = response.json()
    return routes

# 獲取指定路線的所有車站
def get_stations_by_route(route_id):
    access_token = get_access_token()
    url = 'https://tdx.transportdata.tw/api/basic/v2/Rail/TRA/StationOfLine?$format=JSON'
    headers = {
        'authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Failed to retrieve stations:", response.text)
        return []

    stations_data = response.json()

    # 尋找符合指定 route_id 的路線並提取車站資料
    for line in stations_data:
        if line["LineID"] == route_id:
            return line["Stations"]

    return []

# 獲取兩站間的票價資訊
def get_fare_between_stations(origin_station_id, destination_station_id):
    access_token = get_access_token()
    url = f'https://tdx.transportdata.tw/api/basic/v2/Rail/TRA/ODFare/{origin_station_id}/to/{destination_station_id}?%24format=JSON'
    headers = {
        'authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    fares = response.json()
    return fares

@app.route('/')
def index():
    routes = get_rail_routes()
    return render_template('index.html', routes=routes)

@app.route('/m')
def index_m():
    routes = get_rail_routes()
    return render_template('index_m.html', routes=routes)

@app.route('/stations', methods=['GET'])
def stations():
    route_id = request.args.get('route_id')
    stations = get_stations_by_route(route_id)
    return jsonify(stations)

@app.route('/fare', methods=['GET'])
def fare():
    origin_station_id = request.args.get('origin_station_id')
    destination_station_id = request.args.get('destination_station_id')
    fares = get_fare_between_stations(origin_station_id, destination_station_id)
    return jsonify(fares)

if __name__ == '__main__':
    app.run(debug=True)
