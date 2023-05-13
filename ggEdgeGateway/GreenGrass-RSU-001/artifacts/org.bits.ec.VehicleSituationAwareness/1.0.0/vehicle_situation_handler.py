import sys
import time
import traceback
import json
from datetime import datetime

from awsiot.greengrasscoreipc.clientv2 import GreengrassCoreIPCClientV2
from awsiot.greengrasscoreipc.model import (
    PublishMessage,
    BinaryMessage
)

DEVICE_TO_EDGE_ALERT_SUB = 'device/+/alerts/situation'
EDGE_TO_CLOUD_ALERT_PUB = 'edge/GG-Rsu-001/aggregated/alerts'
EDGE_TO_DEVICE_ALERT_PUB = 'edge/GG-Rsu-001/alerts/situation'
CLOUD_TO_EDGE_INFO_SUB = 'cloud/edge/alerts'
TIMEOUT = 10
received_count = 0


def on_device_alert_message(event):
    try:
        message = str(event.binary_message.message, 'utf-8')
        print('Received new alert message: %s' % message)
        global received_count
        received_count += 1
        print('Analyzing situation.....')
        if received_count == 1 or received_count%10==5 :
            print('Situation is confirmed , broadcasting to nearest vehicles....')
            alert_msg = {'situation' : "accident-nearby" , "verified" : "true" , "reroute-avb" : "true"}
            locationdict = {'latitude' : 45.216 , 'longitude' : -122.636  }
            alert_msg["alert_site"] = locationdict
            current_dateTime = datetime.now()
            alert_msg["seqNo"] = received_count
            alert_msg["datetime"] = current_dateTime.strftime("%Y-%m-%d %H:%M:%S")
            message_json = json.dumps(alert_msg)
            time.sleep(100)
            binary_message = BinaryMessage(message=bytes(message_json, 'utf-8'))
            publish_message = PublishMessage(binary_message=binary_message)
            ipc_pub_client = GreengrassCoreIPCClientV2()
            ipc_pub_client.publish_to_topic(topic=EDGE_TO_DEVICE_ALERT_PUB, publish_message=publish_message)
            print('Successfully publised to topic: %s' %EDGE_TO_DEVICE_ALERT_PUB)
            print('Check whether publishing to cloud topic is needed......')
        else :
            print('Same situation and at same location , supressing')

        if received_count%10 == 2 :
             ipc_pub_client2 = GreengrassCoreIPCClientV2()
             alert_msg = {'situation' : "aggregate-accident-report" , "verified" : "true" , "binaryDetails" : "A23GHVDD"}
             locationdict = {'latitude' : 45.216 , 'longitude' : -122.636  }
             alert_msg["alert_site"] = locationdict
             current_dateTime = datetime.now()
             alert_msg["seqNo"] = received_count
             alert_msg["datetime"] = current_dateTime.strftime("%Y-%m-%d %H:%M:%S")
             message_json = json.dumps(alert_msg)
             binary_message = BinaryMessage(message=bytes(message_json, 'utf-8'))
             publish_to_cloud = PublishMessage(binary_message=binary_message)
             ipc_pub_client2.publish_to_topic(topic=EDGE_TO_CLOUD_ALERT_PUB, publish_message=publish_to_cloud)
             print('Successfully publised to topic: %s' %EDGE_TO_CLOUD_ALERT_PUB)			 

    except:
        traceback.print_exc()

def on_alert_from_cloud(event):
    try:
        message = str(event.binary_message.message, 'utf-8')
        print('Received cloud alert message: %s' % message)
        print('Analyzing situation.....')
        time.sleep(1)
        print('Situation is confirmed , broadcasting to nearest vehicles....')
        alert_msg = {'situation' : "oil spill" , "verified" : "ok" }
        locationdict = {'latitude' : 45.216 , 'longitude' : -122.636  }
        alert_msg["alert_site"] = locationdict
        current_dateTime = datetime.now()
        alert_msg["seqNo"] = received_count
        alert_msg["datetime"] = current_dateTime.strftime("%Y-%m-%d %H:%M:%S")
        message_json = json.dumps(alert_msg)
        binary_message = BinaryMessage(message=bytes(message_json, 'utf-8'))
        publish_to_device = PublishMessage(binary_message=binary_message)
        ipc_pub_client3 = GreengrassCoreIPCClientV2()
        ipc_pub_client3.publish_to_topic(topic=EDGE_TO_DEVICE_ALERT_PUB, publish_message=publish_to_device)
        print('Successfully publised to topic: %s' %EDGE_TO_DEVICE_ALERT_PUB)

    except:
        traceback.print_exc()

try:
    ipc_client1 = GreengrassCoreIPCClientV2()

    # SubscribeToTopic returns a tuple with the response and the operation.
    _, operation = ipc_client1.subscribe_to_topic(
        topic=DEVICE_TO_EDGE_ALERT_SUB, on_stream_event=on_device_alert_message)
    print('Successfully subscribed to topic: %s' %
          DEVICE_TO_EDGE_ALERT_SUB)	  
    #Subscribe to cloud alerts
    ipc_client2 = GreengrassCoreIPCClientV2()
    _, operation_1 = ipc_client2.subscribe_to_topic(
    topic=CLOUD_TO_EDGE_INFO_SUB, on_stream_event=on_alert_from_cloud)
    print('Successfully subscribed to topic: %s' %
          CLOUD_TO_EDGE_INFO_SUB)	  
    # Keep the main thread alive, or the process will exit.
    try:
        while True:
            time.sleep(10)
    except InterruptedError:
        print('Subscribe interrupted.')

    operation.close()
    operation_1.close()
except Exception:
    print('Exception occurred when using IPC.', file=sys.stderr)
    traceback.print_exc()
    exit(1)
