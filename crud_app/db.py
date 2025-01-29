from enum import StrEnum, auto
from pprint import pprint

import mysql.connector
from decouple import config


DB_CONN_PARAMS = {
    "user" : config("DB_USER"),
    "password" : config("DB_PASS"),
    "host" : config("DB_HOST"),
    "database" : config("DB_NAME")
}

class Tables(StrEnum):
    KONTRAKTORZY = auto()
    PRACOWNICY = auto()
    STANOWISKA = auto()
    ZESPOLY = auto()


TABLE_TO_PRIMARY_KEY_MAP = {
    Tables.KONTRAKTORZY: 'idkontr',
    Tables.PRACOWNICY: 'idprac',
    Tables.STANOWISKA: 'idstanow',
    Tables.ZESPOLY: 'idzespol'
}

TABLE_HEADERS = {
    Tables.KONTRAKTORZY: ("ID", "Imię", "Nazwisko", "Przełożony", "Data zatrudnienia", "Stawka godzinowa", "Płeć"),
    Tables.PRACOWNICY: ("ID", "Imię", "Nazwisko", "Stanowisko", "Przełożony", "Data zatrudnienia", "Zespół", "Wynagrodzenie", "Płeć"),
    Tables.STANOWISKA: ("ID", "Nazwa", "Wynagrodzenie minimalne", "Wynagrodzenie maksymalne"),
    Tables.ZESPOLY: ("ID", "Nazwa")
}

class DbInterface:
    def __init__(self):
        self.connection = mysql.connector.connect(**DB_CONN_PARAMS)

    def __del__(self):
        self.connection.close()

    def get_table_data(self, table_name: Tables):
        if table_name not in Tables:
            raise ValueError(f"Invalid table {table_name}")

        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {table_name}")
            return cursor.fetchall()

    def remove_table_row(self, table_name: Tables, id: int):
        if table_name not in Tables:
            raise ValueError(f"Invalid table {table_name}")

        with self.connection.cursor() as cursor:
            cursor.execute(f"DELETE FROM {table_name} WHERE {TABLE_TO_PRIMARY_KEY_MAP[table_name]} = %(id)s",
                           {'id':id})
        self.connection.commit()

    @staticmethod
    def get_table_headers(table_name: Tables):
        if table_name not in Tables:
            raise ValueError(f"Invalid table {table_name}")

        return TABLE_HEADERS[table_name]

    @staticmethod
    def check_table_exists(table_name: Tables):
        return table_name in Tables


if __name__ == "__main__":
    db_interface = DbInterface()
    db_interface.remove_table_row('pracownicy', 109)
    pprint(db_interface.get_table_data('pracownicy'))
