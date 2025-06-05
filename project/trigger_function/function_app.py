import azure.functions as func
import logging
import json

from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import CloudToDeviceMethod
import os

logging.info("Function initializing...")

# Replace with your IoT Hub details

DEVICE_ID = "Your device ID"
STORAGE_ID = "Your Azure storage ID"

def send_direct_method(signal: str):
        
    registry_manager_connection_string = os.environ['REGISTRY_MANAGER_CONNECTION_STRING']
    registry_manager = IoTHubRegistryManager(registry_manager_connection_string)
    direct_method = CloudToDeviceMethod(method_name=signal, payload='{}')

    logging.info(f'Sending direct method request for {direct_method.method_name} for device {DEVICE_ID}')
    registry_manager.invoke_device_module_method(DEVICE_ID,"signalreceiver",direct_method)

app = func.FunctionApp()

@app.function_name(name="triggerFunction")
@app.blob_trigger(arg_name="inputBlob",
                  path="banana-result/{name}",
                  connection="bananaclassify_STORAGE")
def blob_trigger_function(inputBlob: func.InputStream):
    name = inputBlob.name
    logging.info(f"Processing blob: {name}")

    try:

        data = json.loads(inputBlob.read().decode('utf-8'))
        if "bad" in json.dumps(data).lower():
            logging.info("'bad' found — Triggering Python logic and sending message to IoT Edge.")
            send_direct_method("bad")

        else:
            logging.info("'good' found — Triggering Python logic and sending message to IoT Edge.")
            send_direct_method("good")
    except Exception as e:

        logging.error(f"Error reading blob '{name}': {e}")
