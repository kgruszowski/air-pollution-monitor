import requests
from api import config, producer

r = requests.get(config.GIOS_FIND_ALL_STATION_URL)
response = r.json()

for station in response:
    normalized_station = {}
    normalized_station['vendor'] = 'GIOS'
    normalized_station['id'] = station['id']
    normalized_station['station_name'] = station['stationName']
    normalized_station['lng'] = station['gegrLon']
    normalized_station['lat'] = station['gegrLat']
    normalized_station['city'] = station['city']['name']
    normalized_station['street'] = station['addressStreet']

    print(normalized_station)
    producer.send('station', normalized_station)
    print("Send info about station {}".format(normalized_station['id']))