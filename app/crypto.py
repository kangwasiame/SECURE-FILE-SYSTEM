import hashlib


def calculate_file_hash(file_data):
    return hashlib.sha256(file_data).hexdigest()


def verify_file_integrity(file_data, expected_hash):
    return calculate_file_hash(file_data) == expected_hash
