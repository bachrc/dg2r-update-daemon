def generate_rsa(passphrase, bits=2048):
    """
    Generate an RSA keypair with an exponent of 65537 in PEM format
    param: bits The key length in bits
    Return private key and public key
    """

    from Crypto.PublicKey import RSA
    new_key = RSA.generate(bits, e=65537)
    public_key = new_key.publickey().exportKey("PEM")
    private_key = new_key.exportKey("PEM", passphrase=passphrase)
    return private_key, public_key


if __name__ == '__main__':
    passphrase = input("Entrez la passphrase : ").rstrip('\n')

    private_key, public_key = generate_rsa(passphrase)

    with open("rsa_public.pem", "wb") as f:
        f.write(public_key)

    with open("rsa_private.pem", "wb") as f:
        f.write(private_key)
