#!/usr/bin/env python3

# Homework Number: 6
# Name: PO YU HAUNG
# ECN Login: huan1338
# Due Date: March 3, 2020

import sys
import os
from PrimeGenerator import PrimeGenerator
from BitVector import *

def gcd(a1,a2):
    while(a2):
        a1,a2 = a2,a1%a2
    return a1

def generate_pq(pfile, qfile):
    e = 65537

    cond = 1
    while(cond):
        p = PrimeGenerator(bits=128).findPrime()
        q = PrimeGenerator(bits=128).findPrime()
        pbv = BitVector(size = 128,intVal = p)
        qbv = BitVector(size = 128,intVal = q)
        if(p!=q) or (pbv[0] != 0 or qbv[0] != 0) or (gcd((p-1),e) != 1 or gcd((q-1),e) != 1):
            cond = 0

            
    open(pfile, "w").write(str(p))
    open(qfile, "w").write(str(q))
        
def encrypt(mesfile, pfile, qfile, output_file):

    e = 65537

    inp_bv = BitVector(filename=mesfile)
    out_file = open(output_file,"w")
    
    p = int(open(pfile,'r').read())
    q = int(open(qfile,'r').read())

    ebv = BitVector(intVal = e)
    pq = (p - 1)*(q - 1)
    dbv = ebv.multiplicative_inverse(BitVector(intVal = pq,size = 256))
    d = dbv.int_val()

    open("d.txt", "w").write(str(d))

    while inp_bv.more_to_read:
        
        one_bv = inp_bv.read_bits_from_file(128)
        one_bv.pad_from_right(128 - one_bv.length())
        one_bv.pad_from_left(128)
##        print(one_bv)

        temp = pow(one_bv.int_val(),e,p*q)
        
        hextext = BitVector(intVal=temp,size = 256).get_hex_string_from_bitvector()
##        print(hextext)
        out_file.write(hextext)
        
def decrypt(input_file, pfile, qfile, output_file):
    e = 65537
    p = int(open(pfile,'r').read())
    q = int(open(qfile,'r').read())
    d = int(open("d.txt",'r').read())

    inp_bv = BitVector(filename = input_file)
    out_file = open(output_file,'wb')
    while inp_bv.more_to_read:

        one_bv = inp_bv.read_bits_from_file(512)
        one_bv = BitVector(hexstring = one_bv.get_bitvector_in_ascii())
        
##        one_bv.int_val(),d,p*q,p,q
        
        #pow(one_bv.int_val(),(d % (q-1)),q)

        qinv = BitVector(intVal=q).multiplicative_inverse(BitVector(intVal=p)).int_val()
        time_p = qinv * q
        
        pinv = BitVector(intVal=p).multiplicative_inverse(BitVector(intVal=q)).int_val()
        time_q = pinv * p
        
        exp_mod = ((pow(one_bv.int_val(),(d % (p-1)),p) * time_p)+(pow(one_bv.int_val(),(d % (q-1)),q) * time_q)) % (p*q)

        dec_bv = BitVector(intVal=exp_mod,size = 128)
##        print(dec_bv)
        dec_bv.write_to_file(out_file)
    out_file.close()
    return
        
    
if __name__ == "__main__":
    argument = sys.argv[1]
    if argument == '-e':
        encrypt(sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
    if argument == '-d':
        decrypt(sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
    if argument == '-g':
        generate_pq(sys.argv[2],sys.argv[3])
        
