import requests
import random
import time
import json
import threading #
from datetime import datetime

with open("config.json", "r") as file:
    CONFIG = json.load(file)

SERVER_URL = CONFIG["server_url"]
LOCATION_LIST = {}

for sensor in CONFIG["sensors"]:
    LOCATION_LIST[sensor["type"]] = sensor["location"]

# print(LOCATION_LIST)

def generate_sensor_data(sensor_type):
    if sensor_type == "temperature":
        value = round(random.uniform(15, 30), 2)
    elif sensor_type == "humidity":
        value = round(random.uniform(40, 80), 2)
    elif sensor_type == "pressure":
        value = round(random.uniform(900, 1100), 2)
    else:
        value = None
        print(f"Not understood sensor type: {sensor_type}")

    data = {
        "sensor_type": sensor_type,
        "value": value,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "location": LOCATION_LIST[sensor_type]
    }

    return data

def simulate_iot_devices():
    pass

if __name__ == "__main__":
    print("End")


#
# # === Функція генерації даних ===
# def generate_sensor_data(sensor_type):
#     """Генерує випадкове значення для конкретного сенсора"""
#     if sensor_type == "temperature":
#         value = round(random.uniform(15, 30), 2)
#     elif sensor_type == "humidity":
#         value = round(random.uniform(40, 90), 2)
#     elif sensor_type == "light":
#         value = round(random.uniform(200, 800), 2)
#     else:
#         value = 0
#
#     data = {
#         "sensor_type": sensor_type,
#         "value": value,
#         "timestamp": datetime.utcnow().isoformat(),
#         "location": LOCATION
#     }
#     return data
#
# # === Функція відправки даних ===
# def send_data(sensor_type, interval_ms):
#     """Надсилає дані з певною частотою"""
#     while True:
#         payload = generate_sensor_data(sensor_type)
#         try:
#             response = requests.post(SERVER_URL, json=payload, timeout=2)
#             print(f"[{sensor_type}] Sent → {response.status_code} | {payload}")
#         except Exception as e:
#             print(f"[{sensor_type}] Error sending data:", e)
#         time.sleep(interval_ms / 1000.0)
#
# # === Запуск потоків для кожного сенсора ===
# def main():
#     threads = []
#     for sensor in CONFIG["sensors"]:
#         t = threading.Thread(
#             target=send_data,
#             args=(sensor["type"], sensor["interval_ms"]),
#             daemon=True
#         )
#         threads.append(t)
#         t.start()
#
#     print("IoT Emulator started. Press Ctrl+C to stop.")
#     while True:
#         time.sleep(1)
#
# if __name__ == "__main__":
#     main()
