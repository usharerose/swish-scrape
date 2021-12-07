# Copyright (c) 2021 usharerose. All rights reserved.
from celery.schedules import crontab
import datetime

from conf import settings


broker_url = settings.BROKER_URL


timezone = 'Asia/Shanghai'
BEAT_SCHEDULE = {
    'scoreboard-daily': {
        'task': 'tasks.crawl_scoreboard',
        'schedule': crontab(minute=0, hour=15),
        'args': ((datetime.datetime.now().date() + datetime.timedelta(days=-1)).strftime('%Y-%m-%d'),)
    }
}
