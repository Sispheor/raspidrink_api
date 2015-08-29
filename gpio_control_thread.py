from threading import Thread
import time
import yaml
import os
import subprocess


class GpioControl(Thread):

    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, verbose=None,
                 timeout=None, slot=None, action=None):
        """
        Thread used to switch GPIO pin HIGH or LOW. Call sudo command because the GPIO library
        must be run as root on the RPI and celery must not. Furthermore, is this code can
        be launched from a computer that is not a RPI thanks to this split.
        :param timeout: Time betxeend we switch the GPIO port from HIGH to LOW
        :param slot:   Slot number to switch
        :param action: If no timeout, set action to switch the slot. String allowed: start or stop
        :return:
        """
        super(GpioControl, self).__init__(group, target, name, args, kwargs, verbose)
        self.timeout = timeout
        self.slot = slot
        self.action = action

        # Load settings. Will be used to convert slot number into GPIO pin number
        __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
        with open(os.path.join(__location__, "settings.yml")) as ymlfile:
            self.cfg = yaml.load(ymlfile)
            print self.cfg

    def run(self):
        # if no slot provided, then switch every slot to the requested action
        if self.slot:
            try:
                # convert slot number into GPIO port number
                gpio_id = self.cfg['gpio_mapping'][int(self.slot)]
                if self.timeout:    # If a timeout is set, then we have to set the PIN HIGH and then LOW
                    # active the pump
                    self.switch_pin_high(gpio_id)

                    # wait the timout before shutting down the pump
                    time.sleep(int(self.timeout))

                    # then the the pump
                    self.switch_pin_low(gpio_id)

                else:   # No timeout, use action instead
                    if self.action == "start":
                        self.switch_pin_high(gpio_id)
                    else:
                        self.switch_pin_low(gpio_id)
            except KeyError:
                print "This slot does not exist"
                return -1
        else:
            gpio_ids = self.cfg['gpio_mapping']
            for gpio_id in gpio_ids:
                if gpio_id is not 0:  # Skip the port number zero used to reverse pump stream order
                    pin_to_switch = self.cfg['gpio_mapping'][gpio_id]
                    if self.action == "start":
                        self.switch_pin_high(pin_to_switch)
                    else:
                        self.switch_pin_low(pin_to_switch)

    def switch_pin_high(self, pin):
        if self.cfg['active_gpio']:
            print 'Switch GPIO slot '+str(pin)+' HIGH'
            self._execute_script(pin, "HIGH")
        else:
            print 'Fake Switch GPIO slot '+str(pin)+' HIGH'

    def switch_pin_low(self, pin):
        if self.cfg['active_gpio']:
            print 'Switch GPIO slot '+str(pin)+' LOW'
            self._execute_script(pin, "LOW")
        else:
            print 'Fake Switch GPIO slot '+str(pin)+' LOW'

    @staticmethod
    def _execute_script(port, status):
        cmd = "sudo python switch_gpio_port_status.py --port "+str(port)+" --status "+status
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        p.communicate()
