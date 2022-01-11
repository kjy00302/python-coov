#!/bin/python

import socketio
import vc_util
import coov_api
import configparser
import os
import threading


QR_CODE = True

if not os.path.isfile('coov.ini'):
    print('Cannot find config file')
    exit()

config = configparser.ConfigParser()
config.read('coov.ini')

key_priv = config['Key']['private']
token = config['Key']['token']

vc = []
for vc_type in ['covid19_2', 'covid19_1', 'name']:
    vc.append(config['VC'][vc_type.lower()])

sio = socketio.Client()

def timeout():
    sio.disconnect()
    print("No challenge from other")

resp_timeout = threading.Timer(15, timeout)

@sio.on('challenge')
def on_challenge(data):
    print("Challenge received")
    resp_timeout.cancel()
    vp = vc_util.makevp(
        key_priv,
        None,
        data['data']['challenge'],
        vc,
        None
    )
    sio.emit('response', {
            'to': data['data']['from'],
            'data': {
                'from': sio.get_sid(),
                'vp': vp
            }
        }
    )

@sio.on('result')
def on_result(data):
    if res := data['data'].get('result'):
        if res == 'success':
            print("Verify success")
        sio.disconnect()

@sio.event
def connect():
    enp_url = f'https://wss.coov.io/{sio.get_sid()}'
    qr_data = coov_api.getkipass(token, enp_url)
    resp_timeout.start()
    if QR_CODE:
        import qrcode
        qr = qrcode.QRCode()
        qr.add_data(qr_data)
        qr.print_ascii()
    print(qr_data)

sio.connect('https://wss.coov.io/', transports='websocket')
