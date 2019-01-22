#!/usr/bin/env python3
"""Python for Secret Agents.

Chapter 2, Example 1

Simple HTTP GET
"""
import http.client
import contextlib

# Paths to get.
path_list = [
    "/wikipedia/commons/7/72/IPhone_Internals.jpg",
    "/wikipedia/en/c/c1/1drachmi_1973.jpg",
]

# Server to use.
host = "upload.wikimedia.org"

# Example 1 gets a number of files.
def ex1():
    with contextlib.closing( http.client.HTTPConnection( host ) ) as connection:
        for path in path_list:
            connection.request( "GET", path )
            response= connection.getresponse()
            print( "Status:", response.status )
            print( "Headers:", response.getheaders() )
            _, _, filename = path.rpartition("/")
            print( "Writing:", filename )
            with open( filename, "wb" ) as image:
                image.write( response.read() )

# Example 2 gets just one file, but uses a different header to 
# act like an iPhone.
def ex2():
    with contextlib.closing( http.client.HTTPConnection( host ) ) as connection:
        connection.request( "GET", "/wikipedia/en/c/c1/1drachmi_1973.jpg", headers= {
            'User-Agent':
                'Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D201 Safari/9537.53',
        })
        response= connection.getresponse()
        print( "Status:", response.status )
        print( "Headers:", response.getheaders() )

ex1()
ex2()
