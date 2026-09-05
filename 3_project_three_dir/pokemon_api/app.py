import aiohttp
import asyncio
import os
import psycopg2

from aiolimiter import AsyncLimiter
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List


app = FastAPI(title="Pokemon API")

DB_HOST = os.getenv("POSTGRES_DB_HOST", "postgres")
DB_NAME = os.getenv("POSTGRES_DB", "pokemon")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POKEMON_API = os.getenv("POKEMON_API_URL", "https://pokeapi.co/api/v2")

class PokemonPayload(BaseModel):
    id: int
    name: str
    height: int = 0
    weight: int = 0
    types: List[str] = []


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )


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
        "types": [item["type"]["name"] for item in data["types"]],
    }


@app.post("/pokemon")
async def save_pokemon(payload: PokemonPayload):
    conn = get_connection()
    cur = conn.cursor()
    # Perform an upsert
    cur.execute(
        """
        INSERT INTO pokemon (id, name, height, weight, types)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (id) DO UPDATE
        SET name = EXCLUDED.name,
            height = EXCLUDED.height,
            weight = EXCLUDED.weight,
            types = EXCLUDED.types
        """,
        (
            payload.id,
            payload.name,
            payload.height,
            payload.weight,
            payload.types,
        ),
    )
    conn.commit()
    cur.close()
    conn.close()

    return {
        "status": "saved",
        "id": payload.id,
        "name": payload.name,
    }


@app.get("/env")
def get_env_variable():
    return {
        "api_url":      os.getenv('POKEMON_API_URL'),
        "concurrency":  os.getenv('POKEMON_CONCURRENCY'),
        "rate_limit":   os.getenv('POKEMON_RATE_LIMIT'),
        "rate_seconds": os.getenv('POKEMON_RATE_SECONDS'),
        "timout":       os.getenv('POKEMON_TIMEOUT'),
    }



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("3_project_three_dir.pokemon_api.app:app", host="0.0.0.0", port=8000, reload=True)