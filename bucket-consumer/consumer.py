import logging
import urllib.parse

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from functools import partial
from random import randint
from threading import Thread, get_ident
from time import sleep
from uuid import uuid4

import orjson
import pika
from pika.exchange_type import ExchangeType

from db import documents_collection
from storage import get_object_bytes

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logging.getLogger('pika').setLevel(logging.WARNING)


class Consumer(Thread):
    _document_types = ['invoice', 'delivery note', 'contract']

    def __init__(self):
        super().__init__()
        self.executor = ThreadPoolExecutor(max_workers=1)

    def run(self):
        connection = pika.BlockingConnection(pika.URLParameters('amqp://guest:guest@localhost:5672'))

        channel = connection.channel()
        channel.exchange_declare(
            exchange="processing-events",
            exchange_type=ExchangeType.direct,
            durable=True)

        channel.exchange_declare(
            exchange="bucket-events",
            exchange_type=ExchangeType.direct,
            durable=True)
        channel.queue_declare(queue="bucket-events", durable=True)
        channel.queue_bind(
            queue="bucket-events", exchange="bucket-events", routing_key="")

        channel.basic_qos(prefetch_count=1)

        channel.basic_consume('bucket-events', self.on_message)
        channel.start_consuming()

    def on_message(self, ch, method_frame, _header_frame, body):
        self.executor.submit(self.run_task, ch, method_frame.delivery_tag, body)

    def run_task(self, ch, delivery_tag, body):
        thread_id = get_ident()
        LOGGER.info('Thread id: %s Delivery tag: %s Message body: %s', thread_id,
                    delivery_tag, body)

        json = orjson.loads(body)
        s3_info = json['Records'][0]['s3']

        obj = get_object_bytes(
            s3_info['bucket']['name'],
            urllib.parse.unquote_plus(s3_info['object']['key']))

        sleep(randint(5, 10))

        document = {
            'identifier': str(uuid4()),
            'type': self._document_types[randint(0, 2)],
            'datetime': datetime.utcnow()
        }
        documents_collection.insert_one(document)

        ch.basic_publish(
            exchange='processing-events',
            routing_key="",
            body=orjson.dumps(document, default=str),
            properties=pika.BasicProperties(content_type='application/json'))

        cb = partial(self.ack_message, ch, delivery_tag)
        ch.connection.add_callback_threadsafe(cb)

    def ack_message(self, ch, delivery_tagy):
        if ch.is_open:
            ch.basic_ack(delivery_tagy)
