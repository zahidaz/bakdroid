from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

from bakdroid.header import Header

import logging
logger = logging.getLogger(__name__)


def _pbkdf2(key_materials: bytes, salt: bytes, rounds: int) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA1(),
        length=32,
        salt=salt,
        iterations=rounds,
    )
    return kdf.derive(key_materials)


def _build_key_from_password(
    password: str, user_salt: bytes, rounds: int, use_utf8: bool = False
):
    password_bytes: bytes = (
        password.encode("utf-8") if use_utf8 else password.encode("ascii")
    )
    return _pbkdf2(password_bytes, user_salt, rounds)


def _decrypt_aes(
    iv: bytes,
    key: bytes,
    blob: bytes,
) -> bytes:
    logger.debug(
        f"Key size for _decrypt_master_key_blob {len(key) = }, {len(iv) = }, {len(blob) = }"
    )
    decryptor = Cipher(algorithms.AES(key), modes.CBC(iv)).decryptor()
    return decryptor.update(blob) + decryptor.finalize()



def _extract_master_key(blob: bytes) -> tuple[bytes, bytes, bytes]:
    offset = 0
    iv_len = blob[offset]
    offset += 1
    iv = blob[offset:offset + iv_len]
    offset += iv_len

    key_len = blob[offset]
    offset += 1
    key = blob[offset:offset + key_len]
    offset += key_len

    ch_len = blob[offset]
    offset += 1
    checksum = blob[offset:offset + ch_len]
    logger.debug(f"Parsed master key blob {len(iv) = }, {len(key) = }, {len(checksum) = }")
    return iv, key, checksum


def _calculate_checksum(key: bytes, salt: bytes, rounds: int, use_utf8: bool=True) -> bytes:
    return _pbkdf2(key, salt, rounds)

def decrypt(
    header: Header,
    data: bytes,
    password: str,
) -> bytes:

    user_key = _build_key_from_password(password, header.user_key_salt, header.rounds)

    blob = _decrypt_aes(
        header.user_key_iv, user_key, header.master_iv_key_blob
    ) # decrypt master key blob

    iv, key, checksum = _extract_master_key(blob)

    calculated_checksum = _calculate_checksum(key, header.master_key_checksum_salt, header.rounds)

    # TODO: confirm checksum calculation and comparison
    if checksum != calculated_checksum:
        logger.error(f"Checksum Mismatch {checksum.hex() } != {calculated_checksum.hex()}")

    return _decrypt_aes(iv, key, data)