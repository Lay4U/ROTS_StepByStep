#!/usr/bin/env python3
"""Python for Secret Agents

Chapter 4, example 4

Grid Square, Georef and NAC conversions of coordinates.
"""
import string

def ll_2_mh( lat, lon ):
    """Convert Lat-Lon to Maidenhead code.
    
    :param lat: Latitude as a signed number
    :param lon: Longitude as a signed number
    """
    def let_num( v ):
        l, n = divmod( int(v), 10 )
        return string.ascii_uppercase[l], string.digits[n]
    f_lat= lat+90
    f_lon= (lon+180)/2
    y0, y1 = let_num( f_lat )
    x0, x1 = let_num( f_lon )
    f_lat= 240*(f_lat-int(f_lat))
    f_lon= 240*(f_lon-int(f_lon))
    y2, y3 = let_num( f_lat )
    x2, x3 = let_num( f_lon )
    f_lat= 240*(f_lat-int(f_lat))
    f_lon= 240*(f_lon-int(f_lon))
    y4, y5 = let_num( f_lat )
    x4, x5 = let_num( f_lon )
    return "".join( [
        x0, y0, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5 ] )


def mh_2_ll( grid ):
    """Convert Grid Square Code to lat and lon pair.

    :param grid: 2 to 12-position grid-square code.
    :returns: latitude and longitude
    """
    lon= grid[0::2] # even positions
    lat= grid[1::2] # odd positions
    assert len(lon) == len(lat)
    # Lookups will alternate letters and digits
    decode = [ string.ascii_uppercase, string.digits,
              string.ascii_uppercase, string.digits,
              string.ascii_uppercase, string.digits,
              ]
    lons= [ lookup.find(char.upper()) for char, lookup in zip( lon, decode ) ]
    lats= [ lookup.find(char.upper()) for char, lookup in zip( lat, decode ) ]
    weights = [ 10.0, 1.0,
               1/24, 1/240,
               1/240/24, 1/240/240, ]
    lon = sum( w*d for w,d in zip(lons, weights) )
    lat = sum( w*d for w,d in zip(lats, weights) )
    #print( lats, lons, weights, lat-90, 2*lon-180 )

    return lat-90, 2*lon-180

georef_uppercase = string.ascii_uppercase.replace("O","").replace("I","")

def ll_2_georef( lat, lon ):
    """Convert Lat-Lon to a Georef code.

    :param lat: Latitude as a signed number
    :param lon: Longitude as a signed number
    """ 
    f_lat, f_lon = lat+90, lon+180
    lat_0, lat_1 = divmod( int(f_lat), 15 )
    lon_0, lon_1 = divmod( int(f_lon), 15 )
    lat_m, lon_m = 6000*(f_lat-int(f_lat)), 6000*(f_lon-int(f_lon))
    return "{lon_0}{lat_0}{lon_1}{lat_1}{lon_m:04d}{lat_m:04d}".format(
        lon_0= georef_uppercase[lon_0],
        lat_0= georef_uppercase[lat_0],
        lon_1= georef_uppercase[lon_1],
        lat_1= georef_uppercase[lat_1],
        lon_m= int(lon_m),
        lat_m= int(lat_m),
    )

def georef_2_ll( grid ):
    """Convert Georef Code to lat and lon pair.

    :param grid: Georef code.
    :returns: latitude and longitude
    """
    lon_0, lat_0, lon_1, lat_1= grid[:4]
    rest= grid[4:]
    pos= len(rest)//2
    if pos:
        scale= { 4: 100, 3: 10, 2: 1 }[pos] # or 10**(pos-1)
        lon_frac, lat_frac = float(rest[:pos])/scale, float(rest[pos:])/scale
    else:
        lon_frac, lat_frac = 0, 0
    lat= georef_uppercase.find(lat_0)*15+georef_uppercase.find(lat_1)+lat_frac/60
    lon= georef_uppercase.find(lon_0)*15+georef_uppercase.find(lon_1)+lon_frac/60
    return lat-90, lon-180

nac_uppercase= "0123456789BCDFGHJKLMNPQRSTVWXZ"
len(nac_uppercase)
nac_uppercase[10]
nac_uppercase.find('B')

