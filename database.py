import sqlite3

def conectar():
    conn = sqlite3.connect("conversaciones.db")
    conn.row_factory = sqlite3.Row
    return conn

def crear_tabla():
    conn = conectar()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS mensajes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def guardar_mensaje(role, content):
    conn = conectar()
    conn.execute("INSERT INTO mensajes (role, content) VALUES (?, ?)",
                 (role, content))
    conn.commit()
    conn.close()

def cargar_historial():
    conn = conectar()
    mensajes = conn.execute(
        "SELECT role, content FROM mensajes ORDER BY id"
    ).fetchall()
    conn.close()
    return [{"role": m["role"], "content": m["content"]} for m in mensajes]