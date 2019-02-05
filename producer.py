import pika
import time

USERNAME=
PASSWORD=
SERVER=

# connect to AMQP server
credentials = pika.PlainCredentials(USERNAME,PASSWORD)
connection = pika.BlockingConnection(pika.ConnectionParameters(SERVER,credentials=credentials))

channel = connection.channel()

channel.queue_declare(queue='connection-test')

# time since epoch in seconds, returned as a float and cast to a string
timestamp = str(time.time())
print (timestamp)

channel.basic_publish(exchange='', routing_key='connection-test', body='connection-test-'+timestamp)

print('pubished message {} onto queue {}'.format(timestamp,'connection-test'))

connection.close()

# now read off the queue

# define a callback function which will be associated with a queue

def callback(ch, method, properties, body):
    print('received message {} from queue {}'.format(body,'connection-test'))

channel.basic_consume(callback, queue='connection-test',no_ack=True)

print('Waiting for messages')
channel.start_consuming()
