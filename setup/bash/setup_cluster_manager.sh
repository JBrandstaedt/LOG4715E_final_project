# Update system
sudo apt update

sudo wget https://dev.mysql.com/get/Downloads/MySQL-Cluster-8.0/mysql-cluster-community-management-server_8.0.31-1ubuntu22.04_amd64.deb
sudo apt install -y ./mysql-cluster-community-management-server_8.0.31-1ubuntu22.04_amd64.deb

sudo mkdir /var/lib/mysql-cluster
sudo mv config.ini /var/lib/mysql-cluster/config.ini

sudo ndb_mgmd -f /var/lib/mysql-cluster/config.ini