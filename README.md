# swish-scrape
[![](https://img.shields.io/badge/language-Python-green.svg)](https://github.com/usharerose/swish-scrape)

## Abstract
Scrape NBA daily score board stats

## Quick Start
1. activate virtual environment and install dependencies

        $ python3 -m venv ./venv
        $ source venv/bin/activate
        (venv) $ pip install --no-cache-dir -I -r requirements.txt

2. scrape single date's data

        (venv) $ PYTHONPATH=. python scoreboard.py --help
        usage: scoreboard.py [-h] [--dry-run] [-d DATE]
        
        NBA ScoreBoard Data Scrape
        
        optional arguments:
          -h, --help            show this help message and exit
          --dry-run
          -d DATE, --date DATE  Match Day

   1. the scraped data would be stored under the root path, except run the command with `--dry-run`
   2. the default date would be today, also can give a specific date as `%Y-%m-%d`
   3. sample command

            (venv) $ PYTHONPATH=. python scoreboard.py -d 2021-10-09
            2021-10-10 22:40:58 | 51332 | INFO | +28 __main__ |> ScoreBoard 2021-10-09 - ready to fetch
            2021-10-10 22:41:00 | 51332 | INFO | +47 __main__ |> ScoreBoard 2021-10-09 - fetched
            (venv) $ ls -l -d scoreboard_*
            -rw-r--r--  1 admin  staff  7273 Oct 10 22:41 scoreboard_2021-10-09.json
