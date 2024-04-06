import json
import os
import sys
import time

import pika
from config import SMS_QUEUE_NAME
from models import Contact
from bson.objectid import ObjectId
import connect


def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue=SMS_QUEUE_NAME, durable=True)

    def callback(ch, method, properties, body):
        message = json.loads(body.decode())
        print(f" [x] Sending sms to id {message} ...")
        time.sleep(0.1)

        Contact.objects(id=ObjectId(
            message)).update_one(set__email=True)

        print(f"Sms sent for {method.delivery_tag} ")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=SMS_QUEUE_NAME, on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
