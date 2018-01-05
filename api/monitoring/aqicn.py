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

        r = requests.get(url, timeout=5)
        station_details = r.json()

        normalized_measurements = {}
        normalized_measurements['id'] = station['uid']
        normalized_measurements['vendor'] = 'AQICN'
        normalized_measurements['pm2_5'] = station_details['data']['iaqi']['pm25']['v']
        normalized_measurements['pm10'] = station_details['data']['iaqi']['pm10']['v']
        normalized_measurements['temperature'] = None
        normalized_measurements['date'] = station_details['data']['time']['s']

        producer.send('monitoring', normalized_measurements)
        print("Send info about station {}".format(normalized_measurements['id']))



