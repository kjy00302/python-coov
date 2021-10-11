#!/bin/python

import eoskey
import coov_api
import vc_util
import configparser
import os
import tempfile
import webbrowser

if os.path.isfile('coov.ini'):
    print("Config file already exists")
    exit()

if not (authpage := coov_api.getauthpage()):
    print("Cannot get auth page")
    exit()

tmpf = tempfile.NamedTemporaryFile('w', suffix='.html')
tmpf.write(authpage)
tmpf.flush()

webbrowser.open_new('file://' + tmpf.name)

print("Paste authentication token here")
token = input("token >>> ").strip()

if not coov_api.checktoken(token):
    print("Invalid token")
    exit()

privkey, pubkey = eoskey.eos_keygen()

config = configparser.ConfigParser()
config['Key'] = {}
config['VC'] = {}

config['Key']['private'] = privkey
config['Key']['public'] = pubkey
config['Key']['token'] = token 


vc_personal = coov_api.getvc(token, vc_util.did_append(pubkey), 'personal')
for vc in vc_personal:
    config['VC'][vc['type']] = vc['vc']

vc_covid = coov_api.getvc(token, vc_util.did_append(pubkey), 'covid19')
for vc in vc_covid:
    vaccine = vc_util.vc_verify(vc['vc'])['vc']['credentialSubject']['vaccine']
    dose = vc_util.vc_verify(vc['vc'])['vc']['credentialSubject']['doseNum']
    config['VC'][f'{vaccine}_{dose}'] = vc['vc']

with open('coov.ini', 'w') as f:
    config.write(f)

print("Done!")
