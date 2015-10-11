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
        :param volume: Volume in cl
        :param slot:   Slot number to switch
        :param action: If no volume, set action to switch the slot. String allowed: start or stop
        :return:
        """
        super(GpioControl, self).__init__(group, target, name, args, kwargs, verbose)
        # get settings
        self.cfg = get_settings()
        self.timeout = volume
        if slot is not None:
            self.slot = int(slot)
        else:
            self.slot = None
        self.action = action
        # get the timeout delay for the selected slot
        if self.timeout is not None and self.slot is not None:
            self.timeout = self._convert_volume_into_time(volume)

    def run(self):
        # if slot number provided, then switch only this one
        if self.slot is not None:
            # convert slot number into GPIO port number
            gpio_id = self._get_pin_from_slot_number()
            # if the slot exist
            if gpio_id is not -1:
                if self.timeout:    # If a timeout is set, then we have to set the PIN HIGH and then LOW
                    # active the pump
                    self.switch_pin_high(gpio_id)

                    print "Waiting timout before shutting down: "+str(self.timeout)
                    time.sleep(int(self.timeout))

                    # then the the pump
                    self.switch_pin_low(gpio_id)

                else:   # No timeout, use action instead
                    if self.action == "start":
                        self.switch_pin_high(gpio_id)
                    else:
                        self.switch_pin_low(gpio_id)

        else:  # no precise slot provided, then switch every slot to the requested action
            gpio_ids = self.cfg['gpio_mapping']
            for gpio_id in gpio_ids:
                # Skip the port number zero used to reverse pump stream order
                if gpio_id is not 0 and gpio_id is not -1:
                    pin_to_switch = self._get_pin_from_slot_number(gpio_id)
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
        """
        Convert a volume for the current slot into time. Each slot has it's own time
        multiplier in the settings file.
        :param volume: Volume in cl to convert
        :return: time in second
        """
        time_multiplier = self.cfg['gpio_mapping'][self.slot]['time_for_1cl']
        return int(volume) * time_multiplier

    def _get_pin_from_slot_number(self, slot_number):
        try:
            pin_number = self.cfg['gpio_mapping'][slot_number]['pin_number']
        except KeyError:
                print "This slot does not exist"
        return pin_number
