#!/usr/bin/env python3
"""Python for Secret Agents

Chapter 5, example 1

Some simple statistical functions.

>>> from ch_5_ex_1 import mean, median
>>> data = [2, 4, 4, 4, 5, 5, 7, 9]
>>> data # doctest: +ELLIPSIS
[2, 4..., 9]
>>> mean( data )
5.0
>>> median( data )
4.5

"""
import csv

# Some manually entered data.
year_cheese = [(2000, 29.87), (2001, 30.12), (2002, 30.6), (2003, 30.66),
    (2004, 31.33), (2005, 32.62), (2006, 32.73), (2007, 33.5),
    (2008, 32.84), (2009, 33.02), (2010, 32.92)
    ]

def get_cheese():
    return year_cheese

# Read the raw data.
def raw():
    with open( "Cause of Death by Year.txt" ) as source:
        rdr= csv.DictReader( source, delimiter="\t" )
        for row in rdr:
            if row['Notes'] == "Total": break
            print( row )

# Read the data, parsing the input to get usable numbers.
def get_deaths():
    with open( "Cause of Death by Year.txt" ) as source:
        rdr= csv.DictReader( source, delimiter="\t" )
        for row in rdr:
            if row['Notes'] == "Total": break
            yield int(row['Year']), int(row['Deaths'])

year_deaths = list( get_deaths() )
#print( year_deaths )

# Calculate the mean of a sequence of numbers.
def mean(values):
    """Mean of a sequence (doesn't work with an iterable)

    >>> from ch_5_ex_1 import mean
    >>> mean( [2, 4, 4, 4, 5, 5, 7, 9])
    5.0
    """
    return sum(values)/len(values)

# One approach to the count that doesn't use len()
def count(values):
    return sum(1 for x in values)

# An approach to mean that doesn't work for generators.
def mean2(values):
    return sum(values)/count(values)

# Median of a sequence.
def median(values):
    """
    >>> from ch_5_ex_1 import median
    >>> median( [2, 4, 4, 4, 5, 5, 7, 9])
    4.5
    """
    s = sorted(values)
    if len(s) % 2 == 1: # Odd
        return s[len(s)//2]
    else:
        mid= len(s)//2
        return (s[mid-1]+s[mid])/2

# Mode of a sequence.
from collections import Counter
def mode(values):
    c = Counter( values )
    mode_value, count = c.most_common(1)[0]
    return mode_value

# Execute doctest strings.
if __name__ == "__main__":
    import doctest
    doctest.testmod()
