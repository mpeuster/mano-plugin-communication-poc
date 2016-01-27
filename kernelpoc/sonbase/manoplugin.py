"""
Base classed to simplify the implementation of new
MANO plugins.
"""
# TODO re-factor this and encapsulate all RabbitMQ related code
# TODO create a nice design with async. messaging instead of blocking connections

import pika
import logging
import threading
import json
logging.getLogger('pika').setLevel(logging.ERROR)

RABBITMQ_HOST = "localhost"
RABBITMQ_EXCHANGE = "son-kernel"


class ManoPlugin(object):

    def __init__(self, blocking=False):
        self.conn = None
        self.chan = None
        logging.info(
            "Starting MANO Plugin: %r ..." % self.__class__.__name__)
        # setup RabbitMQ connection
        self._connect_to_rabbitmq()
        # register subscriptions
        self.declare_subscriptions()
        # register to plugin manager
        self.register()
        # start receiver loop
        self.start_io_loop(blocking=blocking)
        # jump to run()
        self.run()

    def __del__(self):
        # de-register this plugin
        self.deregister()
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

    def declare_subscriptions(self):
        """
        To be overwritten by subclass
        """
        pass

    def run(self):
        """
        To be overwritten by subclass
        """
        pass

    def publish(self, topic, message, exchange=RABBITMQ_EXCHANGE):
        """
        Simplified wrapper method to publish a message.
        """
        properties = pika.BasicProperties(
            app_id=self.__class__.__name__,
            content_type='application/json')

        self.chan.basic_publish(
            exchange=exchange,
            routing_key=topic,
            body=message,
            properties=properties)
        logging.debug("PUBLISHED to %r: %r", topic, message)

    def subscribe(self, topic, callback, exchange=RABBITMQ_EXCHANGE):
        """
        Simplified wrapper method for subscriptions.
        """
        # TODO allow list of topics, to handle multiple topics with a single callback function
        # create a queue for incoming message
        # (each MANO plugin needs it own queue, otherwise messages are only processed by the one which fetches it first)
        self.chan.queue_declare("queue_%s_%s" % (self.__class__.__name__, topic))
        # bind the queue to all given topics
        self.chan.queue_bind(
            exchange=exchange,
            queue="queue_%s_%s" % (self.__class__.__name__, topic),
            routing_key=topic)
        # define a callback function to be called whenever a message arrives in our queue
        self.chan.basic_consume(
            callback,
            queue="queue_%s_%s" % (self.__class__.__name__, topic),
            no_ack=True)
        logging.debug("SUBSCRIBED to %r", topic)

    def start_io_loop(self, blocking=False):
        """
        Lets run our receiver in a own thread
        """
        def reciever_thread():
            self.chan.start_consuming()

        if blocking:
            reciever_thread()
            return

        t = threading.Thread(target=reciever_thread, args=())
        t.daemon = True
        t.start()

    def callback_print(self, ch, method, properties, body):
        """
        Helper callback that prints the received message.
        """
        logging.debug("RECEIVED from %r on %r: %r" % (
            properties.app_id, method.routing_key, json.loads(body)))

    def register(self):
        """
        Send a register event to the plugin manager component to announce this plugin.
        """
        message = {"type": "REQ",
                   "plugin": self.__class__.__name__,
                   "state": "ACTIVE",
                   "version": "v0.1-dev1"}
        self.publish(
            "platform.management.plugins.register", json.dumps(message))

    def deregister(self):
        """
        Send a deregister event to the plugin manager component.
        """
        message = {"type": "REQ",
                   "plugin": self.__class__.__name__,
                   "state": "INACTIVE"}
        self.publish(
            "platform.management.plugins.deregister", json.dumps(message))
