#!/bin/bash
report_file=load_report.txt
echo "start">$report_file
for process in 8
do 
  port=`expr 8000 + $process`
  echo "------------------------port=$port----------------------"
  sed -i '13s/[0-9].*/'${process}'/g'  config.ini
  sed -i '4s/127.0.0.1:[0-9].*/127.0.0.1:'${port}'/g' config.ini
  uwsgi --ini config.ini
  sleep 24
  echo "--------------------------------------uwsgi starting--------------------------------------------"
  echo "process=$process-----------------------------------------------------"
  echo "process=$process-----------------------------------------------------">>$report_file
  for concurrency in  50 100
  do  
    echo "concurrency=$concurrency-------------------------------------------------">>$report_file
    siege -c $concurrency -t 1M --content-type "application/json" "http://127.0.0.1:$port/asr POST <info1.json" --log=./result/result.csv >> $report_file
  sleep 20
  done
  sleep 6
  uwsgi --stop uwsgi.pid
  sleep 3
  echo "*************************************************stopping************************************************************"
done 
#python process.py
#echo "*******************************Finish*****************************************"
