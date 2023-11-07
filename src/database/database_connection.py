'''Context Manager for the database'''

import sqlite3


class DatabaseConnection:
    ''' A class for sqlite3 database connection
        Automatically opens, commits and closes the connections
        
        Implements Singleton Design Pattern
    '''

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance') or not cls.instance:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self, host):
        self.connection = None
        self.host = host

    def __enter__(self):
        self.connection = sqlite3.connect(self.host)
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_tb or exc_val:
            self.connection.close()
        else:
            self.connection.commit()
            self.connection.close()
