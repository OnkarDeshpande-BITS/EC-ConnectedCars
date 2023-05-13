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

CLIENT_DEVICE_HEALTH_TOPIC = 'device/+/health'
EDGE_TO_CLOUD_HEALTH_TOPIC = 'edge/GG-RSU-001/aggregate/health'
TIMEOUT = 10
received_count = 0


def on_device_health_message(event):
    try:
        message = str(event.binary_message.message, 'utf-8')
        print('Received new message: %s' % message)
        global received_count
        received_count += 1
        print('Analyzing device health message ....')
        if received_count % 10 != 0 :
            print('Health Stastics Not deviated....waiting for further messages')
        else :
            print('Sending aggregated vehicle health data to centre')
            health_msg = {}
            health_msg["seqNo"] = received_count
            current_dateTime = datetime.now()
            health_msg["datetime"] = current_dateTime.strftime("%Y-%m-%d %H:%M:%S")
            health_msg["rsu_id"] = "GG-RSU-001"
            health_msg["vehicle_stats"] = message
            message_json = json.dumps(health_msg)
            binary_message = BinaryMessage(message=bytes(message_json, 'utf-8'))
            publish_message = PublishMessage(binary_message=binary_message)
            ipc_pub_client = GreengrassCoreIPCClientV2()
            ipc_pub_client.publish_to_topic(topic=EDGE_TO_CLOUD_HEALTH_TOPIC, publish_message=publish_message)
            print('Successfully publised to topic: %s' %EDGE_TO_CLOUD_HEALTH_TOPIC)

    except:
        traceback.print_exc()


try:
    ipc_client = GreengrassCoreIPCClientV2()

    # SubscribeToTopic returns a tuple with the response and the operation.
    _, operation = ipc_client.subscribe_to_topic(
        topic=CLIENT_DEVICE_HEALTH_TOPIC, on_stream_event=on_device_health_message)
    print('Successfully subscribed to topic: %s' %
          CLIENT_DEVICE_HEALTH_TOPIC)	  
    # Keep the main thread alive, or the process will exit.
    try:
        while True:
            time.sleep(10)
    except InterruptedError:
        print('Subscribe interrupted.')

    operation.close()
except Exception:
    print('Exception occurred when using IPC.', file=sys.stderr)
    traceback.print_exc()
    exit(1)
