#
# Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#

import logging
import sys
import json
import greengrasssdk
from datetime import datetime
import time

# Setup logging to stdout
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# create Client 
gclient = greengrasssdk.client("iot-data")

# event message handler 
def message_handler(event, context):
    logger.info("Received message!")
    logger.info(json.dumps(event))
    
    message = event["message"]
    div_msg(message)
    
# divide and pack message 
def div_msg(message):
    # convert int to float
    for num in range(len(message)) :  
        message[num]=float(round(message[num],2))
    
    # divide and pack message for station 0 
    sta0_msg = {}
    sta0_msg["iConv_Status"] = message[0]
    sta0_msg["iConv_Mode"] = message[1]
    sta0_msg["iConv_LED"] = message[2]
    sta0_msg["iConv_Count"] = message[3]
    sta0_msg["rConv_Angle"] = message[4]
    sta0_msg["sDateTime"] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    
    sta0_msg =json.dumps(sta0_msg)
    
    # divide and pack message for station 1 
    sta1_msg = {}
    sta1_msg["xStation1_IN"] = message[10]
    sta1_msg["xStation1_OUT"] = message[11]
    sta1_msg["iStation1_Product_Info"] = message[12]
    sta1_msg["iStation1_Product_Status"] = message[13]
    sta1_msg["iStation1_Timer"] = message[14]
    sta1_msg["sDateTime"] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

    sta1_msg =json.dumps(sta1_msg)

    # divide and pack message for station 2
    sta2_msg = {}
    sta2_msg["iStation2_ZigNo"] = message[20]
    sta2_msg["xStation2_Vision_TF"] = message[21]
    sta2_msg["wStation2_TP"] = message[22]
    sta2_msg["iStation2_Timer"] = message[23]
    sta2_msg["sDateTime"] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    
    sta2_msg =json.dumps(sta2_msg)
        
    # divide and pack message for station 3
    sta3_msg = {}
    sta3_msg["iStation3_ZigNo"] = message[30]
    sta3_msg["xStation3_Sol1"] = message[31]
    sta3_msg["xStation3_Sol2"] = message[32]
    sta3_msg["xStation3_Sol3"] = message[33]
    sta3_msg["xStation3_Sol4"] = message[34]
    sta3_msg["iStation3_Timer"] = message[35]
    sta3_msg["sDateTime"] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
  
    sta3_msg =json.dumps(sta3_msg)

    # divide and pack message for station 4
    sta4_msg = {}
    sta4_msg["iStation4_ZigNo"] = message[40]
    sta4_msg["rStation4_Q4X_Value"] = message[41]
    sta4_msg["wStation4_Vision_Red"] = message[42]
    sta4_msg["wStation4_Vision_Green"] = message[43]
    sta4_msg["wStation4_Vision_Blue"] = message[44]
    sta4_msg["iStation4_Timer"] = message[45]
    sta4_msg["sDateTime"] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    
    sta4_msg =json.dumps(sta4_msg)

    # divide and pack message for station 5
    sta5_msg = {}
    sta5_msg["iStation5_ZigNo"] = message[50]
    sta5_msg["iStation5_Timer"] = message[51]
    sta5_msg["sDateTime"] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]    

    sta5_msg =json.dumps(sta5_msg)

    # divide and pack message for station 6
    sta6_msg = {}
    sta6_msg["iStation6_ZigNo"] = message[60]
    sta6_msg["xStation6_Status"] = message[61]
    sta6_msg["xStation6_Quaility"] = message[62]
    sta6_msg["iStation6_Quaility_Total"] = message[63]
    sta6_msg["iStation6_Quaility_Pass"] = message[64]
    sta6_msg["xQualityCountReset"] = message[65]
    sta6_msg["iStation6_Timer"] = message[66]
    sta6_msg["sDateTime"] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    
    sta6_msg =json.dumps(sta6_msg)

    # divide and pack message for station 7
    sta7_msg = {}
    sta7_msg["rVibration_Temp"] = message[70]
    sta7_msg["rVibration_Z_RMS_Velocity"] = message[71]
    sta7_msg["rVibration_X_RMS_Velocity"] = message[72]
    sta7_msg["wRMSCurrent"] = message[73]
    sta7_msg["wCurrentLoad"] = message[74]
    sta7_msg["wEncoderVelocity"] = message[75]
    sta7_msg["wCylinderStatus"] = message[76]
    sta7_msg["iCount"] = message[77]
    sta7_msg["iStation_Timer_Total"] = message[78]
    sta7_msg["sDateTime"] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]    

    sta7_msg =json.dumps(sta7_msg)
    logger.info(sta7_msg)
    print(sta7_msg)
    publish_msg (sta0_msg, sta1_msg, sta2_msg, sta3_msg, sta4_msg, sta5_msg, sta6_msg, sta7_msg)
    
    
# publish message by station 0 ~ 7 to AWS iot core
def publish_msg (sta0_msg, sta1_msg, sta2_msg, sta3_msg, sta4_msg, sta5_msg, sta6_msg, sta7_msg): 

    gclient.publish(topic = "turck/station0", payload = sta0_msg)
    gclient.publish(topic = "turck/station1", payload = sta1_msg)
    gclient.publish(topic = "turck/station2", payload = sta2_msg)
    gclient.publish(topic = "turck/station3", payload = sta3_msg)
    gclient.publish(topic = "turck/station4", payload = sta4_msg)
    gclient.publish(topic = "turck/station5", payload = sta5_msg)
    gclient.publish(topic = "turck/station6", payload = sta6_msg)
    gclient.publish(topic = "turck/station7", payload = sta7_msg)

    return True



