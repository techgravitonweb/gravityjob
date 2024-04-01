from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import hashlib
from binascii import hexlify, unhexlify

def pad(data):
    length = 16 - (len(data) % 16)
    data += chr(length) * length
    return data

def unpad(data):
    return data[0:-ord(data[-1])]

def encrypt(plainText, workingKey):
    iv = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
    plainText = pad(plainText)
    bytearrayWorkingKey = bytearray()
    bytearrayWorkingKey.extend(map(ord, workingKey))
    
    key = hashlib.md5(bytearrayWorkingKey).digest()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    return hexlify(encryptor.update(plainText.encode("utf-8")) + encryptor.finalize()).decode('utf-8')

def decrypt(cipherText, workingKey):
    iv = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
    encryptedText = unhexlify(cipherText)
    bytearrayWorkingKey = bytearray()
    bytearrayWorkingKey.extend(map(ord, workingKey))
    
    key = hashlib.md5(bytearrayWorkingKey).digest()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    
    return unpad(decryptor.update(encryptedText) + decryptor.finalize()).decode('utf-8')
