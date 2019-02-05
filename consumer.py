import pika
import logging

USERNAME
PASSWORD
SERVER

def main():
    logging.basicConfig(filename='consumer.log', format='%(asctime)s  %(levelname)s  %(message)s', level=logging.DEBUG)

    # connect to uk-test-other
    credentials = pika.PlainCredentials(USERNAME,PASSWORD)
    connection = pika.BlockingConnection(pika.ConnectionParameters(SERVER,credentials=credentials))

    channel = connection.channel()

    channel.queue_declare(queue='connection-test')

    # now read off the queue
    # define a callback function which will be associated with a queue

    def callback(ch, method, properties, body):
        logging.info('received message {} from queue {}'.format(body, 'connection-test'))

    channel.basic_consume(callback, queue='connection-test',no_ack=True)

    logging.info('Listening for incoming messages')
    channel.start_consuming()


if __name__ == '__main__':
    main()
