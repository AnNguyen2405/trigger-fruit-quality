# Trigger-Fruit-Quality

This is an IoT project developed by a group of Vietnamese-German students majoring in Computer Science and Engineering (CSE).

The project aims to implement Azure in an automatic fruit quality detection prototype. We used a virtual Ubuntu 24.02 environment as an IoT Edge device.
---
Disclaimer: this repo is for storing our work only, no specific contribution can be found here.
---

## 📁 Project Structure

The `project/` folder contains the complete implementation, including the AI model, local sensors, Azure integration, and communication modules:

- **`banana-fruit/`**  
  Contains the AI model and its Docker components. This folder acts as a module deployed on the edge device.

- **`sensor/`**  
  Includes scripts for the counterfeit proximity sensor, camera, and LED logic used in fruit detection.

- **`local_sender/`**  
  Provides scripts for sending local testing results from the edge device to Azure Blob Storage.

- **`trigger_function/`**  
  Contains logic for monitoring Azure Blob Storage and sending messages back to the IoT Edge device using Azure IoT Hub Direct Methods.

- **`signal_receiver/`**  
  Manages incoming signals from Azure. This folder includes the module responsible for responding to cloud messages on the edge device.

---

## 🌐 Technologies Used
- Azure IoT Edge
- Azure Blob Storage
- Azure Functions
- Python, Docker
- Ubuntu 24.02 (Virtual Machine)
