from BitVector import *
import sys
import string

def cryptBreak(ciphertextFile,key_bv):
    PassPhrase = "Hopes and dreams of a million years"
    BLOCKSIZE = 16 #(D)
    numbytes = BLOCKSIZE// 8
    bv_iv = BitVector(bitlist = [0]*BLOCKSIZE)
    for i in range (0,len(PassPhrase) // numbytes):
        textstr = PassPhrase[i*numbytes:(i+1)*numbytes]
        bv_iv ^=BitVector(textstring = textstr)
    FILEIN = open(ciphertextFile) #(J)
    encrypted_bv = BitVector( hexstring = FILEIN.read() )    
    msg_decrypted_bv = BitVector( size = 0 )
    previous_decrypted_block = bv_iv #(U)
    for i in range(0, len(encrypted_bv) // BLOCKSIZE): #(V)
        bv = encrypted_bv[i*BLOCKSIZE:(i+1)*BLOCKSIZE] #(W)
        temp = bv.deep_copy() #(X)
        bv  ^= previous_decrypted_block #(Y)
        previous_decrypted_block = temp #(Z)
        bv ^= key_bv #(a)
        msg_decrypted_bv += bv
    outputtext = msg_decrypted_bv.get_text_from_bitvector() #(c)
    return outputtext
