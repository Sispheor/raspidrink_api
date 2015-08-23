# -*- coding: utf-8 -*-
from celery.task import task
from gpio_control import GpioControl

@task()
def make_cocktail(slot_volume_dict):
    print slot_volume_dict
    for el in slot_volume_dict:
        gpio_control = GpioControl(slot=el['slot_id'], timeout=el['volume'])
        gpio_control.start()


@task()
def reverse_pump():

    return True


@task()
def pump_management(action, slot=None):
    print 'slot: '+str(slot)
    print 'action: '+str(action)
    return True


