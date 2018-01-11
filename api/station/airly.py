import requests, time
from api import config, producer

headers = {
    'apikey': config.AIRLY_TOKEN
}
r = requests.get(config.AIRLY_FIND_ALL_STATION_URL, headers=headers, timeout=5)
resonse = r.json()

for station in resonse:
    normalized_station = {}
    normalized_station['vendor'] = 'AIRLY'
    normalized_station['id'] = station['id']
    normalized_station['station_name'] = station['name']
    normalized_station['lng'] = station['location']['longitude']
    normalized_station['lat'] = station['location']['latitude']
    normalized_station['city'] = station['address']['locality']

    if 'streetNumber' in station['address'] and station['address']['streetNumber'] != '':
        normalized_station['street'] = station['address']['route'] + ' ' + station['address']['streetNumber']
    else:
        normalized_station['street'] = station['address']['route']

    producer.send('station', normalized_station)
    print("Send info about station {}".format(normalized_station['id']))
    time.sleep(2)



