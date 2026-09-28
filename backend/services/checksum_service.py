"""
Checksum validation for document uploads.
Covers CN Experiment 5: Error detection and correction (CRC, Checksum).
"""
import hashlib
import binascii


class ChecksumService:
    @staticmethod
    def sha256(data: bytes) -> str:
        """SHA-256 hash for file integrity verification."""
        return hashlib.sha256(data).hexdigest()

    @staticmethod
    def crc32(data: bytes) -> int:
        """CRC-32 checksum. CN Exp 5."""
        return binascii.crc32(data) & 0xFFFFFFFF

    @staticmethod
    def internet_checksum(data: bytes) -> int:
        """
        Internet checksum as used in TCP/UDP headers (RFC 1071).
        CN Exp 5: Checksum implementation.
        """
        if len(data) % 2 == 1:
            data += b'\x00'
        total = 0
        for i in range(0, len(data), 2):
            word = (data[i] << 8) + data[i + 1]
            total += word
        while total >> 16:
            total = (total & 0xFFFF) + (total >> 16)
        return ~total & 0xFFFF

    @staticmethod
    def verify_integrity(data: bytes, expected_hash: str) -> bool:
        """Verify file hasn't been corrupted during upload."""
        return hashlib.sha256(data).hexdigest() == expected_hash
