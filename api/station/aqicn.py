import requests
from api import config, producer

headers = {
    'apikey': config.AIRLY_TOKEN
}
r = requests.get(config.AQICN_FIND_ALL_STATION_URL, headers=headers, timeout=5)
response = r.json()

if r.status_code == 200:
    for station in response['data']:
        url = config.AQICN_GET_STATION_STATUS_URL
        url = url.replace("LAT", str(station['lat']))
        url = url.replace('LNG', str(station['lon']))

        r = requests.get(url)
        station_details = r.json()

        normalized_station = {}
        normalized_station['vendor'] = 'AQICN'
        normalized_station['id'] = station['uid']
        normalized_station['station_name'] = station_details['data']['attributions'][1]['name']
        normalized_station['lng'] = station['lon']
        normalized_station['lat'] = station['lat']
        normalized_station['city'] = "Krakow"
        normalized_station['street'] = station_details['data']['city']['name']

        producer.send('station', normalized_station)
        print("Send info about station {}".format(normalized_station['id']))



