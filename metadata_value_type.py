from typing import Tuple
from constants import ENDIAN
import struct
from enum import Enum
from abc import ABC, abstractmethod


class Metadata_KV(ABC):
    @abstractmethod
    def read(self): ...

    @abstractmethod
    def __str__(self): ...


class MetadataType(Enum):
    GGUF_METADATA_VALUE_TYPE_UINT8 = 0
    # The value is a 8-bit signed integer.
    GGUF_METADATA_VALUE_TYPE_INT8 = 1
    # The value is a 16-bit unsigned little-endian integer.
    GGUF_METADATA_VALUE_TYPE_UINT16 = 2
    # The value is a 16-bit signed little-endian integer.
    GGUF_METADATA_VALUE_TYPE_INT16 = 3
    # The value is a 32-bit unsigned little-endian integer.
    GGUF_METADATA_VALUE_TYPE_UINT32 = 4
    # The value is a 32-bit signed little-endian integer.
    GGUF_METADATA_VALUE_TYPE_INT32 = 5
    # The value is a 32-bit IEEE754 floating point number.
    GGUF_METADATA_VALUE_TYPE_FLOAT32 = 6
    # The value is a boolean.
    # 1-byte value where 0 is false and 1 is true.
    # Anything else is invalid and should be treated as either the model being invalid or the reader being buggy.
    GGUF_METADATA_VALUE_TYPE_BOOL = 7
    # The value is a UTF-8 non-null-terminated string with length prepended.
    GGUF_METADATA_VALUE_TYPE_STRING = 8
    # The value is an array of other values with the length and type prepended.
    # Arrays can be nested and the length of the array is the number of elements in the array not the number of bytes.
    GGUF_METADATA_VALUE_TYPE_ARRAY = 9
    # The value is a 64-bit unsigned little-endian integer.
    GGUF_METADATA_VALUE_TYPE_UINT64 = 10
    # The value is a 64-bit signed little-endian integer.
    GGUF_METADATA_VALUE_TYPE_INT64 = 11
    # The value is a 64-bit IEEE754 floating point number.
    GGUF_METADATA_VALUE_TYPE_FLOAT64 = 12


class GGUF_METADATA_VALUE_TYPE_STRING(Metadata_KV):
    """
    value is UTF-8 non-null-terminated string with length prepended
    """

    def __init__(self, key, model, _type: int):
        self.model = model
        self.key = key
        self.type = MetadataType(_type)
        self.value = None
        self.read()

    def read(self):
        metadata_string_len = int.from_bytes(self.model.read(8), byteorder=ENDIAN)
        self.value = self.model.read(metadata_string_len)
        return self.value

    def __str__(self):
        return f"type: {self.type}\n" f"key: {self.key}\n" f"value: {self.value}"


class GGUF_METADATA_VALUE_TYPE_INT8(Metadata_KV):
    """
    value is UTF-8 non-null-terminated string with length prepended
    """

    def __init__(self, key, model, _type: int):
        self.model = model
        self.key = key
        self.type = MetadataType(_type)
        self.value = None
        self.read()

    def read(self):
        metadata_string_len = int.from_bytes(self.model.read(1), byteorder=ENDIAN)
        self.value = self.model.read(metadata_string_len)
        return self.value

    def __str__(self):
        return f"type: {self.type}\n" f"key: {self.key}\n" f"value: {self.value}"


class GGUF_METADATA_VALUE_TYPE_UINT32(Metadata_KV):
    """
    The value is a 32-bit unsigned little-endian integer.
    """

    def __init__(self, key, model, _type: int):
        self.model = model
        self.key = key
        self.type = MetadataType(_type)
        self.value = None
        self.read()

    def read(self):
        self.value = int.from_bytes(self.model.read(4), byteorder=ENDIAN)

    def __str__(self):
        return f"type: {self.type}\n" f"key: {self.key}\n" f"value: {self.value}"


class GGUF_METADATA_VALUE_TYPE_FLOAT32(Metadata_KV):
    """
    The value is a 32-bit IEEE754 floating point number.
    """

    def __init__(self, key, model, _type: int):
        self.model = model
        self.key = key
        self.type = MetadataType(_type)
        self.value = None
        self.read()

    def read(self):
        self.value = struct.unpack("<f", self.model.read(4))[0]
        return self.value

    def __str__(self):
        return f"type: {self.type}\n" f"key: {self.key}\n" f"value: {self.value}"


