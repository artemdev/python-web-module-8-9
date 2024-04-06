import json
import random

import pika
import connect
from models import Contact
from faker import Faker
from config import EXCHANGE_NAME, EMAIL_QUEUE_NAME, SMS_QUEUE_NAME

fake = Faker()

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='direct')
# Email queue
channel.queue_declare(queue=EMAIL_QUEUE_NAME, durable=True)
channel.queue_bind(exchange=EXCHANGE_NAME, queue=EMAIL_QUEUE_NAME)

# SMS queue
channel.queue_declare(queue=SMS_QUEUE_NAME, durable=True)
channel.queue_bind(exchange=EXCHANGE_NAME, queue=SMS_QUEUE_NAME)


def create_tasks(nums: int):
    for _ in range(nums):
        contact = Contact(
            name=fake.name(), preferred_contact_method=random.choice(['sms', 'email']))
        contact.save()

        if contact.preferred_contact_method == 'sms':
            queue_name = SMS_QUEUE_NAME
        else:
            queue_name = EMAIL_QUEUE_NAME

        channel.basic_publish(exchange=EXCHANGE_NAME,
                              routing_key=queue_name, body=json.dumps(str(contact.id)).encode())

    connection.close()


if __name__ == '__main__':
    create_tasks(100)
