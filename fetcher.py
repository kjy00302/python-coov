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


vc_personal = coov_api.getvc_v1(token, vc_util.did_append(pubkey), 'personal')
for vc in vc_personal:
    config['VC'][vc['type']] = vc['vc']

coov_api.resetvc_vaccine(token)
vc_vaccine = coov_api.getvc_vaccine(token, vc_util.did_append(pubkey))['VCs']
for vc in vc_vaccine:
    vaccine_vc_cs = vc_util.vc_verify(vc)['vc']['credentialSubject']
    vaccine = vaccine_vc_cs['vaccine']
    dose = vaccine_vc_cs['doseNum']
    config['VC'][f'{vaccine}_{dose}'] = vc

with open('coov.ini', 'w') as f:
    config.write(f)

print("Done!")
