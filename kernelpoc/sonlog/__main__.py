import logging
import json
import time
from ..sonbase.manoplugin import ManoPlugin


class LoggingPlugin(ManoPlugin):
    """
    Subscribes to all topics and prints every message.
    """

    def __init__(self):
        # call super class to do all the messaging and registration overhead
        super(self.__class__, self).__init__(blocking=False)

    def declare_subscriptions(self):
        """
        Declare topics to which we want to listen and define callback methods.
        """
        # receive all messages and print them
        self.subscribe("#", self.callback_print)

    def run(self):
        """
        Overwrites. Put your Plugin code here.
        """
        while True:
            time.sleep(60)
            self.heartbeat()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    p = LoggingPlugin()
