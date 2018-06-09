#!/bin/bash

path=`pwd`
pname=$path/main.py
cmd="start"

function __getpid()
{
	pid=`ps -ef | grep "[0-9] python $pname" | awk '{print $2}'`
	echo $pid
}

function f_start()
{
	echo "r.sh - server start"

	pid=`__getpid`
	if [ -n "$pid" ] ;then
		echo "r.sh - server already exists"
		return
	fi

	python $pname &

	sleep 1
	echo "r.sh - begin tail log/*.log"
	tail -f log/*.log
}

function f_kill()
{
	echo "r.sh - stop server"
	
	pid=`__getpid`
	if [ ! -n "$pid" ] ;then
		echo "r.sh - can not get pid"
		return
	fi
	echo "r.sh - kill:"$pid
	kill $pid
}

function f_restart()
{
	echo "r.sh - server restart"
	f_kill
	sleep 1
	f_start
}

if [ ! -n "$1" ] ;then  
	echo "r.sh - no command,use default 'restart'"
	cmd="restart"
else
	cmd=$1
fi


if [ "$cmd" = "start" ] ;then
	f_start
elif [ "$cmd" = "stop" ] ;then
	f_kill
elif [ "$cmd" = "restart" ] ;then
	f_restart
else
	echo "r.sh - unknown command,use 'start/stop/restart'"
fi

