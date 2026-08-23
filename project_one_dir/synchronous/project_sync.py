import random
import requests
import time

from project_one_dir.constants import POKEMON_IDS, POKEMON_API


def fetch_pokemon(pokemon_id):
    pokemon_api_id = POKEMON_API + f"/pokemon/{pokemon_id}"
    response = requests.get(
        pokemon_api_id,
        timeout=5,
    )
    return response.json()


def main():
    num_pokemon_ids = 5_000
    for _ in range(num_pokemon_ids):
        pokemon_id = random.randint(1, 1_000)
        POKEMON_IDS.append(pokemon_id)

    start_time = time.time()
    for pokemon_id in POKEMON_IDS:
        pokemon_data = fetch_pokemon(pokemon_id)
        print(f"Fetched data for Pokemon ID {pokemon_id}: {pokemon_data['name']}")

    end_time = time.time()
    print(f"Total time taken to fetch data for {num_pokemon_ids} Pokemon IDs: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()