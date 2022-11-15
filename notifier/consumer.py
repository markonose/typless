import logging
from threading import Thread

import pika
from pika.exchange_type import ExchangeType

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logging.getLogger('pika').setLevel(logging.WARNING)


class Consumer(Thread):
    def run(self):
        connection = pika.BlockingConnection(pika.URLParameters('amqp://guest:guest@localhost:5672'))

        channel = connection.channel()
        channel.exchange_declare(
            exchange="processing-events",
            exchange_type=ExchangeType.direct,
            durable=True)

        channel.queue_declare(queue="processing-events", durable=True)
        channel.queue_bind(
            queue="processing-events", exchange="processing-events", routing_key="")

        channel.basic_qos(prefetch_count=1)

        channel.basic_consume('processing-events', self.on_message)
        channel.start_consuming()

    def on_message(self, ch, method_frame, _header_frame, body):
        LOGGER.info('Delivery tag: %s Message body: %s',
                    method_frame.delivery_tag, body)

        if ch.is_open:
            ch.basic_ack(method_frame.delivery_tag)
