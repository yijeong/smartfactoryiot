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



mqttc = AWSIoTMQTTClient("SF_thing")

# Make sure you use your GGC end-point!!
mqttc.configureEndpoint("192.168.8.101",8883)
mqttc.configureCredentials("sf-mqtt-ggc_CA.pem","c93427a475.private.key","c93427a475.cert.pem")


#Function to encode a payload into JSON
def json_encode(string):
    return json.dumps(string)

mqttc.json_encode=json_encode

message ={
  'message': "Hello from our Greengrass Device"
}

#Encoding into JSON
message = mqttc.json_encode(message)

mqttc.connect()

print ("Connected to the Greengrass core!")

mqttc.publish("test/sf", message, 0)

print ("Message Published")
mqttc.disconnect()
time.sleep(2)

