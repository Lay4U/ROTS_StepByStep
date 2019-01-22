#!/usr/bin/env python3
"""Python for Secret Agents.

Chapter 1, Example 6

Examine a corpus, use the words as part of brute
force password guessing.
"""

# Scan the corpus and get a list of words. 
# Count the 10-letter words.
count= 0
corpus_file = "/usr/share/dict/words"
with open( corpus_file ) as corpus:
    for line in corpus:
        word= line.strip()
        if len(word) == 10:
            count += 1
print( count )

# Doesn't work: password required to read this file.
import zipfile
with zipfile.ZipFile( "demo.zip", "r" ) as archive:
    archive.printdir()
    first = archive.infolist()[0]
    try:
        with archive.open(first) as member:
            text= member.read()
            print( text )
    except RuntimeError as e:
        print( e )

# Get a timer so we can measure how long this took.
import time
start= time.perf_counter()

# Brute force search of passwords.
import zipfile
import zlib
corpus_file = "/usr/share/dict/words"

with zipfile.ZipFile( "demo.zip", "r" ) as archive:
    first = archive.infolist()[0]
    print( "Reading", first.filename )
    with open( corpus_file ) as corpus:
        for line in corpus:
            word= line.strip().encode("ASCII")
            try:
                with archive.open(first, 'r', pwd=word) as member:
                    text= member.read()
                print( "Password", word )
                print( text )
                break
            except (RuntimeError, zlib.error, zipfile.BadZipFile):
                pass

# Show the time required to convert.
end= time.perf_counter()
print( "{:.1f} seconds".format(end-start) )
