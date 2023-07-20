import requests
email, password = "tmp123123@123.com", "123"
# print(requests.post("http://localhost:9090/register", data={"email": email, "password": password}))

import random


import asyncio
import aiohttp

async def send_request(session, url, data):
    async with session.post(url, json=data) as response:
        response_text = await response.text()
        print(f'Response from {url}: {response_text}')

import os

my_var = os.environ.get('USERNAME')
urls = []  # Replace with your list of URLs
for i in range(1000):
    email = f"abc@{str(my_var)}@" + str(i) + "@12.com"
    urls.append(["http://localhost:9090/register", {"email": email, "password": password}])

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i, url in enumerate(urls):
            print(url)
            tasks.append(asyncio.ensure_future(send_request(session, url[0], url[1])))
            if i % 50 == 0:  # Send 5 requests every second
                await asyncio.sleep(1)
        await asyncio.gather(*tasks)

asyncio.run(main())



# for i in range(5000):
#     email = f"abc{i}" + "@123.com"
#     username = f"abc{i}" + "@123.com"
#     print(requests.post("http://localhost:9090/register", data={"email": email, "password": password}).json())
    # print(requests.post("http://localhost:9090/login", data={"email": email, "password": password}).json())