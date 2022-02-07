#!/bin/python3.10
import sys
import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def hash_key():
    return hashlib.sha256(bytes(input("key:"), "utf8")).digest()

def decrypt_cbc(enc):
    iv = enc[:AES.block_size]
    cipher = AES.new(hash_key(), AES.MODE_CBC, iv)
    data = (cipher.decrypt(enc[AES.block_size:]))
    padding_bytes = data[-1]
    return data[:-padding_bytes]

def encrypt_cbc(raw):
    raw = raw + bytes(((16 - len(raw) % 16) * chr(16 - len(raw) % 16)), 'utf8')
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new( hash_key(), AES.MODE_CBC,iv)
    return (iv + cipher.encrypt(raw))

def do_enc(filename):
    with open(filename + '.enc', 'wb') as fout:
        with open(filename, "rb") as fin:
            while (data := fin.read(chunk)):
                fout.write(encrypt_cbc(data))

def do_dec(filename):
    with open(filename + '.dec', 'wb') as fout:
        with open(filename, "rb") as fin:
            while (data := fin.read(chunk+32)):
                fout.write(decrypt_cbc(data))

def main():
    if len(sys.argv) == 3:
        global chunk
        chunk = (1024*1024*10)  # 10MB CHUNK
        match sys.argv[1]:
            case "-enc":
                do_enc(sys.argv[2])
            case "-dec":
                do_dec(sys.argv[2])
            case _:
                print("usage: qdfc.py [-enc|-dec] <file>")
    else:
        print("usage: qdfc.py [-enc|-dec] <file>")

if __name__ == "__main__":
    main()
