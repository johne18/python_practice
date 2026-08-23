import asyncio
import aiohttp
import random
import time

from project_one_dir.constants import POKEMON_IDS, POKEMON_API


async def fetch_pokemon(session, semaphore, pokemon_id):
    pokemon_api_id = POKEMON_API + f"/pokemon/{pokemon_id}"

    async with semaphore:
        try:
            async with session.get(pokemon_api_id, timeout=5) as response:
                data = await response.json()
                # print(f"Fetched data for Pokemon ID {pokemon_id}: {data['name']}")
                return data
        except Exception as e:
            print(f"Error fetching data for Pokemon ID {pokemon_id}: {e}")
            return None


async def main():
    num_pokemon_ids = 5_000
    for _ in range(num_pokemon_ids):
        pokemon_id = random.randint(1, 1_000)
        POKEMON_IDS.append(pokemon_id)

    semaphore = asyncio.Semaphore(25)  # Limit the number of concurrent requests
    start_time = time.time()

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_pokemon(session, semaphore, pokemon_id) for pokemon_id in POKEMON_IDS]
        # pokemon_data_list = await asyncio.gather(*tasks)
        await asyncio.gather(*tasks)

    end_time = time.time()
    print(f"Total time taken to fetch data for {num_pokemon_ids} Pokemon IDs: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())