# sakila
sudo wget https://downloads.mysql.com/docs/sakila-db.tar.gz;
sudo tar -xf sakila-db.tar.gz;

# Create database
sudo mysql -e "SOURCE /home/ubuntu/sakila-db/sakila-schema.sql;";
sudo mysql -e "SOURCE /home/ubuntu/sakila-db/sakila-data.sql;";

sudo apt-get install -y sysbench
sudo sysbench oltp_insert --table-size=100000 --mysql-db=sakila --mysql-user=root prepare
sudo sysbench oltp_read_write --table-size=100000 --db-driver=mysql --mysql-db=sakila --mysql-user=root --time=30 --max-requests=0 --threads=6 
run > benchmark_results.txt

sudo sysbench oltp_read_write --mysql-db=sakila --mysql-user=root cleanup