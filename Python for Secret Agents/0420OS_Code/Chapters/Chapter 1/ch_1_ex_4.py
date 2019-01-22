#!/usr/bin/env python3
"""Python for Secret Agents.

Chapter 1, Example 4

The input() function, defining our own report() function.
"""
from decimal import Decimal
import sys

# Create an object for quantization to the nearest cent.
PENNY= Decimal('.01')

def get_decimal(prompt):
    """Display a prompt, get a value and return a Decimal."""
    value= None
    while value is None:
        entry= input(prompt+": ")
        try:
            value= Decimal(entry)
        except decimal.InvalidOperation:
            print("Invalid", entry)
    return value

def report( grd_usd, eur_usd, target=sys.stdout ):
    """Report our budget to the given target file."""
    lunch_eur= Decimal('53')
    bribe_grd= 50000
    cab_usd= Decimal('23.50')

    lunch_usd= (lunch_eur/eur_usd).quantize(PENNY)
    bribe_usd= (bribe_grd/grd_usd).quantize(PENNY)

    receipt_1 = "{0:12s}              {1:6.2f} USD"
    receipt_2 = "{0:12s} {1:8.0f} {2:3s} {3:6.2f} USD"
    print( receipt_2.format("Lunch", lunch_eur, "EUR", lunch_usd), file=target )
    print( receipt_2.format("Bribe", bribe_grd, "GRD", bribe_usd), file=target  )
    print( receipt_2.format("Cab", cab_usd, "USD", cab_usd), file=target  )
    print( receipt_1.format("Total", lunch_usd+bribe_usd+cab_usd), file=target  )

# Get the conversion factors.
grd_usd= get_decimal( "GRD Conversion" )
print( grd_usd, "GRD = 1 USD" )

eur_usd= get_decimal( "EUR Conversion" )
print( eur_usd, "EUR = 1 USD" )

# Report the budget.
report(grd_usd, eur_usd)
