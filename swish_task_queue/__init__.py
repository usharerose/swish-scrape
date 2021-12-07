# Copyright (c) 2021 usharerose. All rights reserved.
from celery import Celery


app = Celery()
app.config_from_object('swish_task_queue.conf.settings')
