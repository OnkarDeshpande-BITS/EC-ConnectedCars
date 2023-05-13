import sys
import traceback

from awsiot.greengrasscoreipc.clientv2 import GreengrassCoreIPCClientV2
from awsiot.greengrasscoreipc.model import (
    PublishMessage,
    BinaryMessage
)
                    
topic = "edge/+/alerts/situation"
message = "Hello from the pub/sub publisher (Python)."
TIMEOUT = 10


def publish_binary_message_to_topic(ipc_client, topic, message):
    binary_message = BinaryMessage(message=bytes(message, 'utf-8'))
    publish_message = PublishMessage(binary_message=binary_message)
    return ipc_client.publish_to_topic(topic=topic, publish_message=publish_message)

try:
    ipc_client = GreengrassCoreIPCClientV2()
    publish_binary_message_to_topic(ipc_client, topic, message)
    print('Successfully published to topic: ' + topic)
	try:
        while True:
            time.sleep(10)
    except InterruptedError:
        print('Subscribe interrupted.')
except Exception:
    print('Exception occurred', file=sys.stderr)
    traceback.print_exc()
    exit(1)
