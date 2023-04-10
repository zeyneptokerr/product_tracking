import json
import requests
import psycopg2.extras

class Database:
    def __init__(self):
        self.connection = self.create_connection()
        if self.connection is None:
            print("Database connection can't estabilish")
        else:
            print("Database connection estabilish")

    def create_connection(self):
        try:
            return psycopg2.connect("dbname=postgres user=dia password=dia host=localhost")
        except Exception as e:
            print(f"Func: Database -> create_connection, Unable to create connection. Error: {e}")
            return None

    def create_cursor(self):
        try:
            cursor = self.connection.cursor(cursor_factory = psycopg2.extras.DictCursor)
            return cursor
        except Exception as e:
            print(f"Func: Database -> create_cursor, Unable to create cursor. Error: {e}")
            return None
    
    def restart_connection(self):
        try:
            self.connection.close()
        except Exception as e:
            print(f"database.py -> restart_connection error: {e}")
        self.connection = self.create_connection()