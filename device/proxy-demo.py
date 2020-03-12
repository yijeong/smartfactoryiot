'''
/*
 * Copyright 2010-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License").
 * You may not use this file except in compliance with the License.
 * A copy of the License is located at
 *
 *  http://aws.amazon.com/apache2.0
 *
 * or in the "license" file accompanying this file. This file is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific language governing
 * permissions and limitations under the License.
 */
 '''

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
import json
import subprocess

# Parameter (Edit if necessary) : 
aws_region = "us-east-1"
localproxy_path = "/home/ubuntu/dependencies/aws-iot-securetunneling-localproxy/build/bin/localproxy"
iot_endpoint = " " # xxxxxxxxxxxx-ats.iot.us-east-1.amazonaws.com
iot_thingname = "SFworkshop-thing"
iot_private_key = " " # xxxxxxxxxx-private.pem.key
iot_certificate = " " # xxxxxxxxxx-certificate.pem.crt



AllowedActions = ['both', 'publish', 'subscribe']


# Custom MQTT message callback
def customCallback(client, userdata, message):
    print("Received a new open tunnel notification: ")
    json_message = json.loads(message.payload.decode('utf-8'))
    print(json_message)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")
    print("Opening tunnel on port 22")
    subprocess.run([localproxy_path, "-t", json_message['clientAccessToken'], "-r", aws_region , "-d", "localhost:22"])

# Read in command-line parameters
parser = argparse.ArgumentParser()
parser.add_argument("-e", "--endpoint", action="store", default=iot_endpoint, required=False, dest="host", help="Your AWS IoT custom endpoint")
parser.add_argument("-t", "--thingName", action="store", default=iot_thingname,
                    help="Thing name")


args = parser.parse_args()
host = args.host
thing_name = args.thingName


if not args.thingName:
    parser.error("Missing thing name.")
    exit(2)

# Port defaults

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
myAWSIoTMQTTClient = AWSIoTMQTTClient(thing_name)
myAWSIoTMQTTClient.configureEndpoint(host, 443)
#myAWSIoTMQTTClient.configureCredentials("AmazonRootCA1.pem", "{0}.private.key".format(thing_name), "{0}.cert.pem".format(thing_name))
myAWSIoTMQTTClient.configureCredentials("AmazonRootCA1.pem", iot_private_key, iot_certificate)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
myAWSIoTMQTTClient.subscribe("$aws/things/{0}/tunnels/notify".format(thing_name), 1, customCallback)
time.sleep(2)

loopCount = 0
while True:
    time.sleep(1)
