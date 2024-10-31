from dataclasses import dataclass, field
from typing import Literal
import logging

logger = logging.getLogger(__name__)


class HeaderValidationError(Exception):
    """Custom exception raised for header validation errors."""

    pass


@dataclass
class Header:
    magic: Literal["ANDROID BACKUP"]
    version: Literal[1, 2, 3, 4, 5]
    compressed: Literal[0, 1]
    encryption_algorithm: Literal["none", "AES-256"]

    user_key_salt: bytes = field(default=b"")
    master_key_checksum_salt: bytes = field(default=b"")
    rounds: int = field(default=0)
    user_key_iv: bytes = field(default=b"")
    master_iv_key_blob: bytes = field(default=b"")

    @property
    def is_encrypted(self):
        return self.encryption_algorithm != "none"

    @property
    def is_compressed(self):
        return self.compressed == 1
