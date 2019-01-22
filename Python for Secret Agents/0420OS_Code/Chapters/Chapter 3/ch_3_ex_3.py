#!/usr/bin/env python3
"""Python for Secret Agents

Chapter 3, example 3

Steganography example.

This requires Pillow.

"""

from PIL import Image

# Our base message as a Unicode string and as bytes.

message= "http://www.kearsarge.navy.mil"
message_bytes= message.encode("UTF-8")
print( [ hex(c) for c in message_bytes ] )

# Convert a single byte to an 8-tuple of bits.
def to_bits( v ):
    b= []
    for i in range(8):
        b.append( v & 1 )
        v >>= 1
    return tuple(reversed(b))

# Convert an 8-tuple of bits to a single byte.
def to_byte( b ):
    v= 0
    for bit in b:
        v = (v<<1)|bit
    return v

# Confirm that our bits <-> bytes conversions work.
for test in range(256):
    b = to_bits(test)
    v = to_byte(b)
    assert v == test

# Convert a list of 8-tuples into a long list of individual values.
def bit_sequence( list_of_tuples ):
    for t8 in list_of_tuples:
        for b in t8:
            yield b

# Demonstrate the bit_sequence of the to_bits of a message.
bits= bit_sequence(
    (to_bits(c) for c in message_bytes)
)
print( bits )
x = list(bits)
print( x )

# Convert a long sequence of bits into a sequence of byte values.
def byte_sequence( bits ):
    byte= []
    for n, b in enumerate(bits):
        if n%8 == 0 and n != 0:
            yield to_byte(byte)
            byte= []
        byte.append( b )
    yield to_byte(byte)

# Demonstrate that the byte_sequence() function  works.
print( [hex(b) for b in byte_sequence(x)] )

# An alternative using more advanced libraries.
from itertools import groupby
groups= (to_byte(b[1] 
    for b in t8) for g,t8 in groupby( enumerate(x), lambda n_v: n_v[0]//8 ))
print( list(hex(b) for b in groups) )

# Part I: Encode

# Open the thumbnail image.
ship = Image.open("LHD_warship_thumb.jpg")
original= ship.copy()

# Encode the message Unicode characters into bytes.
message_bytes= message.encode("UTF-8")

# Expand the bytes into bits.
bits_list = list(to_bits(c) for c in message_bytes )

# Compute the size of the message.
len_h, len_l = divmod( len(message_bytes), 256 )
size_list = [to_bits(len_h), to_bits(len_l)]

# Step through the message, folding each bit into the image bytes.
w, h = ship.size
for p,m in enumerate( bit_sequence( size_list+bits_list ) ):
    y, x = divmod( p, w )
    r, g, b = ship.getpixel( (x,y) )
    r_new = (r & 0xfe) | m
    print( (r, g, b), m, (r_new, g, b) )
    ship.putpixel( (x,y), (r_new, g, b)  )

# Show the two images.
original.show()
ship.show()

# Part II. Decode

# Get the LSB's from the image.

def get_bits( image, offset= 0, size= 16 ):
    w, h = image.size
    for p in range(offset, offset+size):
        y, x = divmod( p, w )
        r, g, b = image.getpixel( (x,y) )
        yield r & 0x01

# Get the size of the message from the first 16 bits.
size_h, size_l = byte_sequence( get_bits( ship ) )
size= size_h*256+size_l

# Get the bits of the message.
message=byte_sequence(get_bits( ship, 16, size*8 ))
print( bytes(message).decode("UTF-8") )
