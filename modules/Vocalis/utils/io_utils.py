import base64

def decode_base64(data):
    return base64.b64decode(data)

def encode_base64(raw_bytes):
    return base64.b64encode(raw_bytes).decode('utf-8')