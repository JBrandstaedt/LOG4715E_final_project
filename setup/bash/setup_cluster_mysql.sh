
# DEB package
echo "Fetch DEB package..."
sudo wget https://dev.mysql.com/get/Downloads/MySQL-Cluster-8.0/mysql-cluster_8.0.31-1ubuntu22.04_amd64.deb-bundle.tar

sudo mkdir mysql_packages

sudo tar -xvf mysql-cluster_8.0.31-1ubuntu22.04_amd64.deb-bundle.tar -C mysql_packages/

# Dependencies
echo "Install dependencies..."
sudo apt install -y libaio1 libmecab2

# Extracted package
echo "Install extracted packages..."
sudo apt install -y ./mysql_packages/mysql-common_8.0.31-1ubuntu22.04_amd64.deb
sudo apt install -y ./mysql_packages/mysql-cluster-community-client-plugins_8.0.31-1ubuntu22.04_amd64.deb
sudo apt install -y ./mysql_packages/mysql-cluster-community-client-core_8.0.31-1ubuntu22.04_amd64.deb
sudo apt install -y ./mysql_packages/mysql-cluster-community-client_8.0.31-1ubuntu22.04_amd64.deb
sudo apt install -y ./mysql_packages/mysql-client_8.0.31-1ubuntu22.04_amd64.deb
sudo apt install -y ./mysql_packages/mysql-cluster-community-server-core_8.0.31-1ubuntu22.04_amd64.deb
sudo apt install -y ./mysql_packages/mysql-cluster-community-server_8.0.31-1ubuntu22.04_amd64.deb
sudo apt install -y ./mysql_packages/mysql-server_8.0.31-1ubuntu22.04_amd64.deb

sudo mv -f mysql.cnf /etc/mysql/my.cnf

# Restart server
echo "Restarting mysql service..."
sudo pkill -f ndb_mgmd
sudo ndb_mgmd -f /var/lib/mysql-cluster/config.ini

sudo systemctl restart mysql
