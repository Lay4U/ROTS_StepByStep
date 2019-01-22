#!/usr/bin/env python3
"""Python for Secret Agents

Chapter 3, example 1

Collect headers from an image file.

PIL.ExifTags.GPSTAGS and PIL.ExifTags.TAGS can help decode the EXIF.

Location details are wedged into the GPSInfo dictionary.

http://owl.phy.queensu.ca/~phil/exiftool/TagNames/EXIF.html

http://www.color.org/specification/ICC1v43_2010-12.pdf

Also, see http://blog.fpmurphy.com/2012/03/extract-icc-profile-from-images.html

This requires Pillow.

"""
from PIL import Image
import PIL.ExifTags
import glob
import pprint
import struct
from collections import namedtuple

# A class to hold the various attributes of a icc profile.

Header= namedtuple('Header',
    "profile_size,cmm_type,version,device_class,colour_space,"
    "PCS,date_time,signature,sig_platform,flags,dev_manufacturer,"
    "dev_model,dev_attributes,intent,illuminant,sig_creator,"
    "id"
    )

def icc_profile( icc_bytes ):
    """Decode the icc_bytes to create a Header object."""
    header = Header( *struct.unpack( ">IIIIII12s4s4sIII8sI12s4s16s28x", icc_bytes[:128]) )
    print( " Header:", header )
    tag_count= struct.unpack( ">I", icc_bytes[128:128+4] )[0]
    for tn in range(tag_count):
        offset= 128+4+12*tn
        sig, data_offset, data_size = struct.unpack( ">4sII", icc_bytes[offset:offset+12] )
        data= icc_bytes[data_offset:data_offset+data_size]
        print( "Tag", tn, sig, data[:4], data[4:8], data[8:] )
    return header

# Open an image and read the various kinds of headers and metadata.

for name in glob.glob("*.jpg"):
    img= Image.open(name)
    print( name, img.format, img.mode, img.size )
    for key in img.info:
        if key == 'exif':
            for k,v in img._getexif().items():
                if k == 34853: # GPSInfo
                    print( " ", PIL.ExifTags.TAGS[k], v )
                    for gk, gv in v.items():
                        print( "  ", PIL.ExifTags.GPSTAGS[gk], gv )
                else:
                    print( " ", PIL.ExifTags.TAGS[k], v )
        elif key == 'icc_profile':
            print( key, )
            icc_profile( img.info[key] )
        else:
            print( key, img.info[key] )
    print()
