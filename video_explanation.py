
print("\nCREATE:\nStandalone server...")
input("Manager...")
input("Workers...")
input("Proxy...")
input("Gatekeeper...")
input("Trusted host...")
print("Wait for instances to run correctly...")
input("Finished")
print("Upload files to SQL manager...")
input("Finished")
print("Set up workers")
input("Finished")

print(f"\nThe following next steps are required to set up correctly the SQL server\n\
Please open a new terminal and run both following commands:\n\
    ssh -i 'key_file' ubuntu@'manager_public_dns[0]'\n\
    sh setup_cluster_mysql.sh")

input("\nIf both commands were successful, you can press a key to continue with the SQL user set up...\n")

print(f"\nThe following ones are made to set up a SQL user\n\
To create the user:\n\
sudo mysql -e \"CREATE USER 'proxy'@'proxy_private_dns[0]' IDENTIFIED BY 'pwd';\"\n\
sudo mysql -e \"GRANT ALL PRIVILEGES ON *.* TO 'proxy'@'proxy_private_dns[0]';\"")

input("\nIf both commands were successful, you can press a key to continue with the proxy set up...\n")

print("\n\Benchmark is processing...\n")
print("Benchmark completed.")
print(f"Follow the next steps to setup the proxy correctly\n\
    Open a new terminal and run the following commands:\n\
        ssh -i 'key_file' ubuntu@'proxy_public_dns[0]'\n\
        sh setup_proxy.sh 'key_file' 'manager_private_dns[0]' 'worker_private_dns[0]' 'worker_private_dns[1]' 'worker_private_dns[2]'\n\
    Now you can run queries from the proxy by using commands similar to this one:\n\
        sudo python3 proxy.py \"SELECT COUNT(*) FROM actor;\"")

input("\nIf previous commands run correctly, you can press a key to continue with the Gatekeeper setup...")
print(f"Follow the next steps to setup the proxy correctly\n\
    Open a new terminal and run the following commands:\n\
        ssh -i 'key_file' ubuntu@gk_public_dns[0]'\n\
        sh setup_gatekeeper.sh 'key_file' 'trusted_private_dns[0]' \n\n\
    Open an other new terminal and run the following commands:\n\
        ssh -i 'key_file' ubuntu@'trusted_public_dns[0]'\n\
        sh setup_trusted_host.sh 'key_file' 'gk_private_dns[0]'\n\n\
    Now both Gatekeeper and Trusted Host should be running fine.\n")

input("\nIf previous commands run correctly, you can press a key to continue with the Gatekeeper setup...")

print(f"Now, you can use the whole architecture by running commands similar to the following one:\n\
        ssh -i 'key_file' ubuntu@'gk_public_dns[0]'\n\n\
    Now you are able to run any query by using this type of command in the gatekeeper:\n\
        sudo python3 gatekeeper.py \"SELECT COUNT(*) FROM actor;\"\n")
input("\n\nPress any key once you have finished.")
