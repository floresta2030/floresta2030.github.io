import zipfile
import uuid
from shapely.geometry import Point, shape
import os
import csv
import json
from sklearn.cluster import KMeans
import numpy as np
import logging
from data.utils import slugify, check_points_in_polygon

logging.basicConfig(level=logging.DEBUG)

base_dir = os.path.dirname(__file__)


forests = []
#forests_by_id = {}
#forests_np_by_id = {}
#forests_point_by_id = {}
#forests_shapes = []
#forests_index_by_shapes_index = []
#forests_distinct_points = {}

if not os.path.exists(f"{base_dir}/data/polygons"):
    with zipfile.ZipFile(f"{base_dir}/data/florestas-polygons.zip", 'r') as zip_ref:
        zip_ref.extractall(f"{base_dir}/data/")


def get_geos_and_jsons(forest):
    file_name = slugify(forest)
    file_name = f"{base_dir}/data/polygons/{file_name}.json"
    result = []
    if os.path.exists(file_name):
        with open(file_name, encoding="utf-8") as json_file:
            data = json.load(json_file)
            if len(data) > 0:
                for geo_data in data:
                    geojson = geo_data.get("geojson", {})
                    #geo_array = geojson.get("coordinates", [])
                    geo = {
                        "json": json.dumps(geojson),
                        "lat": float(geo_data["lat"]),
                        "lng": float(geo_data["lon"])
                    }
                    result.append({"geo": geo, "json": geojson})
    return result


file_name = f'{base_dir}/data/sirenejud.csv'
with open(file_name, newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    i = 0
    id = 1
    for row in reader:
        if i > 0:
            name = row[1]
            orgao = (row[3] or "").upper()
            geos_and_jsons = get_geos_and_jsons(name)
            if geos_and_jsons and len(geos_and_jsons) > 0:
                forest = {
                    "id": id,
                    "name": row[1],
                    "orgao": orgao,
                    "geos": [geos_and_jsons["geo"] for geos_and_jsons in geos_and_jsons],
                    "processos": [],
                    "nps": [
                        [
                            geo_and_json["geo"]["lat"], geo_and_json["geo"]["lng"]
                        ] for geo_and_json in geos_and_jsons
                    ],
                    "points": [
                        Point(
                            geo_and_json["geo"]["lat"], geo_and_json["geo"]["lng"]
                        ) for geo_and_json in geos_and_jsons
                    ],
                    "shapes": [
                        shape(geo_and_json["json"]) for geo_and_json in geos_and_jsons if len(geo_and_json["json"]) > 0
                    ]
                }
                forests.append(forest)
                id = id + 1        
        i = i+1


def forests_full():
    return forests


def forests_get(bounds):
    result = [
        forest for forest in forests
        if check_points_in_polygon(forest["points"], bounds)
    ]
    if len(result) > 30:
        forest_by_np = []
        nps = []
        i = 0
        for forest in result:
            for f_np in forest["nps"]:
                nps.append(f_np)
                forest_by_np.append(forest)
                i = i + 1
            
        X = np.array(nps)
        kmeans = KMeans(n_clusters=30, random_state=0).fit(X)
        labels = {}
        for label in kmeans.labels_:
            count = labels.get(label, 0)
            labels[label] = count + 1
        result = [
            {
                "name": str(uuid.uuid4()),
                "label": str(int(labels[label])),
                "geos": [{
                    "lat": float(kmeans.cluster_centers_[label][0]),
                    "lng": float(kmeans.cluster_centers_[label][1])
                }],
                "title": "Florestas " + str(int(labels[label])),
                "description": ""
            } for label in labels.keys()
        ]
    return result
