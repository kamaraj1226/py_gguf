# GGUF PYTHON PARSER
Main goal is to understand gguf structure and how it is been utilized to load model.

## Usage
python gguf_learning.py

## TODO
- GGUF_METADATA_VALUE_TYPE_FLOAT32.read should able to handle big-endian
- Need to handle all the METADATA_VALUE_TYPE
- GGUF_METADATA_VALUE_TYPE_ARRAY.read should able to handle all type of values (currently only handling string and u32 integer).
- Need to pass model in more efficient way. Should not store it in class instance
