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
                print('Login informations are wrong. Please check "settings.py".')
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print('The database does\'nt exist. Please check "settings.py".')
            else:
                print('Something wrong happen...')
            return False
        else:
            self.cursor = self.connection.cursor(buffered=True)
            return True

    def check_database(self):
        """
            This method check if the database is empty
            If it is, run a method for filling it
        """
        try:
            query = 'SELECT * FROM Products LIMIT 1'
            response = self.cursor.execute(query)
        except mysql.connector.Error as err:
            print(err)

        if not response:
            return False

        return True

if __name__ == '__main__':
    print('Please don\'t load me alone...')
