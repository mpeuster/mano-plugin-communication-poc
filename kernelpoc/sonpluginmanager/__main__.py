import logging
import json
import time
from ..sonbase.manoplugin import ManoPlugin


class SonPluginManager(ManoPlugin):

    def __init__(self):
        super(self.__class__, self).__init__()
        # start receiver loop
        self.start_io_loop(blocking=False)

    def declare_subscriptions(self):
        self.subscribe("platform.*", self.callback_print)

    def test(self):
        self.publish("platform.test", json.dumps("Hello World!"))

    def callback_print(self, ch, method, properties, body):
        logging.debug("RECEIVED from %r on %r: %r" % (
            properties.app_id, method.routing_key, json.loads(body)))


def main():
    spm = SonPluginManager()
    spm.test()
    time.sleep(1)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
