from Crypto.Hash import SHA512
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15

from update_daemon import settings


def is_file_verified(zip_bytes, signature):
    key = RSA.importKey(settings.public_key)
    h = SHA512.new(zip_bytes)
    try:
        pkcs1_15.new(key).verify(h, signature)
        return True
    except (ValueError, TypeError):
        return False
