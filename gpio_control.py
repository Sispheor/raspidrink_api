from threading import Thread
import time


class GpioControl(Thread):

    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, verbose=None,
                 timeout=None, slot=None):
        super(GpioControl, self).__init__(group, target, name, args, kwargs, verbose)
        self.timeout = timeout
        self.slot = slot

    def run(self):
        print 'Switch GPIO slot '+str(self.slot)+' on for '+str(self.timeout)+' seconde'
        time.sleep(int(self.timeout))
        # TODO: switch gpio port to 1
        print 'Switch GPIO slot '+str(self.slot)+' back off'
        # TODO: switch gpio port to 0
