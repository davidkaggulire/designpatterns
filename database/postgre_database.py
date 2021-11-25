# patterns.py


import psycopg2
from psycopg2.extras import RealDictCursor
from .database_interface import IDatabase
from typing import Dict, Tuple


class PostgreSQLDatabase(IDatabase):
    """postgresql database"""
    def __init__(self):
        pass
        # Connect to your postgres DB
        # self.conn = None
        # # Open a cursor to perform database operations
        # self.cur = None

    def connect(self):
        try:
            db_name = "sampledb"
            self.conn = psycopg2.connect(dbname=db_name, user="postgres", password="password", host="localhost", port="5432")
            print(self.conn)
            self.conn.autocommit = True
            self.cur = self.conn.cursor()
            self.dict_cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            print(f"Connected to {db_name}")
        except Exception:
            print("Connection to PostgreSQL failed")
        return True

    def disconnect(self):
        if self.conn:
            query = "DROP TABLE IF EXISTS contact"
            self.cur.execute(query)
            self.cur.close()
            self.conn.close()
            print("PostgreSQL connection is closed")
        return super().disconnect()

    def create_table(self):
        create_table = ("CREATE TABLE IF NOT EXISTS contact"
                        "("
                        "id serial PRIMARY KEY,"
                        "name VARCHAR (50) NOT NULL,"
                        "contact VARCHAR (50) NOT NULL"
                        ")")

        self.cur.execute(create_table)
        return True

    def create(self, location: str, data: Dict[str, str]) -> Tuple[bool, str]:
        try:
            print(data['name'])
            self.create_table()

            insert_stmt = (
                "INSERT INTO contact (id, name, contact) "
                "VALUES (%s, %s, %s)"
            )
            record_to_insert = (location, data['name'], data['phone'])
            self.cur.execute(insert_stmt, record_to_insert)
            count = self.cur.rowcount
            print(count, "Record inserted successfully into mobile table")
            reason = "Data inserted into database successfully"
            return True, reason

        except (Exception, psycopg2.Error) as error:
            print("Failed to insert record into mobile table: ", error)
            reason = "failed to create data in location"
            return False, reason

    def read(self, location: str) -> Tuple[bool, str, Dict[str, str]]:
        
        print("Table After reading record ")
        sql_select_query = """SELECT * from contact where id=%s"""
        self.cur.execute(sql_select_query, (location,))
        record = self.cur.fetchone()
        print("xxxx")
        print(record)
        if record is not None:
            reason = f"-Data viewed successfully in location {location}"
            print(reason)
            return True, reason, record

        else:
            print("Error in read operation")
            reason = (
                f"-Failed to read data in location {location} "
            )
            return False, reason, ""

    def update(self, location: str, data: Dict[str, str]) -> Tuple[bool, str]:
        print("Table Before updating record ")
        sql_select_query = """select * from contact where id = %s"""
        self.cur.execute(sql_select_query, (location,))
        record = self.cur.fetchone()
        print(record)

        # Update single record now
        sql_update_query = """UPDATE contact SET name=%s where id=%s"""
        self.cur.execute(sql_update_query, (data['name'], location))

        count = self.cur.rowcount
        print(count, "Record Updated successfully ")

        print("Table After updating record ")
        sql_select_query = """select * from contact where id = %s"""
        self.cur.execute(sql_select_query, (location,))
        record = self.cur.fetchone()
        print(record)

        if record is not None:

            reason = "Data updated into database successfully"
            return True, reason

        else:
            print("Error in update operation")
            reason = (
                f"-Failed to update data in location {location} "
            )
            return False, reason

    def delete(self, location: str) -> Tuple[bool, str]:
        try:
            # Delete single record now
            sql_delete_query = """DELETE FROM contact where id=%s"""
            self.cur.execute(sql_delete_query, (location,))
            count = self.cur.rowcount
            print(count, "Record deleted successfully ")
            reason = f"-Data deleted successfully in location {location}"
            print(reason)
            return True, reason
        except (Exception, psycopg2.Error) as error:
            print("Error in Delete operation", error)
            reason = "Record not found"
            print(reason)
            return False, reason
