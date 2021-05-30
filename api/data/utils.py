import unicodedata
import re
from math import sin, cos, sqrt, atan2, radians
from shapely.geometry import Point, Polygon, shape, box

# approximate radius of earth in km
R = 6373.0

def slugify(value, allow_unicode=False):
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode(
            'ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s\\/]+', '-', value).strip('-_')


def check_point_in_polygon(point, poly):
    return point.within(poly)

def check_points_in_polygon(points, poly):
    for point in points:
        if check_point_in_polygon(point, poly):
            return True
    return False

def check_points_in_polygons(points, polys):
    for poly in polys:
        if check_points_in_polygon(points, poly):
            return True
    return False

def check_point_in_polygons(point, polys):
    for poly in polys:
        if hasattr(poly, "exterior") and poly.exterior.distance(point) < 0.01: # 1.11 km
                return True
        if check_point_in_polygon(point, poly):
            return True
    return False