import asyncio
import boto3
import random
import json
from datetime import datetime

with open("config.json", "r") as file:
    CONFIG = json.load(file)

sqs = boto3.client("sqs", region_name=CONFIG["region"])
SQS_URL = CONFIG["sqs_url"]
LOCATION_LIST = {}
DEVICE_ID = {}

for sensor in CONFIG["sensors"]:
    LOCATION_LIST[sensor["type"]] = sensor["location"]
    DEVICE_ID[sensor["type"]] = sensor["device_id"]


semaphore = asyncio.Semaphore(CONFIG["number_of_semaphores"])

def generate_sensor_data(sensor_type):
    if sensor_type == "temperature":
        value = round(random.uniform(15, 30), 2)
    elif sensor_type == "humidity":
        value = round(random.uniform(40, 80), 2)
    elif sensor_type == "pressure":
        value = round(random.uniform(900, 1100), 2)
    elif sensor_type == "error_sensor_type":
        value = 0
    else:
        value = None
        print(f"Not understood sensor type: {sensor_type}")

    data = {
        "device_id": DEVICE_ID[sensor_type],
        "sensor_type": sensor_type,
        "value": value,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "location_lat": LOCATION_LIST[sensor_type]["lat"],
        "location_lon": LOCATION_LIST[sensor_type]["lon"]
    }

    return data


async def send_data(sensor_type, interval_ms):
    while True:
        await asyncio.sleep(interval_ms / 1000)
        data = generate_sensor_data(sensor_type)
        async with semaphore:
            try:
                loop = asyncio.get_running_loop()
                await loop.run_in_executor(
                    None,
                    lambda: sqs.send_message(
                        QueueUrl=SQS_URL,
                        MessageBody=json.dumps(data),
                    )
                )
            except Exception as ex:
                print(f"| {sensor_type} | Error: {ex}")


async def main():
    tasks = []
    for sensor in CONFIG["sensors"]:
        task = asyncio.create_task(send_data(sensor["type"], sensor["interval_ms"]))
        tasks.append(task)
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Emulator stopped")
