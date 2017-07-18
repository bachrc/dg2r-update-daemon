import os

from Crypto.Hash import SHA512
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15


def is_file_verified(zip_bytes, signature):
    key_file = open("%s/rsa_public.pem" % os.path.dirname(__file__), "r")

    key = RSA.importKey(key_file.read())
    h = SHA512.new(zip_bytes)
    try:
        pkcs1_15.new(key).verify(h, signature)
        return True
    except (ValueError, TypeError):
        return False
