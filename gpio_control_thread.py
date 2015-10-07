from threading import Thread
import time
from lib.utils import *


class GpioControl(Thread):

    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, verbose=None,
                 volume=None, slot=None, action=None):
        """
        Thread used to switch GPIO pin HIGH or LOW. Call sudo command because the GPIO library
        must be run as root on the RPI and celery must not. Furthermore, is this code can
        be launched from a computer that is not a RPI thanks to this split.
        :param volume: Volume to
        :param slot:   Slot number to switch
        :param action: If no timeout, set action to switch the slot. String allowed: start or stop
        :return:
        """
        super(GpioControl, self).__init__(group, target, name, args, kwargs, verbose)
        self.timeout = self._convert_volume_into_time(volume)
        self.slot = slot
        self.action = action

        # get settings
        self.cfg = get_settings()

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
            execute_script(pin, "HIGH")
        else:
            print 'Fake Switch GPIO slot '+str(pin)+' HIGH'

    def switch_pin_low(self, pin):
        if self.cfg['active_gpio']:
            print 'Switch GPIO slot '+str(pin)+' LOW'
            execute_script(pin, "LOW")
        else:
            print 'Fake Switch GPIO slot '+str(pin)+' LOW'

    def _convert_volume_into_time(self, volume):
        time_multiplier = self.cfg['time_multiplier']
        return volume * time_multiplier
