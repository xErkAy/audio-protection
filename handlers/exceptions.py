class NoDataSpecifiedException(Exception):
    def __init__(self):
        super().__init__('No data specified')


class FileDoesNotExist(Exception):
    def __init__(self):
        super().__init__('The file does not exist')


class NotWavFileException(Exception):
    def __init__(self):
        super().__init__('This is not .wav audio file')


class FingerprintAlreadyExists(Exception):
    def __init__(self):
        super().__init__('This file has already been fingerprinted')


class InvalidPassword(Exception):
    def __init__(self):
        super().__init__('The provided password is invalid')


class ArgumentNotProvided(Exception):
    def __init__(self, argument: str):
        super().__init__(f'The argument: {argument} has not been provided')
