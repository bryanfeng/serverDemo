#!/bin/bash

# 项目地址
projectPath="/home/bryanfeng/pm"
# 代码放置路径
codePath=$projectPath'/code'
# git远端地址
gitPath='git@github.com:bryanfeng/springboot-demo.git'
# 工程文件名
projectName="springboot-demo"
# 打包后到jar名称
jarName="demo-0.0.1-SNAPSHOT.jar" 
# config 地址
configPath=$projectPath"/config"



echo "============================================================="
echo $0 "begin update code from svn and complie"
echo "update from git:" $gitPath

# 判断当前代码是否下载，如果没有直接clone，如果下载就更新
if [ -d $codePath"/"$projectName ];then
	echo "code folder exist，git pull command"
	# cd $codePath"/"$projectName
	# TODO 这里后续需要改，因为默认clone下来是master分支，切换到dev很有可能冲突
	#git pull
	#这里不能直接拉，因为编译后，有些没有排查的class文件变更，导致pull失败
	#rm -rf
	rm -rf $codePath"/"$projectName
	git clone $gitPath
else
	echo "code folder not exist，git clone command"
	git clone $gitPath
fi

# 替换配置文件
cp $configPath'/application.properties' $codePath'/springboot-demo/src/main/resources/application.properties'

# 最新代码编译为jar
echo "begin mvn package"
cd $codePath"/"$projectName
mvn clean package

# 打包好的内容移动到单独地方进行部署
if [ -f $codePath"/"$projectName"/target/"$jarName ];then
        echo $jarName " is complie success"
else
	echo $jarName " is complie fail! "
fi

# 移动到要启动到地方
cp $codePath"/"$projectName"/target/"$jarName $codePath"/../application/"
echo 'move' $codePath"/"$projectName"/target/"$jarName 'to' $codePath"/../application/"

echo $0 "finish update code from svn and complie"
echo "============================================================="


