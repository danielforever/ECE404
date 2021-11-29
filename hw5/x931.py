
#!/usr/bin/env python3

# Homework Number: 5
# Name: PO YU HAUNG
# ECN Login: huan1338
# Due Date: February 24, 2020

import sys
import io
##import argparse
import numpy as np
from BitVector import *
##import x931


def genTables(cond):
    AES_modulus = BitVector(bitstring="100011011")
    c = BitVector(bitstring="001100011")
    d = BitVector(bitstring="00000101")
    subBytesTable = [] # SBox for encryption
    invSubBytesTable = []
    for i in range(0, 256):
# For the encryption SBox
        a = BitVector(intVal = i, size=8).gf_MI(AES_modulus, 8) if i != 0 else BitVector(intVal=0)
# For bit scrambling for the encryption SBox entries:
        a1,a2,a3,a4 = [a.deep_copy() for x in range(4)]
        a ^= (a1 >> 4) ^ (a2 >> 5) ^ (a3 >> 6) ^ (a4 >> 7) ^ c
        subBytesTable.append(int(a))
        # For the decryption Sbox:
        b = BitVector(intVal = i, size=8)
        # For bit scrambling for the decryption SBox entries:
        b1,b2,b3 = [b.deep_copy() for x in range(3)]
        b = (b1 >> 2) ^ (b2 >> 5) ^ (b3 >> 7) ^ d
        check = b.gf_MI(AES_modulus, 8)
        b = check if isinstance(check, BitVector) else 0
        invSubBytesTable.append(int(b))

    if (cond):
        return subBytesTable
    else:
        return invSubBytesTable

    
