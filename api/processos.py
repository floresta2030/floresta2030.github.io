import uuid
from shapely.geometry import Point, Polygon, shape, box
import os
import json
from flask import request, jsonify
from flask_cors import CORS
from sklearn.cluster import KMeans
import numpy as np
import logging
from data.utils import check_point_in_polygon

logging.basicConfig(level=logging.DEBUG)

base_dir = os.path.dirname(__file__)


processos_by_nr = {}
processos_by_index = {}
processos_nps = []
processos_points = []
processos_points_to_shape_compare = []
processos_index_by_nr = {}

processos = []


def processos_full():
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
                processos_by_nr[processo["nrProcesso"]] = processo
                processos_index_by_nr[processo["nrProcesso"]] = processos_index_by_nr.get(
                    processo["nrProcesso"], [])
                for address in processo["address"]:
                    if address["lat"]:
                        i_np = len(processos_nps)
                        lat = float(address["lat"])
                        lng = float(address["lng"])
                        processos_nps.append([lat, lng])
                        processos_by_index[i_np] = processo
                        processos_points.append(
                            Point(lat, lng)
                        )
                        processos_points_to_shape_compare.append(
                            Point(lng, lat)
                        )
                        processos_index_by_nr[processo["nrProcesso"]].append(
                            i_np)
    return processos


def filter_in_forest(forests_polygons, forests, forests_index_by_shapes_index):
    result = []
    cache = {}
    cache_forest = {}
    for i, point in enumerate(processos_points):
        for j, polygons in enumerate(forests_polygons):
            if check_point_in_polygon(point, polygons):
                processo = processos_by_index[i]
                if not cache.get(processo["nrProcesso"], False):
                    result.append(
                        processo
                    )
                    cache[processo["nrProcesso"]] = True
                forest_index = forests_index_by_shapes_index[j]
                if not cache_forest.get(forest_index, {}).get(processo["nrProcesso"], False):
                    forests[forest_index]["processos"].append(
                        processo
                    )
                    tmp = cache_forest.get(forest_index, {})
                    tmp[processo["nrProcesso"]] = True
                    cache_forest[forest_index] = tmp
    return result


def check_points_in_polygon(indexes, bounds):
    for index in indexes:
        if check_point_in_polygon(processos_points[index], bounds):
            return True
    return False


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
            "title": processo["nrProcesso"],
            "description": processo.get("description", "\n".join(address["name"] for address in processo.get("address", []))),
        } for processo in processos if check_points_in_polygon(processos_index_by_nr[processo["nrProcesso"]], bounds)
    ]
    if len(result) > 30:
        X = np.array(processos_nps)
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
                "title": "Processos " + str(int(counts[label])),
                "description": ""
            } for label in unique
        ]
    return result
