#!/bin/sh
scrapyd-deploy
python -u /data/gemantic_crawl/crawls/app.py >> /data/gemantic_crawl/logs/crawls_stdout.log 2>&1 &
