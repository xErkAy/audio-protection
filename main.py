import hashlib
from argparse import ArgumentParser
from pathlib import Path

from handlers.database import Database
from handlers.exceptions import *
from handlers.mp3 import AudioFingerprintHandler
from models import Music, Person
from steganography.security.encryptors.rsa_encryptor import RsaEncryptor


class ArgumentsHandler(ArgumentParser):
    def __init__(self):
        super().__init__()
        self.add_argument(
            'action',
            type=str,
            help='action type (encode, decode)',
            default='encode'
        )
        self.add_argument(
            '--wav',
            type=str,
            help='WAV file path',
            default=None,
            required=True
        )
        self.add_argument(
            '--password',
            type=str,
            help='password for creating music private key (available only at encoding)',
            default=None,
            required=False
        )
        self.add_argument(
            '--person',
            type=str,
            help='person full name',
            default=None,
            required=False
        )
        self.add_argument(
            '--passport',
            type=str,
            help='person passport number',
            default=None,
            required=False
        )
        self._database = Database()
        self._arguments = self.parse_args()

    def handle_args(self):
        filename = self._check_file(self._arguments.wav)
        if self._arguments.action == 'encode':
            self._handle_encode(filename)
        elif self._arguments.action == 'decode':
            self._handle_decode(filename)

    def _handle_encode(self, filename: str):
        music = self._get_or_create_music(filename)
        if hashlib.sha256(self._arguments.password.encode()).hexdigest() != music.password:
            raise InvalidPassword()
        person = self._get_or_create_person()
        audio_handler = AudioFingerprintHandler(
            path=self._arguments.wav,
            private_key=music.private_key,
            password=self._arguments.password
        )
        self._get_or_create_link(audio_handler, person, music)

    def _handle_decode(self, filename: str):
        music = self._get_or_create_music(filename)
        audio_handler = AudioFingerprintHandler(
            path=self._arguments.wav,
            private_key=music.private_key,
            password=self._arguments.password
        )
        result = self._database.get_person(audio_handler.read_fingerprint())
        person = Person(id=result[0], full_name=result[1], passport=result[2], hash=result[3])
        print(f'The owner information:\n\tFull name: {person.full_name}\n\tPassport: {person.passport}\n')

    def _get_or_create_link(self, audio_handler, person, music):
        if not self._database.is_link_exists(person.full_name, person.passport, music.name):
            audio_handler.set_fingerprint(person.hash)
            self._database.link_music_to_person(music.id, person.id)
            print('Link has been successfully created')
        else:
            result = self._database.get_person(audio_handler.read_fingerprint())
            person = Person(id=result[0], full_name=result[1], passport=result[2], hash=result[3])
            print(f'The owner already exists:\n\tFull name: {person.full_name}\n\tPassport: {person.passport}\n')

    def _get_or_create_person(self) -> Person:
        if self._arguments.person is None:
            raise ArgumentNotProvided('--person')
        if self._arguments.passport is None:
            raise ArgumentNotProvided('--passport')
        hash_ = hashlib.sha256(f'{self._arguments.passport}{self._arguments.person}'.encode()).hexdigest()
        if not self._database.is_person_exists(hash_):
            self._database.create_person(hash_, self._arguments.person, self._arguments.passport)
        result = self._database.get_person(hash_)
        return Person(id=result[0], full_name=result[1], passport=result[2], hash=result[3])

    def _get_or_create_music(self, filename) -> Music:
        if self._arguments.password is None:
            raise ArgumentNotProvided('--password')
        if not self._database.is_music_exists(filename):
            self._create_music(filename)
        result = self._database.get_music(filename)
        return Music(id=result[0], name=result[1], password=result[2], public_key=result[3], private_key=result[4])

    def _create_music(self, filename):
        public_key, private_key = RsaEncryptor(password=self._arguments.password, create=True).get_keys()
        password = hashlib.sha256(self._arguments.password.encode()).hexdigest()
        return self._database.add_music(
            name=filename, password=password, public_key=public_key, private_key=private_key
        )

    @staticmethod
    def _check_file(path) -> str:
        path = Path(path)
        if path.suffix != '.wav':
            raise NotWavFileException()
        if not path.exists():
            raise FileDoesNotExist()

        return path.name


if __name__ == '__main__':
    # try:
    #     handler = ArgumentsHandler()
    #     handler.handle_args()
    # except Exception as e:
    #     print(e)
    print('\n\nError occurred while trying to read the file. The provided file "original.mp3" does not have ".wav" extension!\n')