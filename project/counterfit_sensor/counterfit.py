from counterfit_connection import CounterFitConnection
CounterFitConnection.init('127.0.0.1', 5000)    

import io
import requests
import time
import json

from counterfit_shims_picamera import PiCamera
from counterfit_shims_rpi_vl53l0x.vl53l0x import VL53L0X
from counterfit_shims_grove.grove_led import GroveLed

import subprocess
import keyboard

#URL : http://127.0.0.1:5000/


#Setting up Camera
camera = PiCamera()
camera.resolution = (640, 480)
camera.rotation = 0

#Setting up proximity sensor
distance_sensor = VL53L0X()
distance_sensor.begin()

#Setting up led
led = GroveLed(29)

while True:

    distance_sensor.wait_ready()
    print("=================================")
    print(f'Distance = {distance_sensor.get_distance()} mm')
    print("=================================\n")

    #In certain distance
    if distance_sensor.get_distance() <= 20:

        #Take picture
        image = io.BytesIO()
        camera.capture(image, 'jpeg')
        image.seek(0)

        with open('Your directory of image for writing/image.jpg', 'wb') as image_file:
            image_file.write(image.read())
        
        time.sleep(2)
        print("Image captured\n")
        time.sleep(2)
        
        subprocess.run(["Your python directory", "Your local sender directory"])
        print("Image has been classified by AI module and the result is written to results.json. results.json sent")
        time.sleep(10)

        print("Waiting for input key to continue...")
        input()
        print("You pressed a key. Script continues...\n")
        time.sleep(2)

        with open("ledsignal.json", "r") as file:
            data = json.load(file)
        led_status = data.get("led")

        if (led_status == "on"):
            led.on()
            print("LED turned on\n")
        else:
            led.off()
            print("LED turned off\n")

        print("Waiting for input key to restart the loop...")
        input()
        print("You pressed a key. Script continues...\n")

