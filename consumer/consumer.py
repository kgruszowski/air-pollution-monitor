import pika

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='monitoring')

channel.basic_consume(callback,
                      queue='monitoring',
                      no_ack=False)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()