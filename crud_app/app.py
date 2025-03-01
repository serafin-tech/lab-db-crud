# pylint: disable=undefined-variable
from decouple import config
from fasthtml.common import *  # pylint: disable=unused-wildcard-import
from fasthtml.components import *  # pylint: disable=unused-wildcard-import

from crud_app.db import DbInterface
from crud_app.db_structure import FieldDetails, FormFieldTypes, Kontraktor, Pracownik, Stanowisko, Zespol


css = Style(':root {--pico-font-size:90%,--pico-font-family: Pacifico, cursive;}')
app = FastHTML(hdrs=(picolink, css))

rt = app.route

db_interface = DbInterface(db_user=config("DB_USER"),
                           db_pass=config("DB_PASS"),
                           db_host=config("DB_HOST"),
                           db_name=config("DB_NAME"))


def page_template(header: str, payload):
    return (Title("CRUD Application"),
            Main(Div(H1(header), payload),
                 cls="container"))


@rt("/")
def get():
    return page_template(header="Tables",
                         payload=Div(*[P(A(item.capitalize(), href=f"/{item}"))
                                       for item in sorted(db_interface.get_tables())]))


def generate_action_buttons(url_prefix, id):
    return Td(Group(
        A("Edytuj", href=f"{url_prefix}/edit/{id}", role="button", cls="button is-small is-primary"),
        A("Usuń", href=f"{url_prefix}/remove?id={id}", role="button", cls="button is-small is-danger",
          hx_confirm="Are you sure?", hx_delete=f"{url_prefix}/remove?id={id}")))


def generate_table(headers, table_data, actions_url_prefix):
    return Container(Table(
        Thead(Tr(*[Th(col) for col in headers], Th("Akcje"))),
        Tbody(*[Tr(*[Td(str(cell)) for cell in row],
                   generate_action_buttons(actions_url_prefix, row[0])) for row in table_data])),
        A("Nowy element", href=f"{actions_url_prefix}/new", role="button", cls="button is-small is-primary"))


def generate_form(fields_details: List[FieldDetails], record_data:List[str], submit_url: str):
    return Form(
        *[Div(
            Label(field_details.header, cls="label", for_=field_details.name)
                if field_details.form_type != FormFieldTypes.HIDDEN else None,
            Input(value=str(cell_value), name=field_details.name, id=field_details.name,
                  type=field_details.form_type, cls="input")
        )
            for field_details, cell_value in zip(fields_details, record_data)
        ],
        Input(type="submit", value="Zapisz", cls="button is-primary"),
        action=submit_url,
        method="POST")


@rt("/{table_name}")
def get(table_name: str):
    if not db_interface.check_table_exists(table_name):
        return Response(status_code=404)

    table_data = db_interface.get_table_data(table_name)
    table_headers = db_interface.get_table_headers(table_name)

    return page_template(header=table_name.capitalize(),
                         payload=generate_table(table_headers, table_data, f"/{table_name}"))


@rt("/{table_name}/remove")
def delete(table_name: str, id:int):
    if not db_interface.check_table_exists(table_name):
        return Response(status_code=404)

    db_interface.remove_table_row(table_name, id)
    return Redirect(f"/{table_name}")


@rt("/{table_name}/new")
def get(table_name: str):
    if not db_interface.check_table_exists(table_name):
        return Response(status_code=404)

    table_fields_details = db_interface.get_table_fields_details(table_name)
    record_data = ['' for _ in table_fields_details]

    return page_template(header=f"{table_name.capitalize()}, nowy record",
                         payload=generate_form(table_fields_details, record_data, f"/{table_name}/0"))


@rt("/{table_name}/edit/{id}")
def get(table_name: str, id:int):
    if not db_interface.check_table_exists(table_name):
        return Response(status_code=404)

    table_fields_details = db_interface.get_table_fields_details(table_name)
    record_data = db_interface.get_record_data(table_name, id)

    return page_template(header=f"{table_name.capitalize()}, record: {id}",
                         payload=generate_form(table_fields_details, record_data, f"/{table_name}/{id}"))


@rt("/kontraktorzy/{id}")
def post(id:int, data:Kontraktor):
    return post_processing('kontraktorzy', id, data)


@rt("/pracownicy/{id}")
def post(id:int, data:Pracownik):
    return post_processing('pracownicy', id, data)


@rt("/stanowiska/{id}")
def post(id:int, data:Stanowisko):
    return post_processing('stanowiska', id, data)


@rt("/zespoly/{id}")
def post(id:int, data:Zespol):
    return post_processing('zespoly', id, data)


def post_processing(table_name: str, id:int, data: type[Kontraktor | Pracownik | Stanowisko | Zespol]):
    if not db_interface.check_table_exists(table_name):
        return Response(status_code=404)

    if id > 0:
        db_interface.update_table_row(table_name, id, data)
    else:
        db_interface.insert_table_row(table_name, data)

    return Redirect(f"/{table_name}")


serve()
