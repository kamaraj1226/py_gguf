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

    def __init__(self, key, model, endian, _type: int):
        self.model = model
        self.key = key
        self.endian = endian
        self.type = MetadataType(_type)
        self.value = None
        self.read()

    def read(self):
        metadata_string_len = int.from_bytes(self.model.read(8), byteorder=self.endian)
        self.value = self.model.read(metadata_string_len)

    def __str__(self):
        return f"type: {self.type}\n" f"key: {self.key}\n" f"value: {self.value}"


class GGUF_METADATA_VALUE_TYPE_UINT32(Metadata_KV):
    """
    The value is a 32-bit unsigned little-endian integer.
    """

    def __init__(self, key, model, endian, _type: int):
        self.model = model
        self.key = key
        self.endian = endian
        self.type = MetadataType(_type)
        self.value = None
        self.read()

    def read(self):
        self.value = int.from_bytes(self.model.read(4), byteorder=self.endian)

    def __str__(self):
        return f"type: {self.type}\n" f"key: {self.key}\n" f"value: {self.value}"


class GGUF_METADATA_VALUE_TYPE_FLOAT32(Metadata_KV):
    """
    The value is a 32-bit IEEE754 floating point number.
    """

    def __init__(self, key, model, endian, _type: int):
        self.model = model
        self.key = key
        self.endian = endian
        self.type = MetadataType(_type)
        self.value = None
        self.read()

    def read(self):
        self.value = struct.unpack("<f", self.model.read(4))[0]

    def __str__(self):
        return f"type: {self.type}\n" f"key: {self.key}\n" f"value: {self.value}"


class GGUF_METADATA_VALUE_TYPE_BOOL(Metadata_KV):

    def __init__(self, key, model, endian, _type: int):
        self.model = model
        self.key = key
        self.endian = endian
        self.type = MetadataType(_type)
        self.value = None
        self.read()

    def read(self):
        self.value = int.from_bytes(self.model.read(1), byteorder=self.endian)

    def __str__(self):
        return f"type: {self.type}\n" f"key: {self.key}\n" f"value: {self.value}"


class GGUF_METADATA_VALUE_TYPE_UINT64(Metadata_KV):

    def __init__(self, key, model, endian, _type: int):
        self.model = model
        self.key = key
        self.endian = endian
        self.type = MetadataType(_type)
        self.value = None
        self.read()

    def read(self):
        self.value = int.from_bytes(self.model.read(4), byteorder=self.endian)

    def __str__(self):
        return f"type: {self.type}\n" f"key: {self.key}\n" f"value: {self.value}"


def array(model):
    # metadata value type uint32
    # len uint64
    # array of values
    _metadata_value_type = metadata_value_type(model)
    length = uint64(model)
    print(f"{_metadata_value_type=}")
    print(f"{length=}")
    print(MT(_metadata_value_type))
    for _ in range(length):
        ...


class GGUF_METADATA_VALUE_TYPE_ARRAY(Metadata_KV):
    """
    Need to read manually
    Auto read is not available because array size can be huge
    """

    def __init__(self, key, model, endian, _type: int):
        self.model = model
        self.key = key
        self.endian = endian
        self.type = MetadataType(_type)
        self.value = None

    def read(self):
        # will be array of values of type MetadataType
        # Nested array can also be there
        array_value_type = int.from_bytes(self.model.read(4), byteorder=self.endian)
        array_length = int.from_bytes(self.model.read(8), byteorder=self.endian)
        tokens = []
        for _ in range(array_length):
            string = GGUF_METADATA_VALUE_TYPE_STRING(
                self.key, self.model, self.endian, MetadataType(8)
            )
            tokens.append(string.value)
        self.value = tokens
        return tokens

    def __str__(self):
        return f"type: {self.type}\n" f"key: {self.key}\n" f"value: {self.value}"
