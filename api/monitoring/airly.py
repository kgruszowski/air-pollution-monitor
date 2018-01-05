import requests
from api import config, producer
from datetime import datetime

headers = {
    'apikey': config.AIRLY_TOKEN
}
r = requests.get(config.AIRLY_FIND_ALL_STATION_URL, headers=headers, timeout=5)
resonse = r.json()

for station in resonse:
    r = requests.get(config.AIRLY_GET_STATION_STATUS_URL + str(station['id']), headers=headers, timeout=5)

    station_details = r.json()
    history = station_details['history']

    for status in history:
        measurements = status['measurements']
        normalized_measurements = {}
        normalized_measurements['id'] = station['id']
        normalized_measurements['vendor'] = 'AIRLY'
        normalized_measurements['pm2_5'] = measurements['pm25']
        normalized_measurements['pm10'] = measurements['pm10']
        normalized_measurements['temperature'] = measurements['temperature']
        normalized_measurements['date'] = datetime.strptime(status['fromDateTime'], '%Y-%m-%dT%H:%M:%SZ').strftime("%Y-%m-%d %H:%M:%S")

        producer.send('monitoring', normalized_measurements)
        print("Send info about station {}".format(station['id']))
