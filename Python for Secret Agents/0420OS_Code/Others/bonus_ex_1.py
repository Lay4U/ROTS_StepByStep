"""Chapter 2, Example 2

HTTP GET with FORM
"""
import http.client
import urllib.parse
import contextlib
import pprint

host = "finance.yahoo.com"

form = {
    's': 'YHOO',
    'ql': '1',
}
query = urllib.parse.urlencode( form )
print( query )

with contextlib.closing( http.client.HTTPConnection( host ) ) as connection:
    url = "{path}?{query}".format(path="/q", query=query)
    connection.request( "GET", url )
    response= connection.getresponse()
    print( "Status:", response.status )
    pprint.pprint( response.getheaders() )
    page= response.read()
#print( page )

# Looking for <span class="time_rtq_ticker" id="yui_3_9_1_8_1400427694114_39">
# <span id="yfs_l84_yhoo">33.41</span></span>

from bs4 import BeautifulSoup
soup = BeautifulSoup(page)
print( "Reading", soup.html.head.title.text )
for tag in soup.find_all("span", class_="time_rtq_ticker"):
    print( tag )
    print( tag.span )
    print( tag.text )
