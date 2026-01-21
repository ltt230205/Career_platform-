@echo off
docker run --rm ^
  -v %cd%:/app ^
  selenium-crawler ^
  python crawl_category_job.py
