# sudo docker rm -f $(sudo docker ps -a -q)

# docker rmi Image Image

# sudo docker rmi $(sudo docker images | grep "^<none" | awk '{print $3}')

# https://intellipaat.com/community/44143/how-to-uninstall-docker-in-ubuntu

sudo apt-get purge -y docker-engine docker docker.io docker-ce &&
sudo apt-get autoremove -y --purge docker-engine docker docker.io docker-ce &&
sudo rm -rf /var/lib/docker /etc/docker &&
sudo rm /etc/apparmor.d/docker &&
sudo groupdel docker &&
sudo rm -rf /var/run/docker.sock
