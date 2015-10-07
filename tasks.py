# -*- coding: utf-8 -*-
from celery.task import task
from gpio_control_thread import GpioControl
from FileLock import FileLock


def get_highter_volume(slot_volume_dict):
        """
        Return the bigger integer in the list
        :param slot_volume_dict:
        :return:
        """
        list_volume = []
        for el in slot_volume_dict:
            list_volume.append(int(el['volume']))
        return max(list_volume)


@task()
def make_cocktail(slot_volume_dict):
    print slot_volume_dict
    # run a thread for each slot
    for el in slot_volume_dict:
        gpio_control = GpioControl(slot=el['slot_id'], volume=el['volume'])
        gpio_control.start()
    # get highest number in volume list
    bigger_volume = get_highter_volume(slot_volume_dict)
    # create file locker
    filelock = FileLock("raspidrink", timeout=int(bigger_volume))
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


