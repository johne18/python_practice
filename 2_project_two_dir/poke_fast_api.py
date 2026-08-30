import aiohttp
import asyncio
import os

from aiolimiter import AsyncLimiter
from fastapi import FastAPI, HTTPException


app = FastAPI(title="Pokemon API")
POKEMON_API = os.getenv("POKEMON_API_URL", "https://pokeapi.co/api/v2")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/pokemon/{pokemon_id}")
async def get_pokemon_by_id(pokemon_id: int):
    if not 1 <= pokemon_id <= 1000:
        raise HTTPException(
            status_code=400,
            detail="Pokemon ID must be between 1 and 1000."
        )

    url = f"{POKEMON_API}/pokemon/{pokemon_id}"
    semaphore = asyncio.Semaphore(
        int(os.getenv("POKEMON_CONCURRENCY", "25"))
    ) # Limit to n number of concurrent requests

    rate_limiter = AsyncLimiter(
        int(os.getenv("POKEMON_RATE_LIMIT", "100")), 
        int(os.getenv("POKEMON_RATE_SECONDS", "3"))
    ) # Limit to 100 requests every 3 seconds

    timeout = int(os.getenv("POKEMON_TIMEOUT", "10"))

    async with semaphore:
        async with rate_limiter:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=timeout) as response:
                    if response.status == 404:
                        raise HTTPException(status_code=404, detail="Pokemon not found.")
                    response.raise_for_status()
                    data = await response.json()

    return {
        "id": data["id"],
        "name": data["name"],
        "height": data["height"],
        "weight": data["weight"],
        "base_experience": data["base_experience"],
        "types": [item["type"]["name"] for item in data["types"]],
        "sprite": data["sprites"]["front_default"],
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("2_project_two_dir.async.project_async:app", host="0.0.0.0", port=8000, reload=True)