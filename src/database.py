"""
    This module manage all operations with the database
"""
import mysql.connector
from mysql.connector import errorcode


class Database:
    """
        This class manage differents operations with the database like:
            - connection
            - insert data
            - remove data
            - select data
    """

    def __init__(self, db_name, user, host, password):
        self.db_name = db_name
        self.user = user
        self.host = host
        self.password = password
        self.connection = False
        self.cursor = False

    def connect_databse(self):
        """
            This method connect the application to the database
        """

        # Connect to the database
        try:
            self.connection = mysql.connector.connect(
                user=self.user,
                host=self.host,
                password=self.password,
                database=self.db_name)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                raise Exception(f'Login informations are wrong. Please check "settings.py".\n{err}')
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                raise Exception(f'The database does\'nt exist. Please check "settings.py".\n{err}')
            raise err
        else:
            self.cursor = self.connection.cursor(buffered=True)

    def check_database(self):
        """
            This method check if the database is empty
            If it is, run a method for filling it
        """
        try:
            query = 'SELECT * FROM Products LIMIT 1'
            self.cursor.execute(query)
        except mysql.connector.Error as err:
            print(err)

        return self.cursor.fetchone()

    def insert_in_database(self, query, values):
        """
            This method insert in the database with "query" as argument and an optionnal crieterion
            to manage possible duplicates entry
        """
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
        except mysql.connector.Error as err:
            if err.errno != 1062: # Duplicates entries
                print(err)

    def select_in_database(self, query, values=None):
        """
            This method select data in the database
        """
        try:
            self.cursor.execute(query, values)
        except mysql.connector.Error as err:
            print(err)

        return self.cursor

    def close_database(self):
        """
            This method is called for closing the connection with the database
        """
        self.cursor.close()
        self.connection.close()

if __name__ == '__main__':
    print('Please don\'t load me alone...')
