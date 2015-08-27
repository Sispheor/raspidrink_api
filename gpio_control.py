from threading import Thread
import time
import yaml
import os
import subprocess


class GpioControl(Thread):

    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, verbose=None,
                 timeout=None, slot=None):
        super(GpioControl, self).__init__(group, target, name, args, kwargs, verbose)
        self.timeout = timeout
        self.slot = slot

        __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
        with open(os.path.join(__location__, "settings.yml")) as ymlfile:
            self.cfg = yaml.load(ymlfile)
            print self.cfg

    def run(self):
        # convert slot number into GPIO port number
        gpio_id = self.cfg['gpio_mapping'][int(self.slot)]

        if self.cfg['active_gpio']:
            print 'Switch GPIO slot '+str(gpio_id)+' on for '+str(self.timeout)+' seconde'
            self._execute_script(gpio_id, "HIGH")
            # wait the timout before shutting down the pump
            time.sleep(int(self.timeout))
            print 'Switch GPIO slot '+str(gpio_id)+' back off'
            self._execute_script(gpio_id, "LOW")
        else:
            print 'Fake switch GPIO slot '+str(gpio_id)+' on for '+str(self.timeout)+' seconde'
            time.sleep(int(self.timeout))
            print 'Fake switch GPIO slot '+str(gpio_id)+' back off'

    def _execute_script(self, port, status):
        cmd = "sudo python switch_gpio_port_status.py --port "+str(port)+" --status "+status
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        # print "Output:", output
