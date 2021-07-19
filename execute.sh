#!/usr/bin/env bash

service=${PWD##*/}  

echo "Execute command [ up | down | clean ]"
read input

if [ $input == 'up' ]
then
sudo docker-compose up
elif [ $input == 'down' ]
then
sudo docker-compose down
sudo docker rm -f $(sudo docker ps -a -q)
sudo docker rmi $(sudo docker images | grep "^<none" | awk '{print $3}') --force
elif [ $input == 'clean' ]
then
sudo docker rm -f $(sudo docker ps -a -q)
sudo docker rmi $(sudo docker images | grep "^<none" | awk '{print $3}') --force
elif [ $input == 'stop' ]
then
echo Sorry command for $input not found
else
echo Sorry command for $input not found
fi