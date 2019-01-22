#!/usr/bin/env python3
"""Python for Secret Agents

Chapter 4, Example 2

Reverse Geocoding.
"""
import urllib.request
import urllib.parse
import json

form = {
    "latlng": "36.844305,-76.29112",
    "sensor": "false",
    #"key": Your API Key,
}
query = urllib.parse.urlencode( form, safe="," )
scheme_netloc_path = "https://maps.googleapis.com/maps/api/geocode/json"
print( scheme_netloc_path+"?"+query )
with urllib.request.urlopen( scheme_netloc_path+"?"+query ) as geocode:
    print( geocode.info() )
    response= json.loads( geocode.read().decode("UTF-8") )

import pprint
pprint.pprint(response)

for alt in response['results']:
    print(alt['types'], alt['formatted_address'])
