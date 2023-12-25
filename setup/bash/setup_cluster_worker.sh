sudo apt update
sudo apt install libclass-methodmaker-perl

# DEB package
sudo wget https://dev.mysql.com/get/Downloads/MySQL-Cluster-8.0/mysql-cluster-community-data-node_8.0.31-1ubuntu22.04_amd64.deb

sudo apt install ./mysql-cluster-community-data-node_8.0.31-1ubuntu22.04_amd64.deb

sudo mv -f my.cnf /etc/my.cnf
sudo mkdir -p /usr/local/mysql/data
sudo ndbd