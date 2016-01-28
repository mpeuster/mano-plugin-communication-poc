import logging
import json
import time
from ..sonbase.manoplugin import ManoPlugin


class SonPluginManager(ManoPlugin):

    def __init__(self):
        # plugin management: simple dict for bookkeeping
        self.plugins = {}
        # call super class to do all the messaging and registration overhead
        super(self.__class__, self).__init__(blocking=True)  # we block and wait until someone registers

    def declare_subscriptions(self):
        """
        Declare topics to which we want to listen and define callback methods.
        """
        self.subscribe("platform.management.plugins.register", self.on_register)
        self.subscribe("platform.management.plugins.deregister", self.on_deregister)
        self.subscribe("platform.management.plugins.list", self.on_list)

    def on_register(self, ch, method, properties, body):
        sender = properties.app_id
        message = json.loads(body)
        # simplified example for plugin bookkeeping
        self.plugins[sender] = message
        logging.info("REGISTERED: %r" % message.get("plugin"))

    def on_deregister(self, ch, method, properties, body):
        sender = properties.app_id
        message = json.loads(body)
        # simplified example for plugin bookkeeping
        self.plugins[sender] = message
        logging.info("DE-REGISTERED: %r" % message.get("plugin"))

    def on_list(self, ch, method, properties, body):
        sender = properties.app_id
        message = json.loads(body)
        if message.get("type") == "REQ":
            # we have a request, lets answer
            message = {"type": "REP",
                       "plugins": self.plugins}
            self.publish("platform.management.plugins.list", json.dumps(message))


def main():
    spm = SonPluginManager()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
