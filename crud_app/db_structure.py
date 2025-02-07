from dataclasses import dataclass
from enum import StrEnum, auto
from typing import List, NamedTuple


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


@dataclass
class Kontraktor:
    idkontr: int
    imie: str
    nazwisko: str
    przelozony: int
    data_zatrudn: str = None
    stawka_godzinowa: float = None
    plec: str = None

    @staticmethod
    def generate_update_query_str():
        return "UPDATE kontraktorzy SET imie=%(imie)s, nazwisko=%(nazwisko)s, przelozony=%(przelozony)s, " \
               "data_zatrudn=%(data_zatrudn)s, stawka_godzinowa=%(stawka_godzinowa)s, plec=%(plec)s " \
               "WHERE idkontr=%(idkontr)s"


@dataclass
class Pracownik:
    idprac: int
    imie: str
    nazwisko: str
    stanowisko: int
    przelozony: int
    zespol: int
    data_zatrudn: str = None
    wynagrodzenie: float = None
    plec: str = None

    @staticmethod
    def generate_update_query_str():
        return "UPDATE pracownicy SET imie=%(imie)s, nazwisko=%(nazwisko)s, stanowisko=%(stanowisko)s, " \
               "przelozony=%(przelozony)s, data_zatrudn=%(data_zatrudn)s, zespol=%(zespol)s, " \
               "wynagrodzenie=%(wynagrodzenie)s, plec=%(plec)s WHERE idprac=%(idprac)s"


@dataclass
class Stanowisko:
    idstanow: int
    nazwa: str
    placa_min: float = None
    placa_max: float = None

    @staticmethod
    def generate_update_query_str():
        return "UPDATE stanowiska SET nazwa=%(nazwa)s, placa_min=%(placa_min)s, placa_max=%(placa_max)s " \
                "WHERE idstanow=%(idstanow)s"


@dataclass
class Zespol:
    idzespol: int
    nazwa: str
    dzial: str

    @staticmethod
    def generate_update_query_str():
        return "UPDATE zespoly SET nazwa=%(nazwa)s, dzial=%(dzial)s WHERE idzespol=%(idzespol)s"
