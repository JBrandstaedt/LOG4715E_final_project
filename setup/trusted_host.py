from proxy_connect import SQLConnect
from sshtunnel import SSHTunnelForwarder
import random
import os
import sys

class TrustedHost:
    """Proxy pattern implementation used to route requests to MySQL cluster."""
    def __init__(self, private_key, target_private_dns):
        self.private_key = private_key
        self.target_private_dns = target_private_dns 

    def forward_request(self, target_host, query):
        """SSH Tunnel for following requests.
        
        Parameters
        ----------
        target_host :   string
        query : string
        """
        with SSHTunnelForwarder(target_host, ssh_username="ubuntu", ssh_pkey=self.private_key, remote_bind_address=(self.target_private_dns, 3306)):
            SQLConnect(self.target_private_dns).execute_query(query)  

        
    def forward(self, query):
        """Directly to SQL manager.
        
        Parameters
        ----------
        query : string
        target_private_dns: string
        """
        self.forward_request(self.target_private_dns, query)


if __name__ == "__main__":

    # Get env variables
    private_key = os.getenv('KEYPAIR')
    gatekeeper_private_dns = os.getenv('PROXY_DNS')

    target_private_dns = sys.argv[1]

    trustedhost_proxy = TrustedHost(private_key, target_private_dns)

    trusted_host_gatekeeper = TrustedHost(private_key, gatekeeper_private_dns)
    # if sys.argv.__len__ == 2:
    # while True:
    #     # get precedent request and forward it to proxy
    #     # wait for response from proxy and send it back to Gatekeeper