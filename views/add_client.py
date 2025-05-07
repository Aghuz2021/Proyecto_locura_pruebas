import flet as ft
import json
import sqlite3
from views.Menu import vista_menu
from database.db import conectar_db
from datetime import datetime

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

    menu = vista_menu(page)

    txt_name = ft.TextField(
        label="Nombre",
        text_style=ft.TextStyle(color=configuracion["color_letras"]),
        border_color=configuracion["color_letras"],
        bgcolor=configuracion["color_tematica"],
        hint_style=ft.TextStyle(color=configuracion["color_letras"]),
        label_style=ft.TextStyle(color=configuracion["color_letras"]),
        width=600
    )
    txt_surname = ft.TextField(
        label="Apellido",
        text_style=ft.TextStyle(color=configuracion["color_letras"]),
        border_color=configuracion["color_letras"],
        bgcolor=configuracion["color_tematica"],
        hint_style=ft.TextStyle(color=configuracion["color_letras"]),
        label_style=ft.TextStyle(color=configuracion["color_letras"]),
        width=600
    )
    txt_dni = ft.TextField(
        label="DNI",
        text_style=ft.TextStyle(color=configuracion["color_letras"]),
        border_color=configuracion["color_letras"],
        bgcolor=configuracion["color_tematica"],
        hint_style=ft.TextStyle(color=configuracion["color_letras"]),
        label_style=ft.TextStyle(color=configuracion["color_letras"]),
        width=600
    )
    txt_phone = ft.TextField(
        label="Teléfono",
        text_style=ft.TextStyle(color=configuracion["color_letras"]),
        border_color=configuracion["color_letras"],
        bgcolor=configuracion["color_tematica"],
        hint_style=ft.TextStyle(color=configuracion["color_letras"]),
        label_style=ft.TextStyle(color=configuracion["color_letras"]),
        width=600
    )
    txt_phone_opcional = ft.TextField(
        label="Teléfono opcional",
        text_style=ft.TextStyle(color=configuracion["color_letras"]),
        border_color=configuracion["color_letras"],
        bgcolor=configuracion["color_tematica"],
        hint_style=ft.TextStyle(color=configuracion["color_letras"]),
        label_style=ft.TextStyle(color=configuracion["color_letras"]),
        width=600
    )
    txt_email = ft.TextField(
        label="Correo Electrónico",
        text_style=ft.TextStyle(color=configuracion["color_letras"]),
        border_color=configuracion["color_letras"],
        bgcolor=configuracion["color_tematica"],
        hint_style=ft.TextStyle(color=configuracion["color_letras"]),
        label_style=ft.TextStyle(color=configuracion["color_letras"]),
        width=600
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
        bgcolor=configuracion["color_tematica"],
        width=600
    )


    dropdown_tipo_pago = ft.Dropdown(
        label="Tipo de Pago",
        options=[
            ft.dropdown.Option(key="Efectivo", text="Efectivo"),
            ft.dropdown.Option(key="Debito", text="Debito"),
            ft.dropdown.Option(key="Transferencia", text="Transferencia"),
        ],
        value="Efectivo",
        text_style=ft.TextStyle(color=configuracion["color_letras"]),
        border_color=configuracion["color_letras"],
        hint_style=ft.TextStyle(color=configuracion["color_letras"]),
        label_style=ft.TextStyle(color=configuracion["color_letras"]),
        bgcolor=configuracion["color_tematica"],
        width=600
    )

    # Obtén la fecha actual en formato AAAA-MM-DD
    fecha_actual = datetime.now().strftime("%Y-%m-%d")

    txt_fecha_abono = ft.TextField(
        label="Fecha de Abono",
        hint_text="YYYY-MM-DD",
        value=fecha_actual,  # Establece la fecha actual como valor inicial
        text_style=ft.TextStyle(color=configuracion["color_letras"]),
        border_color=configuracion["color_letras"],
        bgcolor=configuracion["color_tematica"],
        width=600
    )
    txt_monto_abono = ft.TextField(
        label="Monto",
        keyboard_type=ft.KeyboardType.NUMBER,
        text_style=ft.TextStyle(color=configuracion["color_letras"]),
        border_color=configuracion["color_letras"],
        bgcolor=configuracion["color_tematica"],
        width=600
    )
    dropdown_meses_pagados = ft.Dropdown(
        label="Meses Pagados",
        options=[ft.dropdown.Option(key=str(i), text=str(i)) for i in range(1, 13)],
        value="1",
        text_style=ft.TextStyle(color=configuracion["color_letras"]),
        border_color=configuracion["color_letras"],
        bgcolor=configuracion["color_tematica"],
        width=600
    )
    tipo_membresia_field = ft.TextField(
        label="Tipo de Membresía",
        value="Pago inicial",
        disabled=True,
        text_style=ft.TextStyle(color=configuracion["color_letras"]),
        border_color=configuracion["color_letras"],
        hint_style=ft.TextStyle(color=configuracion["color_letras"]),
        label_style=ft.TextStyle(color=configuracion["color_letras"]),
        bgcolor=configuracion["color_tematica"],
        width=600
    )

    def on_field_change(e):
        control = e.control
        if isinstance(control, ft.TextField):
            if control.value.strip():
                control.border_color = "green"
            else:
                control.border_color = configuracion["color_letras"]
        elif isinstance(control, ft.Dropdown):
            if control.value:
                control.border_color = "green"
            else:
                control.border_color = configuracion["color_letras"]
        control.update()

    txt_name.on_change = on_field_change
    txt_surname.on_change = on_field_change
    txt_dni.on_change = on_field_change
    txt_phone.on_change = on_field_change
    txt_phone_opcional.on_change = on_field_change
    txt_email.on_change = on_field_change
    txt_fecha_abono.on_change = on_field_change
    txt_monto_abono.on_change = on_field_change
    dropdown_gender.on_change = on_field_change
    dropdown_tipo_pago.on_change = on_field_change
    dropdown_meses_pagados.on_change = on_field_change

    async def submit_client_and_abono(e):
        # (Tu lógica de guardado aquí - sin cambios importantes)
        campos_cliente = [txt_name, txt_surname, txt_dni, txt_phone, dropdown_gender]
        campos_abono = [dropdown_tipo_pago, txt_fecha_abono, txt_monto_abono, dropdown_meses_pagados]
        campos_obligatorios = campos_cliente + campos_abono

        estan_completos = all(
            (field.value.strip() if isinstance(field, ft.TextField) else field.value) for field in campos_obligatorios
        )

        if not estan_completos:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Por favor, complete todos los campos obligatorios."),
                bgcolor="red"
            )
            page.snack_bar.open = True
            page.update()
            return

        conn = None
        try:
            # Registrar cliente
            client_data = {
                "Nombre": txt_name.value.strip(),
                "Apellido": txt_surname.value.strip(),
                "Telefono": txt_phone.value.strip(),
                "Telefono_opcional": txt_phone_opcional.value.strip(),
                "Correo": txt_email.value.strip(),
                "DNI": txt_dni.value.strip(),
                "sexo": dropdown_gender.value.strip(),
            }
            conn = conectar_db()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Clientes (Nombre, Apellido, Telefono, Telefono_opcional, Correo, Dni, sexo)
                VALUES (:Nombre, :Apellido, :Telefono, :Telefono_opcional, :Correo, :DNI, :sexo)
            ''', client_data)
            conn.commit()
            cliente_id = cursor.lastrowid  # Asigna el ID del cliente después de la inserción
               # Confirmación por consola
            print("Cliente registrado con éxito:")
            print(f"ID: {cliente_id}")
            print("Datos:", client_data)
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Cliente registrados exitosamente."),
                bgcolor="green"
            )
            page.snack_bar.open = True
            page.update()
            # Registrar abono
            abono_data = {
                "ClienteID": cliente_id,
                "Metodo": dropdown_tipo_pago.value.strip(),
                "FechaPago": txt_fecha_abono.value.strip(),
                "Monto": txt_monto_abono.value.strip(),
                "MesesPagados": dropdown_meses_pagados.value.strip(),
                "Tipo_membresia": tipo_membresia_field.value.strip(),
            }
            cursor.execute('''
                INSERT INTO Pagos (ClienteID, Metodo, FechaPago, Monto, MesesPagados, Tipo_membresia)
                VALUES (:ClienteID, :Metodo, :FechaPago, :Monto, :MesesPagados, :Tipo_membresia)
            ''', abono_data)
            conn.commit()
        except sqlite3.Error as err:
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Error al registrar cliente o abono: {err}"),
                bgcolor="red"
            )
            page.snack_bar.open = True
        finally:
            if conn:
                conn.close()

        for field in [txt_name, txt_surname, txt_phone, txt_phone_opcional, txt_email, txt_dni, txt_fecha_abono, txt_monto_abono]:
            field.value = ""
            field.border_color = configuracion["color_letras"] # Resetear el color del borde
        dropdown_gender.value = "Masculino"
        dropdown_gender.border_color = configuracion["color_letras"]
        dropdown_tipo_pago.value = "Efectivo"
        dropdown_tipo_pago.border_color = configuracion["color_letras"]
        dropdown_meses_pagados.value = "1"
        dropdown_meses_pagados.border_color = configuracion["color_letras"]
        page.update()

    # Botón para registrar cliente y abono
    btn_submit_all = ft.ElevatedButton(
        text="Registrar Cliente y Abono",
        on_click=submit_client_and_abono,  # Llama directamente a la función
        style=ft.ButtonStyle(bgcolor=configuracion["color_tematica"], color=configuracion["color_letras"]),
    )

    # Actualizar el formulario
    form_cliente = ft.Column(
        controls=[
            ft.Text("Agregar Cliente", size=32, weight="bold", color=configuracion["color_letras"]),
            txt_name, txt_surname, txt_phone, txt_phone_opcional, txt_email, txt_dni, dropdown_gender,
            ft.Text("Registrar Abono", size=32, weight="bold", color=configuracion["color_letras"]),
            dropdown_tipo_pago, txt_fecha_abono, txt_monto_abono, dropdown_meses_pagados, tipo_membresia_field,
            btn_submit_all,  # Botón combinado
        ],
        spacing=10,
    )

    page.add(
        ft.Column(
            controls=[
                menu,
                ft.ListView(
                    expand=True,
                    controls=[
                        form_cliente,
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