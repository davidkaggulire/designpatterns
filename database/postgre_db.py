# patterns.py


import psycopg2
from .database_interface import IDatabase
from typing import Dict, Tuple


class PostgreSQLDatabase(IDatabase):
    """sql database"""
    def __init__(self):
        try:
            db_name = "sampledb"

            # Connect to your postgres DB
            self.conn = psycopg2.connect(dbname=db_name, user="postgres", password="password", host="localhost", port="5432")
            print(self.conn)
            self.conn.autocommit = True
            # Open a cursor to perform database operations
            self.cur = self.conn.cursor()

            # Execute a query
            # cur.execute("SELECT * FROM my_data")

            # Retrieve query results
            # records = cur.fetchall()
            print("Connected to {}".format(db_name))
        except Exception:
            print("Database connection failed")

    def connect(self):
        try:
            db_name = "sampledb"
            self.conn = psycopg2.connect(dbname=db_name, user="postgres", password="password", host="localhost", port="5432")
            print(self.conn)
            self.conn.autocommit = True
            print(f"Connected to {db_name}")
        except Exception:
            print("Connection to PostgreSQL failed")
        return True


    def disconnect(self):
        return super().disconnect()

    def create_table(self):
        create_table = ("CREATE TABLE IF NOT EXISTS contact"
                        "("
                        "id serial PRIMARY KEY,"
                        "name VARCHAR (50) NOT NULL,"
                       "contact VARCHAR (50) NOT NULL"
                        ")")

        self.cur.execute(create_table)

    def create(self, location: str, data: Dict[str, str]) -> Tuple[bool, str]:
        print(data['name'])

        insert_stmt = (
            "INSERT INTO contact (id, name, contact) "
            "VALUES (%s, %s, %s)"
        )
        fi_data = (location, data['name'], data['phone'])
        self.cur.execute(insert_stmt, fi_data)
        reason = "Data inserted into database successfully"
        return True, reason

    def read(self, location: str) -> Tuple[bool, str, Dict[str, str]]:
        return super().read(location)

    def update(self, location: str, data: Dict[str, str]) -> Tuple[bool, str]:
        return super().update(location, data)

    def delete(self, location: str) -> Tuple[bool, str]:
        return super().delete(location)
