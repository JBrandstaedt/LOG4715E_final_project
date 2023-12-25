# Set environment variables for proxy.py
echo export KEYPAIR=$1 | sudo tee -a /etc/environment
echo export MANAGER_PRIVATE_DNS=$2 | sudo tee -a /etc/environment
echo export WORKER1_PRIVATE_DNS=$3 | sudo tee -a /etc/environment
echo export WORKER2_PRIVATE_DNS=$4 | sudo tee -a /etc/environment
echo export WORKER3_PRIVATE_DNS=$5 | sudo tee -a /etc/environment

sudo apt update
sudo apt install -y python3-pip
sudo pip install paramiko sshtunnel pymysql pythonping