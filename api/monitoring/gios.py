import requests
from api import config, producer

r = requests.get(config.GIOS_FIND_ALL_STATION_URL)
response = r.json()

for station in response:
    status = requests.get(config.GIOS_GET_STATION_STATUS_URL + str(station['id']))
    if status.status_code == 200:
        station_status = status.json()
        station_status['provider'] = 'GIOS'
        station_status['station_id'] = station['id']
        producer.send('monitoring', station_status)
        print("Send info about station {}".format(station['id']))