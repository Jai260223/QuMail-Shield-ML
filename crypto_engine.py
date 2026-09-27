import os
import secrets
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class CryptoEngine:
    @staticmethod
    def generate_quantum_seed(size_bytes: int = 32) -> bytes:
        """Simulates high-entropy Quantum Random Number Generation (QRNG)."""
        return secrets.token_bytes(size_bytes)

    @staticmethod
    def encrypt_level2_aes(plaintext: bytes, key: bytes):
        """Level 2: Quantum-seeded authenticated AES-256-GCM."""
        aesgcm = AESGCM(key)
        nonce = os.urandom(12)  # Standard 96-bit GCM IV
        ciphertext = aesgcm.encrypt(nonce, plaintext, None)
        return nonce, ciphertext

    @staticmethod
    def decrypt_level2_aes(ciphertext: bytes, key: bytes, nonce: bytes) -> bytes:
        """Level 2 Decryption with integrity verification."""
        aesgcm = AESGCM(key)
        return aesgcm.decrypt(nonce, ciphertext, None)

    @staticmethod
    def encrypt_level3_otp(plaintext: bytes, key: bytes) -> bytes:
        """Level 3: Information-Theoretic One-Time Pad (XOR)."""
        if len(key) < len(plaintext):
            raise ValueError("OTP key length must be >= plaintext length!")
        return bytes([p ^ k for p, k in zip(plaintext, key[:len(plaintext)])])

    @staticmethod
    def decrypt_level3_otp(ciphertext: bytes, key: bytes) -> bytes:
        """Level 3 Decryption (Symmetric XOR Stream)."""
        return CryptoEngine.encrypt_level3_otp(ciphertext, key)