from proxy_connect import SQLConnect
from sshtunnel import SSHTunnelForwarder
import random
import os
import sys

class TrustedHost:
    """Proxy pattern implementation used to route requests to MySQL cluster."""
    def __init__(self, private_key, proxy_pirvate_dns):
        self.private_key = private_key
        self.proxy_private_dns = proxy_pirvate_dns 

    def forward_request(self, target_host, query, target_private_dns):
        """SSH Tunnel for following requests.
        
        Parameters
        ----------
        target_host :   string
        query : string
        """
        with SSHTunnelForwarder(target_host, ssh_username="ubuntu", ssh_pkey=self.private_key, remote_bind_address=(self.proxy_private_dns, 3306)):
            if (target_private_dns == ''):
                SQLConnect(self.proxy_private_dns).execute_query(query)  
            else:   
                SQLConnect(target_private_dns).execute_query(query)

        
    def forward(self, query, target_private_dns=''):
        """Directly to SQL manager.
        
        Parameters
        ----------
        query : string
        target_private_dns: string
        """
        self.forward_request(self.proxy_private_dns, query, target_private_dns)


if __name__ == "__main__":

    # Get env variables
    private_key = os.getenv('KEYPAIR')
    proxy_private_dns = os.getenv('PROXY_DNS')

    query = sys.argv[1]

    gatekeeper = TrustedHost(private_key, proxy_private_dns)

    # if sys.argv.__len__ == 2:
    # while True:
    #     # get precedent request and forward it to proxy
    #     # wait for response from proxy and send it back to Gatekeeper
    # else:
    #     target = sys.argv[2]
