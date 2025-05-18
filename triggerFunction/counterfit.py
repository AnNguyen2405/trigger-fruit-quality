from counterfit_connection import CounterFitConnection
CounterFitConnection.init('127.0.0.1', 5000)    

import io
import requests
from counterfit_shims_picamera import PiCamera

import time
from counterfit_shims_rpi_vl53l0x.vl53l0x import VL53L0X

import subprocess

#URL : http://127.0.0.1:5000/


#Setting up Camera
camera = PiCamera()
camera.resolution = (640, 480)
camera.rotation = 0

image = io.BytesIO()
camera.capture(image, 'jpeg')
image.seek(0)

#Setting up proximity sensor
distance_sensor = VL53L0X()
distance_sensor.begin()

while True:

    distance_sensor.wait_ready()
    print("=================================")
    print(f'Distance = {distance_sensor.get_distance()} mm')
    print("=================================\n")
    time.sleep(1)

    if distance_sensor.get_distance() <= 20:
        with open('//home//annguyen//Desktop//localTester//image.jpg', 'wb') as image_file:
            image_file.write(image.read())
        time.sleep(20)
        subprocess.run(["/home/annguyen/Desktop/localTester/.venv/bin/python", "/home/annguyen/Desktop/localTester/test.py"])
        time.sleep(10)
        
    #     prediction_url = 'https://southeastasia.api.cognitive.microsoft.com/customvision/v3.0/Prediction/8d7ebd96-12c6-4df6-80d1-5b448ea5288d/classify/iterations/Iteration2/image'
    #     headers = {
    #         'Content-Type' : 'application/octet-stream',
    #         'Prediction-Key': '01f0cb2c62ae44e199eab3eca0ec0e52'
    #     }

    #     image.seek(0)
    #     response = requests.post(prediction_url, headers=headers, data=image)

    #     results = response.json()

    #     for prediction in results['predictions']:
    #         print(f'{prediction["tagName"]}:\t{prediction["probability"] * 100:.2f}%')
        
    #     print("=================================\n")
    #     time.sleep(10)

#prediction_url = 'https://southeastasia.api.cognitive.microsoft.com/customvision/v3.0/Prediction/8d7ebd96-12c6-4df6-80d1-5b448ea5288d/classify/iterations/Iteration2/image'
#prediction_key = '01f0cb2c62ae44e199eab3eca0ec0e52'

