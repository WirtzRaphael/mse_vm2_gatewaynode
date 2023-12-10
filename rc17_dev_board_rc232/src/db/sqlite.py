import sqlite3
from sqlite3 import Error
class DbConnection:
    def __init__(self, db_file):
        self.db_file = db_file
        self.connection = None
    
    def __enter__(self, *args, **kwargs):
        self.connection = create_connection(self.db_file)
        return self.connection
    
    def __exit__(self, *args, **kwargs):
        close_connection(self.connection)
        return
    
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    connection = None
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:
        print(e)
    
    return connection

def close_connection(connection):
    if connection:
        connection.close()

def create_table(connection, create_table_sql):
    """ create a table from the create_table_sql statement
    :param connection: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        cursor = connection.cursor()
        cursor.execute(create_table_sql)
    except Error as e:
        print(e)

def create_connection_test(db_file):
    """ test connection to a SQLite database """
    connection = None
    try:
        connection = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if connection:
            connection.close()
