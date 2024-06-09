from getpass import getpass

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa

from steganography.security.encryptors.generic_encryptor import GenericEncryptor
from steganography.security.enums.encryption_type import EncryptionType


class RsaEncryptorWithFile(GenericEncryptor):

    # https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/

    def __init__(self, decryption: bool, is_test: bool = False):
        super().__init__(EncryptionType.RSA)

        if decryption:

            private_key_password = getpass(
                'Please enter a password for the private key (leave empty if there is none): ')

            self.__private_key = self.__load_private_key(private_key_password)
            self.__public_key = self.__private_key.public_key()

        else:
            self.__private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
            self.__public_key = self.__private_key.public_key()

            if not is_test:
                private_key_password = getpass('Please enter a password for the private key (empty = no encryption): ')
                self.__save_keys(private_key_password)

    def encrypt(self, data: bytes) -> bytes:
        encrypted_data = self.__public_key.encrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return encrypted_data

    def decrypt(self, data: bytes) -> bytes:
        encrypted_data = self.__private_key.decrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return encrypted_data

    def __save_keys(self, password: str):

        if password:
            encryption = serialization.BestAvailableEncryption(password.encode('UTF-8'))
        else:
            encryption = serialization.NoEncryption()

        private_pem = self.__private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=encryption
        )

        self.__save_key('private_key', private_pem)

        public_pem = self.__public_key.public_bytes(
            encoding = serialization.Encoding.PEM,
            format = serialization.PublicFormat.SubjectPublicKeyInfo
        )

        self.__save_key('public_key', public_pem)

    @staticmethod
    def __save_key(filename: str, data: bytes):
        with open(f'{filename}.pem', 'wb') as f:
            f.write(data)

    @staticmethod
    def __load_private_key(password_input):
        if password_input:
            password = password_input.encode('UTF-8')
        else:
            password = None

        with open("private_key.pem", "rb") as key_file:

            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=password,
            )

            return private_key


class RsaEncryptor(GenericEncryptor):

    # https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/

    def __init__(self, password: str = None, create: bool = False, private_key: bytes = None):
        super().__init__(EncryptionType.RSA)

        if create:
            self.__private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
            self.__public_key = self.__private_key.public_key()
        else:
            self.__private_key = self.__load_private_key(password, private_key)
            self.__public_key = self.__private_key.public_key()

        self.__save_keys(password)

    def encrypt(self, data: bytes) -> bytes:
        encrypted_data = self.__public_key.encrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return encrypted_data

    def decrypt(self, data: bytes) -> bytes:
        encrypted_data = self.__private_key.decrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return encrypted_data

    def __save_keys(self, password: str):
        encryption = serialization.BestAvailableEncryption(password.encode('UTF-8'))
        self.__private_pem = self.__private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=encryption
        )
        self.__public_pem = self.__public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    def get_keys(self) -> [bytes, bytes]:
        return [self.__public_pem, self.__private_pem]

    @staticmethod
    def __load_private_key(password_input: str, private_key: bytes):
        password = password_input.encode('UTF-8')
        key = serialization.load_pem_private_key(
            private_key,
            password=password,
        )
        return key
