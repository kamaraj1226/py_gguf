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


class GGUF_METADATA_VALUE_TYPE_UINT8(Metadata_KV):
    """
    The value is a 8-bit signed integer.
    """

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
        return self.value

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
        self.value = int.from_bytes(self.model.read(8), byteorder=ENDIAN)
        return self.value

    def __str__(self):
        return f"type: {self.type}\n" f"key: {self.key}\n" f"value: {self.value}"


class GGUF_METADATA_VALUE_TYPE_ARRAY(Metadata_KV):
    """
    TODO!
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
        def get_metadata_type() -> Tuple[str, MetadataType]:
            # get string_t values
            string_len = int.from_bytes(self.model.read(8), byteorder=ENDIAN)
            string = self.model.read(string_len)
            metadata_value_type = MetadataType(
                int.from_bytes(self.model.read(4), byteorder=ENDIAN)
            )

            return (string, metadata_value_type)

        array_value_type = int.from_bytes(self.model.read(4), byteorder=ENDIAN)
        array_value_type = MetadataType(array_value_type)

        array_length = int.from_bytes(self.model.read(8), byteorder=ENDIAN)
        tokens = []
        parser = Metadata_parser(self.model)
        for _ in range(array_length):
            match array_value_type:
                case MetadataType.GGUF_METADATA_VALUE_TYPE_STRING:
                    metadata_string_len = int.from_bytes(
                        self.model.read(8), byteorder=ENDIAN
                    )
                    value = self.model.read(metadata_string_len).decode()
                    tokens.append(value)
                case MetadataType.GGUF_METADATA_VALUE_TYPE_INT32:
                    value = int.from_bytes(self.model.read(4), byteorder=ENDIAN)
                    tokens.append(value)
                case _:
                    raise Exception(
                        f"Not Implemented {MetadataType(array_value_type)} TODO: dynamic type handling"
                    )
        self.value = tokens.copy()
        return tokens

    def __str__(self):
        return f"type: {self.type}\n" f"key: {self.key}\n" f"value: {self.value}"


class Metadata_parser:
    def __init__(self, model, debug=False):
        self.model = model
        self.debug = debug

    def get_metadata_type(self) -> Tuple[str, MetadataType]:
        # get string_t values
        string_len = int.from_bytes(self.model.read(8), byteorder=ENDIAN)
        string = self.model.read(string_len)
        metadata_value_type = MetadataType(
            int.from_bytes(self.model.read(4), byteorder=ENDIAN)
        )

        return (string, metadata_value_type)

    def handle_case(self):
        key, metadata_value_type = self.get_metadata_type()
        # print(f"{metadata_value_type=}")
        match metadata_value_type:
            case MetadataType.GGUF_METADATA_VALUE_TYPE_UINT32:
                int_32_handler = GGUF_METADATA_VALUE_TYPE_UINT32(
                    key, self.model, metadata_value_type
                )
                if self.debug:
                    print(int_32_handler)

            case MetadataType.GGUF_METADATA_VALUE_TYPE_FLOAT32:
                float_32_handler = GGUF_METADATA_VALUE_TYPE_FLOAT32(
                    key, self.model, metadata_value_type
                )
                if self.debug:
                    print(float_32_handler)

            case MetadataType.GGUF_METADATA_VALUE_TYPE_BOOL:
                # value is a boolean with 1-byte len
                boolean_handler = GGUF_METADATA_VALUE_TYPE_BOOL(
                    key, self.model, metadata_value_type
                )
                if self.debug:
                    print(boolean_handler)

            case MetadataType.GGUF_METADATA_VALUE_TYPE_STRING:
                string_handler = GGUF_METADATA_VALUE_TYPE_STRING(
                    key, self.model, metadata_value_type
                )
                if self.debug:
                    print(string_handler)
            case MetadataType.GGUF_METADATA_VALUE_TYPE_INT8:
                int_8_handler = GGUF_METADATA_VALUE_TYPE_INT8(
                    key, self.model, metadata_value_type
                )
                if self.debug:
                    print(int_8_handler)

            case MetadataType.GGUF_METADATA_VALUE_TYPE_ARRAY:
                # Array is stored here
                array_handler = GGUF_METADATA_VALUE_TYPE_ARRAY(
                    key, self.model, metadata_value_type
                )
                tokens = array_handler.read()
                print("Array tokens")
                print(tokens[-1:-5:-1])
                if len(tokens) <= 0:
                    raise Exception("Tokens are empty")

            case MetadataType.GGUF_METADATA_VALUE_TYPE_UINT8:
                uint_8_handler = GGUF_METADATA_VALUE_TYPE_UINT8(
                    key, self.model, metadata_value_type
                )
                if self.debug:
                    print(uint_8_handler)
            case _:
                raise Exception(f"{metadata_value_type} is not implemented")
