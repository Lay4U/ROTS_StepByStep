#!/usr/bin/env python3
"""Python for Secret Agents

Chapter 5 Example 4

Correlation between deaths and cheese consumption.

http://www.tylervigen.com/view_correlation?id=7
"""
from collections import Counter
import math

class AnnualStats:
    """Collect (year, measurement) data for statistical analysis.

    >>> from ch_5_ex_4 import AnnualStats
    >>> test = AnnualStats( [(2000, 2),
    ...    (2001, 4),
    ...    (2002, 4),
    ...    (2003, 4),
    ...    (2004, 5),
    ...    (2005, 5),
    ...    (2006, 7),
    ...    (2007, 9),] )
    ...
    >>> test.min_year()
    2000
    >>> test.max_year()
    2007
    >>> test.mean()
    5.0
    >>> test.median()
    4.5
    >>> test.mode()
    4
    >>> test.stddev()
    2.0
    >>> list(test.stdscore())
    [-1.5, -0.5, -0.5, -0.5, 0.0, 0.0, 1.0, 2.0]
    """
    def __init__(self, year_measure):
        self.year_measure = list(year_measure)
        self.data = list(v for yr, v in self.year_measure)
        self.counter= Counter(self.data)
    def __repr__(self):
        return repr(self.year_measure)
    def min_year(self):
        return min( yr for yr, v in self.year_measure )
    def max_year(self):
        return max( yr for yr, v in self.year_measure )
    def mean(self):
        return sum(self.data)/len(self.data)
    def median(self):
        mid, odd = divmod( len(self.data), 2 )
        if odd:
            return sorted(self.data)[mid]
        else:
            pair= sorted(self.data)[mid-1:mid+1]
            return sum(pair)/2
    def mode(self):
        value, count = self.counter.most_common(1)[0]
        return value

    def stddev(self):
        μ_x = self.mean()
        n = len(self.data)
        σ_x= math.sqrt( sum( (x-μ_x)**2 for x in self.data )/n )
        return σ_x
    def stddev2(self):
        s_0 = sum(1 for x in self.data) # x**0
        s_1 = sum(x for x in self.data) # x**1
        s_2 = sum(x**2 for x in self.data)
        return math.sqrt( s_2/s_0 - (s_1/s_0)**2 )
    def stdscore(self):
        μ_x= self.mean()
        σ_x= self.stddev()
        return ((x-μ_x)/σ_x for x in self.data)

def demo1():
    from ch_5_ex_1 import get_deaths, get_cheese

    deaths = AnnualStats( get_deaths() )
    cheese = AnnualStats( get_cheese() )

    print( "Year Range", deaths.min_year(), deaths.max_year() )
    print( "Average W75 Deaths", deaths.mean() )

    print( "Median Cheese Consumption", cheese.median() )
    print( "Mean Cheese Consumption", cheese.mean() )
    print( "Stddev Cheese Consumption", cheese.stddev() )

    print( "Cheese", cheese )
    print( "Std scores", cheese.stdscore() )

    print( "Deaths", deaths )

# One way to compute correlation coefficient
def correlation1( d1, d2 ):
    n= len(d1.data)
    std_score_pairs = zip( d1.stdscore(), d2.stdscore() )
    r = sum( x*y for x,y in std_score_pairs )/n
    return r

# Another way to compute correlation coefficient
def correlation2( dx, dy ):
    n= len(dx.data)
    mx= dx.mean()
    my= dy.mean()
    pairs= zip( dx.data, dy.data )
    s1 = sum( (x-mx)*(y-my) for x,y in pairs )
    s2x = sum( (x-mx)**2 for x in dx.data )
    s2y = sum( (y-my)**2 for y in dy.data )
    r= s1/(math.sqrt(s2x)*math.sqrt(s2y))
    return r

def demo2():
    from ch_5_ex_1 import get_deaths, get_cheese

    deaths = AnnualStats( get_deaths() )
    cheese = AnnualStats( get_cheese() )

    print( correlation1( deaths, cheese ) )
    print( correlation2( deaths, cheese ) )

if __name__ == "__main__":
    demo1()
    demo2()
