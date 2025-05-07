import sqlite3
import os

# Función para conectar a la base de datos
def conectar_db():
    if not os.path.exists("database"):
        os.makedirs("database")
    conn = sqlite3.connect("database/clientes22.db")
    conn.row_factory = sqlite3.Row
    return conn

# Función para crear tablas y triggers
def crear_tablas():
    conn = conectar_db()
    cursor = conn.cursor()

    # Tabla Clientes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Clientes (
            ClienteID INTEGER PRIMARY KEY AUTOINCREMENT,
            Nombre TEXT NOT NULL,
            Apellido TEXT NOT NULL,
            Telefono TEXT NOT NULL,
            Telefono_opcional TEXT,
            correo TEXT,
            Dni TEXT NOT NULL,
            fecha_nacimiento DATE,
            sexo TEXT NOT NULL CHECK (sexo IN ('Masculino', 'Femenino', 'Otro')),
            Estado TEXT DEFAULT 'Activo',
            fecha_creacion TEXT DEFAULT (DATE('now')),
            Tipo TEXT DEFAULT 'Cliente',
            Day_inactivo INTEGER DEFAULT 0
        )
    ''')

    # Tabla Pagos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Pagos (
            PagoID INTEGER PRIMARY KEY AUTOINCREMENT,
            ClienteID INTEGER,
            Metodo TEXT CHECK (Metodo IN ('Efectivo', 'Transferencia', 'Debito')),
            FechaPago DATE NOT NULL,
            FechaVencimiento DATE,
            Monto INTEGER,
            MesesPagados INTEGER,
            Tipo_membresia TEXT CHECK (Tipo_membresia IN ('Pago inicial', 'Renovación')),
            FOREIGN KEY (ClienteID) REFERENCES Clientes (ClienteID)
        )
    ''')

    # Trigger para calcular FechaVencimiento según MesesPagados
    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS calcular_fecha_vencimiento
        AFTER INSERT ON Pagos
        FOR EACH ROW
        BEGIN
            UPDATE Pagos
            SET FechaVencimiento = 
                CASE
                    WHEN NEW.MesesPagados BETWEEN 1 AND 12
                    THEN date(NEW.FechaPago, '+' || NEW.MesesPagados || ' months')
                    ELSE NEW.FechaPago
                END
            WHERE PagoID = NEW.PagoID;
        END;
    ''')

    # Trigger para actualizar estado y días inactivos después de insertar un pago
    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS trg_actualizar_estado_despues_insert
        AFTER INSERT ON Pagos
        FOR EACH ROW
        BEGIN
            UPDATE Clientes
            SET 
                Estado = CASE 
                            WHEN (
                                SELECT MAX(FechaVencimiento)
                                FROM Pagos
                                WHERE ClienteID = NEW.ClienteID
                            ) < DATE('now') THEN 'Inactivo'
                            ELSE 'Activo'
                        END,
                Day_inactivo = CASE 
                                WHEN (
                                    SELECT MAX(FechaVencimiento)
                                    FROM Pagos
                                    WHERE ClienteID = NEW.ClienteID
                                ) < DATE('now') THEN
                                    CAST(
                                        JULIANDAY('now') - JULIANDAY((
                                            SELECT MAX(FechaVencimiento)
                                            FROM Pagos
                                            WHERE ClienteID = NEW.ClienteID
                                        )) AS INTEGER
                                    )
                                ELSE 0
                              END
            WHERE ClienteID = NEW.ClienteID;
        END;
    ''')

    # Trigger para actualizar estado y días inactivos después de actualizar un pago
    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS trg_actualizar_estado_despues_update
        AFTER UPDATE ON Pagos
        FOR EACH ROW
        BEGIN
            UPDATE Clientes
            SET 
                Estado = CASE 
                            WHEN (
                                SELECT MAX(FechaVencimiento)
                                FROM Pagos
                                WHERE ClienteID = NEW.ClienteID
                            ) < DATE('now') THEN 'Inactivo'
                            ELSE 'Activo'
                        END,
                Day_inactivo = CASE 
                                WHEN (
                                    SELECT MAX(FechaVencimiento)
                                    FROM Pagos
                                    WHERE ClienteID = NEW.ClienteID
                                ) < DATE('now') THEN
                                    CAST(
                                        JULIANDAY('now') - JULIANDAY((
                                            SELECT MAX(FechaVencimiento)
                                            FROM Pagos
                                            WHERE ClienteID = NEW.ClienteID
                                        )) AS INTEGER
                                    )
                                ELSE 0
                              END
            WHERE ClienteID = NEW.ClienteID;
        END;
    ''')

    conn.commit()
    conn.close()
