import sqlite3
import os

# Función para conectar a la base de datos
def conectar_db():
    # Asegurar que el directorio existe
    if not os.path.exists("database"):
        os.makedirs("database")
    
    # Conexión a la base de datos (clientes de gimnasio)
    conn = sqlite3.connect("database/clientes.db")
    conn.row_factory = sqlite3.Row  # Configurar filas como diccionarios
    return conn

# Función para crear tablas y triggers
def crear_tablas():
    conn = conectar_db()
    cursor = conn.cursor()

    # Crear tabla Clientes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Clientes (
            ClienteID INTEGER PRIMARY KEY AUTOINCREMENT,
            Nombre TEXT,
            Apellido TEXT,
            Telefono TEXT,
            Telefono_Opcional TEXT,
            Correo TEXT,
            DNI TEXT,
            fecha_nacimiento TEXT,
            sexo TEXT NOT NULL CHECK (sexo IN ('Masculino', 'Femenino', 'Otro')),
            Tipo TEXT DEFAULT 'Cliente',
            FechaCreacion TEXT DEFAULT (DATE('now')),
            estado TEXT DEFAULT 'Activo',
            day_inactivo INTEGER DEFAULT 0
        )
    ''')

    # Crear tabla Productos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Productos (
            ProductoID INTEGER PRIMARY KEY AUTOINCREMENT,
            Nombre TEXT,
            Tipo TEXT DEFAULT 'Producto',
            stock INTEGER
        )
    ''')

    # Crear tabla Pagos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Pagos (
            PagoID INTEGER PRIMARY KEY AUTOINCREMENT,
            ClienteID INTEGER,
            FechaPago TEXT NOT NULL,
            FechaVencimiento TEXT,
            Monto INTEGER,
            FOREIGN KEY (ClienteID) REFERENCES Clientes(ClienteID)
        )
    ''')

    # Crear tabla productos_pagos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos_pagos (
            Pago_productoID INTEGER PRIMARY KEY AUTOINCREMENT,
            ProductoID INTEGER,
            FechaPago TEXT NOT NULL,
            Monto INTEGER,
            FOREIGN KEY (ProductoID) REFERENCES Productos(ProductoID)
        )
    ''')

    # Crear trigger Trg_ActualizarEstado
    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS Trg_ActualizarEstado
        AFTER INSERT ON Pagos
        BEGIN
            -- Si el cliente no tiene pagos no vencidos, actualizar su estado a 'Inactivo'
            UPDATE Clientes
            SET estado = 'Inactivo',
                day_inactivo = (
                    SELECT MAX(
                        julianday('now') - julianday(COALESCE(FechaVencimiento, DATE(FechaPago, '+1 month')))
                    )
                    FROM Pagos
                    WHERE ClienteID = NEW.ClienteID
                )
            WHERE ClienteID = NEW.ClienteID
              AND NOT EXISTS (
                  SELECT 1
                  FROM Pagos
                  WHERE ClienteID = NEW.ClienteID
                    AND COALESCE(FechaVencimiento, DATE(FechaPago, '+1 month')) >= DATE('now')
              );

            -- Si el cliente tiene pagos no vencidos, actualizar su estado a 'Activo'
            UPDATE Clientes
            SET estado = 'Activo',
                day_inactivo = 0
            WHERE ClienteID = NEW.ClienteID
              AND EXISTS (
                  SELECT 1
                  FROM Pagos
                  WHERE ClienteID = NEW.ClienteID
                    AND COALESCE(FechaVencimiento, DATE(FechaPago, '+1 month')) >= DATE('now')
              );
        END;
    ''')

    # Crear trigger Trg_AutomaticFechaVencimiento
    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS Trg_AutomaticFechaVencimiento
        AFTER INSERT ON Pagos
        BEGIN
            UPDATE Pagos
            SET FechaVencimiento = DATE(FechaPago, '+1 month')
            WHERE PagoID = NEW.PagoID;
        END;
    ''')

    conn.commit()
    conn.close()