import requests
from datetime import datetime

# CONFIG
url = "http://localhost:80/image"
image_path = "Your directory of image for checking/image.jpg"

# SEND IMAGE
with open(image_path, "rb") as image:
    response = requests.post(
        url,
        headers={"Content-Type": "application/octet-stream"},
        data=image
    )

# PARSE RESULT
if response.status_code == 200:
    predictions = response.json().get("predictions", [])
    top = max(predictions, key=lambda x: x["probability"])
    wstring = f"Top tag: {top['tagName']} ({top['probability']:.2%})" + " " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(wstring)
else:
    print(f"Error: {response.status_code}, {response.text}")

import json

with open("results.json", "w") as f:
    json.dump(wstring, f, indent=2)


from azure.storage.blob import BlobServiceClient

# CONFIG
connection_string = "Your connection string"
container_name = "banana-result"
local_file_path = "results.json"
blob_name = "results.json"  # Path inside blob

# INIT CLIENT
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

# UPLOAD
with open(local_file_path, "rb") as data:
    blob_client.upload_blob(data, overwrite=True)

print("Upload complete.")