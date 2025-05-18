from azure.iot.hub import IoTHubRegistryManager
import json

# IoT Hub connection string (owner policy)
CONNECTION_STRING = "HostName=fruit.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=gZbnAEQPW/kPorMBITjERyPfuQQ4OF3fjAIoTNb6+V8="
DEVICE_ID = "fruit-quality-detector-edge"

def send_test_signal(signal_type="bad"):
    manager = IoTHubRegistryManager(CONNECTION_STRING)
    payload = json.dumps({"signal": signal_type})
    
    print(f"📤 Sending C2D message to device {DEVICE_ID}: {payload}")
    manager.send_c2d_message(DEVICE_ID, payload)
    print("✅ Message sent")

if __name__ == "__main__":
    # Choose "bad" or "good"
    send_test_signal("bad")
