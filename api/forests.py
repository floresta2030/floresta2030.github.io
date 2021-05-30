import zipfile
import uuid
from shapely.geometry import Point, shape
import os
import csv
import json
from sklearn.cluster import KMeans
import numpy as np
import logging
from data.utils import slugify, check_point_in_polygon

logging.basicConfig(level=logging.DEBUG)

base_dir = os.path.dirname(__file__)


forests = []
forests_by_name = {}
forests_np_by_name = {}
forests_point_by_name = {}
forests_shapes = []
forests_index_by_shapes_index = []
forests_distinct_points = {}


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
                    if forests_distinct_points.get(geo_data["lat"], {}).get(geo_data["lon"], True):
                        geojson = geo_data.get("geojson", {})
                        geo = {
                            "json": json.dumps(geojson),
                            "lat": float(geo_data["lat"]),
                            "lng": float(geo_data["lon"])
                        }
                        dis = forests_distinct_points.get(geo_data["lat"], {})
                        dis[geo_data["lon"]] = False
                        forests_distinct_points[geo_data["lat"]] = dis
                        result.append({"geo": geo, "json": geojson})
    return result


file_name = f'{base_dir}/data/sirenejud.csv'
with open(file_name, newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    i = 0
    for row in reader:
        if i > 0:
            name = row[1]
            orgao = (row[3] or "").upper()
            geos_and_jsons = get_geos_and_jsons(name)
            if geos_and_jsons and len(geos_and_jsons) > 1:
                forest = {
                    "name": row[1],
                    "orgao": orgao,
                    "geos": [geos_and_jsons["geo"] for geos_and_jsons in geos_and_jsons],
                    "processos": []
                }
                index = len(forests)
                forests.append(forest)
                forests_by_name[name] = forest
                forests_np_by_name[name] = [
                    forest["geos"][0]["lat"], forest["geos"][0]["lng"]]
                forests_point_by_name[name] = Point(
                    forest["geos"][0]["lat"], forest["geos"][0]["lng"]
                )
                for geo_and_json in geos_and_jsons:
                    obj = geo_and_json["json"]
                    if len(obj) > 0:
                        forests_shapes.append(
                            shape(obj)
                        )
                        forests_index_by_shapes_index.append(index)

        i = i+1


def forests_full():
    return forests


def shapes_get():
    return forests_shapes, forests_index_by_shapes_index


def forests_get(bounds):
    result = [
        forest for forest in forests
        #if forest["name"] == "PARQUE ESTADUAL DA SERRA DO MAR"
        if check_point_in_polygon(
            forests_point_by_name[forest["name"]], bounds)
    ]
    if len(result) > 30:
        X = np.array(
            [
                forests_np_by_name[forest["name"]] for forest in result
            ]
        )
        kmeans = KMeans(n_clusters=30, random_state=0).fit(X)
        unique, counts = np.unique(kmeans.labels_, return_counts=True)
        result = [
            {
                "name": str(uuid.uuid4()),
                "label": str(int(counts[label])),
                "geos": [{
                    "lat": float(kmeans.cluster_centers_[label][0]),
                    "lng": float(kmeans.cluster_centers_[label][1])
                }],
                "title": "Florestas " + str(int(counts[label])),
                "description": "Processos: " + str(sum(
                    [
                        len(forest["processos"])
                        for i, forest in enumerate(result) if kmeans.labels_[i] == label
                    ]
                ))
            } for label in unique
        ]
    return result
