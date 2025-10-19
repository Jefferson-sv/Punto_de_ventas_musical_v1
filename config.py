# config.py
# Ajusta estos valores a tu entorno de SQL Server

import pyodbc

DB_CONFIG = {
    "driver": "ODBC Driver 17 for SQL Server",  # Asegúrate de tenerlo instalado
    "server": r"3NRIQFLORES\SQLSERVER20022",    # Ej: "localhost" o "MI-PC\\SQLEXPRESS"
    "database": "minimarket",
    "username": "Market_User",                  # Tu usuario SQL
    "password": "User1234",                     # Tu contraseña
    "encrypt": "yes",                           # "yes" o "no"
    "trust_server_certificate": "yes"           # "yes" para entornos locales
}

# Devuelve una conexión a SQL Server usando pyodbc
def get_connection():
    try:
        conn_str = (
            f"DRIVER={{{DB_CONFIG['driver']}}};"
            f"SERVER={DB_CONFIG['server']};"
            f"DATABASE={DB_CONFIG['database']};"
            f"UID={DB_CONFIG['username']};"
            f"PWD={DB_CONFIG['password']};"
            f"Encrypt={DB_CONFIG['encrypt']};"
            f"TrustServerCertificate={DB_CONFIG['trust_server_certificate']};"
        )
        conn = pyodbc.connect(conn_str)
        return conn
    except pyodbc.Error as e:
        raise Exception(f"No se pudo conectar a SQL Server: {e}")