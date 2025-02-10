"""
Database interface definition for FastHTML application backend.
"""
from dataclasses import asdict
from typing import List, Set

import mysql.connector

from crud_app.db_structure import (FieldDetails, Kontraktor, Pracownik,
                                   Stanowisko, TABLE_DETAILS, Tables, Zespol)


class DbInterface:
    """
    Class representing the interface to the database, depends on `db_structure` objects.
    """
    def __init__(self, db_user: str, db_pass: str, db_host: str, db_name: str):
        self.connection = mysql.connector.connect(user = db_user, password = db_pass,
                                                  host = db_host, database = db_name)

    def __del__(self):
        self.connection.close()

    @staticmethod
    def get_tables() -> Set[str]:
        """
        :return: Set of table names available for CRUD operations
        """
        return {table.value for table in Tables}

    @staticmethod
    def check_table_exists(table_name: Tables):
        """
        :param table_name: Table name to check
        :return: bool value indicating if the table exists
        """
        return table_name in Tables

    def get_table_data(self, table_name: Tables):
        """
        :param table_name: Table name to get data from
        :return: list of tuples with the data from the table
        """
        if table_name not in Tables:
            raise ValueError(f"Invalid table {table_name}")

        with self.connection.cursor() as cursor:
            table_fields = ','.join([field.name for field in TABLE_DETAILS[table_name].fields_details])
            cursor.execute(f"SELECT {table_fields} FROM {table_name}")
            return cursor.fetchall()

    def get_record_data(self, table_name: Tables, id: int):
        if table_name not in Tables:
            raise ValueError(f"Invalid table {table_name}")

        with self.connection.cursor() as cursor:
            table_fields = ','.join([field.name for field in TABLE_DETAILS[table_name].fields_details])
            cursor.execute(f"SELECT {table_fields} FROM {table_name} "
                           f"WHERE {TABLE_DETAILS[table_name].primary_key} = %(id)s",
                           {'id':id})
            return cursor.fetchone()

    def remove_table_row(self, table_name: Tables, id: int):
        if table_name not in Tables:
            raise ValueError(f"Invalid table {table_name}")

        with self.connection.cursor() as cursor:
            cursor.execute(f"DELETE FROM {table_name} "
                           f"WHERE {TABLE_DETAILS[table_name].primary_key} = %(id)s",
                           {'id':id})
        self.connection.commit()

    def update_table_row(self, table_name: Tables, id: int,
                         data: type[Kontraktor | Pracownik | Stanowisko | Zespol]):
        if table_name not in Tables:
            raise ValueError(f"Invalid table {table_name}")

        if id != int(getattr(data, TABLE_DETAILS[table_name].primary_key)):
            raise ValueError("Primary key value mismatch")

        if table_name == Tables.KONTRAKTORZY:
            query_template = Kontraktor.generate_update_query_str()
        elif table_name == Tables.PRACOWNICY:
            query_template = Pracownik.generate_update_query_str()
        elif table_name == Tables.STANOWISKA:
            query_template = Stanowisko.generate_update_query_str()
        elif table_name == Tables.ZESPOLY:
            query_template = Zespol.generate_update_query_str()
        else:
            raise ValueError(f"No query template available for {table_name}")

        with self.connection.cursor() as cursor:
            cursor.execute(query_template, asdict(data))

        self.connection.commit

    def insert_table_row(self, table_name: Tables,
                         data: type[Kontraktor | Pracownik | Stanowisko | Zespol]):
        if table_name not in Tables:
            raise ValueError(f"Invalid table {table_name}")

        if table_name == Tables.KONTRAKTORZY:
            query_template = Kontraktor.generate_insert_query_str()
        elif table_name == Tables.PRACOWNICY:
            query_template = Pracownik.generate_insert_query_str()
        elif table_name == Tables.STANOWISKA:
            query_template = Stanowisko.generate_insert_query_str()
        elif table_name == Tables.ZESPOLY:
            query_template = Zespol.generate_insert_query_str()
        else:
            raise ValueError(f"No query template available for {table_name}")

        with self.connection.cursor() as cursor:
            cursor.execute(query_template, asdict(data))

        self.connection.commit

    @staticmethod
    def get_table_headers(table_name: Tables) -> List[str]:
        if table_name not in Tables:
            raise ValueError(f"Invalid table {table_name}")

        return [item.header for item in TABLE_DETAILS[table_name].fields_details]

    @staticmethod
    def get_table_fields_details(table_name: Tables) -> List[FieldDetails]:
        if table_name not in Tables:
            raise ValueError(f"Invalid table {table_name}")

        return list(TABLE_DETAILS[table_name].fields_details)
