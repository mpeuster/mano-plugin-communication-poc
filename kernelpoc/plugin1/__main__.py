import logging
import json
import time
from ..sonbase.manoplugin import ManoPlugin


class DemoPlugin1(ManoPlugin):

    def __init__(self):
        # call super class to do all the messaging and registration overhead
        super(self.__class__, self).__init__(blocking=False)

    def declare_subscriptions(self):
        """
        Declare topics to which we want to listen and define callback methods.
        """
        # receive all platform.# messages and print them
        self.subscribe("platform.#", self.callback_print)

    def run(self):
        """
        Overwrites. Put your Plugin code here.
        """
        # lets have some fun and query the plugin manager for a list of plugins
        self.publish("platform.management.plugins.list", json.dumps({"type": "REQ"}))
        # give us some time to react
        time.sleep(3)
        # lets stop this plugin
        self.deregister()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    p = DemoPlugin1()
