#!/usr/bin/env python3
"""Python for Secret Agents

Chapter 4 example 5

Norfolk health inspection HTML reading.

This requires Beautiful Soup 4
"""
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import json
from types import SimpleNamespace

# A place we're going to work with.
some_place = { 'name': 'The Name', 'address': '333 Waterside Drive' }
some_place['lat']= 36.844305
some_place['lng']= -76.29111999999999

# A class definition for a Restaurant.
class Restaurant:
    def __init__( self, name, address ):
        self.name= name
        self.address= address
        
# Example of an object of class Restaurant.
some_place= Restaurant( 'The Name', '333 Waterside Drive' )
some_place.lat= 36.844305
some_place.lng= -76.29111999999999
some_place= SimpleNamespace( name='The Name', address='333 Waterside Drive' )

# A place to get healthcode data.
scheme_host= "http://healthspace.com"
def get_food_list_by_name():
    path= "/Clients/VDH/Norfolk/Norolk_Website.nsf/Food-List-ByName"
    form = {
        "OpenView": "",
        "RestrictToCategory": "FAA4E68B1BBBB48F008D02BF09DD656F",
        "count": "400",
        "start": "1",
    }
    query= urllib.parse.urlencode( form )
    with urllib.request.urlopen(scheme_host + path + "?" + query) as data:
        soup= BeautifulSoup( data.read() )
    return soup

# Explore the BeautifulSoup object to gather data.
def food_table_iter( soup ):
    """Get the food table from a parsed Soup.
    
    Columns are 'Name', '', 'Facility Location', 'Last Inspection', 'Details URL'
    """
    table= soup.html.body.table
    for row in table.find_all("tr"):
        columns = [ td.text.strip() for td in row.find_all("td") ]
        for td in row.find_all("td"):
            if td.a:
                url= urllib.parse.urlparse( td.a["href"] )
                form= urllib.parse.parse_qs( url.query )
                columns.append( form['RestrictToCategory'][0] )
        yield columns

def food_row_iter( table_iter ):
    """Translate raw column names to more useful names

    'Name', '', 'Facility Location', 'Last Inspection' plus a URL

    to a namespace with attributes

    name, address, last_inspection, category
    """

    heading= next(table_iter)
    assert ['Name', '', 'Facility Location', 'Last Inspection'] == heading
    for row in table_iter:
        yield SimpleNamespace(
            name= row[0], address= row[2], last_inspection= row[3],
            category= row[4]
        )

# Demonstrate that we're finding the food table in the healthcode data.
for row in  food_table_iter(get_food_list_by_name()):
    print(row)
    
# Get facility history
def get_food_facility_history( category_key ):
    url_detail= "/Clients/VDH/Norfolk/Norolk_Website.nsf/Food-FacilityHistory"
    form = {
        "OpenView": "",
        "RestrictToCategory": category_key
    }
    query= urllib.parse.urlencode( form )
    with urllib.request.urlopen(scheme_host + url_detail + "?" + query) as data:
        soup= BeautifulSoup( data.read() )
    return soup

# Translate HTML column titles to Python attribute names.
vdh_detail_translate = {
    'Phone Number:': 'phone_number',
    'Facility Type:': 'facility_type',
    '# of Priority Foundation Items on Last Inspection:':
        'priority_foundation_items',
    '# of Priority Items on Last Inspection:': 'priority_items',
    '# of Core Items on Last Inspection:': 'core_items',
    '# of Critical Violations on Last Inspection:': 'critical_items',
    '# of Non-Critical Violations on Last Inspection:': 'non_critical_items',
}

# Get inspection details, creating details for a given Business object.
def inspection_detail( business ):
    """Rows in table are
        'Phone Number:',
        'Facility Type:',
        '# of Priority Foundation Items on Last Inspection:',
        '# of Priority Items on Last Inspection:',
        '# of Core Items on Last Inspection:',
        '# of Critical Violations on Last Inspection:'
        '# of Non-Critical Violations on Last Inspection:',

    Translate to more useful names

    phone_number, facility_type, priority_foundation_items,
    priority_items, core_items, critical_items, non_critical_items
    """
    soup= get_food_facility_history( business.category )
    business.name2= soup.body.h2.text.strip()
    table= soup.body.table
    #print( table )
    for row in table.find_all("tr"):
        column = list( row.find_all( "td" ) )
        #print( column )
        name= column[0].text.strip()
        value= column[1].text.strip()
        setattr( business, vdh_detail_translate[name], value )
    return business

# Get geocode details for a business.
def geocode_detail( business ):
    scheme_netloc_path = "https://maps.googleapis.com/maps/api/geocode/json"
    form = {
        "address": business.address + ", Norfolk, VA",
        "sensor": "false",
        #"key": Your API Key,
    }
    query = urllib.parse.urlencode( form, safe="," )
    with urllib.request.urlopen( scheme_netloc_path+"?"+query ) as geocode:
        response= json.loads( geocode.read().decode("UTF-8") )
    lat_lon = response['results'][0]['geometry']['location']
    business.latitude= lat_lon['lat']
    business.longitude= lat_lon['lng']
    return business

# Demonstrate that we have the basic tools in place.
soup= get_food_list_by_name()
for row in food_row_iter( food_table_iter( soup ) ):
    inspection_detail( row )

# Add our haversine() function to compute distances.
from ch_4_ex_3 import haversine

# Iterate through restaurants, providing distance from our HQ.
def choice_iter():
    base= SimpleNamespace( address= '333 Waterside Drive' )
    geocode_detail( base )
    print( base ) # latitude= 36.844305, longitude= -76.29111999999999 )
    soup= get_food_list_by_name()
    for row in food_row_iter( food_table_iter( soup ) ):
        geocode_detail( row )
        inspection_detail( row )
        row.distance= haversine(
            (row.latitude, row.longitude),
            (base.latitude, base.longitude) )
        yield row

# This may be slow; depends on your internet connection.

#for c in choice_iter():
#    print( c )
