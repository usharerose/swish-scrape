# Copyright (c) 2021 usharerose. All rights reserved.
import datetime
import json
import os

from scoreboard import crawl
from swish_task_queue import app


@app.task
def crawl_scoreboard(date_string):
    a_date = datetime.datetime.strptime(date_string, '%Y-%m-%d')
    data = crawl(a_date)

    filename = f'./data/scoreboard/{a_date.year}/{a_date.month}/{date_string}.json'
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as f:
        json.dump(data, f)
