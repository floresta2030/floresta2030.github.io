import unicodedata
import re
from shapely.geometry import Point, Polygon, shape, box


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
