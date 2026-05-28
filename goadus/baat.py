# SPDX-PackageName: rf-tools
# SPDX-PackageSupplier: Ryan Finnie <ryan@finnie.org>
# SPDX-PackageDownloadLocation: https://forge.colobox.com/rfinnie/rf-tools
# SPDX-FileComment: Better-Assembled Access Tokens
# SPDX-FileCopyrightText: © 2023 Ryan Finnie <ryan@finnie.org>
# SPDX-License-Identifier: MIT

# https://www.finnie.org/2023/10/18/better-assembled-access-tokens/

import argparse
import base64
import logging
import os
import random
import sys
import zlib


class BAAT:
    version = 1
    prefix = "bat"
    payload = None
    crc = None

    class Error(ValueError):
        pass

    class LoadError(Error):
        pass

    class DumpError(Error):
        pass

    def __init__(self, baat=None, prefix="bat"):
        self.prefix = prefix
        if baat is not None:
            self.load(str(baat))

    def __str__(self):
        return self.dump()

    def __eq__(self, other):
        return str(self) == str(other)

    def __repr__(self):
        return "<{}.{} object at {}: version {}, prefix {}, payload {}, crc {}>".format(
            self.__class__.__module__,
            self.__class__.__name__,
            hex(id(self)),
            self.version,
            self.prefix,
            self.payload,
            self.crc,
        )

    def dump(self):
        if self.payload is None:
            self.payload = bytes([random.randint(0, 255) for _ in range(18)])

        magic = b"\x8f\xa5"
        if self.version != 1:
            raise self.DumpError("Invalid version")
        if len(self.payload) != 18:
            raise self.DumpError("Invalid payload size")
        if not self.prefix.isalnum():
            raise self.DumpError("Invalid prefix (non-alphanumeric character)")
        self.prefix = self.prefix.lower()
        baat_ver = bytes([self.version])
        self.crc = zlib.crc32(self.prefix.encode("utf-8") + self.payload + magic + baat_ver) & 0xFFFFFFFF
        wrapped_data_b32 = base64.b32encode(self.payload + magic + baat_ver + self.crc.to_bytes(4))
        return (self.prefix + "_" + wrapped_data_b32.decode("utf-8")).lower()

    def load(self, baat):
        parts = baat.split("_")
        if len(parts) != 2:
            raise self.LoadError("Malformed")
        prefix = parts[0].lower()
        wrapped_data = base64.b32decode(parts[1].upper())
        if len(wrapped_data) < 7:
            raise self.LoadError("Impossible length")
        magic = wrapped_data[-7:-5]
        baat_ver = wrapped_data[-5:-4]
        if magic != b"\x8f\xa5":
            raise self.LoadError("Invalid magic number")
        if baat_ver != b"\x01":
            raise self.LoadError("Invalid BAAT version")
        if len(wrapped_data) != 25:
            raise self.LoadError("Wrong length")
        payload = wrapped_data[0:18]
        crc = zlib.crc32(prefix.encode("utf-8") + payload + magic + baat_ver) & 0xFFFFFFFF
        if wrapped_data[-4:] != crc.to_bytes(4):
            raise self.LoadError("Invalid CRC")
        self.version = int.from_bytes(baat_ver)
        self.prefix = prefix
        self.payload = payload
        self.crc = crc


class BAATProgram:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def parse_args(self, argv=None):
        if argv is None:
            argv = sys.argv

        parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            prog=os.path.basename(argv[0]),
        )

        parser.add_argument(
            "--prefix",
            type=str,
            default="bat",
            help="Token prefix",
        )
        parser.add_argument(
            "--count",
            type=int,
            default="1",
            help="Number of BAATs to generate",
        )
        parser.add_argument(
            "--validate",
            type=str,
            help="Verify a BAAT is valid",
        )
        parser.add_argument(
            "--debug",
            action="store_true",
            help="output additional debugging information",
        )

        return parser.parse_args(args=argv[1:])

    def debug_baat(self, baat):
        self.logger.debug("Str: {}".format(baat))
        self.logger.debug("Repr: {}".format(repr(baat)))
        self.logger.debug("Version: {}".format(baat.version))
        self.logger.debug("Prefix: {}".format(baat.prefix))
        self.logger.debug("Payload: {}".format(baat.payload))
        self.logger.debug("CRC: {}".format(baat.crc))

    def main(self):
        self.args = self.parse_args()
        logging.basicConfig(
            level=(logging.DEBUG if self.args.debug else logging.INFO),
            format="%(name)s %(levelname)s: %(message)s",
        )
        if self.args.validate:
            b = BAAT(baat=self.args.validate)
            self.debug_baat(b)
            return 0

        for _ in range(self.args.count):
            b = BAAT(prefix=self.args.prefix)
            b2 = BAAT(baat=b)
            assert b == b2
            print(b)
            self.debug_baat(b)


if __name__ == "__main__":
    sys.exit(BAATProgram().main())
