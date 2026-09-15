import hashlib
import base64
import os

class CryptoManager:
    @staticmethod
    def calculate_file_hash(file_data):
        """Calculate SHA-256 hash for file integrity"""
        return hashlib.sha256(file_data).hexdigest()
    
    @staticmethod
    def verify_file_integrity(file_data, expected_hash):
        """Verify file integrity"""
        calculated_hash = hashlib.sha256(file_data).hexdigest()
        return calculated_hash == expected_hash