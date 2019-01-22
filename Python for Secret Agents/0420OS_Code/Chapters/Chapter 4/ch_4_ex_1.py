#!/usr/bin/env python3
"""Python for Secret Agents

Chapter 4, Example 1

Forward Geocoding.
"""

import urllib.request
import urllib.parse

def geocoder_us():
    """Nice-looking service.
    Couldn't find 333 Waterside."""
    form = {
        #'address': '1600 Pennsylvania Ave, Washington DC',
        'address': '333 Waterside Drive, Norfolk, VA 23510',
    }
    query = urllib.parse.urlencode( form, safe="," )

    scheme_netloc_path = "http://rpc.geocoder.us/service/csv"
    print( scheme_netloc_path+"?"+query )
    with urllib.request.urlopen( scheme_netloc_path+"?"+query ) as geocode:
        for row in geocode:
            print( row )

def open_geocoding_org():
    """Doesn't work at all."""
    form = {
        'country': 'USA',
        'city': 'Norfolk',
        'streetnames': '333 Waterside Drive',
        'postcode': '23510',
        'output': 'json',
    }
    query = urllib.parse.urlencode( form )

    scheme_netloc_path= "http://www.opengeocoding.org/geocoding/geoservice.php"
    # ?country=germany&province=bw&city=Stuttgart&district=&streetnames=&postcode=&output=xml

    print( scheme_netloc_path+"?"+query )
    with urllib.request.urlopen( scheme_netloc_path+"?"+query ) as geocode:
        for row in geocode:
            print( row )

def maplarge():
    form = {
        "address":"333 waterside drive",
        "city":"Norfolk",
        "state":"VA",
        "zip":"30309",
        "key":"YOUR-API-KEY",
    }
    query = urllib.parse.urlencode( form )
    scheme_netloc_path = "http://geocoder.maplarge.com/geocoder/json"
    print( scheme_netloc_path+"?"+query )
    with urllib.request.urlopen( scheme_netloc_path+"?"+query ) as geocode:
        for row in geocode:
            print( row )

# Here's the Google example. This works nicely.

import urllib.request
import urllib.parse
import json

form = {
    "address": "333 waterside drive, norfolk, va, 23510",
    "sensor": "false",
    #"key": Your API Key,
}
query = urllib.parse.urlencode( form, safe="," )
scheme_netloc_path = "https://maps.googleapis.com/maps/api/geocode/json"
print( scheme_netloc_path+"?"+query )
with urllib.request.urlopen( scheme_netloc_path+"?"+query ) as geocode:
    print(geocode.info())
    response= json.loads( geocode.read().decode("UTF-8") )

import pprint
pprint.pprint(response)

print(response['results'][0]['geometry']['location'])
