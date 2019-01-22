#!/usr/bin/env python3
"""Python for Secret Agents

Chapter 3, Example 4

Simple hashcode examples.
"""
import hashlib

# Compute a hash of a file's content.
md5 = hashlib.new("md5")
with open( "LHD_warship.jpg", "rb" ) as some_file:
    md5.update( some_file.read() )
print( "MD5", md5.hexdigest() )

# Compute a secure hash of a file's content.
import hmac
with open( "LHD_warship.jpg", "rb" ) as some_file:
    keyed= hmac.new( b"Agent Garbo", some_file.read() )
print( "HMAC", keyed.hexdigest() )

# Wikipedia Example of hashing.
print( hmac.new(b"key", b"The quick brown fox jumps over the lazy dog").hexdigest() )
print( '80070713463e7749b90c2dc24911e275' )
