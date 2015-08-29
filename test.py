"""
Test API file
"""
import json
from requests import put, get, post
from FileLock import FileLock


"""
# create a lock file with 10 seconde of validity
filelock = FileLock("raspidrink", 15)
print filelock.is_valide()
filelock.create_lock_file()

"""
# -------------------------
# Test API
# -------------------------
# local test
# url = 'http://localhost:5000'
# RPI2 test
url = 'http://192.168.0.22:5000'
headers = {'content-type': 'application/json'}
# get /
#print get(url).json()

# Test create cocktail
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