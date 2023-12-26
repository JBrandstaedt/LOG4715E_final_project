from proxy_connect import SQLConnect
from sshtunnel import SSHTunnelForwarder
import random
import os
import sys

class TrustedHost:
    """Proxy pattern implementation used to route requests to MySQL cluster."""
    def __init__(self, private_key, gatekeeper_private_dns):
        self.private_key = private_key
        self.gatekeeper_private_dns = gatekeeper_private_dns 

    def forward_request(self, target_host, query, target_private_dns):
        """SSH Tunnel for following requests.
        
        Parameters
        ----------
        target_host :   string
        query : string
        """

        # Connection to an other instance
        if target_private_dns != '':
            with SSHTunnelForwarder(target_host, ssh_username="ubuntu", ssh_pkey=self.private_key, remote_bind_address=(self.gatekeeper_private_dns, 3306)):
                SQLConnect(self.gatekeeper_private_dns).execute_query(query)  
        # Connection to the Gatekeeper
        else:
            with SSHTunnelForwarder(target_host, ssh_username="ubuntu", ssh_pkey=self.private_key, remote_bind_address=(target_private_dns, 3306)):
                SQLConnect(target_private_dns).execute_query(query)  


        
    def forward(self, query, target_private_dns=''):
        """Directly to SQL manager.
        
        Parameters
        ----------
        query : string
        target_private_dns: string
        """
        self.forward_request(target_private_dns, query)


if __name__ == "__main__":

    # Get env variables
    private_key = os.getenv('KEYPAIR')
    gatekeeper_private_dns = os.getenv('PROXY_DNS')

    target_private_dns = sys.argv[1]


    trusted_host = TrustedHost(private_key, gatekeeper_private_dns)

    # if sys.argv.__len__ == 2:
    #     # listen to gatekeeper
    #     query = 
    #     # get precedent request and forward it to proxy
    #     trusted_host.forward(query, target_private_dns)
    #     # wait for response from proxy 
    #     response = 
    #     #and send it back to Gatekeeper
    #     trusted_host.forward(response)