import hashlib


def H(m):
    return hashlib.sha512(m).digest() 

if __name__ == "__main__":
   print(H("input.txt"))
