import logging
import json
import time
from ..sonbase.manoplugin import ManoPlugin


class LifecyclemanagementPlugin(ManoPlugin):

    def __init__(self):
        # call super class to do all the messaging and registration overhead
        super(self.__class__, self).__init__(blocking=False)

    def declare_subscriptions(self):
        """
        Declare topics to which we want to listen and define callback methods.
        """
        # receive all platform.# messages and print them
        self.subscribe("service.management.lifecycle.start", self.on_start)

    def on_start(self, ch, method, properties, body):
        logging.info("=" * 60)
        logging.info(" [x] Trigger the instantiation of the service through the infrastructure abstraction here.")
        logging.info("=" * 60)

    def run(self):
        """
        Overwrites. Put your Plugin code here.
        """
        while True:
            time.sleep(60)
            self.heartbeat()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    p = LifecyclemanagementPlugin()
