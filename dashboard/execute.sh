#!/usr/bin/env bash

service=${PWD##*/}  

read -p "Available Command :
1.build
2.bash
3.run
4.clean
5.images
6.status 
Execute Command >> " input 

if [ $input == 1 ]
then
    git pull
    sudo docker build -t $service .
    sudo docker rmi $(sudo docker images | grep "^<none" | awk '{print $3}') --force
elif [ $input == 2 ]
then
    sudo docker run -it $service bash
elif [ $input == 3 ]
then
    sudo docker run $service
elif [ $input == 4 ]
then
    sudo docker rm -f $(sudo docker ps -a -q)
    sudo docker rmi $(sudo docker images | grep "^<none" | awk '{print $3}') --force
elif [ $input == 5 ]
then 
    sudo docker images
elif [ $input == 6 ]
then 
    sudo docker-compose ps -a
elif [ $input == 'stop' ]
then
sudo docker stop $service
else
echo Sorry command for $input not found
fi