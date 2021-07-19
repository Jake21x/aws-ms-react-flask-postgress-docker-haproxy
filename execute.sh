# #!/usr/bin/env bash

# service=${PWD##*/}  

# echo "Execute command [ up | down | clean | images | status ]"
# read input

# if [ $input == 'up' ]
# then
#     sudo docker-compose up
# elif [ $input == 'down' ]
# then
#     sudo docker-compose down
#     sudo docker rm -f $(sudo docker ps -a -q)
#     sudo docker rmi $(sudo docker images | grep "^<none" | awk '{print $3}') --force
# elif [ $input == 'clean' ]
# then
#     sudo docker rm -f $(sudo docker ps -a -q)
#     sudo docker rmi $(sudo docker images | grep "^<none" | awk '{print $3}') --force
# elif [ $input == 'images' ]
# then 
#     sudo docker images
# elif [ $input == 'status' ]
# then 
#     sudo docker-compose ps -a
# elif [ $input == 'stop' ]
#     echo "No command"
# then
#     echo Sorry command for $input not found
# else
#     echo Sorry command for $input not found
# fi

#!/usr/bin/env bash

service=${PWD##*/}  

read -p "Available Command :
1.up
2.down
3.clean
4.images
5.status 
Execute Command >> " input 

if [ $input == 1 ]
then
    sudo docker-compose up
elif [ $input == 2 ]
then
    sudo docker-compose down
    sudo docker rm -f $(sudo docker ps -a -q)
    sudo docker rmi $(sudo docker images | grep "^<none" | awk '{print $3}') --force
elif [ $input == 3 ]
then
    sudo docker rm -f $(sudo docker ps -a -q)
    sudo docker rmi $(sudo docker images | grep "^<none" | awk '{print $3}') --force
elif [ $input == 4 ]
then
    sudo docker images
elif [ $input == 5 ]
then 
    sudo docker-compose ps -a
elif [ $input == 6 ]
then 
    echo Sorry command for $input not found
elif [ $input == 'stop' ]
then
    sudo docker stop $service
else
    echo Sorry command for $input not found
fi