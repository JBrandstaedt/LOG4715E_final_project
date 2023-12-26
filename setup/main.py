import boto3
import utils_create_instances as utils_instances
from server_client import ServerClient
import threading
import paramiko

if __name__ == "__main__":
    ec2_ressource = boto3.resource("ec2")
    ec2_client = boto3.client('ec2')
    ami_id = "ami-0c7217cdde317cfec" # ubuntu ami id 

    # It should already have multiple subnets listed, on different availability zones
    # (at least it is the case for us with our student accounts)
    ec2_client_subnets = ec2_client.describe_subnets()['Subnets']

    key_pair_name = "my_key_pair" 
    # Create EC2 key pair
    key_pair = utils_instances.create_key_pair(ec2_client, key_pair_name)
    key_file = "../key/"+key_pair_name+".pem"

    # Security group
    security_group_id = "tp3_sg"

    security_group_id_gatekeeper = "tp3_gk"

    security_group_id_trustedhost = "tp3_th"

    # Create variables used for setup
    standalone_type = 't2.micro'

    manager_type = 't2.micro'

    worker_type = 't2.micro'
    number_workers = 3

    proxy_type ='t2.large'

    gatekeeper_type='t2.large'

    trustedhost_type='t2.large'

    # We want to delete everything previously created with the same name
    # so we can create them again without any conflict
    # Delete security groups (and associated instances) if they already exist
    for group_name in [security_group_id]:
        deleted = utils_instances.delete_security_group_by_name(ec2_client, group_name)

    security_group = utils_instances.create_security_group(ec2_client, security_group_id)

    # We have a second security group for the Gatekeeper pattern
    for group_name in [security_group_id_gatekeeper]:
        deleted = utils_instances.delete_security_group_by_name(ec2_client, group_name)

    security_group_gk = utils_instances.create_security_group(ec2_client, security_group_id_gatekeeper)

    # We have a third security group for the Gatekeeper pattern (trusted host)
    for group_name in [security_group_id_trustedhost]:
        deleted = utils_instances.delete_security_group_by_name(ec2_client, group_name)

    security_group_th = utils_instances.create_security_group(ec2_client, security_group_id_trustedhost)

    # Create standalone
    print("\nCREATE:\nStandalone server...")
    standalone_instance = utils_instances.create_ec2_instances(ec2_ressource, ami_id, standalone_type, security_group, ec2_client_subnets, key_pair_name)

    # Create manager
    print("Manager...")
    manager_instance = utils_instances.create_ec2_instances(ec2_ressource, ami_id, manager_type, security_group, ec2_client_subnets, key_pair_name)
    # We wait for the instances to be running

    # Create workers
    print("Workers...")
    worker_instances = utils_instances.create_ec2_instances(ec2_ressource, ami_id, worker_type, security_group, ec2_client_subnets, key_pair_name, number_workers)
    # We wait for the instances to be running

    # Create proxy
    print("Proxy...")
    proxy_instance = utils_instances.create_ec2_instances(ec2_ressource, ami_id, proxy_type, security_group, ec2_client_subnets, key_pair_name)
    # We wait for the instances to be running

    # Create Gatekeeper
    print("Gatekeeper...")
    gatekeeper_instance = utils_instances.create_ec2_instances(ec2_ressource, ami_id, gatekeeper_type, security_group_gk, ec2_client_subnets, key_pair_name)
    # We wait for the instances to be running
   
    # Create trusted host
    print("Trusted host...")
    trustedhost_instance = utils_instances.create_ec2_instances(ec2_ressource, ami_id, trustedhost_type, security_group_th, ec2_client_subnets, key_pair_name)
    # We wait for the instances to be running

    # We wait for the instances to be running
    print("\nWait for instances to run correctly...")
    utils_instances.wait_instances_to_run(ec2_client, standalone_instance)
    utils_instances.wait_instances_to_run(ec2_client, manager_instance)
    utils_instances.wait_instances_to_run(ec2_client, worker_instances)
    utils_instances.wait_instances_to_run(ec2_client, proxy_instance)
    utils_instances.wait_instances_to_run(ec2_client, gatekeeper_instance)
    utils_instances.wait_instances_to_run(ec2_client, trustedhost_instance)


    # We get the public and private dns name for every instance
    public_dns          = [utils_instances.get_dns(ec2_client, id) for id in standalone_instance] 
    private_dns         = [utils_instances.get_dns(ec2_client, id, public=False) for id in standalone_instance]

    manager_public_dns  = [utils_instances.get_dns(ec2_client, id) for id in manager_instance]
    manager_private_dns = [utils_instances.get_dns(ec2_client, id, public=False) for id in manager_instance]

    worker_public_dns   = [utils_instances.get_dns(ec2_client, id) for id in worker_instances]
    worker_private_dns  = [utils_instances.get_dns(ec2_client, id, public=False) for id in worker_instances]

    proxy_public_dns    = [utils_instances.get_dns(ec2_client, id) for id in proxy_instance]
    proxy_private_dns   = [utils_instances.get_dns(ec2_client, id, public=False) for id in proxy_instance]

    gk_public_dns       = [utils_instances.get_dns(ec2_client, id) for id in gatekeeper_instance]
    gk_private_dns      = [utils_instances.get_dns(ec2_client, id, public=False) for id in gatekeeper_instance]

    trusted_public_dns  = [utils_instances.get_dns(ec2_client, id) for id in trustedhost_instance]
    trusted_private_dns = [utils_instances.get_dns(ec2_client, id, public=False) for id in trustedhost_instance]

    standalone_server = ServerClient(public_dns[0], 'ubuntu', key_file)

    standalone_server.exec_command("sudo apt update;")
    standalone_server.exec_command("sudo apt install -y mysql-server-8.0")
    
    standalone_server.upload_file(local_filepath='/home/jbrandstaedt/PolyMtl/Cloud_Computing/TP3/LOG4715E_final_project/setup/bash/setup_benchmark.sh', remote_filepath='/home/ubuntu/setup_benchmark.sh')
    print("Finished")

    # We upload all needed files to the manager
    print("Upload files to SQL manager...")
    manager_server = ServerClient(manager_public_dns[0], "ubuntu", key_file)
    manager_server.upload_file(local_filepath='/home/jbrandstaedt/PolyMtl/Cloud_Computing/TP3/LOG4715E_final_project/setup/bash/setup_cluster_manager.sh', remote_filepath='/home/ubuntu/setup_cluster_manager.sh')
    manager_server.upload_file(local_filepath='/home/jbrandstaedt/PolyMtl/Cloud_Computing/TP3/LOG4715E_final_project/setup/bash/setup_cluster_mysql.sh', remote_filepath='/home/ubuntu/setup_cluster_mysql.sh')
    manager_server.upload_file(local_filepath='/home/jbrandstaedt/PolyMtl/Cloud_Computing/TP3/LOG4715E_final_project/setup/bash/setup_benchmark.sh', remote_filepath='/home/ubuntu/setup_benchmark.sh')
    manager_server.upload_file(local_filepath='/home/jbrandstaedt/PolyMtl/Cloud_Computing/TP3/LOG4715E_final_project/config/config.ini', remote_filepath='/home/ubuntu/config.ini')
    manager_server.upload_file(local_filepath='/home/jbrandstaedt/PolyMtl/Cloud_Computing/TP3/LOG4715E_final_project/config/mysql.cnf', remote_filepath='/home/ubuntu/mysql.cnf')

    manager_server.exec_command("sh setup_cluster_manager.sh")
    print("Finished")

    print("Set up workers")
    thread1 = threading.Thread(target=utils_instances.workers_thread, args=(key_file, worker_public_dns[0], 1))
    thread2 = threading.Thread(target=utils_instances.workers_thread, args=(key_file, worker_public_dns[1], 2))
    thread3 = threading.Thread(target=utils_instances.workers_thread, args=(key_file, worker_public_dns[2], 3))

    thread1.start()
    thread2.start()
    thread3.start()

    thread1.join()
    thread2.join()
    thread3.join()
    print("Finished")

    print(f"\nThe following next steps are required to set up correctly the SQL server\n\
Please open a new terminal and run both following commands:\n\
        ssh -i {key_file} ubuntu@{manager_public_dns[0]}\n\
        sh setup_cluster_mysql.sh")
    
    input("\nIf both commands were successful, you can press a key to continue with the SQL user set up...\n")

    print(f"\nThe following ones are made to set up a SQL user\n\
To create the user:\n\
    sudo mysql -e \"CREATE USER 'proxy'@'{proxy_private_dns[0]}' IDENTIFIED BY 'pwd';\"\n\
    sudo mysql -e \"GRANT ALL PRIVILEGES ON *.* TO 'proxy'@'{proxy_private_dns[0]}';\"")
    
    input("\nIf both commands were successful, you can press a key to continue with the proxy set up...\n")

    print("\n\Benchmark is processing...\n")
    manager_server.exec_command("sh setup_benchmark.sh")
    standalone_server.exec_command("sh setup_benchmark.sh")

    manager_server.download_file(remote_filepath='benchmark_results.txt', local_filepath='/home/jbrandstaedt/PolyMtl/Cloud_Computing/TP3/LOG4715E_final_project/results/sql_benchmark_results.txt')
    standalone_server.download_file(remote_filepath='benchmark_results.txt',local_filepath='/home/jbrandstaedt/PolyMtl/Cloud_Computing/TP3/LOG4715E_final_project/results/standalone_benchmark.results.txt')
    print("Benchmark completed.")


    print("Set up proxy...")
    # Setup proxy
    proxy_server = ServerClient(proxy_public_dns[0], "ubuntu", key_file)

    # Upload required files
    proxy_server.upload_file(local_filepath='/home/jbrandstaedt/PolyMtl/Cloud_Computing/TP3/LOG4715E_final_project/setup/bash/setup_proxy.sh', remote_filepath='/home/ubuntu/setup_proxy.sh')
    proxy_server.upload_file(local_filepath=f'/home/jbrandstaedt/PolyMtl/Cloud_Computing/key/{key_file}', remote_filepath=f'/home/ubuntu/{key_file}')
    proxy_server.upload_file(local_filepath='/home/jbrandstaedt/PolyMtl/Cloud_Computing/TP3/LOG4715E_final_project/setup/proxy_connect.py', remote_filepath='/home/ubuntu/proxy_connect.py')
    proxy_server.upload_file(local_filepath='/home/jbrandstaedt/PolyMtl/Cloud_Computing/TP3/LOG4715E_final_project/setup/proxy.py', remote_filepath='/home/ubuntu/proxy.py')

    print(f"Follow the next steps to setup the proxy correctly and DO NOT CLOSE the terminal\n\
        Open a new terminal and run the following commands:\n\
            ssh -i {key_file} ubuntu@{proxy_public_dns[0]}\n\
            sh setup_proxy.sh {key_file} {manager_private_dns[0]} {worker_private_dns[0]} {worker_private_dns[1]} {worker_private_dns[2]}\n\
        Now you can run queries from the proxy by using commands similar to this one:\n\
            sudo python3 proxy.py \"SELECT COUNT(*) FROM actor;\"")
    
    input("\nIf previous commands run correctly, you can press a key to continue with the Gatekeeper setup...")

    # Setup gatekeeper
    gatekeeper_server = ServerClient(gk_public_dns[0], "ubuntu", key_file)
    trustedhost_server = ServerClient(trusted_public_dns[0], "ubuntu", key_file)

    gatekeeper_server.upload_file(local_filepath='/home/jbrandstaedt/PolyMtl/Cloud_Computing/TP3/LOG4715E_final_project/setup/bash/setup_gatekeeper.sh', remote_filepath='/home/ubuntu/setup_gatekeeper.sh')
    gatekeeper_server.upload_file(local_filepath=f'/home/jbrandstaedt/PolyMtl/Cloud_Computing/key/{key_file}', remote_filepath=f'/home/ubuntu/{key_file}')
    gatekeeper_server.upload_file(local_filepath='/home/jbrandstaedt/PolyMtl/Cloud_Computing/TP3/LOG4715E_final_project/setup/gatekeeper.py', remote_filepath='/home/ubuntu/gatekeeper.py')

    trustedhost_server.upload_file(local_filepath='/home/jbrandstaedt/PolyMtl/Cloud_Computing/TP3/LOG4715E_final_project/setup/bash/setup_trusted_host.sh', remote_filepath='/home/ubuntu/setup_trusted_host.sh')
    trustedhost_server.upload_file(local_filepath=f'/home/jbrandstaedt/PolyMtl/Cloud_Computing/key/{key_file}', remote_filepath=f'/home/ubuntu/{key_file}')
    trustedhost_server.upload_file(local_filepath='/home/jbrandstaedt/PolyMtl/Cloud_Computing/TP3/LOG4715E_final_project/setup/trusted_host.py', remote_filepath='/home/ubuntu/trusted_host.py')

    print(f"Follow the next steps to setup the proxy correctly\n\
        Open a new terminal and run the following commands:\n\
            ssh -i {key_file} ubuntu@{gk_public_dns[0]}\n\
            sh setup_gatekeeper.sh {key_file} {trusted_private_dns[0]} \n\n\
        Open an other new terminal and run the following commands:\n\
            ssh -i {key_file} ubuntu@{trusted_public_dns[0]}\n\
            sh setup_trusted_host.sh {key_file} {gk_private_dns[0]}\n\n\
        Now both Gatekeeper and Trusted Host should be running fine.\n")
    
    input("\nIf previous commands run correctly, you can press a key to continue with the Gatekeeper setup...")

print(f"Now, you can use the whole architecture by running commands similar to the following one:\n\
        ssh -i 'key_file' ubuntu@'gk_public_dns[0]'\n\n\
    Now you are able to run any query by using this type of command in the gatekeeper:\n\
        sudo python3 gatekeeper.py \"SELECT COUNT(*) FROM actor;\"\n")
input("\n\nPress any key once you have finished.")
