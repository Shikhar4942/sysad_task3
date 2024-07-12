from math import gcd
from sympy import mod_inverse

def generate_keypair(a,b):
    n=a*b
    phi=(a-1)*(b-1)
    e=65537
    d=mod_inverse(e,phi)
    return ((e,n),(d,n))

def encrypt(plaintext,public_key):
    e,n=public_key
    cipher=[pow(ord(char),e,n) for char in plaintext]
    return cipher

def decrypt(cipher,private_key):
    d,n=private_key
    plaintext=''.join([chr(pow(char ,d, n))for char in cipher])
    return plaintext

def sign(message,private_key):
    d,n=private_key
    hash_value=sum(ord(char) for char in message)
    signature= pow(hash_value,d,n)
    return signature

def verify(message,signature,public_key):
    e,n=public_key
    hash_value=sum(ord(char) for char in message)
    hash_to_be_verified=pow(signature ,e,n)
    return hash_to_be_verified==hash_value

if __name__=="__main__":
    p=67
    q=53
    
    public_key,private_key=generate_keypair(p,q)
    print(public_key)
    
    plaintext="shikhargoel108123114"
    cipher=encrypt(plaintext,public_key)
    print(cipher)
    
    d_message=decrypt(cipher,private_key)
    
    message="hello"
    signature=sign(message,private_key)
    print(signature)
    
    verified=verify(message,signature,public_key)
    print(verified)