import httpx
import asyncio
import time

async def fetch_user(id):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://jsonplaceholder.typicode.com/users/{id}")
        print(response.json()['name'])

start = time.time()
asyncio.run(fetch_user(1))
asyncio.run(fetch_user(2))
asyncio.run(fetch_user(3))
asyncio.run(fetch_user(4))
asyncio.run(fetch_user(5))
end = time.time()
print(f"Time taken: {end - start:.2f} seconds")

async def fetch_multiple():
    async with httpx.AsyncClient() as client:
        task = [
            client.get(f"https://jsonplaceholder.typicode.com/users/{i}")
            for i in range(1,6)
        ]

        responses = await asyncio.gather(*task)

        for response in responses:
            data = response.json()
            print(f"{data['name']} - {data['address']['city']}")

start = time.time()
asyncio.run(fetch_multiple())
end = time.time()
print(f"Time taken: {end - start:.2f} seconds")