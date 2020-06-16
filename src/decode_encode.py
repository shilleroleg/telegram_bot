import base64
import config


# Кодируем в base64
def encode(in_str):
    # Encoding the string into bytes
    byte_obj = in_str.encode("UTF-8")
    # Base64 Encode the bytes
    enc = base64.b64encode(byte_obj)
    # Decoding the Base64 bytes to string
    enc = enc.decode()

    return enc


# Декодируем из base64
def decode(in_str):
    # Encoding the Base64 encoded string into bytes
    byte_obj = in_str.encode("UTF-8")
    # Decoding the Base64 bytes
    dec = base64.b64decode(byte_obj)
    # Decoding the bytes to string
    dec = dec.decode()

    return dec


if __name__ == "__main__":
    s = encode(config.API_KEY_WEATHER)
    print(s)
    print(decode(s))


