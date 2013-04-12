#!/bin/bash
#nohup ./test_client.py>print.out & 
echo "[INFO] close binder...."
pid_list=`ps -ef |grep test_client |grep -v grep | awk '{print $2}'`
if [ -n "$pid_list" ];then
	echo "[INFO] the existing binder ara $pid_list"
	for pid in $pid_list;do
		kill -9 $pid
		sleep 2
		echo "[INFO] closed binder with pid $pid"
	done
	echo "[INFO] close binder successfully"
else
	echo "[INFO] no binder is existing"
fi
echo "[INFO] start binder"
nohup ./test_client.py>print.out &
echo `ps -ef | grep test_client | grep -v grep`
echo "[INFO] binder is starting ...."

