#!/usr/bin/env python3
"""Python for Secret Agents.

Chapter 2 Example 5

Processing with lists and dictionaries, defaultdict, and Counter.

Data extracted manually from

http://www.ers.usda.gov/datafiles/Dairy_Data/chezcon_1_.xls.

http://wonder.cdc.gov/wonder/help/ucd.html

http://wonder.cdc.gov/controller/datarequest/D76
"""

# A simple list.

cheese = [29.87, 30.12, 30.60, 30.66, 31.33, 32.62,
    32.73, 33.50, 32.84, 33.02,]
len(cheese)
min(cheese)
cheese.index( max(cheese) )

cheese += [32.92, 33.27, 33.51,]
cheese

cheese.sort()
cheese

cheese[0]
cheese[1]
cheese[-2]
cheese[-1]

cheese[:5]
cheese[5:]

# Some additional features of lists.

[2, 3, 5, 7] + [11, 13, 17]
[2, 3, 5, 7] * 2
[0]*10

# A list-of-tuples.

year_cheese = [(2000, 29.87), (2001, 30.12), (2002, 30.6), (2003, 30.66),
    (2004, 31.33), (2005, 32.62), (2006, 32.73), (2007, 33.5),
    (2008, 32.84), (2009, 33.02), (2010, 32.92), (2011, 33.27),
    (2012, 33.51)]

max( year_cheese, key=lambda x:x[1] )

def by_weight( yr_wt_tuple ):
    year, weight =  yr_wt_tuple
    return weight

by_cheese = sorted( year_cheese, key=by_weight )

years = [ item[0] for item in year_cheese ]
years

years.index(2005)
year_cheese[years.index(2005)]

# A simple dictionary.

form = {
    's': 'YHOO',
    'ql': '1',
}
form['s']
form['ql']

# Encoding a dictionary as if it was form input on a web page.

import urllib.parse
urllib.parse.urlencode( form )

form['s']
form['oops']
form.get('s')
form.get('oops')
form.get('oops', '#Missing')

# Working with defaultdict and Counter.

import pprint
from collections import defaultdict, Counter

corpus_file = "/usr/share/dict/words"
digram_count = Counter() # defaultdict( int )
with open( corpus_file ) as corpus:
    for line in corpus:
        word= line.lower().strip()
        for position in range(len(word)-1):
            digram= word[position:position+2]
            digram_count[digram] += 1

#pprint.pprint( digram_count )
print( digram_count.most_common( 10 ) )

total= sum( digram_count.values() )
for digram, count in digram_count.items():
    print( "{:2s} {:7d} {:.3%}".format(digram, count, count/total)  )

corpus_file = "/usr/share/dict/words"
hyphenated = set()
with open( corpus_file ) as corpus:
    for line in corpus:
        word= line.lower().strip()
        if '-' in word:
            hyphenated.add(word)

print( hyphenated )
