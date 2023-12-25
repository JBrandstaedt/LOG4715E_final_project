import pymysql


class SQLConnect:
    def __init__(self, manager_private_dns):
        self.connection = self.create_connection(manager_private_dns)
        pass


    def create_connection(self, host):
        # Connect to the database
        connection = pymysql.connect(host=host,
                                    port=3306,
                                    user='proxy',
                                    password='pwd',
                                    database='sakila',
                                    autocommit=True)

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