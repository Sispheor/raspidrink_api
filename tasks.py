# -*- coding: utf-8 -*-
from celery.task import task


@task()
def make_cocktail(slot_volume_dict):
    print slot_volume_dict
    return True


@task()
def reverse_pump():

    return True


@task()
def pump_management(action, slot=None):
    print 'slot: '+str(slot)
    print 'action: '+str(action)
    return True


