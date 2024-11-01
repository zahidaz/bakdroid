from io import BufferedReader
import logging
from pathlib import Path
import zlib

from bakdroid.crypto import decrypt
from bakdroid.header import Header, HeaderValidationError

logger = logging.getLogger(__name__)


class Unpacker:

    def __init__(self, in_file: Path, out_file: Path):
        self._in_file = in_file
        self._out_file = out_file

    def unpack(self, password: str = None):
        with self._in_file.open("rb") as f:
            self.header: Header = self._read_header(f)

            logger.debug(self.header)

            data = f.read()
            if self.header.is_encrypted:
                if password:
                    data = decrypt(self.header, data, password)
                else:
                    raise RuntimeError("File is encrypted but no password is provided")
            if self.header.is_compressed:
                data = zlib.decompress(data)
            self._write_out(data=data)

    def _write_out(self, data):
        with self._out_file.open("wb") as f:
            f.write(data)
        logger.info(f"File unpacked to {self._out_file.absolute()}")

    def _read_header(self, data: BufferedReader) -> Header:
        try:
            header_lines = [data.readline().decode("ascii").strip() for _ in range(4)]
            header = Header(
                magic=header_lines[0],
                version=int(header_lines[1]),
                compressed=int(header_lines[2]),
                encryption_algorithm=header_lines[3],
            )

            if header.encryption_algorithm != "none":
                header_lines += [
                    data.readline().decode("ascii").strip() for _ in range(5)
                ]

                header.user_key_salt = bytes.fromhex(header_lines[4])
                header.master_key_checksum_salt = bytes.fromhex(header_lines[5])
                header.rounds = int(header_lines[6])
                header.user_key_iv = bytes.fromhex(header_lines[7])
                header.master_iv_key_blob = bytes.fromhex(header_lines[8])
            return header

        except (IndexError, ValueError, TypeError) as e:
            logger.error("Invalid header format or data type encountered.", exc_info=e)
            raise HeaderValidationError("Invalid header format.") from e
