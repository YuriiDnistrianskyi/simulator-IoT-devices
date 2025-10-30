import asyncio
import aiohttp
import random
import json
from datetime import datetime

with open("config.json", "r") as file:
    CONFIG = json.load(file)

SERVER_URL = CONFIG["server_url"]
LOCATION_LIST = {}

for sensor in CONFIG["sensors"]:
    LOCATION_LIST[sensor["type"]] = sensor["location"]

semaphore = asyncio.Semaphore(CONFIG["number_of_semaphores"])

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


async def send_data(session, sensor_type, interval_ms):
    while True:
        await asyncio.sleep(interval_ms / 1000)
        payload = generate_sensor_data(sensor_type)
        async with semaphore:
            try:
                async with session.post(SERVER_URL, json=payload) as response:
                    status = response.status
                    print(status)
            except Exception as ex:
                print(f"| {sensor_type} | Error: {ex}")


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for sensor in CONFIG["sensors"]:
            task = asyncio.create_task(send_data(session, sensor["type"], sensor["interval_ms"]))
            tasks.append(task)

        await asyncio.gather(*tasks)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Emulator stopped")
