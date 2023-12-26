import pymysql
from paramiko import SSHClient


class SQLConnect:
    def __init__(self, target_private_dns, connection_to_sql=False):
        if connection_to_sql:
            #create ssh connection
            self.client = SSHClient()
            self.connection = self.create_ssh_connection(self.client, target_private_dns)
        else:
            self.connection = self.create_sql_connection(target_private_dns)
        pass


    def create_sql_connection(self, host):
        # Connect to the database
        connection = pymysql.connect(host=host,
                                    port=3306,
                                    user='proxy',
                                    password='pwd',
                                    database='sakila',
                                    autocommit=True)

        return connection
    
    def create_ssh_connection(self, client_ssh, host_private_dns):
        connection = client_ssh.connect()

        return connection


    def execute_query(self, query):
        """SQL query using previous connection.
        
        Parameters
        ----------
        query : string
        """
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                print(cursor.fetchall())