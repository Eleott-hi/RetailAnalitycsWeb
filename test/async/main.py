import time
import requests
import asyncio
import aiohttp

N = 20
# URL = 'https://jsonplaceholder.typicode.com/posts/1'
URL = 'http://test_fastapi:8000/proxy'


async def fetch_async(session):
    async with session.get(URL) as response:
        return await response.text()


async def main_async():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_async(session) for _ in range(N)]
        start_time = time.time()
        results = await asyncio.gather(*tasks)
        end_time = time.time()
        for i, result in enumerate(results):
            print(i, result)

        print(len(results))
        return end_time - start_time


def main():
    start_time = time.time()
    for i in range(N):
        res = requests.get(URL).text
        print(i, res)

    end_time = time.time()
    return end_time - start_time


if __name__ == "__main__":
    sync_time = main()
    async_time = asyncio.run(main_async())
    print(f"Async time taken: {async_time} seconds")
    print(f"Sync time taken: {sync_time} seconds")
