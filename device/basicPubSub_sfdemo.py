'''
/*
 * Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 */
 '''
 
# Smart Factory Thing device demo Client
import sys
import ssl
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json
import time
import logging
import argparse
import turck_modbus as tm
from datetime import datetime

# Parameter (Edit if necessary) : 
gg_core_endpoint = "192.168.8.101"
gg_core_port = 8883
gg_core_root_ca_path = "sf-mqtt-ggc_CA.pem"
thing_private_key = "c93427a475.private.key"
thing_certificate = "c93427a475.cert.pem"
thing_name = "SF_thing"
topic_default_path = "turck/station"

# Custom MQTT message callback
def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")

# Read in command-line parameters
AllowedActions = ['both', 'publish', 'subscribe']

parser = argparse.ArgumentParser()
parser.add_argument("-e", "--endpoint", default=gg_core_endpoint, action="store", required=False, dest="host", help="Your AWS IoT custom endpoint")
parser.add_argument("-r", "--rootCA", default=gg_core_root_ca_path, action="store", required=False, dest="rootCAPath", help="Root CA file path")
parser.add_argument("-c", "--cert", default=thing_certificate, action="store", dest="certificatePath", help="Certificate file path")
parser.add_argument("-k", "--key", default=thing_private_key, action="store", dest="privateKeyPath", help="Private key file path")
parser.add_argument("-p", "--port", default=gg_core_port, action="store", dest="port", type=int, help="Port number override")
parser.add_argument("-w", "--websocket", action="store_true", dest="useWebsocket", default=False,
                    help="Use MQTT over WebSocket")
parser.add_argument("-id", "--clientId", action="store", dest="clientId", default=thing_name,
                    help="Targeted client id")
parser.add_argument("-t", "--topic", action="store", dest="topic", default=topic_default_path, help="Targeted topic")
parser.add_argument("-m", "--mode", action="store", dest="mode", default="publish",
                    help="Operation modes: %s"%str(AllowedActions))
parser.add_argument("-M", "--message", action="store", dest="message", default="Test message from vanessa",
                    help="Message to publish")

args = parser.parse_args()
host = args.host
rootCAPath = args.rootCAPath
certificatePath = args.certificatePath
privateKeyPath = args.privateKeyPath
port = args.port
useWebsocket = args.useWebsocket
clientId = args.clientId
topic = args.topic

if args.mode not in AllowedActions:
    parser.error("Unknown --mode option %s. Must be one of %s" % (args.mode, str(AllowedActions)))
    exit(2)

if args.useWebsocket and args.certificatePath and args.privateKeyPath:
    parser.error("X.509 cert authentication and WebSocket are mutual exclusive. Please pick one.")
    exit(2)

if not args.useWebsocket and (not args.certificatePath or not args.privateKeyPath):
    parser.error("Missing credentials for authentication.")
    exit(2)


# Port defaults
if args.useWebsocket and not args.port:  # When no port override for WebSocket, default to 443
    port = 443
if not args.useWebsocket and not args.port:  # When no port override for non-WebSocket, default to 8883
    port = 8883

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
if useWebsocket:
    myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId, useWebsocket=True)
    myAWSIoTMQTTClient.configureEndpoint(host, port)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath)
else:
    myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
    myAWSIoTMQTTClient.configureEndpoint(host, port)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
if args.mode == 'both' or args.mode == 'subscribe':
    myAWSIoTMQTTClient.subscribe(topic, 1, customCallback)
time.sleep(2)

# Publish to the same topic in a loop forever
loopCount = 0
while True:
    if args.mode == 'both' or args.mode == 'publish':
        c = tm.modbustcp_client()
        readInputRegisters = tm.read_input_regs(c)

        message = {}
        message['message'] = args.message
        # message['sequence'] = loopCount
        # message['timestamp'] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        message['message'] = readInputRegisters.registers[0:100]
        messageJson = json.dumps(message)
        myAWSIoTMQTTClient.publish(topic, messageJson,0)
        if args.mode == 'publish':
            print('Published topic %s: %s\n' % (topic, messageJson))
        loopCount += 1
        tm.close(c)
    time.sleep(1)
