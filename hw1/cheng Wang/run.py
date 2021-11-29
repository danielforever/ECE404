import sys
import cryptBreak
from BitVector import *
for k in range(0,2**16):
    key_bv = BitVector(intVal=k, size=16)
    decryptedMessage = cryptBreak.cryptBreak("encrypted.txt", key_bv)
    if "Mark Twain" in decryptedMessage:
        print("Encryption Broken!")
        print(decryptedMessage)
        sys.exit()
    else:
        print("Not decrypted yet")



