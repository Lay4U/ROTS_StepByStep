#!/usr/bin/env python3
"""Python for Secret Agents.

Chapter 1, Example 3

The input() function and formatting.
"""
from decimal import Decimal

# Create an object for quantization to the nearest cent.
PENNY= Decimal('.01')

def get_decimal( prompt ):
    """Display a prompt, get a value and return a Decimal."""
    number= None
    while number is None:
        entry= input(prompt+": ")
        try:
            number= Decimal(entry)
        except decimal.InvalidOperation:
            print( "Invalid", entry )
    return number

# Get conversion factors.
grd_usd= get_decimal( "GRD Conversion" )
print( grd_usd, "GRD = 1 USD" )

eur_usd= get_decimal( "EUR Conversion" )
print( eur_usd, "EUR = 1 USD" )

# Amounts in the budget.
lunch_eur= Decimal('53')
bribe_grd= 50000
cab_usd= Decimal('23.50')

lunch_usd= (lunch_eur/eur_usd).quantize(PENNY)
bribe_usd= (bribe_grd/grd_usd).quantize(PENNY)

# Output our total bill: much nicer looking with formatted messages.
receipt_1 = "{0:12s}              {1:6.2f} USD"
receipt_2 = "{0:12s} {1:8.0f} {2:3s} {3:6.2f} USD"
print( receipt_2.format("Lunch", lunch_eur, "EUR", lunch_usd) )
print( receipt_2.format("Bribe", bribe_grd, "GRD", bribe_usd) )
print( receipt_2.format("Cab", cab_usd, "USD", cab_usd) )
print( receipt_1.format("Total", lunch_usd+bribe_usd+cab_usd) )
