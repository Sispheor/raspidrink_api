"""
Test API file
"""

from requests import put, get
from FileLock import FileLock

#print get('http://localhost:5000/').json()

# create a lock file with 10 seconde of validity
filelock = FileLock("raspidrink", 30)
#print filelock.is_valide()
filelock.create_lock_file()


