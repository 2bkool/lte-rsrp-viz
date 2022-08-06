import numpy as np
from numpy import cos, sin, radians, arctan2, rad2deg, deg2rad


def bearing(lat1, lon1, lat2, lon2):
    lat1, lat2 = radians(lat1), radians(lat2)
    lon1, lon2 = radians(lon1), radians(lon2)
    y = sin(lon2 - lon1) * cos(lat2)
    x = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(lon2 - lon1)
    return rad2deg(arctan2(y, x))


def rotate_point(x, y, theta):
    theta_ = deg2rad(theta)
    x_ = x * cos(theta_) - y * sin(theta_)
    y_ = x * sin(theta_) + y * cos(theta_)
    return x_, y_


def calc_distance(x1, y1, x2, y2):
    return np.sqrt(((x2 - x1) ** 2) + (y2 - y1) ** 2)