class GGUF_METADATA_VALUE_TYPE_BOOL(Metadata_KV):

    def __init__(self, key, model, _type: int):
        self.model = model
        self.key = key
        self.type = MetadataType(_type)
        self.value = None
        self.read()

    def read(self):
        self.value = int.from_bytes(self.model.read(1), byteorder=ENDIAN)
        return self.value

    def __str__(self):
        return f"type: {self.type}\n" f"key: {self.key}\n" f"value: {self.value}"


class GGUF_METADATA_VALUE_TYPE_UINT64(Metadata_KV):

    def __init__(self, key, model, _type: int):
        self.model = model
        self.key = key
        self.type = MetadataType(_type)
        self.value = None
        self.read()

    def read(self):
        self.value = int.from_bytes(self.model.read(4), byteorder=ENDIAN)
        return self.value

    def __str__(self):
        return f"type: {self.type}\n" f"key: {self.key}\n" f"value: {self.value}"


class GGUF_METADATA_VALUE_TYPE_ARRAY(Metadata_KV):
    """
    Need to read manually
    Auto read is not available because array size can be huge
    """

    def __init__(self, key, model, _type: int):
        self.model = model
        self.key = key
        self.type = MetadataType(_type)
        self.value = None

    def read(self):
        # will be array of values of type MetadataType
        # Nested array can also be there
        array_value_type = int.from_bytes(self.model.read(4), byteorder=ENDIAN)
        array_length = int.from_bytes(self.model.read(8), byteorder=ENDIAN)
        tokens = []
        parser = Metadata_parser(self.model)
        for _ in range(array_length):
            if array_value_type != MetadataType.GGUF_METADATA_VALUE_TYPE_STRING.value:
                raise Exception("Not Implemented TODO: dynamic type handling")
            value = parser.handle_case()
            print("value=", value)
        return tokens

    def __str__(self):
        return f"type: {self.type}\n" f"key: {self.key}\n" f"value: {self.value}"


class Metadata_parser:
    def __init__(self, model):
        self.model = model

    def get_metadata_type(self) -> Tuple[str, MetadataType]:
        # get string_t values
        string_len = int.from_bytes(self.model.read(8), byteorder=ENDIAN)
        string = self.model.read(string_len).decode("utf-8")
        metadata_value_type = MetadataType(
            int.from_bytes(self.model.read(4), byteorder=ENDIAN)
        )

        return (string, metadata_value_type)

    def handle_case(self):
        key, metadata_value_type = self.get_metadata_type()
        print(f"{metadata_value_type=}")
        match metadata_value_type:
            case MetadataType.GGUF_METADATA_VALUE_TYPE_UINT32:
                int_32_handler = GGUF_METADATA_VALUE_TYPE_UINT32(
                    key, self.model, metadata_value_type
                )
                print(int_32_handler)

            case MetadataType.GGUF_METADATA_VALUE_TYPE_FLOAT32:
                float_32_handler = GGUF_METADATA_VALUE_TYPE_FLOAT32(
                    key, self.model, metadata_value_type
                )
                print(float_32_handler)

            case MetadataType.GGUF_METADATA_VALUE_TYPE_BOOL:
                # value is a boolean with 1-byte len
                boolean_handler = GGUF_METADATA_VALUE_TYPE_BOOL(
                    key, self.model, metadata_value_type
                )
                print(boolean_handler)

            case MetadataType.GGUF_METADATA_VALUE_TYPE_STRING:
                string_handler = GGUF_METADATA_VALUE_TYPE_STRING(
                    key, self.model, metadata_value_type
                )
                print(string_handler)
            case MetadataType.GGUF_METADATA_VALUE_TYPE_INT8:
                int_8_handler = GGUF_METADATA_VALUE_TYPE_INT8(
                    key, self.model, metadata_value_type
                )
                print(int_8_handler)
            case MetadataType.GGUF_METADATA_VALUE_TYPE_ARRAY:
                # Array is stored here
                print("handling array.....")
                array_handler = GGUF_METADATA_VALUE_TYPE_ARRAY(
                    key, self.model, metadata_value_type
                )
                tokens = array_handler.read()
                print(tokens[-1:-5:-1])
                print("Array tokens")
            case _:
                raise Exception(f"{metadata_value_type} is not implemented")
