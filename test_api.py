"""
Test API file. This test every availlable function over the API.
"""
import json
from requests import put, get, post


# -------------------------
# Test API
# -------------------------
# local test
url = 'http://localhost:5000'
# RPI2 test
# url = 'http://192.168.0.22:5000'
headers = {'content-type': 'application/json'}


# Test make a cocktail
payload = {'data': [
    {'slot_id': '1', 'volume': '5'},
    {'slot_id': '5', 'volume': '11'}]}
r = post(url+'/make_cocktail', data=json.dumps(payload), headers=headers)
print r.text
"""

# Test start specific pump
payload = {'slot_id': '4', 'action': 'start'}
r = post(url+'/active_pump', data=json.dumps(payload), headers=headers)
print r.text


# Test stop specific pump
payload = {'slot_id': '4', 'action': 'stop'}
r = post(url+'/active_pump', data=json.dumps(payload), headers=headers)
print r.text


# Test start all pump
payload = {'action': 'start'}
r = post(url+'/active_pump', data=json.dumps(payload), headers=headers)
print r.text


# Test stop all pump
payload = {'action': 'stop'}
r = post(url+'/active_pump', data=json.dumps(payload), headers=headers)
print r.text


# Test reverse pump On
payload = {'action': 'on'}
r = post(url+'/reverse_pump', data=json.dumps(payload), headers=headers)
print r.text


# Test reverse pump Off
payload = {'action': 'off'}
r = post(url+'/reverse_pump', data=json.dumps(payload), headers=headers)
print r.text

"""