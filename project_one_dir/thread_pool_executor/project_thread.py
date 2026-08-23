import random
import requests
import time

from concurrent.futures import ThreadPoolExecutor
from project_one_dir.constants import POKEMON_IDS, POKEMON_API


def fetch_pokemon(pokemon_id):
    pokemon_api_id = POKEMON_API + f"/pokemon/{pokemon_id}"

    try:
        response = requests.get(
            pokemon_api_id,
            timeout=5,
        )
        # print(f"Fetched data for Pokemon ID {pokemon_id}: {response.json()['name']}")
        return response.json()
    except Exception as e:
        print(f"Error fetching data for Pokemon ID {pokemon_id}: {e}")
        return None


def main():
    num_pokemon_ids = 5_000
    for _ in range(num_pokemon_ids):
        pokemon_id = random.randint(1, 1_000)
        POKEMON_IDS.append(pokemon_id)

    start_time = time.time()
    with ThreadPoolExecutor(max_workers=25) as executor:
        results = list(executor.map(fetch_pokemon, POKEMON_IDS))
    # for pokemon_id in POKEMON_IDS:
    #     pokemon_data = fetch_pokemon(pokemon_id)
    #     print(f"Fetched data for Pokemon ID {pokemon_id}: {pokemon_data['name']}")

    end_time = time.time()
    print(f"Total time taken to fetch data for {num_pokemon_ids} Pokemon IDs: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()