#!/usr/bin/env python
## extract_sshpubkey_params.py
## Author: Avi Kak
## Date: February 11, 2013
import sys
import base64
import BitVector

if len(sys.argv) != 2:
    sys.stderr.write("Usage: %s <public key file>\n" % sys.argv[0])
    sys.exit(1)
keydata = base64.b64decode(open(sys.argv[1]).read().split(None)[1])
bv = BitVector.BitVector( rawbytes = keydata )
parts = []
while bv.length() > 0:
    bv_length = int(bv[:32]) # read 4 bytes for length of data
    data_bv = bv[32:32+bv_length*8] # read the data
    parts.append(data_bv)
    bv.shift_left(32+bv_length*8) # shift the starting BV and
    bv = bv[0:-32-bv_length*8] # and truncate its length
public_exponent = int(parts[1])
modulus = int(parts[2])
print "public exponent: ", public_exponent
print "modulus: ", modulus
