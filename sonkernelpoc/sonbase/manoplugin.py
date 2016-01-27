"""
Base classed to simplify the implementation of new
MANO plugins.
"""
# TODO re-factor this and encapsulate all RabbitMQ related code
# TODO create a nice design with async. messaging instead of blocking connections

import pika
import logging
logging.getLogger('pika').setLevel(logging.ERROR)

RABBITMQ_HOST = "localhost"
RABBITMQ_EXCHANGE = "son-kernel"


class ManoPlugin(object):

    def __init__(self):
        self.conn = None
        self.chan = None
        logging.info(
            "Starting MANO Plugin: %r ..." % self.__class__.__name__)
        # setup RabbitMQ connection
        self._connect_to_rabbitmq()

    def __del__(self):
        if self.chan:
            self.chan.close()
        if self.conn:
            self.conn.close()

    def _connect_to_rabbitmq(self):
        # connect to RabbitMQ and channel
        self.conn = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST))
        self.chan = self.conn.channel()
        # select exchange
        self.chan.exchange_declare(
            exchange=RABBITMQ_EXCHANGE, type='topic')
        logging.info("Connected to RabbitMQ on %r", RABBITMQ_HOST)

    def publish(self, topic, message, exchange=RABBITMQ_EXCHANGE):
        """
        Simplified wrapper to publish a message.
        """
        self.chan.basic_publish(
            exchange=exchange,
            routing_key=topic,
            body=message)
        logging.debug("PUBLISHED to %r: %r", topic, message)

    def subscribe(self, topic, callback, exchange=RABBITMQ_EXCHANGE):
        """
        Simplified wrapper for subscriptions.
        """
        # TODO allow list of topics, to handle multiple topics with a single callback function
        # create a queue for incoming message
        self.chan.queue_declare("queue_%s" % topic)
        # bind the queue to all given topics
        self.chan.queue_bind(
            exchange=exchange,
            queue="queue_%s" % topic,
            routing_key=topic)
        # define a callback function to be called whenever a message arrives in our queue
        self.chan.basic_consume(
            callback,
            queue="queue_%s" % topic,
            no_ack=True)
        logging.debug("SUBSCRIBED to %r", topic)
