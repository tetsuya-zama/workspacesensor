#!/bin/sh
PID=`ps -x | grep -v grep | grep workspacesensor.py | awk '{print $1}'`
kill -9 ${PID}
