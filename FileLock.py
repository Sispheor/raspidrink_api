import os
from datetime import datetime, timedelta
"""
The lock is used to know if RaspiDrink machine is currently running
and making a cocktail
"""


class FileLock(object):

    def __init__(self, fname, timeout=None):
        self.fname = fname
        # path of the file.
        self.path = '/tmp/%s.lock' % self.fname
        x = datetime.now()
        if timeout is not None:
            x += timedelta(seconds=timeout)

        x = x.strftime("%d-%m-%Y %H:%M:%S")
        self.datetimeout = x
        self.pid = os.getpid()
        print "Current PID: "+str(self.pid)
        print "Current date: "+datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    def check_pid(self, pid):
        """ Check For the existence of a unix pid. """
        try:
            os.kill(pid, 0)
        except OSError:
            return False
        else:
            return True

    def is_valide(self):
        """
        Check if the current lock file is valide. Timeout ok and pid still exist on the system
        """
        if os.path.exists(self.path):
            fh = open(self.path)
            data = fh.read().rstrip().split('@')
            fh.close()
            datetimeout_in_file, pid_in_file = data
            print "date in file: "+datetimeout_in_file
            print "pid in file: "+pid_in_file
            # if the date set in the file is lower than now the process should be kill
            if datetime.strptime(datetimeout_in_file, "%d-%m-%Y %H:%M:%S") < datetime.now():
                return False
            else:
                return True
        else:
            return False

    def create_lock_file(self):
        """

        :return: Return True if created
        """
        if not self.is_valide():
            fh = open(self.path, 'w')
            fh.write(str(self.datetimeout)+"@"+str(self.pid))
            fh.close()
            return True
        else:
            # Lock file already there
            print "Lock file already there and valid"
            return False

    def remove_lock_file(self):
        if os.path.exists(self.path):
            os.remove(self.path)
