import logging
import json
import time
import argparse
import sys
from ..sonbase.manoplugin import ManoPlugin


class DemoPlugin1(ManoPlugin):

    def __init__(self):
        # call super class to do all the messaging and registration overhead
        super(self.__class__, self).__init__(blocking=False)

    def declare_subscriptions(self):
        """
        Declare topics to which we want to listen and define callback methods.
        """
        self.subscribe("platform.management.plugins.list", self.on_list_result)
        self.subscribe("service.management.#", self.on_deployment_step)

    def on_list_result(self, ch, method, properties, body):
        sender = properties.app_id
        message = json.loads(body)
        if message.get("type") == "REP":
            # we have a reply, lets print it
            print "-" * 20 + " Plugins " + "-" * 20
            for k, v in message.get("plugins").iteritems():
                print "%s, %s, %s" % (k, v.get("version"), v.get("state"))
            print "-" * 49

    def on_deployment_step(self, ch, method, properties, body):
        sender = properties.app_id
        topic = method.routing_key
        message = json.loads(body)
        if "placement.compute" in topic:
            logging.info("NOTIFY: Running placement ...")
        if "onflictresolution.validate" in topic:
            logging.info("NOTIFY: Running conflict resolution ...")
        if "lifecycle.start" in topic:
            logging.info("NOTIFY: Running lifecycle management ...")

    def list_plugins(self):
        # lets have some fun and query the plugin manager for a list of plugins
        self.publish("platform.management.plugins.list", json.dumps({"type": "REQ"}))

    def deploy_example(self):
        # trigger deployment workflow of example B
        self.publish("service.management.placement.compute", json.dumps(
            {"service": "Service A", "service_chain_graph": "I am a complex service chain."}))

parser = argparse.ArgumentParser(description='plugin1 example interface')
parser.add_argument(
    "command",
    choices=['deploy', 'list'],
    help="Action to be executed.")

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    p = DemoPlugin1()
    # parse inputs and react accordingly
    args = vars(parser.parse_args(sys.argv[1:]))
    if args.get("command") == "deploy":
        p.deploy_example()
    else:
        p.list_plugins()
    # give us some time to react
    time.sleep(1)
    p.deregister()
