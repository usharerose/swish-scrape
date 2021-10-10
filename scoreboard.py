# Copyright (c) 2021 usharerose. All rights reserved.
import argparse
import copy
import datetime
from http import HTTPStatus
import json
import logging
import os

from logging_config import config_logging
from utils import requests_retry_session, get_random_mobile_user_agent


config_logging()
logger = logging.getLogger(__name__)


SCOREBOARD_URL = 'https://stats.nba.com/stats/scoreboardv3?GameDate={date}&LeagueID={league_id}'
LEAGUE_IDS = {
    'nba': '00'
}
DATE_FORMAT_PATTERN = '%Y-%m-%d'
DEFAULT_RETRIES = 5
TIMEOUT = 10


def crawl(a_date):
    logger.info('ScoreBoard {} - ready to fetch'.format(a_date))

    session = requests_retry_session()
    target_url = SCOREBOARD_URL.format(date=a_date.strftime(DATE_FORMAT_PATTERN),
                                       league_id=LEAGUE_IDS['nba'])
    base_req_headers = {
        'host': 'stats.nba.com',
        'origin': 'https://www.nba.com',
        'referer': 'https://www.nba.com/'
    }

    req_headers = copy.deepcopy(base_req_headers)
    req_headers['user-agent'] = get_random_mobile_user_agent()

    r = session.get(url=target_url, timeout=TIMEOUT, headers=req_headers)

    if r.status_code != HTTPStatus.OK.value:
        raise

    logger.info('ScoreBoard {} - fetched'.format(a_date))

    result = json.loads(r.content.decode('utf-8'))
    return result


MODULE_ROOT = os.path.abspath(os.path.dirname(__file__))


def main(args):
    target_date = args.date
    result = crawl(target_date)
    if args.dry_run:
        logger.info('ScoreBoard {} - {}'.format(target_date, result))
    else:
        with open(os.path.join(MODULE_ROOT, 'scoreboard_{}.json'.format(target_date)), 'w') as f:
            json.dump(result, f)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='NBA ScoreBoard Data Scrape')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('-d', '--date',
                        type=lambda date_str: datetime.datetime.strptime(date_str, '%Y-%m-%d').date(),
                        default=datetime.datetime.utcnow().date() - datetime.timedelta(days=1),
                        help='Match Day')
    args = parser.parse_args()
    main(args)
