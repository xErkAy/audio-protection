from reedsolo import RSCodec

from steganography.error_correction.error_correction_type import ErrorCorrectionType
from steganography.error_correction.generic_error_correction import GenericErrorCorrection


class NoneErrorCorrection(GenericErrorCorrection):
    """
        No actual error correction
    """

    def __init__(self):
        super().__init__(ErrorCorrectionType.NONE)

    @staticmethod
    def encode(data: bytes, redundant_bits: int) -> bytes:

        return data

    @staticmethod
    def decode(data: bytes, redundant_bits: int) -> bytes:

        return data
