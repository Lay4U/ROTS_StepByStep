#!/usr/bin/env python3
"""Python for Secret Agents

Chapter 3, Example 5

More complete steganography with secure hash.

This requires Pillow.

"""
from PIL import Image
from zipfile import ZipFile
import hmac
import os

def package( text, image_source, key_hmac, filename ):
    image= Image.open( image_source )
    steg_embed( image, text )
    image.save( "/tmp/package.tiff", format="TIFF" )
    with open("/tmp/package.tiff","rb") as saved:
        digest= hmac.new( key_hmac.encode("ASCII"), saved.read() )
    with ZipFile( filename, "w" ) as archive:
        archive.write( "/tmp/package.tiff", "image.tiff" )
        archive.comment= digest.hexdigest().encode("ASCII")
    os.remove( "/tmp/package.tiff" )

def unpackage( filename, key_hmac ):
    try:
        os.remove( "/tmp/image.tiff" )
    except FileNotFoundError:
        pass
    with ZipFile( filename, "r" ) as archive:
        with archive.open( "image.tiff", "r" ) as member:
            keyed= hmac.new( key_hmac.encode("ASCII"), member.read() )
        assert  archive.comment == keyed.hexdigest().encode("ASCII"), "Invalid HMAC"
        archive.extract( "image.tiff", "/tmp" )
    image= Image.open( "/tmp/image.tiff" )
    text= steg_extract( image )
    os.remove( "/tmp/image.tiff" )
    return text, image

def steg_embed( image, text ):
    message_bytes= text.encode("UTF-8")
    bits_list = list(to_bits(c) for c in message_bytes )
    len_h, len_l = divmod( len(message_bytes), 256 )
    size_list = [to_bits(len_h), to_bits(len_l)]
    w, h = image.size
    for p,m in enumerate( bit_sequence( size_list+bits_list ) ):
        y, x = divmod( p, w )
        r, g, b = image.getpixel( (x,y) )
        r_new = (r & 0xfe) | m
        #print( (r,g,b), m, (r_new,g,b) )
        image.putpixel( (x,y), (r_new, g, b)  )

def steg_extract( image ):
    size_h, size_l = byte_sequence( get_bits( image ) )
    size= size_h*256+size_l
    message= byte_sequence(get_bits( image, 16, size*8 ))
    return bytes(message).decode("UTF-8")

def get_bits( image, offset= 0, size= 16 ):
    w, h = image.size
    for p in range(offset, offset+size):
        y, x = divmod( p, w )
        r, g, b = image.getpixel( (x,y) )
        #print( (r, g, b), r&0x01 )
        yield r & 0x01

def to_bits( v ):
    b= []
    for i in range(8):
        b.append( v & 1 )
        v >>= 1
    return tuple(reversed(b))

def bit_sequence( list_of_tuples ):
    for t8 in list_of_tuples:
        for b in t8:
            yield b

def byte_sequence( bits ):
    byte= []
    for n, b in enumerate(bits):
        if n%8 == 0 and n != 0:
            yield to_byte(byte)
            byte= []
        byte.append( b )
    yield to_byte(byte)

def to_byte( b ):
    v= 0
    for bit in b:
        v = (v<<1)+bit
    return v

if __name__ == "__main__":
    package( "Appears to be LHD-3", "LHD_Number_3_thumb.jpg",
            "Agent Garbo", "encrypted.zip" )
    text, image = unpackage( "encrypted.zip", "Agent Garbo" )
    print( "Found {0!r}".format(text) )
