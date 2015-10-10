# -*- coding: utf-8 -*-
from celery.task import task
from gpio_control_thread import GpioControl
from FileLock import FileLock
from lib.utils import *


@task()
def make_cocktail(slot_volume_dict):
    # run a thread for each slot    
    for el in slot_volume_dict:
        gpio_control = GpioControl(slot=el['slot_id'], volume=el['volume'])
        gpio_control.start()    
    # get the timeout delay from this volume and the concerned slot
    timeout_delay = get_time_delay_for_slot_and_volume(slot_volume_dict)
    print "timeout max: "+str(timeout_delay)
    # create file locker
    filelock = FileLock("raspidrink", timeout=int(timeout_delay))
    filelock.create_lock_file()


@task()
def reverse_pump(action):
    if action == "on":
        print "Reverse pump stream order"
        gpio_control = GpioControl(slot="0", action="start")
        gpio_control.start()
    else:
        print "Stop reverse pump stream order"
        gpio_control = GpioControl(slot="0", action="stop")
        gpio_control.start()


@task()
def pump_management(action, slot=None):
    print 'slot: '+str(slot)
    print 'action: '+str(action)
    gpio_control = GpioControl(slot=slot, action=action)
    gpio_control.start()


