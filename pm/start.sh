#!/bin/bash


# 包所在地址
appPath="/home/bryanfeng/pm/application/"
# 打包后到jar名称
jarName="demo-0.0.1-SNAPSHOT.jar" 
# 日志
appLogFile=$appPath"application.log"

echo "============================================================="
echo $0 " start application"


# 日志文件自动生产
if [ -f "$appLogFile" ];then
	echo "app log file:" $appLogFile
else
	echo "touch app log file:" $appLogFile
	touch $appLogFile
fi

progress=`ps -ax|grep $jarName | grep -v "grep"`
pid=`ps -ax|grep $jarName | grep -v "grep" | awk '{print $1}'`

# 判断当前进程是否启动
if [ -z "$progress" ]; then 
	echo "no progress, start this"
else
	echo "progress is running, we will kill first" 
	echo $progress
	echo $pid
	kill $pid
	sleep 2
fi



nohup java -jar $appPath$jarName > $appLogFile &

echo $0 "finish start application"
echo "============================================================="
 


#git clone $gitpath
