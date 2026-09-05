import os
import requests

API_URL = os.getenv("API_URL", "http://pokemon-fastapi")


def fetch_pokemon_from_api(pokemon_id: int):
    response = requests.get(f"{API_URL}/pokemon/{pokemon_id}", timeout=10)
    response.raise_for_status()
    return response.json()


def save_to_api(pokemon: dict):
    response = requests.post(
        f"{API_URL}/pokemon",
        json=pokemon,
        timeout=10,
    )
    response.raise_for_status()
    return response.json()
    

if __name__ == "__main__":
    pokemon_ids = [258, 69, 67, 420]
    for pokemon_id in pokemon_ids:
        pokemon = fetch_pokemon_from_api(pokemon_id)
        result = save_to_api(pokemon)
        print(f"Saved {pokemon_id}: {result}")