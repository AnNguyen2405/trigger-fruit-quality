print("🚀 signalResponder module started")
import json
import time
import requests
import asyncio
from azure.iot.device.aio import IoTHubModuleClient


async def handle_input_message(message):
    try:
        payload_str = message.data.decode('utf-8') if isinstance(message.data, bytes) else message.data
        print(f"📥 Received message on: {message.input_name}")
        print(f"📦 Payload: {payload_str}")

        data = json.loads(payload_str)

        if data.get("signal") == "bad":
            print("🚨 Triggering Counterfit GPIO: ON")
            requests.post(
                "http://localhost:5000/api/gpio/digitalwrite",
                json={"pin": 4, "value": 1}
            )
        elif data.get("signal") == "good":
            print("✅ Triggering Counterfit GPIO: OFF")
            requests.post(
                "http://localhost:5000/api/gpio/digitalwrite",
                json={"pin": 4, "value": 0}
            )
        else:
            print("⚠️ Unknown signal value")
    except Exception as e:
        print(f"❌ Error processing message: {e}")


async def main():
    print("🔌 Initializing IoT Edge Module Client...")
    client = IoTHubModuleClient.create_from_edge_environment()

    time.sleep(10)  # Optional: wait for Edge runtime to stabilize
    await client.connect()
    print("✅ Connected to IoT Edge runtime.")

    # Handle all inputs generically
    async def generic_handler(message):
        await handle_input_message(message)

    client.on_message_received = generic_handler

    print("👂 Module is listening for messages on all inputs...")

    # Keep the module alive
    while True:
        await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())
