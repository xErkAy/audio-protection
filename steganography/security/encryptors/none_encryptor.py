from steganography.security.encryptors.generic_encryptor import GenericEncryptor
from steganography.security.enums.encryption_type import EncryptionType


class NoneEncryptor(GenericEncryptor):

    # https://cryptography.io/en/latest/fernet/

    def __init__(self):
        super().__init__(EncryptionType.NONE)

    def encrypt(self, data: bytes) -> bytes:
        return data

    def decrypt(self, data: bytes) -> bytes:
        return data
