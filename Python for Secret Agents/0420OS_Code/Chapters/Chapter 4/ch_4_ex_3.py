#!/usr/bin/env python3
"""Python for Secret Agents

Chapter 4, Example 3

Haversine distance between points.
"""
from math import radians, sin, cos, sqrt, asin

MI= 3959
NM= 3440
KM= 6371

def haversine( point1, point2, R=MI ):
    """Distance between points.
    point1 and point2 are two-tuples of latitude and longitude.
    R is radius, R=MI computes in miles.

    >>> from ch_4_ex_3 import haversine
    >>> round(haversine((36.12, -86.67), (33.94, -118.40), R=6372.8), 5)
    2887.25995
    """
    lat_1, lon_1= point1
    lat_2, lon_2= point2

    Δ_lat = radians(lat_2 - lat_1)
    Δ_lon = radians(lon_2 - lon_1)
    lat_1 = radians(lat_1)
    lat_2 = radians(lat_2)

    a = sin(Δ_lat/2)**2 + cos(lat_1)*cos(lat_2)*sin(Δ_lon/2)**2
    c = 2*asin(sqrt(a))

    return R * c

import urllib.request
import urllib.parse
import json

def geocode( address ):
    form = {
        "address": address,
        "sensor": "false",
        #"key": Your API Key,
    }
    query = urllib.parse.urlencode( form, safe="," )
    scheme_netloc_path = "https://maps.googleapis.com/maps/api/geocode/json"
    with urllib.request.urlopen( scheme_netloc_path+"?"+query ) as geocode:
        response= json.loads( geocode.read().decode("UTF-8") )

    loc_dict= [r['geometry']['location'] for r in response['results']]
    loc_pairs= [(l['lat'],l['lng']) for l in loc_dict]
    return loc_pairs

def demo1():
    base = geocode( "333 Waterside, Norfolk, VA, 23510" )[0]
    loc1 = geocode( "456 Granby St, Norfolk, VA")[0]
    loc2 = geocode( "111 W Tazewell, Norfolk, VA")[0]

    print( "Base", base )
    print( "Loc1", loc1, haversine(base, loc1) )
    print( "Loc2", loc2, haversine(base, loc2) )

if __name__ == "__main__":
    demo1()
