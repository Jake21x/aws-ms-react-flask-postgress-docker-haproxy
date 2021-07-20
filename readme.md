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

# install docker engine

curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# install docker compose

# sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# sudo chmod +x /usr/local/bin/docker-compose