def ll_2_nac( lat, lon ):
    """Convert Lat-Lon to a NAC.

    :param lat: Latitude as a signed number
    :param lon: Longitude as a signed number
    """ 
    f_lon= (lon+180)/360
    x0 = int(   f_lon*30)
    x1 = int((  f_lon*30-x0)*30)
    x2 = int((( f_lon*30-x0)*30-x1)*30)
    x3 = int(.5+(((f_lon*30-x0)*30-x1)*30-x2)*30)

    f_lat= (lat+90)/180
    y0 = int(   f_lat*30 )
    y1 = int((  f_lat*30-y0)*30)
    y2 = int((( f_lat*30-y0)*30-y1)*30)
    y3 = int(.5+(((f_lat*30-y0)*30-y1)*30-y2)*30)

    print( x0, x1, x2, x3, y0, y1, y2, y3 )
    return "".join( [
        nac_uppercase[x0], nac_uppercase[x1],
        nac_uppercase[x2], nac_uppercase[x3],
        " ",
        nac_uppercase[y0], nac_uppercase[y1],
        nac_uppercase[y2], nac_uppercase[y3],
    ])

def ll_2_nac_alt( lat, lon ):
    """Convert Lat-Lon to a NAC.
    
    Alternative, uses divmod() instead of more complex int() conversions.

    :param lat: Latitude as a signed number
    :param lon: Longitude as a signed number
    """ 
    f_lon= int(.5+810000*(lon+180)/360)
    f_lon, x3 = divmod( f_lon, 30 )
    f_lon, x2 = divmod( f_lon, 30 )
    x0, x1 = divmod( f_lon, 30 )

    f_lat= int(.5+810000*(lat+90)/180)
    f_lat, y3= divmod( f_lat, 30 )
    f_lat, y2= divmod( f_lat, 30 )
    y0, y1= divmod( f_lat, 30 )

    print( x0, x1, x2, x3, y0, y1, y2, y3 )
    return "".join( [
        nac_uppercase[x0], nac_uppercase[x1],
        nac_uppercase[x2], nac_uppercase[x3],
        " ",
        nac_uppercase[y0], nac_uppercase[y1],
        nac_uppercase[y2], nac_uppercase[y3],
    ])

def nac_2_ll( grid ):
    """Convert NAC to lat and lon pair.

    :param grid: NAC.
    :returns: latitude and longitude
    """
    X, Y = grid[:4], grid[5:]
    x = [nac_uppercase.find(c) for c in X]
    y = [nac_uppercase.find(c) for c in Y]
    print( x, y )

    lon = (x[0]/30+x[1]/30**2+x[2]/30**3+x[3]/30**4)*360-180

    lat = (y[0]/30+y[1]/30**2+y[2]/30**3+y[3]/30**4)*180-90

    return lat, lon

# Demonstration of Maidenhead.

#36°50.63′N 076°17.49′W
lat, lon = 36+50.63/60, -(76+17.49/60)
print( lat, lon )
print( ll_2_mh( lat=36+50.63/60, lon=-(76+17.49/60) ) )
print( mh_2_ll( "FM16UU62AM04" ) )
print( mh_2_ll( "FM16UU62AM" ) )
print( "*", mh_2_ll( "FM16UU62" ) )
print( mh_2_ll( "FM16UU" ) )
print( mh_2_ll( "FM16" ) )

print( "Maidenhead", ll_2_mh( 51.522751, -0.720209) )

# Demonstration of Georef.

print( ll_2_georef( lat, lon ) )
print( georef_2_ll( "GJPG42515063" ) )
print( "*", georef_2_ll( "GJPG425506" ) )
print( georef_2_ll( "GJPG4350" ) )
print( georef_2_ll( "GJPG" ) )

# More formal test of NAC.

def test_nac():
    lat, lon = 43.6508, -151.3947
    # 2CHD Q87M
    print( ll_2_nac( lat, lon ) )
    print( ll_2_nac_alt( lat, lon ) )
    print( nac_2_ll( "2CHD Q87M" ) )

test_nac()

# More formal test of Georef

def test_georef():
    lat, lon = 38+17/60+10/3600, -(76+24/60+42/3600)
    print( "Georef", lat, lon )
    print( ll_2_georef( lat, lon ) )
    print( georef_2_ll( "GJPJ35291716" ) )
    print( georef_2_ll( "GJPJ3517" ) )
    print( georef_2_ll( "GJPJ" ) )

test_georef()
