#!/usr/bin/env bash

service=${PWD##*/}  

echo "Execute command [ build | run | bash | clean ]"
read input

if [ $input == 'build' ]
then
git pull
sudo docker build -t $service .
sudo docker rmi $(sudo docker images | grep "^<none" | awk '{print $3}') --force
elif [ $input == 'bash' ]
then
sudo docker run -it $service bash
elif [ $input == 'run' ]
then
sudo docker run $service
elif [ $input == 'clean' ]
then
bash ../docker-clean.sh
elif [ $input == 'stop' ]
then
sudo docker stop $service
else
echo Sorry command for $input not found
fi