import uuid
from shapely.geometry import Point, Polygon, shape, box
import os
import json
from flask import request, jsonify
from flask_cors import CORS
from sklearn.cluster import KMeans
import numpy as np
import logging
from data.utils import check_point_in_polygons, check_points_in_polygon

logging.basicConfig(level=logging.DEBUG)

base_dir = os.path.dirname(__file__)


def processos_full():
    processos = []
    cache = {}
    file_name = "processos"
    file_name = f"{base_dir}/data/{file_name}.json"
    if os.path.exists(file_name):
        with open(file_name, encoding="utf-8") as json_file:
            tmp = json.load(json_file)
            for processo in tmp:
                if not cache.get(processo["nrProcesso"], False):
                    processos.append(processo)
                    cache[processo["nrProcesso"]] = True
                processo["nps"] = []
                processo["points"] = []
                processo["points_to_shape"] = []
                for address in processo["address"]:
                    if address["lat"]:
                        lat = float(address["lat"])
                        lng = float(address["lng"])

                        processo["nps"].append([lat, lng])
                        processo["points"].append(
                            Point(lat, lng)
                        )
                        processo["points_to_shape"].append(
                            Point(lng, lat)
                        )
    return processos


def filter_in_forest(processos, forests):
    result = []
    cache = {}
    cache_forest = {}
    for processo in processos:
        points = []
        nps = []
        points_to_shape = []
        address = []
        for i, point in enumerate(processo["points_to_shape"]):
            found = False
            for forest in forests:
                if check_point_in_polygons(point, forest["shapes"]):
                    found = True
                    if not cache.get(processo["nrProcesso"], False):
                        result.append(
                            processo
                        )
                        cache[processo["nrProcesso"]] = True
                    if processo["nrProcesso"] == "0018492-45":
                        print(processo["nrProcesso"])
                        print(forest["name"])
                    # if not cache_forest.get(forest["id"], {}).get(processo["nrProcesso"], False):
                    forest["processos"].append(
                        processo
                    )
                    #   tmp = cache_forest.get(forest["id"], {})
                    #   tmp[processo["nrProcesso"]] = True
                    #   cache_forest[forest["id"]] = tmp
            if found:
                points.append(processo["points"][i])
                points_to_shape.append(processo["points_to_shape"][i])
                nps.append(processo["nps"][i])
                address.append(processo["address"][i])
        processo["points"] = points
        processo["points_to_shape"] = points_to_shape
        processo["nps"] = nps
        processo["address"] = address
    return result


def processos_get(processos, bounds):
    result = [
        {
            "nrProcesso": processo["nrProcesso"],
            "name": processo["nrProcesso"],
            "label": processo["nrProcesso"],
            "geos": [
                {
                    "lat": address["lat"],
                    "lng": address["lng"]
                } for address in processo.get("address", [])
            ],
            "nps": processo["nps"],
            "title": processo["nrProcesso"],
            "description": processo.get("description", "\n".join(address["name"] for address in processo.get("address", []))),
        } for processo in processos if check_points_in_polygon(processo["points"], bounds)
    ]
    if len(result) > 30:
        processo_by_np = []
        nps = []
        i = 0
        for processo in result:
            for f_np in processo["nps"]:
                nps.append(f_np)
                processo_by_np.append(processo)
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
                "title": "Processos " + str(int(labels[label])),
                "description": ""
            } for label in labels.keys()
        ]
    return result
