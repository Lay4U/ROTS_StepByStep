#!/usr/bin/env python3
"""Python for Secret Agents.

Chapter 1, Example 2

The input() function.
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
lunch_grd= Decimal('53')
bribe_grd= 50000
cab_usd= Decimal('23.50')

lunch_usd= (lunch_grd/grd_usd).quantize(PENNY)
bribe_usd= (bribe_grd/grd_usd).quantize(PENNY)

# Output our total bill.
print( "Lunch", lunch_grd, "GRD", lunch_usd, "USD" )
print( "Bribe", bribe_grd, "GRD", bribe_usd, "USD" )
print( "Cab", cab_usd, "USD" )
print( "Total", lunch_usd+bribe_usd+cab_usd, "USD" )
