import requests


KDCA_DID = 'did:infra:01:PUB_K1_5LnLPSFL1ioJyATiTQ7jUzQJe1PqzEbBWyE8efzyn88TBz4w8N'
AUTH_SECRET = 'EC1CYhJoAXwyJkvmV7ZrrtZYRuVEJm3b8j4xhZt8Cw8AgvE82'

def getvc_v1(token, did, type_):
    resp = requests.post(
        'https://app.coov.io/api/v1/issue/coov/vc',
        params={'type':type_},
        json={'did':did},
        headers={'authorization': token}
    ).json()
    if resp['messageCode'] == 'Success':
        return resp['result']

def getvc_vaccine(token, did):
    resp = requests.post(
        'https://app.coov.io/api/v2/issue/coov/vc/vaccination',
        json={'did':did},
        headers={'authorization': token}
    ).json()
    if resp['resCode'] == 'Success':
        return resp['result']

def resetvc_vaccine(token):
    resp = requests.post(
        'https://app.coov.io/api/v2/issue/coov/reset',
        headers={'authorization': token}
    ).json()
    if resp['resCode'] == 'Success':
        return True
    return False

def getauthpage():
    resp = requests.get('https://app.coov.io/api/v1/auth', headers={'secret-key': AUTH_SECRET})
    if resp.status_code == 200:
        return resp.text

def checktoken(token):
    resp = requests.get('https://app.coov.io/api/v1/auth/token/check', headers={'authorization': token})
    if resp.json()['messageCode'] == 'Success':
        return True
    return False

def getkipass(token, endpoint):
    resp = requests.post(
        'https://kipass.coov.io/v1/kipass/issueCheckInQRCode',
        json={'enp': endpoint},
        headers={'authorization': f'Bearer {token}'}
    ).json()
    return resp['qrCode']
