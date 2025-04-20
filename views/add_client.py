import flet as ft
import json
import sqlite3
from views.Menu import vista_menu
from views.custom_date_picker import open_custom_date_picker_modal
from database.db import conectar_db

CONFIG_FILE = "config.json"

def cargar_configuracion():
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "color_fondo": "#FFFFFF",
            "color_tematica": "#E8E8E8",
            "color_letras": "#000000",
            "nombre_gimnasio": "Mi Gimnasio"
        }

def vista_add_client(page: ft.Page):
    configuracion = cargar_configuracion()

    page.title = "Agregar Cliente"
    page.window_maximized = True
    page.bgcolor = configuracion["color_fondo"]

    # Se incluye el menú desde el módulo correspondiente.
    menu = vista_menu(page)

    # Campos para datos del cliente
    txt_name = ft.TextField(
        label="Nombre", 
        text_style=ft.TextStyle(color=configuracion["color_letras"]),
        border_color=configuracion["color_letras"], 
        bgcolor=configuracion["color_tematica"],
        hint_style=ft.TextStyle(color=configuracion["color_letras"]),
        label_style=ft.TextStyle(color=configuracion["color_letras"])
    )
    txt_surname = ft.TextField(
        label="Apellido", 
        text_style=ft.TextStyle(color=configuracion["color_letras"]),
        border_color=configuracion["color_letras"], 
        bgcolor=configuracion["color_tematica"],
        hint_style=ft.TextStyle(color=configuracion["color_letras"]),
        label_style=ft.TextStyle(color=configuracion["color_letras"])
    )
    txt_dni = ft.TextField(
        label="DNI", 
        keyboard_type=ft.KeyboardType.NUMBER,
        text_style=ft.TextStyle(color=configuracion["color_letras"]),
        border_color=configuracion["color_letras"], 
        bgcolor=configuracion["color_tematica"],
        hint_style=ft.TextStyle(color=configuracion["color_letras"]),
        label_style=ft.TextStyle(color=configuracion["color_letras"])
    )
    txt_phone = ft.TextField(
        label="Teléfono", 
        keyboard_type=ft.KeyboardType.NUMBER,
        text_style=ft.TextStyle(color=configuracion["color_letras"]),
        border_color=configuracion["color_letras"],
        bgcolor=configuracion["color_tematica"],
        hint_style=ft.TextStyle(color=configuracion["color_letras"]),
        label_style=ft.TextStyle(color=configuracion["color_letras"])
    )
    txt_email = ft.TextField(
        label="Correo Electrónico", 
        keyboard_type=ft.KeyboardType.EMAIL,
        text_style=ft.TextStyle(color=configuracion["color_letras"]),
        border_color=configuracion["color_letras"],
        bgcolor=configuracion["color_tematica"],
        hint_style=ft.TextStyle(color=configuracion["color_letras"]),
        label_style=ft.TextStyle(color=configuracion["color_letras"])
    )
    dropdown_gender = ft.Dropdown(
        label="Sexo",
        options=[
            ft.dropdown.Option(key="Masculino", text="Masculino"),
            ft.dropdown.Option(key="Femenino", text="Femenino"),
            ft.dropdown.Option(key="Otro", text="Otro"),
        ],
        value="Masculino",
        text_style=ft.TextStyle(color=configuracion["color_letras"]),
        border_color=configuracion["color_letras"],
        hint_style=ft.TextStyle(color=configuracion["color_letras"]),
        label_style=ft.TextStyle(color=configuracion["color_letras"]),
    )

    # Campos para registrar el abono
    txt_fecha_abono = ft.TextField(
        label="Fecha de Abono", 
        hint_text="YYYY-MM-DD",
        text_style=ft.TextStyle(color=configuracion["color_letras"]),
        border_color=configuracion["color_letras"],
        bgcolor=configuracion["color_tematica"]
    )
    txt_monto_abono = ft.TextField(
        label="Monto", 
        keyboard_type=ft.KeyboardType.NUMBER,
        text_style=ft.TextStyle(color=configuracion["color_letras"]),
        border_color=configuracion["color_letras"],
        bgcolor=configuracion["color_tematica"]
    )
    btn_guardar_abono = ft.ElevatedButton(
        text="Guardar Abono",
        visible=True,
        on_click=lambda e: guardar_abono(e),
    )

    # Función para guardar el abono del cliente
    def guardar_abono(e):
        if not txt_fecha_abono.value.strip() or not txt_monto_abono.value.strip():
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Por favor, complete todos los campos del abono."),
                bgcolor="red"
            )
            page.snack_bar.open = True
            page.update()
            return

        try:
            abono_data = {
                "ClienteID": cliente_id,  # Utiliza la variable global definida al registrar el cliente
                "FechaPago": txt_fecha_abono.value.strip(),
                "Monto": txt_monto_abono.value.strip(),
            }
            conn = conectar_db()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Pagos (ClienteID, FechaPago, Monto)
                VALUES (:ClienteID, :FechaPago, :Monto)
            ''', abono_data)
            conn.commit()
            print(f"Se cargó el pago para el cliente con ID: {cliente_id}. Datos del abono: {abono_data}")
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Abono registrado exitosamente."),
                bgcolor="green"
            )
            page.snack_bar.open = True
        except sqlite3.Error as err:
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Error al registrar abono: {err}"),
                bgcolor="red"
            )
            page.snack_bar.open = True
        finally:
            if conn:
                conn.close()

        txt_fecha_abono.value = ""
        txt_monto_abono.value = ""
        page.update()

    # Función para registrar al cliente
    def submit_client(e):
        if not txt_name.value.strip() or not txt_surname.value.strip() or not txt_dni.value.strip() or not txt_phone.value.strip() or not dropdown_gender.value:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Por favor, complete todos los campos obligatorios."),
                bgcolor="red"
            )
            page.snack_bar.open = True
            page.update()
            return

        try:
            client_data = {
                "Nombre": txt_name.value.strip(),
                "Apellido": txt_surname.value.strip(),
                "Telefono": txt_phone.value.strip(),
                "Correo": txt_email.value.strip(),
                "DNI": txt_dni.value.strip(),
                "sexo": dropdown_gender.value,
            }
            conn = conectar_db()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Clientes (Nombre, Apellido, Telefono, Correo, DNI, sexo)
                VALUES (:Nombre, :Apellido, :Telefono, :Correo, :DNI, :sexo)
            ''', client_data)
            conn.commit()
            global cliente_id
            cliente_id = cursor.lastrowid
            print(f"Usuario cargado: {client_data}. ID del usuario: {cliente_id}")
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Cliente registrado exitosamente."),
                bgcolor="green"
            )
            page.snack_bar.open = True
        except sqlite3.Error as err:
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Error al registrar cliente: {err}"),
                bgcolor="red"
            )
            page.snack_bar.open = True
        finally:
            if conn:
                conn.close()

        # Limpieza de campos luego de registrar
        for field in [txt_name, txt_surname, txt_phone, txt_email, txt_dni]:
            field.value = ""
        dropdown_gender.value = "Masculino"
        page.update()

    btn_submit = ft.ElevatedButton(
        text="Agregar Cliente",
        on_click=submit_client,
        style=ft.ButtonStyle(bgcolor=configuracion["color_tematica"], color=configuracion["color_letras"]),
    )

    # Columna para el formulario de registro de cliente
    form_cliente = ft.Column(
        controls=[
            ft.Text("Agregar Cliente", size=32, weight="bold", color=configuracion["color_letras"]),
            txt_name, txt_surname, txt_phone, txt_email, txt_dni, dropdown_gender, btn_submit,
        ],
        spacing=10,
    )

    # Columna para el registro de abono
    form_abono = ft.Column(
        controls=[
            ft.Text("Registrar Abono", size=32, weight="bold", color=configuracion["color_letras"]),
            txt_fecha_abono, txt_monto_abono, btn_guardar_abono,
        ],
        spacing=10,
        visible=True,
    )

    # Se agregan todos los controles a la página (ya sin la tabla de clientes)
    page.add(
        ft.Column(
            controls=[
                menu,
                ft.ListView(
                    expand=True,
                    controls=[
                        form_cliente,
                        form_abono,
                    ]
                )
            ],
            spacing=20
        )
    )
    page.update()

def main(page: ft.Page):
    vista_add_client(page)

if __name__ == "__main__":
    ft.app(target=main)
