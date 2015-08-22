# -*- coding: utf-8 -*-
from celery.task import task


@task()
def add_together(a, b):
    return a + b