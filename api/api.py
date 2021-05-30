import flask
from shapely.geometry import Point, Polygon, shape, box
from flask import request, jsonify
from flask_cors import CORS
from sklearn.cluster import KMeans
import numpy as np
import logging
from forests import forests_get, forests_full, shapes_get
from processos import processos_get, processos_full, filter_in_forest

logging.basicConfig(level=logging.DEBUG)

app = flask.Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config["DEBUG"] = True
app.config['CORS_HEADERS'] = 'Content-Type'

forests = forests_full()
shapes, forests_index_by_shapes_index = shapes_get()
processos = processos_full()
processos = filter_in_forest(shapes, forests, forests_index_by_shapes_index)


@app.route('/pins', methods=['GET'])
def point_get():
    result = []
    try:
        bounds = request.args.get('bounds')
        bounds = [float(c) for c in bounds.split(',')]
        bounds = box(bounds[0], bounds[1], bounds[2], bounds[3])
        forests = forests_get(bounds)
        ps = processos_get(processos, bounds)
        for forest in forests:
            result.append(
                {
                    "name": forest["name"],
                    "text": forest.get("label", forest["name"]),
                    "color": "Green",
                    "title": forest.get("title", forest["name"]),
                    "description": forest.get("description", "\n".join(forest.get("processos", {}))),
                    "geos": forest.get("geos")

                }
            )
        for processo in ps:
            result.append(
                {
                    "name": processo.get("name", processo["nrProcesso"]),
                    "text": processo.get("label", processo["nrProcesso"]),
                    "color": "Red",
                    "title": processo.get("title", processo["nrProcesso"]),
                    "description": processo.get("description", "\n".join(address["name"] for address in forest.get("address", []))),
                    "geos": processo.get("geos")
                }
            )

    except Exception as ex:
        result = ex

    return jsonify(result)


if __name__ == '__main__':
    app.run()
