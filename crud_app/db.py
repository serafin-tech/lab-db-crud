from enum import StrEnum, auto
from pprint import pprint
from typing import List, NamedTuple, Tuple

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


class FormFieldTypes(StrEnum):
    CHECKBOX = auto()
    DATE = auto()
    EMAIL = auto()
    HIDDEN = auto()
    NUMBER = auto()
    PASSWORD = auto()
    RADIO = auto()
    TEXT = auto()


class FieldDetails(NamedTuple):
    name: str
    header: str
    form_type: FormFieldTypes
    required: bool


class TableDetails(NamedTuple):
    table_name: str
    primary_key: str
    fields_details: List[FieldDetails]


TABLE_DETAILS = {
    Tables.KONTRAKTORZY: TableDetails(
        table_name='kontraktorzy',
        primary_key='idkontr',
        fields_details=[
            FieldDetails('idkontr', 'ID', FormFieldTypes.HIDDEN, True),
            FieldDetails('imie', 'Imię', FormFieldTypes.TEXT, True),
            FieldDetails('nazwisko', 'Nazwisko', FormFieldTypes.TEXT, True),
            FieldDetails('przelozony', 'Przełożony', FormFieldTypes.NUMBER, True),
            FieldDetails('data_zatrudn', 'Data zatrudnienia', FormFieldTypes.DATE, False),
            FieldDetails('stawka_godzinowa', 'Stawka godzinowa', FormFieldTypes.NUMBER, False),
            FieldDetails('plec', 'Płeć', FormFieldTypes.RADIO, False)
        ]
    ),
    Tables.PRACOWNICY: TableDetails(
        table_name='pracownicy',
        primary_key='idprac',
        fields_details=[
            FieldDetails('idprac', 'ID', FormFieldTypes.HIDDEN, True),
            FieldDetails('imie', 'Imię', FormFieldTypes.TEXT, True),
            FieldDetails('nazwisko', 'Nazwisko', FormFieldTypes.TEXT, True),
            FieldDetails('stanowisko', 'Stanowisko', FormFieldTypes.NUMBER, True),
            FieldDetails('przelozony', 'Przełożony', FormFieldTypes.NUMBER, True),
            FieldDetails('data_zatrudn', 'Data zatrudnienia', FormFieldTypes.DATE, False),
            FieldDetails('zespol', 'Zespół', FormFieldTypes.NUMBER, True),
            FieldDetails('wynagrodzenie', 'Wynagrodzenie', FormFieldTypes.NUMBER, False),
            FieldDetails('plec', 'Płeć', FormFieldTypes.RADIO, False)
        ]
    ),
    Tables.STANOWISKA: TableDetails(
        table_name='stanowiska',
        primary_key='idstanow',
        fields_details=[
            FieldDetails('idstanow', 'ID', FormFieldTypes.HIDDEN, True),
            FieldDetails('nazwa', 'Nazwa', FormFieldTypes.TEXT, True),
            FieldDetails('placa_min', 'Wynagrodzenie minimalne', FormFieldTypes.NUMBER, False),
            FieldDetails('placa_max', 'Wynagrodzenie maksymalne', FormFieldTypes.NUMBER, False)
        ]
    ),
    Tables.ZESPOLY: TableDetails(
        table_name='zespoły',
        primary_key='idzespol',
        fields_details=[
            FieldDetails('idzespol', 'ID', FormFieldTypes.HIDDEN, True),
            FieldDetails('nazwa', 'Nazwa', FormFieldTypes.TEXT, True),
            FieldDetails('dzial', 'Dział', FormFieldTypes.TEXT, True)
        ]
    )
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

    @staticmethod
    def get_table_headers(table_name: Tables) -> List[str]:
        if table_name not in Tables:
            raise ValueError(f"Invalid table {table_name}")

        return [item.header for item in TABLE_DETAILS[table_name].fields_details]

    @staticmethod
    def check_table_exists(table_name: Tables):
        return table_name in Tables

    @staticmethod
    def get_table_fields_details(table_name: Tables) -> List[FieldDetails]:
        if table_name not in Tables:
            raise ValueError(f"Invalid table {table_name}")

        return list(TABLE_DETAILS[table_name].fields_details)


if __name__ == "__main__":
    db_interface = DbInterface()
    db_interface.remove_table_row('pracownicy', 109)
    pprint(db_interface.get_table_data('pracownicy'))
