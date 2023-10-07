from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
# from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
# import secrets
import base64
import random
import string


def keygen():
    backend = default_backend()

    # Generate a new rsa key pair
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=backend
    )

    # Get public key in PEM format
    public_key = private_key.public_key()
    pem_public_key = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Generate a random passphrase and salt
    # passphrase = secrets.token_bytes(16)
    # salt = secrets.token_bytes(16)

    # Derive a key from passphrase and salt
    # kdf = PBKDF2HMAC(
    #    algorithm=hashes.SHA256(),
    #    length=32,
    #    salt=salt,
    #    iterations=100000,
    #    backend=backend
    # )
    # key = kdf.derive(passphrase)

    # Get private key in PEM format
    pem_private_key = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    return pem_public_key, pem_private_key


pub_key, priv_key = keygen()

pub64 = base64.b64encode(pub_key).decode("utf-8")
priv64 = base64.b64encode(priv_key).decode("utf-8")

print(f"{pub64}\n\n{priv64}")

characters = string.ascii_letters + string.digits
name = ''.join(random.choice(characters) for _ in range(8))
keys_path = os.path.join(os.getcwd(), "Key Files", f"Key_File_{name}.txt")
if not os.path.isdir(os.path.join(os.getcwd(), "Key Files")):
    os.mkdir(os.path.join(os.getcwd(), "Key Files"))
with open(keys_path, "w") as f:
    f.write(f"\tPUBLIC KEY\n{pub64}\n\tPRIVATE KEY\n{priv64}\n\nKey Id = {name}")

print(f"Keys written to file:\n\t{keys_path}\nKey Id = {name}")
