#!/usr/bin/env python3
from fractions import Fraction

p = 0
for i in range(1, 2000):
    p += Fraction(1, i**2)
print( (p*6)**Fraction(1,2) )
