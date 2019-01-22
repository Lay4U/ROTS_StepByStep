#!/usr/bin/env python3
"""Python for Secret Agents.

Chapter 2, Example 2

FTP Examples
"""
import ftplib
import sys

# Path to search.
root = "/pub/docs/books/gutenberg/"
# Server to connect to.
host = "ftp.ibiblio.org"

def directory_list( host, path="/" ):
    """Directory on a given host starting from a given path."""
    with ftplib.FTP( host, user="anonymous" ) as connection:
        print( "Welcome", connection.getwelcome() )
        for name, details in connection.mlsd(path):
            print( name, details['type'], details.get('size') )

# A function to get a file.
def get( host, fullname, output=sys.stdout ):
    """Get named file from the given host, writing dots to show progress."""
    download= 0
    expected= 0
    dots= 0
    def line_save( aLine ):
        nonlocal download, expected, dots
        print( aLine, file=output )
        if output != sys.stdout:
            download += len(aLine)
            show= (20*download)//expected
            if show > dots:
                print( "●", end="", file=sys.stdout )
                sys.stdout.flush()
                dots= show
    with ftplib.FTP( host, user="anonymous" ) as connection:
        print( "Welcome", connection.getwelcome() )
        expected= connection.size( fullname )
        print( "Getting", fullname, "to", output, "size", expected )
        connection.retrlines( "RETR {0}".format(fullname), line_save )
    if output != sys.stdout:
        print( ) # End the "dots"

# Start exploring.
# directory_list(host, root)

# Show the README.
get(host, root+"README") # Will display on sys.stdout

# Get GUTINDEX.ALL
with open("GUTINDEX.ALL", "w", encoding="UTF-8") as output:
    get(host, root+"GUTINDEX.ALL", output)

with open("GUTINDEX.ALL", encoding="UTF-8") as index:
    clean_lines= (line.rstrip() for line in index)
    for line in clean_lines:
        if "CIA" in line:
            print( line )
            nxt= next(clean_lines)
            while len(nxt) != 0:
                print( nxt )
                nxt= next(clean_lines)

# Want 2010 CIA World Factbook, document 35830.
# Note manual transformation from file number "35830" to directory path.
directory_list(host, root+"3/5/8/3/35830/")

# Actually getting the factbook can be pretty slow. 
# Be sure everything else works before starting this.

# with open("35830.txt", "w", encoding="UTF-8") as output:
#    get(host, root+"3/5/8/3/35830/"+"35830.txt", output)
