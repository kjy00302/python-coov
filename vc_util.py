import eoskey
from jwcrypto import jwt, jwk
from jwcrypto.common import json_decode
import time

def diduri_split(did):
    return did_strip(did).split('/')

def did_valid(did: str):
    return True if did.startswith('did:infra:') else False

def did_strip(did):
    return did.split(':')[-1]

def did_append(key):
    return f'did:infra:01:{key}'

def vc_verify(data, check_issuer=None, check_subject=None):
    token = jwt.JWT(jwt=data).token
    payload = json_decode(token.objects['payload'])
    issuer = payload['iss']
    key = eoskey.eos_to_pyca(did_strip(issuer))
    token.verify(jwk.JWK.from_pyca(key))
    if check_issuer:
        assert check_issuer == issuer
    if check_subject:
        assert check_subject == payload['sub']
    return payload 

def makevp(key_priv_eos, audience_dids, nonce, vc):
    key_priv = eoskey.eos_to_pyca(key_priv_eos)
    key_pub = eoskey.eos_from_pyca(key_priv.public_key())
    token = jwt.JWT(
        header={'typ': 'JWT', 'alg': 'ES256K'},
        claims={
            'exp': int(time.time())+60,
            'vp': {
                '@context': [
                'https://www.w3.org/2018/credentials/v1'
                ],
                'type': [
                'VerifiablePresentation'
                ],
                'verifiableCredential': vc
            },
            'nbf': int(time.time()),
            'iss': did_append(key_pub),
            'aud': audience_dids,
            'nonce': nonce
    })
    token.make_signed_token(jwk.JWK.from_pyca(key_priv))
    return token.serialize()
