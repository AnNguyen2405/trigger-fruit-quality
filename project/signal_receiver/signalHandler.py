from azure.iot.device import IoTHubModuleClient, MethodResponse
import time
import logging
import json

logging.basicConfig(level=logging.INFO)
logging.info("         Starting module...         ")
signal = False

def handle_method(method_request):
    global signal
    print(f"         Received direct method: {method_request.name}         ")
    logging.info(f"         Received method: {method_request.name}         ")
    print(f"         Payload: {method_request.payload}         ")
    logging.info(f"         Payload: {method_request.payload}         \n")

    if method_request.name == "bad":
        print("Taking action for 'bad' method...")
        logging.info(f"         Taking action for 'bad' method...         ")
        signal = True
        led_state = "on"
        logging.info(f"         Action for 'bad' taken         \n")
        status = 200
        payload = {"result": "bad result received"}
    else:
        status = 404
        logging.info(f"         Taking action for other method...         ")
        signal = False
        led_state = "off"
        logging.info(f"         Action for 'good' taken         ")
        payload = {"error": "Unknown method"}
    
    try:
        with open("Your signal json directory", "w") as f:
            json.dump({"led": led_state}, f, indent=2)
        logging.info(f"Wrote LED state to file: {led_state}")
    except Exception as e:
        logging.error(f"Could not write to LED file: {e}")

    response = MethodResponse.create_from_method_request(method_request, status, payload)
    module_client.send_method_response(response)

module_client = IoTHubModuleClient.create_from_edge_environment()
module_client.connect()
module_client.on_method_request_received = handle_method

print("Listening for direct methods on module...")

while True:
    time.sleep(10)
