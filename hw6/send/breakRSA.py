#!/usr/bin/env python3

# Homework Number: 6
# Name: PO YU HAUNG
# ECN Login: huan1338
# Due Date: March 3, 2020

import sys
import os
import numpy as np
from PrimeGenerator import PrimeGenerator
from BitVector import *


def solve_pRoot(p, x): #O(lgn) solution
	'''
	Finds pth root of an integer x.  Uses Binary Search logic.	Starts
	with a lower bound l and go up until upper bound u.	Breaks the problem into
	halves depending on the search logic.  The search logic says whether the mid
	(which is the mid value of l and u) raised to the power to p is less than x or
	it is greater than x.	Once we reach a mid that when raised to the power p is
	equal to x, we return mid + 1. 

	Author: Shayan Akbar 
		sakbar at purdue edu

	'''

	#Upper bound u is set to as follows:
	#We start with the 2**0 and keep increasing the power so that u is 2**1, 2**2, ...
	#Until we hit a u such that u**p is > x
	u = 1
	while u ** p <= x: u *= 2

	#Lower bound set to half of upper bound
	l = u // 2

	#Keep the search going until upper u becomes less than lower l
	while l < u:
		mid = (l + u) // 2
		mid_pth = mid ** p
		if l < mid and mid_pth < x:
			l = mid
		elif u > mid and mid_pth > x:
			u = mid
		else:
			# Found perfect pth root.
			return mid
	return mid + 1

def gcd(a1,a2):
    while(a2):
        a1,a2 = a2,a1%a2
    return a1

def generate_key(e):

    cond = 0
    while not (cond):
        p = PrimeGenerator(bits=128).findPrime()
        q = PrimeGenerator(bits=128).findPrime()
        pbv = BitVector(size = 128,intVal = p)
        qbv = BitVector(size = 128,intVal = q)
        cond = 1
        if(p==q) or (pbv[0] == 0 or qbv[0] == 0) or (gcd((p-1),e) != 1 or gcd((q-1),e) != 1):
            cond = 0

    d = BitVector(intVal = e).multiplicative_inverse(BitVector(intVal = p * q)).int_val()

    return e,d,p*q


def encrypt(mesfile, enc1, enc2, enc3, n_1_2_3, keylist):
    enclist = [enc1, enc2, enc3]
##    n=[]
##    with open(n_1_2_3, "r") as f:
##        for line in f:
##            n.append(line.strip())
##    f.close()
##    print(n[0])
##    print(n[1])
##    print(n[2])
##    out_file = open("encrypted.txt", "w")
    out_pub_file = open(n_1_2_3, "w")
    for i in range(3):
        e, d, n = keylist[i]
##        print(n)
        out_pub_file.write(str(n)+"\n")
##        print(e,d,n)
        enc = enclist[i]
        out_file = open(enc, "w")
        inp_bv = BitVector(filename = mesfile)
        
        while(inp_bv.more_to_read):
            one_bv = inp_bv.read_bits_from_file(128)
            one_bv.pad_from_right(128 - one_bv.length())
            one_bv.pad_from_left(128)

            enc_bv = BitVector(intVal = pow(one_bv.int_val(),e,int(n)),size = 256)

            hex_text = enc_bv.get_hex_string_from_bitvector()
            out_file.write(hex_text)
##        print(enc)
    return



def get_m_3(one_bv, two_bv, three_bv, n1, n2, n3, n1n2n3):

    m1_bv = BitVector(intVal= (n2 * n3))
    m1_inv = m1_bv.multiplicative_inverse(BitVector(intVal= n1)).int_val()
    m1_res = m1_inv * int(m1_bv) * int(one_bv)
    
    m2_bv = BitVector(intVal= n1 * n3)
    m2_inv = m2_bv.multiplicative_inverse(BitVector(intVal= n2)).int_val()
    m2_res = m2_inv * int(m2_bv) * int(two_bv)
    
    m3_bv = BitVector(intVal= n1 * n2)
    m3_inv = m3_bv.multiplicative_inverse(BitVector(intVal= n3)).int_val()
    m3_res = m3_inv * int(m3_bv) * int(three_bv)


    return ((m1_res + m2_res + m3_res) % n1n2n3)

def decrypt(enc1, enc2, enc3, n_1_2_3, crack):
    f_input1 = open(enc1,"r")
    f_input2 = open(enc2,"r")
    f_input3 = open(enc3,"r")

    enc1_bv = BitVector(hexstring = f_input1.read())
    enc2_bv = BitVector(hexstring = f_input2.read())
    enc3_bv = BitVector(hexstring = f_input3.read())
    n=[]
    with open(n_1_2_3, "r") as f:
        for line in f:
            n.append(line.strip())
    f.close()
##    print(n[0])
##    print(n[1])
##    print(n[2])
    out_file = open(crack, "wb")
    file = [enc1_bv, enc2_bv, enc3_bv]
    m=0
    for l in range(int(len(enc1_bv)/256)):
        
##        print("check")
        one_bv = enc1_bv[m:m+256]
##        print(one_bv)
        two_bv = enc2_bv[m:m+256]
        three_bv = enc3_bv[m:m+256]
##        print("check1")
        cube_m = get_m_3( one_bv, two_bv, three_bv, int(n[0]), int(n[1]), int(n[2]), int(n[0])* int(n[1])* int(n[2]) )
##        print(int(solve_pRoot(3,cube_m)))
##        print("check2")
##        ans = solve_pRoot(3,cube_m)
##        print("check3")
        m_bv = BitVector(intVal=solve_pRoot(3,cube_m), size=128)
##        print("check4")
        m_bv.write_to_file(out_file)
        m = m+256

        
            
if __name__ == "__main__":
    
    keylist=list()
    
    for i in range(3):
        keylist.append(generate_key(3))
    
    argument = sys.argv[1]
    if argument == '-e':
        encrypt(sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6],keylist)
    if argument == '-c':
        decrypt(sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6])
