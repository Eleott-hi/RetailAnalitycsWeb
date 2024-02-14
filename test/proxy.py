from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI()

PROXY_URL = 'https://jsonplaceholder.typicode.com/posts/1'


@app.get("/proxy")
async def proxy():
    async with httpx.AsyncClient() as client:
        response = await client.get(PROXY_URL)
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code, detail="Proxy error")
        return response.json()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("proxy:app", host="test_fastapi", port=8000, reload=True)
