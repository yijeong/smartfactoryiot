#
# Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#

import logging
import sys
import greengrasssdk

# Setup logging to stdout
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

client = greengrasssdk.client("iot-data")


def message_handler(event, context):
    logger.info("Received message!")
    logger.info(json.dumps(event))

    # publish a response back to AWS IoT
    client.publish(topic = "/test/sf/data", payload = json.dumps(event))

    return True