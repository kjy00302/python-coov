#!/bin/python

import socketio
import sys
import coov_api
import vc_util
import eoskey
import random
import threading


if len(sys.argv) != 2:
    print(f"{sys.argv[0]} <responder session code>")
    exit()

if not vc_util.did_valid(sys.argv[1]):
    print("Invaild session code")
    exit()

key_pub = eoskey.eos_keygen()[1]
key_nonce = eoskey.eos_keygen()[1]

url, servernum, responder_session_id = vc_util.diduri_split(sys.argv[1])

sio = socketio.Client()

def timeout():
    sio.disconnect()
    print("No response from other")

resp_timeout = threading.Timer(5, timeout)

def send_data(to, data):
    sio.emit('send', {
        'to': f'{servernum}/'+to,
        'data': data
    })

@sio.on('send')
def on_msg(data):
    try:
        did_data = vc_util.vc_verify(data['data']['vp'])
        assert vc_util.did_strip(did_data['nonce']) == key_nonce
        for vc in did_data['vp']['verifiableCredential']:
            vc_json = vc_util.vc_verify(vc, check_issuer=coov_api.KDCA_DID, check_subject=did_data['iss'])
            for k, v in vc_json['vc']['credentialSubject'].items():
                print(f'{k}: {v}')
        send_data(
            responder_session_id,
            {
                'from': sio.get_sid(),
                'result': 'success',
                'successCode': f'{random.randrange(100):02d}'
            }
        )
        sio.sleep(0.01)
    except:
        print(sys.exc_info()[2])
    finally:
        resp_timeout.cancel()
        sio.disconnect()

sio.connect(f'https://{url.replace("wss", f"wss-{servernum}")}', transports="websocket")

send_data(
    responder_session_id,
    {
        'from': sio.get_sid(),
        'verifierDid': vc_util.did_append(key_pub),
        'challenge': vc_util.did_append(key_nonce)
})

resp_timeout.start()
