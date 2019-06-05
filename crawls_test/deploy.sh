#!/bin/sh
rm -rf build
rm -rf setup.py
rm -rf crawl_commons
rm -rf crawl_test
cp -r ../crawls/crawl_commons ./
cp -r ../crawls/crawl_test ./
scrapyd-deploy
