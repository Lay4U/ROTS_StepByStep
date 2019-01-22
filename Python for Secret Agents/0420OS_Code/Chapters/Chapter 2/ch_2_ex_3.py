#!/usr/bin/env python3
"""Python for Secret Agents.

Chapter 1, Example 3

urllib examples.
"""
import urllib.request

# Places to look.
url_list = [
    "http://upload.wikimedia.org/wikipedia/commons/7/72/IPhone_Internals.jpg",
    "http://upload.wikimedia.org/wikipedia/en/2/26/Common_face_of_one_euro_coin.jpg",
    ]

# Get all the named files using http: scheme.
for url in url_list:
    with urllib.request.urlopen( url ) as response:
        print( "Status:", response.status )
        _, _, filename = response.geturl().rpartition("/")
        print( "Writing:", filename )
        with open( filename, "wb" ) as image:
            image.write( response.read() )

# Get a file using ftp: scheme.
readme= "ftp://ftp.ibiblio.org/pub/docs/books/gutenberg/README"
with urllib.request.urlopen( readme ) as response:
    for line in response.readlines():
        print( line.rstrip() )

# Get a local file using the file: scheme.
local= "file:///Users/slott/Documents/Writing/Secret Agent's Python/currency.html"
with urllib.request.urlopen( local ) as response:
    print( response.read() )
