import logging
import json
import time
from ..sonbase.manoplugin import ManoPlugin


class PlacementPlugin(ManoPlugin):

    def __init__(self):
        # call super class to do all the messaging and registration overhead
        super(self.__class__, self).__init__(blocking=False)

    def declare_subscriptions(self):
        """
        Declare topics to which we want to listen and define callback methods.
        """
        self.subscribe("service.management.placement.compute", self.on_compute)

    def on_compute(self, ch, method, properties, body):
        sender = properties.app_id
        message = json.loads(body)
        logging.info(" [x] Do a complicated placement computation here!")
        message = {"service": message.get("service"),
                   "placement_graph": "I am a placement graph description."}
        # send result to conflict resolution
        self.publish("service.management.conflictresolution.validate", json.dumps(message))

    def run(self):
        """
        Overwrites. Put your Plugin code here.
        """
        while True:
            time.sleep(60)
            logging.debug("Heartbeat.")

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    p = PlacementPlugin()
