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


class Metadata_Value_handler:
    value_pairs = {}

    def __init__(self, model, debug=False):
        self.model = model
        self.debug = debug

    def handle_value_type(self, metadata_parser: Metadata_parser):
        key = metadata_parser.string
        metadata_value_type = metadata_parser.metadata_value_type

        match metadata_value_type:
            case 4:
                int_32_handler = mvt.GGUF_METADATA_VALUE_TYPE_UINT32(
                    key, self.model, ENDIAN, metadata_value_type
                )
                if self.debug:
                    print(int_32_handler)

            case 6:
                float_32_handler = mvt.GGUF_METADATA_VALUE_TYPE_FLOAT32(
                    key, self.model, ENDIAN, metadata_value_type
                )
                if self.debug:
                    print(float_32_handler)

            case 7:
                # value is a boolean with 1-byte len
                boolean_handler = mvt.GGUF_METADATA_VALUE_TYPE_BOOL(
                    key, self.model, ENDIAN, metadata_value_type
                )
                if self.debug:
                    print(boolean_handler)

            case 8:
                string_handler = mvt.GGUF_METADATA_VALUE_TYPE_STRING(
                    key, self.model, ENDIAN, metadata_value_type
                )
                if self.debug:
                    print(string_handler)
            case 9:
                # Array is stored here
                array_handler = mvt.GGUF_METADATA_VALUE_TYPE_ARRAY(
                    key, self.model, ENDIAN, metadata_value_type
                )
                tokens = array_handler.read()
                if self.debug:
                    print(tokens[-1:-5:-1])
            case _:
                raise Exception("Not implemented")


with open(MODEL, mode="rb") as model:
    Header.read_header(model)
    # Header.print_header()
    handler = mvt.Metadata_parser(model, debug=True)

    for i, _ in enumerate(range(Header.metadata_kv_count)):
        print("--" * 10)

        handler.handle_case()
        # metadata_value_handler = Metadata_Value_handler(model)
        # metadata_value_handler.handle_value_type(r)
