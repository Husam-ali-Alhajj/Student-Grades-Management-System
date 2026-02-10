# database.py
import mysql.connector
from mysql.connector import Error

class Database:
    _connection = None

    @staticmethod
    def get_connection():
        """Create or return existing DB connection"""
        if Database._connection is None or not Database._connection.is_connected():
            Database._connection = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="813297",
                database="sis"
            )
        return Database._connection

    @staticmethod
    def get_cursor(dictionary=True):
        """Always get cursor the same way"""
        conn = Database.get_connection()
        return conn.cursor(dictionary=dictionary)

    @staticmethod
    def commit():
        Database.get_connection().commit()

    @staticmethod
    def rollback():
        Database.get_connection().rollback()

    @staticmethod
    def close():
        if Database._connection and Database._connection.is_connected():
            Database._connection.close()
            Database._connection = None
