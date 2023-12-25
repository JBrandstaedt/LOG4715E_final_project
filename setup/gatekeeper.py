from proxy_connect import SQLConnect
from sshtunnel import SSHTunnelForwarder
import random
import os
import sys

class GateKeeper:
    """Proxy pattern implementation used to route requests to MySQL cluster."""
    def __init__(self, private_key, trusted_host_private_dns):
        self.private_key = private_key
        self.trusted_host_private_dns = trusted_host_private_dns 

    def forward_request(self, target_host, query):
        """SSH Tunnel for following requests.
        
        Parameters
        ----------
        target_host :   string
        query : string
        """
        with SSHTunnelForwarder(target_host, ssh_username="ubuntu", ssh_pkey=self.private_key, remote_bind_address=(self.trusted_host_private_dns, 3306)):
            SQLConnect(self.trusted_host_private_dns).execute_query(query)     

        
    def forward(self, query):
        """Directly to SQL manager.
        
        Parameters
        ----------
        query : string
        """
        self.forward_request(self.trusted_host_private_dns, query)


if __name__ == "__main__":

    # Get env variables
    private_key = os.getenv('KEYPAIR')
    th_private_dns = os.getenv('TRUSTED_HOST_DNS')

    query = sys.argv[1]

    gatekeeper = GateKeeper(private_key, th_private_dns)

    gatekeeper.forward(query)

    # wait for response and send the result

