import pika, json, psycopg2
from psycopg2 import IntegrityError 

def callback(channel, method, properties, body):

    print('consume data from queue: '+method.routing_key)
    body = body.decode("UTF-8")
    data = json.loads(body)
    
    try:
        connDB = psycopg2.connect("dbname=airpollutionmonitor user=air host=localhost")
    except:
        print("Unable to connect the db, please check logs!")
    
    curDB = connDB.cursor()

    if method.routing_key == "station":
        curDB.execute("SELECT COUNT(*) FROM stations WHERE id = %s AND vendor = %s;", (data["id"],data["vendor"],))

        if curDB.fetchall()[0][0] == 0:
            curDB.execute("INSERT INTO stations (vendor, stationid, stationname, lng, lat, city, street) VALUES (%s, %s, %s, %s, %s, %s, %s)", (data["vendor"], data["id"], data["station_name"], data["lng"], data["lat"], data["city"], data["street"] ))
            connDB.commit()
    
    if method.routing_key == "monitoring":
        curDB.execute("SELECT id FROM stations WHERE stationid = %s AND vendor = %s;", (data["id"],data["vendor"]))

        #this is NOT stationid in API meaning but the system internal stations(id), which identifies particular stations from stations table primary key
        stationID = curDB.fetchall()[0][0]

        curDB.execute("SELECT COUNT(*) FROM monitoring WHERE stationid = %s AND date = %s;", (stationID, data["date"]))
        if curDB.fetchall()[0][0] == 0:
            try:
                curDB.execute("INSERT INTO monitoring (stationid, pm2_5, pm10, temp, date) VALUES (%s, %s, %s, %s, %s)", (stationID , data["pm2_5"], data["pm10"], data["temperature"], data["date"] ))
            except IntegrityError:
                print("!ERROR! Received data about " + data["vendor"] + " station id:" + str(data["id"]) + " haven't been found in stations set, the data is dropped!!!")
            connDB.commit()

    connDB.close()
    channel.basic_ack(delivery_tag=method.delivery_tag)

def on_open(connection):
    connection.channel(on_channel_open)

def on_channel_open(channel):
    channel.basic_consume(callback, queue='station')
    channel.basic_consume(callback, queue='monitoring')

parameters = pika.URLParameters('amqp://guest:guest@localhost:5672/%2F')
connection = pika.SelectConnection(parameters=parameters, 
                                    on_open_callback=on_open)

try:
    connection.ioloop.start()
except KeyboardInterrupt:
    connection.close()
