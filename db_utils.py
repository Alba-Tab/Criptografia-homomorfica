import sqlite3

def init_db():
    conn = sqlite3.connect("operaciones.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS operaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            operacion TEXT,
            v1 TEXT,
            v2 TEXT,
            escalar REAL,
            resultado TEXT,
            v1_cifrado TEXT,
            v2_cifrado TEXT,
            resultado_cifrado TEXT,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def guardar_operacion(operacion, v1, v2, escalar, resultado, v1_cifrado, v2_cifrado, resultado_cifrado):
    conn = sqlite3.connect("operaciones.db")
    c = conn.cursor()
    c.execute("""
        INSERT INTO operaciones (operacion, v1, v2, escalar, resultado, v1_cifrado, v2_cifrado, resultado_cifrado)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (operacion, v1, v2, escalar, resultado, v1_cifrado, v2_cifrado, resultado_cifrado))
    conn.commit()
    conn.close()

def obtener_historial():
    conn = sqlite3.connect("operaciones.db")
    c = conn.cursor()
    c.execute("SELECT operacion, v1, v2, escalar, resultado, fecha FROM operaciones ORDER BY fecha DESC")
    rows = c.fetchall()
    conn.close()
    return rows

def obtener_historial_cifrado():
    conn = sqlite3.connect("operaciones.db")
    c = conn.cursor()
    c.execute("SELECT operacion, v1_cifrado, v2_cifrado, escalar, resultado_cifrado, fecha FROM operaciones ORDER BY fecha DESC")
    rows = c.fetchall()
    conn.close()
    return rows