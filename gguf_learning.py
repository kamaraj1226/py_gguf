import sys
import struct
def check_byte_type():
    return sys.byteorder

MODEL_DIR='model/'
ENDIAN = check_byte_type()
MODEL=f"{MODEL_DIR}phi-2.Q2_K.gguf"



def parse_string(model):
    metadata_string_len = int.from_bytes(model.read(8), byteorder=ENDIAN)
    metadata_string = model.read(metadata_string_len)
    print(f"{metadata_string_len=}")
    print(f"{metadata_string=}")

with open(MODEL, mode='rb') as model:
    MAGIC_NUMBER = model.read(4)
    VERSION = int.from_bytes(model.read(4), byteorder=ENDIAN)
    tensor_count = int.from_bytes(model.read(8), byteorder=ENDIAN)
    metadata_kv_count = int.from_bytes(model.read(8), byteorder=ENDIAN)
    print(f"{MAGIC_NUMBER=}")
    print(f"{VERSION=}")
    print(f"{tensor_count=}")
    print(f"{metadata_kv_count=}")

    for _ in range(metadata_kv_count):
        # get string_t values
        string_len = int.from_bytes(model.read(8), byteorder=ENDIAN)
        string = model.read(string_len).decode('utf-8')
        metadata_value_type = int.from_bytes(model.read(4), byteorder=ENDIAN)
        print('--'*35)
        # print(f"{string_len=}")
        print(f"{string=}")
        print(f"{metadata_value_type=}")

        # if statement should be added
        match metadata_value_type:
            case 4:
                # The value is a 32 bit unsigned little-endian integer
                print(f"metadata_int_value={int.from_bytes(model.read(4), byteorder=ENDIAN)}")

            case 6:
                # value is 32 bit IEEE754 floating point number
               float_value = struct.unpack('<f',model.read(4))[0]
               print(f'metadata_float_value={float_value}')
            case 7:
                # value is a boolean with 1-byte len
                boolean_value = int.from_bytes(model.read(1), byteorder=ENDIAN)
                print(f"{boolean_value=}")
            case 8:
                # value is UTF-8 non-null-terminated string with length prepended
                parse_string(model)
            case _:
                raise Exception('Not implemented')
