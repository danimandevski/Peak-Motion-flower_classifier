import aiohttp
import asyncio
import os
import json
from aiofiles import open as aio_open
from tqdm import tqdm

species_file = "all_plant_species.txt"

output_dir = "inat_images"
os.makedirs(output_dir, exist_ok=True)

async def fetch_image_urls(session, species_name, max_images=500):
    """Fetch image URLs for a given species from iNaturalist API."""
    url = f"https://api.inaturalist.org/v1/observations?taxon_name={species_name.replace(' ', '%20')}&per_page={max_images}&order=desc&order_by=created_at"
    try:
        async with session.get(url) as response:
            data = await response.json()
            return [obs["photos"][0]["url"].replace("square", "original") for obs in data["results"] if "photos" in obs and obs["photos"]]
    except:
        return []

async def download_image(session, url, species_folder, index):
    """Download an image and save it to a folder."""
    filename = f"{species_folder}/{index}.jpg"
    try:
        async with session.get(url) as response:
            if response.status == 200:
                async with aio_open(filename, "wb") as file:
                    await file.write(await response.read())
    except:
        pass

async def main():
    async with aiohttp.ClientSession() as session:
        # Read species list
        with open(species_file, "r", encoding="utf-8") as file:
            species_list = [line.strip() for line in file if line.strip()]

        tasks = []
        for species in tqdm(species_list[:5], desc="Fetching URLs"):
            species_folder = os.path.join(output_dir, species.replace(" ", "_"))
            os.makedirs(species_folder, exist_ok=True)

            urls = await fetch_image_urls(session, species)
            for i, url in enumerate(urls):
                tasks.append(download_image(session, url, species_folder, i))

        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
