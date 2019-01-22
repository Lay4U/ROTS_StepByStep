#!/usr/bin/env python3
"""Python for Secret Agents

Chapter 4 example 6

Chicago health inspection using JSON data.

"""
import urllib.request
import urllib.parse
import json
from types import SimpleNamespace

# Get the JSON document from the city of Chicago data portal.
def get_chicago_json():
    scheme_netloc_path= "https://data.cityofchicago.org/api/views/4ijn-s7e5/rows.json"
    form = {
        "accessType": "DOWNLOAD",
        "$where": "inspection_date>2014-01-01",
    }
    query= urllib.parse.urlencode(form)
    with urllib.request.urlopen( scheme_netloc_path+"?"+query ) as data:
        with open("chicago_data.json","w") as output:
            output.write( data.read() )

#get_chicago_json()

# Get individual rows of data from the JSON document.
def food_row_iter():
    with open( "chicago_data.json", encoding="UTF-8" ) as data_file:
        inspections = json.load( data_file )
    #import pprint
    #pprint.pprint( inspections["meta"]["view"]["columns"] )
    headings = [item['fieldName']
        for item in inspections["meta"]["view"]["columns"] ]
    print( headings )
    for row in inspections["data"]:
        data= SimpleNamespace(
            **dict( zip( headings, row ) )
        )
        yield data

# Tweak the details of a business record to convert coordinates
# to float() numbers and parse the details of the inspection report.
def parse_details( business ):
    business.latitude= float(business.latitude)
    business.longitude= float(business.longitude)
    if business.violations is None:
        business.details = []
    else:
        business.details = [ v.strip() for v in business.violations.split("|") ]
    return business

# Add our haversine() function to compute distances.
from ch_4_ex_3 import haversine

# Iterate through restaurants, providing distance from our HQ.
def choice_iter():
    base= SimpleNamespace( address="3420 W GRACE ST",
        city= "CHICAGO", state="IL", zip="60618",
        latitude=41.9503, longitude=-87.7138)
    for row in food_row_iter():
        try:
            parse_details( row )
            row.distance= haversine(
                (row.latitude, row.longitude),
                (base.latitude, base.longitude) )
            yield row
        except TypeError:
            pass
            # print( "problems with", row.dba_name, row.address, row.latitude, row.longitude )

# Show businesses within a quarter mile of HQ that have acceptable health inspections.
for business in choice_iter():
    if business.distance > .25: continue
    if business.results == "Fail": continue
    print( business.dba_name,
        business.address, business.results,
        len(business.details) )
