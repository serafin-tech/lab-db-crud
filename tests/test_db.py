import pytest
from unittest.mock import MagicMock, patch
from crud_app.db import DbInterface
from crud_app.db_structure import Tables, FieldDetails


@pytest.fixture
def mock_db():
    with patch("mysql.connector.connect") as mock_connect:
        mock_conn = mock_connect.return_value
        mock_cursor = mock_conn.cursor.return_value.__enter__.return_value
        yield mock_conn, mock_cursor


@pytest.fixture
def db_interface(mock_db):
    mock_conn, _ = mock_db
    return DbInterface("user", "pass", "host", "dbname")


def test_get_tables():
    tables = DbInterface.get_tables()
    assert isinstance(tables, set)
    assert all(isinstance(table, str) for table in tables)


def test_check_table_exists():
    assert DbInterface.check_table_exists(Tables.PRACOWNICY) is True
    assert DbInterface.check_table_exists("NON_EXISTENT_TABLE") is False


def test_get_table_data(db_interface, mock_db):
    _, mock_cursor = mock_db
    mock_cursor.fetchall.return_value = [(1, "John Doe"), (2, "Jane Doe")]

    result = db_interface.get_table_data(Tables.PRACOWNICY)

    mock_cursor.execute.assert_called()
    assert result == [(1, "John Doe"), (2, "Jane Doe")]


def test_get_record_data(db_interface, mock_db):
    _, mock_cursor = mock_db
    mock_cursor.fetchone.return_value = (1, "John Doe")

    result = db_interface.get_record_data(Tables.PRACOWNICY, 1)

    mock_cursor.execute.assert_called()
    assert result == (1, "John Doe")


def test_remove_table_row(db_interface, mock_db):
    mock_conn, mock_cursor = mock_db

    db_interface.remove_table_row(Tables.PRACOWNICY, 1)

    mock_cursor.execute.assert_called()
    mock_conn.commit.assert_called()


# def test_update_table_row(db_interface, mock_db):
#     mock_conn, mock_cursor = mock_db
#
#     data_mock = MagicMock()
#     data_mock.generate_update_query_str.return_value = "UPDATE ..."
#     data_mock.primary_key = "id"
#
#     with patch("crud_app.db_structure.Pracownik", data_mock):
#         db_interface.update_table_row(Tables.PRACOWNICY, 1, data_mock)
#
#     mock_cursor.execute.assert_called()
#     mock_conn.commit.assert_called()


def test_get_table_headers():
    headers = DbInterface.get_table_headers(Tables.PRACOWNICY)
    assert isinstance(headers, list)
    assert all(isinstance(header, str) for header in headers)


def test_get_table_fields_details():
    details = DbInterface.get_table_fields_details(Tables.PRACOWNICY)
    assert isinstance(details, list)
    assert all(isinstance(detail, FieldDetails) for detail in details)
