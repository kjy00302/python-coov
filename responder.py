#!/bin/python

import socketio
import time
import vc_util
import configparser
import sys
import os


QR_CODE = True

if not os.path.isfile('coov.ini'):
    print('Cannot find config file')
    exit()

config = configparser.ConfigParser()
config.read('coov.ini')

if len(sys.argv) != 3:
    print(f"{sys.argv[0]} <credential type> <comma-separated vc types>")
    print("Available credential types: user, vaccine")
    print(f"Available VC types: {', '.join(config['VC'])}")
    exit()

key_priv = config['Key']['private']

vp_type = sys.argv[1]
assert vp_type in ['user', 'vaccine']

vc_list = sys.argv[2].split(',')

vc = []
for vc_type in vc_list:
    vc.append(config['VC'][vc_type.lower()])

has_dob = True if 'dob' in vc_list else None
has_name = True if 'name' in vc_list else None

sio = socketio.Client()

@sio.on('send')
def on_msg(data):
    if res := data['data'].get('result'):
        if res == 'success':
            print("Verify success")
        sio.disconnect()
    else:
        print("Request received")
        vp = vc_util.makevp(
            key_priv,
            [data['data']['verifierDid']],
            data['data']['challenge'],
            vc
        )
        send_data(
            data['data']['from'], 
            {
                'from': sio.get_sid(),
                'vp': vp,
                'user': {'dob': has_dob, 'name': has_name},
                'type':'user'
            }
        )

def send_data(to, data):
    sio.emit('send', {
        'to': to,
        'data': data
    })


@sio.event
def connect():
    sid_uri = f'did:infra:{sio.get_sid()}'
    if QR_CODE:
        import qrcode
        qr = qrcode.QRCode()
        qr.add_data(sid_uri)
        qr.print_ascii()
    print(sid_uri)

sio.connect('https://wss.coov.io/', transports='websocket')
