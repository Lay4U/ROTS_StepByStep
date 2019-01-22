#!/usr/bin/env python3
"""Python for Secret Agents

Chapter 3, example 6.

More details on picture cropping.

This requires Pillow.

"""
from PIL import Image
from PIL import ImageColor
import glob
import os

from fractions import Fraction

# How many slices? 6×6.
slices = 6
box = [ Fraction(i,slices) for i in range(slices+1) ]

# Open the image.
ship= Image.open( "LHD_warship.jpg" ).convert("CMYK")
w, h = ship.size

# Open the output image that we'll create.
illustration = Image.new( "RGB", (w+(slices+1)*12, h+(slices+1*12)),
                        ImageColor.getcolor("White","RGB") )

# For each of the (x,y) combinations, get the slice and put them into the output.
# The destination boundaries include offsets between each slice.
for s_x in range(slices):
    for s_y in range(slices):
        bounds = tuple( map( int, (w*box[s_x], h*box[s_y], w*box[s_x+1], h*box[s_y+1]) ) )
        section= ship.crop( bounds )
        destination = bounds[0]+12*s_x, bounds[1]+12*s_y, bounds[2]+12*s_x, bounds[3]+12*s_y
        illustration.paste( section, destination )

#illustration.show()
illustration.convert("CMYK").save("sliced.jpg")
