import requests

def get_all_species(max_limit = 500, place_id=8241, iconic_taxa="Plantae"):
    url = "https://api.inaturalist.org/v1/observations/species_counts"
    species = []
    page = 1
    per_page = max_limit
    while True:
        params = {
            "place_id": place_id,
            "iconic_taxa": iconic_taxa,
            "per_page": per_page,
            "page": page
        }

        response = requests.get(url, params=params)
        data = response.json()

        if "results" not in data or not data["results"]:
            break

        species.extend([result["taxon"]["name"] for result in data["results"]])

        print(f"Fetched {len(species)} species so far...")

        page += 1

    return species

def main():
    species_list = get_all_species()
    print(f"Total species found: {len(species_list)}")

    with open("all_plant_species.txt", "w", encoding="utf-8") as file:
        for name in species_list:
            file.write(name + "\n")
        
if __name__ == '__main__':
    main()