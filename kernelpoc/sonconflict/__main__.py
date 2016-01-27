import logging
import json
import time
from ..sonbase.manoplugin import ManoPlugin


class ConflictresolutionPlugin(ManoPlugin):

    def __init__(self):
        # call super class to do all the messaging and registration overhead
        super(self.__class__, self).__init__(blocking=False)

    def declare_subscriptions(self):
        """
        Declare topics to which we want to listen and define callback methods.
        """
        self.subscribe("service.management.conflictresolution.validate", self.on_validate)

    def on_validate(self, ch, method, properties, body):
        sender = properties.app_id
        message = json.loads(body)
        logging.info(" [x] Do the conflict resolution here!")
        message = {"service": message.get("service"),
                   "placement_graph": "I am a placement graph description.",
                   "validated_placement_graph": "I am a placement graph that was modified by the conflict resolution plugin."}
        # send result to lifecycle plugin
        self.publish("service.management.lifecycle.start", json.dumps(message))

    def run(self):
        """
        Overwrites. Put your Plugin code here.
        """
        while True:
            time.sleep(60)
            logging.debug("Heartbeat.")

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    p = ConflictresolutionPlugin()
