import metadata_value_type as mvt
import sys
from constants import ENDIAN


def check_byte_type():
    return sys.byteorder


# ENDIAN = check_byte_type()
MODEL_DIR = "model/"
MODEL = f"{MODEL_DIR}phi-2.Q2_K.gguf"


class Header:
    MAGIC_NUMBER = None
    VERSION = None
    tensor_count = None
    metadata_kv_count = None

    @classmethod
    def read_header(cls, model):
        cls.MAGIC_NUMBER = model.read(4).decode()
        cls.VERSION = int.from_bytes(model.read(4), byteorder=ENDIAN)
        cls.tensor_count = int.from_bytes(model.read(8), byteorder=ENDIAN)
        cls.metadata_kv_count = int.from_bytes(model.read(8), byteorder=ENDIAN)

    @classmethod
    def print_header(cls):
        print(f"MAGIC_NUMBER = {cls.MAGIC_NUMBER}")
        print(f"VERSION = {cls.VERSION}")
        print(f"tensor_count = {cls.tensor_count}")
        print(f"metadata_kv_count = {cls.metadata_kv_count}")


class Metadata_parser:
    def __init__(self): ...

    def read_string(self, model):
        # get string_t values
        self.string_len = int.from_bytes(model.read(8), byteorder=ENDIAN)
        self.string = model.read(self.string_len).decode("utf-8")
        self.metadata_value_type = int.from_bytes(model.read(4), byteorder=ENDIAN)

    def print_string(self):
        print(f"{self.string=}")
        print(f"{self.metadata_value_type=}")


with open(MODEL, mode="rb") as model:
    Header.read_header(model)
    # Header.print_header()
    handler = mvt.Metadata_parser(model, debug=False)

    for _ in range(Header.metadata_kv_count):
        handler.handle_case()
