from proxy_connect import SQLConnect
from sshtunnel import SSHTunnelForwarder
from pythonping import ping
import random
import os
import sys

class ProxyServer:
    """Proxy pattern implementation used to route requests to MySQL cluster."""
    def __init__(self, private_key, manager_private_dns, worker1_private_dns, worker2_private_dns, worker3_private_dns):
        self.private_key = private_key
        self.manager_private_dns = manager_private_dns
        self.worker1_private_dns = worker1_private_dns
        self.worker2_private_dns = worker2_private_dns
        self.worker3_private_dns = worker3_private_dns


    def forward_request(self, target_host, query):
        """SSH Tunnel for following requests.
        
        Parameters
        ----------
        target_host :   string
        query : string
        """
        with SSHTunnelForwarder(target_host, ssh_username="ubuntu", ssh_pkey=self.private_key, remote_bind_address=(self.manager_private_dns, 3306)):
            SQLConnect(self.manager_private_dns).execute_query(query)     

        
    def direct_hit(self, query):
        """Directly to SQL manager.
        
        Parameters
        ----------
        query : string
        """
        self.forward_request(self.manager_private_dns, query)

    
    def random_hit(self, query):
        """Contact a random worker among the three available.
        
        Parameters
        ----------
        query : string
        """
        # Choose randomly a data node
        target_host = random.choice([self.worker1_private_dns, self.worker2_private_dns, self.worker3_private_dns])
        print(f"Chosen worker node: {target_host}")
        self.forward_request(target_host, query)


    def ping_server(self, server_private_dns):
        return ping(target=server_private_dns, count=1, timeout=2).rtt_avg_ms
        

   
    def custom_hit(self, query):
        """Contact node with the lowest ping.
        Parameters
        ----------
        query : string
        """
        nodes = [self.worker1_private_dns, self.worker2_private_dns, self.worker3_private_dns]
        # Compute average latencies
        avg_latencies = [self.ping_server(host) for host in nodes]
        # Choose worker according to latency
        fastest_node = nodes[avg_latencies.index(min(avg_latencies))]
        print(f"Chosen node: {fastest_node}")
        self.forward_request(fastest_node, query)


if __name__ == "__main__":

    # Get env variables
    private_key = os.getenv('KEYPAIR')
    manager_private_dns = os.getenv('MANAGER_PRIVATE_DNS')
    worker1_private_dns = os.getenv('WORKER1_PRIVATE_DNS')
    worker2_private_dns = os.getenv('WORKER2_PRIVATE_DNS')
    worker3_private_dns = os.getenv('WORKER3_PRIVATE_DNS')

    # Get passed request
    query = sys.argv[1]

    proxy = ProxyServer(private_key, manager_private_dns, worker1_private_dns, worker2_private_dns, worker3_private_dns)

    print("proxy direct hit:")
    proxy.direct_hit(query)

    print("proxy random hit:")
    proxy.random_hit(query)

    print("proxy custom hit:")
    proxy.custom_hit(query)