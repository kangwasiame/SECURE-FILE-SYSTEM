import hashlib
import os

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


ENCRYPTED_FILE_MARKER = b'VLT1'


def _encryption_key(secret):
    return hashlib.sha256(secret.encode('utf-8')).digest()


def encrypt_file(file_data, secret):
    nonce = os.urandom(12)
    encrypted = AESGCM(_encryption_key(secret)).encrypt(nonce, file_data, ENCRYPTED_FILE_MARKER)
    return ENCRYPTED_FILE_MARKER + nonce + encrypted


def decrypt_file(encrypted_data, secret):
    if not encrypted_data.startswith(ENCRYPTED_FILE_MARKER):
        raise ValueError('Unsupported encrypted file format.')
    nonce_start = len(ENCRYPTED_FILE_MARKER)
    nonce = encrypted_data[nonce_start:nonce_start + 12]
    ciphertext = encrypted_data[nonce_start + 12:]
    if len(nonce) != 12 or not ciphertext:
        raise ValueError('Encrypted file is incomplete.')
    try:
        return AESGCM(_encryption_key(secret)).decrypt(nonce, ciphertext, ENCRYPTED_FILE_MARKER)
    except InvalidTag as error:
        raise ValueError('Encrypted file authentication failed.') from error


def calculate_file_hash(file_data):
    return hashlib.sha256(file_data).hexdigest()


def verify_file_integrity(file_data, expected_hash):
    return calculate_file_hash(file_data) == expected_hash
