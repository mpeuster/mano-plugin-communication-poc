import logging
from ..sonbase.manoplugin import ManoPlugin


def callback_print(ch, method, properties, body):
    logging.debug("RECEIVED from %r: %r" % (method.routing_key, body))


class SonPluginManager(ManoPlugin):

    def __init__(self):
        super(self.__class__, self).__init__()

    def start(self):
        self.subscribe("platform.*", callback_print)
        self.publish("platform.test", "Hello World!")
        self.chan.start_consuming()


def main():
    spm = SonPluginManager()
    spm.start()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
