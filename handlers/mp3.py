from handlers.exceptions import (
    NoDataSpecifiedException,
)
from steganography.security.encryptors.rsa_encryptor import RsaEncryptor
from steganography.wav_steganography.wav_file import WAVFile


class AudioFingerprintHandler:

    def __init__(self, path: str = None, private_key: bytes = None, password: str = None):
        if path is None or private_key is None or password is None:
            raise NoDataSpecifiedException()
        self._path = path
        self._private_key = private_key
        self._password = password
        self.wav_file = WAVFile(self._path)

    def read_fingerprint(self):
        encryptor = RsaEncryptor(password=self._password, private_key=self._private_key)
        return self.wav_file.decode(encryptor).decode('UTF-8')

    def _is_exists(self, fingerprint: str) -> bool:
        return bool(fingerprint == self.read_fingerprint())

    def set_fingerprint(self, fingerprint: str):
        # if self._is_exists(fingerprint):
        #     raise FingerprintAlreadyExists()
        encryptor = RsaEncryptor(password=self._password, private_key=self._private_key)
        self.wav_file.encode(
            bytes(fingerprint, "utf-8"),
            least_significant_bits=2,
            redundant_bits=8,
            every_nth_byte=4,
            encryptor=encryptor,
            repeat_data=False,
        )
        self.wav_file.write(filename=self._path, overwrite=True)
