#!/bin/sh

JAR_NAME="anaconda3/bin/gerapy"

SERVER_PID=`ps auxf | grep ${JAR_NAME} | grep -v "grep"| awk '{print $2}'`
echo "${JAR_NAME} pid is ${SERVER_PID}"
if [ -n $SERVER_PID ] 
then
  kill $SERVER_PID
  echo "$SERVER_PID is killed!"
fi
