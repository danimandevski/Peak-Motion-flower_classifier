import json

txt_file_path = "cleaned_plants.txt"
json_file_path = "plantnet300K_species_id_2_name.json"
output_matches_path = "matching_species.txt"

with open(txt_file_path, "r", encoding="utf-8") as file:
    txt_species = {line.strip() for line in file if line.strip()}

with open(json_file_path, "r", encoding="utf-8") as file:
    plantnet_species = set(json.load(file).values())

matches = sorted(txt_species.intersection(plantnet_species))

with open(output_matches_path, "w", encoding="utf-8") as file:
    file.write("\n".join(matches))

print(f"Found {len(matches)} matching species. Saved to {output_matches_path}.")
