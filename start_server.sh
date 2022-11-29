#!/bin/bash
sh clearpath.sh &
source activate /data/app/work && uwsgi --ini config.ini