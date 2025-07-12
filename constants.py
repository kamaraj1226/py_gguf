import sys


def check_byte_type() -> str:
    """
    Helper:
        will help to identify if the system uses little-endian or big-endian
    """
    return sys.byteorder


ENDIAN = check_byte_type()