def gen_key_schedule_256(key_bv):
    byte_sub_table = gen_subbytes_table()
    # We need 60 keywords (each keyword consists of 32 bits) in the key schedule for
    # 256 bit AES. The 256-bit AES uses the first four keywords to xor the input
    # block with. Subsequently, each of the 14 rounds uses 4 keywords from the key
    # schedule. We will store all 60 keywords in the following list:
    key_words = [None for i in range(60)]
    round_constant = BitVector(intVal = 0x01, size=8)
    for i in range(8):
        key_words[i] = key_bv[i*32 : i*32 + 32]
    for i in range(8,60):
        if i%8 == 0:
            kwd, round_constant = gee(key_words[i-1], round_constant, byte_sub_table)
            key_words[i] = key_words[i-8] ^ kwd
        elif (i - (i//8)*8) < 4:
            key_words[i] = key_words[i-8] ^ key_words[i-1]
        elif (i - (i//8)*8) == 4:
            key_words[i] = BitVector(size = 0)
            for j in range(4):
                key_words[i] += BitVector(intVal =
                    byte_sub_table[key_words[i-1][8*j:8*j+8].intValue()], size = 8)
            key_words[i] ^= key_words[i-8]
        elif ((i - (i//8)*8) > 4) and ((i - (i//8)*8) < 8):
            key_words[i] = key_words[i-8] ^ key_words[i-1]
        else:
            sys.exit("error in key scheduling algo for i = %d" % i)
    return key_words


def gen_subbytes_table():
    subBytesTable = []
    AES_modulus = BitVector(bitstring="100011011")
    c = BitVector(bitstring="01100011")
    for i in range(0, 256):
        a = BitVector(intVal = i, size=8).gf_MI(AES_modulus, 8) if i != 0 else BitVector(intVal=0)
        a1,a2,a3,a4 = [a.deep_copy() for x in range(4)]
        a ^= (a1 >> 4) ^ (a2 >> 5) ^ (a3 >> 6) ^ (a4 >> 7) ^ c
        subBytesTable.append(int(a))
    return subBytesTable


def gee(keyword, round_constant, byte_sub_table):
    AES_modulus = BitVector(bitstring="100011011")
##    print(keyword,"here")
    rotated_word = keyword.deep_copy()
    rotated_word << 8
    newword = BitVector(size = 0)
    for i in range(4):
        newword += BitVector(intVal = byte_sub_table[rotated_word[8*i:8*i+8].intValue()], size = 8)
    newword[:8] ^= round_constant
    round_constant = round_constant.gf_multiply_modular(BitVector(intVal = 0x02), AES_modulus, 8)
    return newword, round_constant


def shiftrowleft(statearray):
    temp = [0,0,0,0]
    flag = 0
    for i in range(1,4):
        while(flag<i):
            statearray[0][i],statearray[1][i],statearray[2][i],statearray[3][i] = leftRotate([statearray[0][i],statearray[1][i],statearray[2][i],statearray[3][i]],4)
            flag=flag+1
        flag=0
    return statearray
            
                
            
def leftRotate(line,n):
    temp = line[0]
    for i in range(n-1):
        line[i] = line [i+1]
    line[n-1] = temp
    return line
    


def mixcolumn(inputarray):
    statearray = [[0 for x in range(4)] for x in range(4)]
    AES = BitVector(bitstring='100011011')
    two = BitVector(bitstring = '00000010')
    thr = BitVector(bitstring = '00000011')
    for i in range(4):
        fir_col = inputarray[i][0].gf_multiply_modular(two,AES,8)
        sec_col = inputarray[i][1].gf_multiply_modular(thr,AES,8)
        fir_col_1 = inputarray[i][1].gf_multiply_modular(two,AES,8)
        sec_col_2 = inputarray[i][2].gf_multiply_modular(thr,AES,8)
        fir_col_3 = inputarray[i][2].gf_multiply_modular(two,AES,8)
        sec_col_4 = inputarray[i][3].gf_multiply_modular(thr,AES,8)
        fir_col_5 = inputarray[i][3].gf_multiply_modular(two,AES,8)
        sec_col_6 = inputarray[i][0].gf_multiply_modular(thr,AES,8)
        statearray[i][0] = fir_col ^ sec_col ^ inputarray[i][2] ^ inputarray[i][3]
        statearray[i][1] = fir_col_1 ^ sec_col_2 ^ inputarray[i][0] ^ inputarray[i][3]
        statearray[i][2] = fir_col_3 ^ sec_col_4 ^ inputarray[i][1] ^ inputarray[i][0]
        statearray[i][3] = fir_col_5 ^ sec_col_6 ^ inputarray[i][2] ^ inputarray[i][1]
    return statearray
      
        


def encrypt(message,key):
    return_string=BitVector(size=0)
    f_key = open(key,"r")
    key = BitVector(textstring=f_key.read().strip())
    bv = message
    a = []
    round_keys = [None for i in range(15)]

    key_words = gen_key_schedule_256(key)
    subBytesTable = genTables(True)
    statearray = [[0 for x in range(4)] for x in range(4)]
    for i in range(15):
        round_keys[i] = (key_words[i*4] + key_words[i*4+1] + key_words[i*4+2] + key_words[i*4+3])
##    print(round_keys[0])
##    with open(encrypted,"w") as f:
    m=0
    for l in range(int(len(bv)/128)):
        bitvec = bv[m:m+128]
        m = m+128
##        bitvec = bv.read_bits_from_file(128)
##        if (len(bitvec)<128):
##            bitvec.pad_from_right(128-len(bitvec))
                
            #first round xor with key##################
        bitvec = bitvec ^ (round_keys[0])
        
        for k in range(14):
            z=0
            for j in range(4):
                for i in range(4):
                    statearray[j][i] = bitvec[z:z+8]
                    z = z+8
                # substitution bytes
            for i in range(4):
                for j in range(4):
                    statearray[i][j] = BitVector(intVal = subBytesTable[int(statearray[i][j])], size=8)

                # shift rows
            statearray = shiftrowleft(statearray)

                # Mix Column
            if (k != 13):
                statearray = mixcolumn(statearray)
                
            bitvec = BitVector(size = 0)
            for j in range(4):
                for i in range(4):
                    bitvec = bitvec + statearray[j][i]
                    z = z+8

                #Add roundkey
            bitvec = bitvec ^ (round_keys[k+1])
        return_string +=bitvec
    return return_string 





def x931(v0,dt,totalNum,key_file):
    random_num = list()
    V_val = v0
    dt_encrypted = encrypt(dt,key_file)
    
    for i in range(totalNum):
        
        dt_encrypted_xor = dt_encrypted ^ V_val

        ran_val = encrypt(dt_encrypted_xor,key_file)


        random_num.append(ran_val)

        V_val = encrypt((dt_encrypted ^ ran_val),key_file)

    return random_num 





