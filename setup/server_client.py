import paramiko
import time
import logging

class ServerClient:
    def __init__(self, hostname, username, private_key_file, connection_try=20) -> None:
        """
        Instanciate the standalone server

        Parameters:
        - hostname: name of server to connect
        - username: used for identification
        - private_key: filename of private key
        """
        self.clientSSH = paramiko.SSHClient()
        self.clientSSH.load_system_host_keys()
        self.clientSSH.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # logging.basicConfig()
        # logging.getLogger("paramiko").setLevel(logging.DEBUG)
                                       
        while True:
            try:
              self.clientSSH.connect(hostname, username=username, key_filename=private_key_file)
            except paramiko.ssh_exception.NoValidConnectionsError as error:
                time.sleep(10)
            else:
                break
        
        self.clientFTP = self.clientSSH.open_sftp()

    def exec_command(self, command):
        """Execute the given command on SSH serv
        
        Parameters:
        - command: command to execute
        """
        
        stdin, stdout, stderr = self.clientSSH.exec_command(command)

    def close_connection(self):
        """
        Close SSH connection to server
        """
        self.clientSSH.close()

    def download_file(self, remote_filepath, local_filepath):
        """
        Download a file from SFTP to local
        """
        self.clientFTP.get(remote_filepath, local_filepath)

    def upload_file(self, remote_filepath, local_filepath):
        """
        Upload a file from local to SFTP
        """
        self.clientFTP.put(local_filepath, remote_filepath)