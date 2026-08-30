import asyncio
import aiohttp
import random
import time

from aiolimiter import AsyncLimiter
from project_one_dir.constants import POKEMON_IDS, POKEMON_API


async def fetch_pokemon(session, semaphore, rate_limiter, pokemon_id):
    pokemon_api_id = POKEMON_API + f"/pokemon/{pokemon_id}"

    # Can add a retry
    async with semaphore:
        async with rate_limiter:
            try:
                async with session.get(pokemon_api_id, timeout=5) as response:
                    data = await response.json()
                    # print(f"Fetched data for Pokemon ID {pokemon_id}: {data['name']}")
                    return data
            except Exception as e:
                print(f"Error fetching data for Pokemon ID {pokemon_id}: {e}")
                # if attempt == max_retries:
                #     return None
                # await asyncio.sleep(1)  # Wait for a second before retrying


async def main():
    num_pokemon_ids = 250
    for _ in range(num_pokemon_ids):
        pokemon_id = random.randint(1, 1_000)
        POKEMON_IDS.append(pokemon_id)

    semaphore = asyncio.Semaphore(25)  # Limit the number of concurrent requests
    rate_limiter = AsyncLimiter(100, 3) # Limit to 100 requests every n seconds
    start_time = time.time()

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_pokemon(session, semaphore, rate_limiter, pokemon_id) for pokemon_id in POKEMON_IDS]
        pokemon_data_list = await asyncio.gather(*tasks)

    end_time = time.time()
    print(f"Total time taken to fetch data for {num_pokemon_ids} Pokemon IDs: {end_time - start_time:.2f} seconds")

    print(f"First 10 fetched Pokemon data:")
    for pokemon in pokemon_data_list[:10]:
        print("="*80)
        print(pokemon["name"])
        print(pokemon["types"])
        print("="*80)


if __name__ == "__main__":
    asyncio.run(main())