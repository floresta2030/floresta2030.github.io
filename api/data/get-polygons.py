import csv
import unicodedata
import re
import json
import requests
from utils import slugify

cache = {}
ammount = {"Found": 0, "NotFound": 0, "Duplicated": 0}


def get_polygon(floresta):
    if not floresta in cache:
        cache[floresta] = True
        response = requests.get(
            f"https://nominatim.openstreetmap.org/search.php?q={floresta}&polygon_geojson=1&format=json")
        response.raise_for_status()
        slug = slugify(floresta)
        data = response.json()
        if len(data) > 0:
            with open(f"polygons/{slug}.json", "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False)
            ammount["Found"] = ammount["Found"] + 1
            return True
        else:
            print(f"Not found: {slug}, {floresta}")
        ammount["NotFound"] = ammount["NotFound"] + 1
        return False
    ammount["Duplicated"] = ammount["Duplicated"] + 1
    return False


with open('sirenejud.csv', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    i = 0
    for row in reader:
        if i > 0:
            floresta = row[1]
            print(floresta)

            get_polygon(floresta)
        i = i + 1
print(ammount)
