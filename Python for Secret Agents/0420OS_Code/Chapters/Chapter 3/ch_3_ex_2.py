#!/usr/bin/env python3
"""Python for Secret Agents

Chapter 3, example 2.

Thumbnailing. Cropping. Filtering.

This requires Pillow.

"""
from PIL import Image
import PIL.ExifTags
import glob
import os

# Create thumbnails for all files in a given directory.

for filename in glob.glob("*.jpg"):
    name, ext = os.path.splitext( filename )
    if name.endswith("_thumb"):
        continue
    img = Image.open( filename )
    thumb= img.copy()
    w, h = img.size
    largest = max(w,h)
    w_t, h_t = w*128//largest, h*128//largest
    print( "Resize", filename, "from", w,h, "to", w_t,h_t )
    thumb.thumbnail( (w_t,h_t), PIL.Image.ANTIALIAS )
    thumb.save( name+"_thumb"+ext )

# Compute some slices of an image.

from fractions import Fraction
slices = 12
box = [ Fraction(i,slices) for i in range(slices+1) ]
ship= Image.open( "LHD_warship.jpg" )
w, h = ship.size
#x, y = 3*w//12, 5*h//12
#logo= ship.crop( box=(x,y,x+480,int(y+480*p)) )
bounds = map( int, (w*box[3], h*box[6], w*box[5], h*box[7]) )
logo= ship.crop( bounds )
logo.show()
logo.save( "LHD_number.jpg" )

# Step 1: contrast.
from PIL iCport ImageEnhance
e= ImageEnhance.Contrast(logo)
e.enhance(8.0).save( "LHD_Number_1.jpg" )

# Step 2: Edge Enhance.
from PIL import ImageFilter
e.enhance(8.0).filter( ImageFilter.EDGE_ENHANCE ).save( "LHD_Number_2.jpg" )

# Step 3: Autocontrast. 
from PIL import ImageOps
ac= ImageEnhance.Contrast( ImageOps.autocontrast( logo ) )
ac.enhance( 2.5 ).save( "LHD_Number_3.jpg" )
