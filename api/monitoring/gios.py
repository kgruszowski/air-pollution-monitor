import requests
from api import config, producer

r = requests.get(config.GIOS_FIND_ALL_STATION_URL, timeout=5)

if r.status_code == 200:
    response = r.json()
    for station in response:
        if station['city'] is not None and station['city']['id'] == 415:

            r = requests.get(config.GIOS_GET_SENSORS_IN_STATION_URL + str(station['id']), timeout=5)
            if r.status_code == 200:
                sensors = r.json()
                pm = {}
                date = ''
                for param in sensors:
                    if param['param']['paramFormula'] == "PM10" or param['param']['paramFormula'] == "PM2.5":
                        r = requests.get(config.GIOS_GET_SENSOR_STATUS_URL + str(param['id']), timeout=5)

                        if r.status_code == 200:
                            measurements = r.json()

                            for measurement in measurements['values']:
                                if measurement['value'] is not None:
                                    pm[measurements['key']] = measurement['value']
                                    date = measurement['date']
                                    break


                normalized_measurements = {}
                normalized_measurements['id'] = station['id']
                normalized_measurements['vendor'] = 'GIOS'
                normalized_measurements['temperature'] = None
                normalized_measurements['date'] = date

                if 'PM10' in pm:
                    normalized_measurements['pm10'] = pm['PM10']
                else:
                    normalized_measurements['pm10'] = None

                if 'PM2.5' in pm:
                    normalized_measurements['pm2_5'] = pm['PM2.5']
                else:
                    normalized_measurements['pm2_5'] = None

                producer.send('monitoring', normalized_measurements)
                print("Send info about station {}".format(station['id']))