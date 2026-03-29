@echo off
docker run --rm ^
  -v %cd%:/app ^
  selenium-crawler ^
  python job/job_topcv_category.py
