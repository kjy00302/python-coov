from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
import hashlib
import base58

def eos_to_pyca(key):
    keytype, algo, data = key.split('_')
    key = base58.b58decode(data.encode())
    assert key[-4:] == hashlib.new('ripemd160', key[:-4]+algo.encode()).digest()[:4], "Key check failed"
    if keytype == 'PUB':
        return ec.EllipticCurvePublicKey.from_encoded_point(ec.SECP256K1(), key[:-4])
    elif keytype == 'PVT':
        return ec.derive_private_key(int.from_bytes(key[:-4], 'big'), ec.SECP256K1())
    else:
        raise AttributeError

def eos_from_pyca(key):
    if key.curve.name == 'secp256k1':
        algo = 'K1'
    elif key.curve.name == 'secp256r1':
        algo = 'R1'
    else:
        raise AttributeError

    if isinstance(key, ec.EllipticCurvePrivateKey):
        data = key.private_numbers().private_value.to_bytes(32, 'big')
        keytype = 'PVT'
    else:
        data = key.public_bytes(Encoding.X962, PublicFormat.CompressedPoint)
        keytype = 'PUB'

    digest = hashlib.new('ripemd160', data+algo.encode()).digest()[:4]
    return f'{keytype}_{algo}_{base58.b58encode(data + digest).decode()}'

def eos_keygen():
    pyca_priv = ec.generate_private_key(ec.SECP256K1())
    pyca_pub = pyca_priv.public_key()
    return (eos_from_pyca(pyca_priv), eos_from_pyca(pyca_pub))
