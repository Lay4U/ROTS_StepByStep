#!/usr/bin/env python3
"""Python for Secret Agents.

Chapter 1, Example 1

Decimal math.
"""
from decimal import Decimal

# Create an object for quantization to the nearest cent.
PENNY= Decimal('.01')

# The amounts.
grd_usd= Decimal('247.616')
eur_usd= Decimal('.73')

lunch_eur= Decimal('53')
bribe_grd= 50000
cab_usd= Decimal('23.50')

# Conversion with quantization. 
lunch_usd= (lunch_eur/eur_usd).quantize(PENNY)
bribe_usd= (bribe_grd/grd_usd).quantize(PENNY)

# Outputs to see the results.
print( "Lunch", lunch_eur, "EUR", lunch_usd, "USD" )
print( "Bribe", bribe_grd, "GRD", bribe_usd, "USD" )
print( "Cab", cab_usd, "USD" )
print( "Total", lunch_usd+bribe_usd+cab_usd, "USD" )
