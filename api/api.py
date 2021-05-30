import flask
import sys
import traceback
from shapely.geometry import Point, Polygon, shape, box
from flask import request, jsonify
from flask_cors import CORS
from sklearn.cluster import KMeans
import numpy as np
import logging
from forests import forests_get, forests_full
from processos import processos_get, processos_full, filter_in_forest

logging.basicConfig(level=logging.DEBUG)

app = flask.Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config["DEBUG"] = True
app.config['CORS_HEADERS'] = 'Content-Type'

forests = forests_full()
processos = processos_full()
processos = filter_in_forest(processos, forests)


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
                    "description": 
                        forest.get(
                            "description",
                            "\n".join(
                                [processo["nrProcesso"] for processo in forest.get("processos", [])]
                            )
                        ),
                    "geos": forest.get("geos")

                }
            )
        for processo in ps:
            result.append(
                {
                    "name": processo["name"],
                    "text": processo["label"],
                    "color": "Red",
                    "title": processo["title"],
                    "description": processo.get("description", "\n".join([address["name"] for address in processo.get("address", [])])),
                    "geos": processo["geos"]
                }
            )

    except Exception as ex:
        traceback.print_exc(file=sys.stdout)
        app.logger.error("Error on get pins", ex)
        result = str(ex)

    return jsonify(result)


if __name__ == '__main__':
    app.run()
