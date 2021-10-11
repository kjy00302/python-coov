import math
B58CHARS = b'123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def b58encode(b):
    t = len(b)
    b = b.lstrip(b'\0')
    zc = t - len(b)
    n = int.from_bytes(b, 'big')
    l = math.ceil(math.log(n, 58))
    out = bytearray(l)
    i = l - 1
    while n > 0:
        n, remainder = divmod(n, 58)
        out[i] = B58CHARS[remainder]
        i -= 1
    return b'1'*zc + out

def b58decode(b):
    t = len(b)
    b = b.lstrip(b'1')
    zc = t - len(b)
    n = 0
    for c in b:
        n = n * 58 + B58CHARS.index(c)
    l = math.ceil(math.log(n, 256))
    out = bytearray(l)
    i = l - 1
    while n > 0:
        n, remainder = divmod(n, 256)
        out[i] = remainder
        i -= 1
    return b'\0'*zc + out
