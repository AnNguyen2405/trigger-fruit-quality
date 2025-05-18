import azure.functions as func
import logging
import json
from run_script import run_my_script

from azure.iot.hub import IoTHubRegistryManager
import os

# Replace with your IoT Hub details
IOTHUB_CONNECTION_STRING = "HostName=fruit.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=gZbnAEQPW/kPorMBITjERyPfuQQ4OF3fjAIoTNb6+V8="
DEVICE_ID = "fruit-quality-detector-edge"

def send_c2d_message(signal: str):
    manager = IoTHubRegistryManager(IOTHUB_CONNECTION_STRING)

    message = f'{{"signal": "{signal}"}}'

    print(f"Sending C2D message to {DEVICE_ID}: {message}")
    manager.send_c2d_message(DEVICE_ID, message)

app = func.FunctionApp()

@app.function_name(name="triggerFunction")
@app.blob_trigger(arg_name="inputBlob",
                  path="banana-result/{name}",
                  connection="AzureWebJobsStorage")
def blob_trigger_function(inputBlob: func.InputStream):
    name = inputBlob.name
    logging.info(f"Processing blob: {name}")

    try:
        data = json.loads(inputBlob.read().decode('utf-8'))
        if "bad" in json.dumps(data).lower():
            logging.info("'bad' found — triggering Python logic and sending message to IoT Edge.")
            run_my_script()
            send_c2d_message("bad")
        # elif "good" in json.dumps(data).lower():
        #     logging.info("'good' found — sending message to IoT Edge.")
        #     send_c2d_message("good")
        else:
            logging.info("No actionable signal found — nothing triggered.")
    except Exception as e:
        logging.error(f"Error reading blob '{name}': {e}")