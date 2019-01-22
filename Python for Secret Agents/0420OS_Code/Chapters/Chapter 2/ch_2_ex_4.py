#!/usr/bin/env python3
"""Python for Secret Agents.

Chapter 2 example 4

Bitcoin and currency conversion using urrlib

For more information, see https://coinbase.com/api/doc/1.0/currencies.html
"""
import pprint

import urllib.request
import json

# Part I: basic currency info.

# The basic query to locate currency names and codes.
query_currencies= "http://www.coinbase.com/api/v1/currencies/"

with urllib.request.urlopen( query_currencies ) as document:
    pprint.pprint( document.info().items() )
    currencies= json.loads( document.read().decode("utf-8") )

print( len(currencies) )
print( currencies )

# Confirm that USD and EUR are covered.
for country, currency in currencies:
    if currency in ( "USD", "EUR", "GBP" ):
        print( country, currency )

# Part II: encode a query string.

import urllib.parse

def get_spot_rate( currency ):
    scheme_netloc_path= "https://coinbase.com/api/v1/prices/spot_rate"
    form= {"currency":currency}
    query= urllib.parse.urlencode(form)

    with urllib.request.urlopen( scheme_netloc_path+"?"+query ) as document:
        spot_rate= json.loads( document.read().decode("utf-8") )
    return spot_rate

# Part III: Build a JSON document with rate information.

rates = [
    get_spot_rate("USD"), get_spot_rate("EUR"),
    get_spot_rate("GBP") ]
with open("rate.json","w") as save:
    json.dump( rates, save )

with open("rate.json") as spot_rates:
    print( spot_rates.read() )

# Part IV: Examine all the exchange rates.

def get_all_rates():

    scheme_netloc_path= "http://www.coinbase.com/api/v1/currencies/exchange_rates/"

    with urllib.request.urlopen( scheme_netloc_path ) as document:
        pprint.pprint( document.info().items() )
        exchange_rates= json.loads( document.read().decode("utf-8") )

    print( len(exchange_rates) )
    pprint.pprint( exchange_rates )

    from collections import defaultdict
    from decimal import Decimal
    rates = defaultdict( list )
    for conversion, rate in exchange_rates.items():
        source, _, target = conversion.upper().partition("_TO_")
        rates[source].append( (target, float(rate)) )

    #pprint.pprint( rates )

    currency_details = dict( (code,name) for name,code in currencies )

    for c in 'USD', 'GBP', 'EUR':
        print( currency_details[c], rates[c] )

# Takes a while. Be sure everything else works before removing the
# command and trying this function.

# get_all_rates()
