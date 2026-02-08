"""
============================================================================
CONFIG - CONFIGURACIÓN DE LA BASE DE DATOS
============================================================================
Este módulo maneja la conexión a la base de datos SQLite y su inicialización.

CONCEPTOS CLAVE:
- SQLite: Base de datos que se guarda en un archivo (no necesita servidor)
- Context Manager: El 'with' asegura que la conexión se cierre correctamente
- Singleton: Solo una instancia de la DB para toda la aplicación
============================================================================
"""

import sqlite3
import os
from pathlib import Path


class DatabaseConfig:
    """
    Clase para configurar y gestionar la conexión a la base de datos.
    
    ¿Por qué una clase? Porque queremos tener un solo punto de control
    para todas las operaciones de base de datos.
    """
    
    # Ruta donde se guardará la base de datos
    # Path.home() obtiene la carpeta del usuario (ej: /home/usuario)
    DB_DIR = Path.home() / '.sistema_pagos'  # Carpeta oculta en el home
    DB_PATH = DB_DIR / 'pagos.db'            # Archivo de base de datos
    
    # Ruta al archivo con el esquema SQL
    SCHEMA_PATH = Path(__file__).parent.parent / 'database' / 'schema.sql'
    
    @classmethod
    def inicializar_db(cls):
        """
        Inicializa la base de datos creando las tablas si no existen.
        
        ¿Qué hace este método?
        1. Crea la carpeta para la DB si no existe
        2. Lee el archivo schema.sql
        3. Ejecuta todas las sentencias SQL para crear las tablas
        
        Se llama automáticamente la primera vez que se usa la app.
        """
        # Crear directorio si no existe
        cls.DB_DIR.mkdir(parents=True, exist_ok=True)
        
        # Verificar si es la primera vez (DB no existe)
        primera_vez = not cls.DB_PATH.exists()
        
        # Conectar a la base de datos (se crea si no existe)
        conn = sqlite3.connect(cls.DB_PATH)
        cursor = conn.cursor()
        
        try:
            # Leer el archivo schema.sql
            with open(cls.SCHEMA_PATH, 'r', encoding='utf-8') as f:
                schema_sql = f.read()
            
            # Ejecutar todo el SQL del schema
            cursor.executescript(schema_sql)
            conn.commit()
            
            if primera_vez:
                print("✅ Base de datos creada exitosamente")
            else:
                print("✅ Base de datos inicializada")
                
        except Exception as e:
            print(f"❌ Error al inicializar la base de datos: {e}")
            conn.rollback()
            raise
        finally:
            conn.close()
    
    @classmethod
    def get_connection(cls):
        """
        Obtiene una conexión a la base de datos.
        
        Retorna:
            sqlite3.Connection: Objeto de conexión a la base de datos
            
        Ejemplo de uso:
            conn = DatabaseConfig.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM referencias")
            conn.close()
        """
        # Asegurarse de que la DB existe
        if not cls.DB_PATH.exists():
            cls.inicializar_db()
        
        # Crear conexión
        conn = sqlite3.connect(cls.DB_PATH)
        
        # Configurar para que devuelva filas como diccionarios
        # Esto es MUY útil porque podemos hacer row['nombre'] en vez de row[0]
        conn.row_factory = sqlite3.Row
        
        return conn
    
    @classmethod
    def ejecutar_query(cls, query, params=None, fetch_one=False, fetch_all=False):
        """
        Ejecuta una query SQL y maneja automáticamente la conexión.
        
        Este es un método de conveniencia que abre la conexión,
        ejecuta la query y la cierra automáticamente.
        
        Args:
            query (str): La consulta SQL a ejecutar
            params (tuple): Parámetros para la query (evita SQL injection)
            fetch_one (bool): Si True, retorna solo un resultado
            fetch_all (bool): Si True, retorna todos los resultados
            
        Returns:
            Si fetch_one=True: Una fila o None
            Si fetch_all=True: Lista de filas
            Si ninguno: cursor.lastrowid (útil para INSERT)
            
        Ejemplo:
            # INSERT
            id_nuevo = DatabaseConfig.ejecutar_query(
                "INSERT INTO referencias (codigo) VALUES (?)",
                params=("LABSEM0001",)
            )
            
            # SELECT ONE
            ref = DatabaseConfig.ejecutar_query(
                "SELECT * FROM referencias WHERE id = ?",
                params=(5,),
                fetch_one=True
            )
            
            # SELECT ALL
            todas = DatabaseConfig.ejecutar_query(
                "SELECT * FROM referencias",
                fetch_all=True
            )
        """
        conn = cls.get_connection()
        cursor = conn.cursor()
        
        try:
            # Ejecutar la query
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            # Commit si es INSERT, UPDATE o DELETE
            if query.strip().upper().startswith(('INSERT', 'UPDATE', 'DELETE')):
                conn.commit()
            
            # Retornar según lo solicitado
            if fetch_one:
                return cursor.fetchone()
            elif fetch_all:
                return cursor.fetchall()
            else:
                # Para INSERT, retornar el ID del nuevo registro
                return cursor.lastrowid
                
        except Exception as e:
            conn.rollback()
            print(f"❌ Error en query: {e}")
            print(f"Query: {query}")
            print(f"Params: {params}")
            raise
        finally:
            conn.close()


# ============================================================================
# FUNCIONES DE UTILIDAD
# ============================================================================

def resetear_base_datos():
    """
    Elimina la base de datos existente y la crea de nuevo.
    ⚠️ CUIDADO: Esto borra TODOS los datos.
    
    Útil para desarrollo y testing.
    """
    if DatabaseConfig.DB_PATH.exists():
        DatabaseConfig.DB_PATH.unlink()  # Eliminar archivo
        print("🗑️  Base de datos eliminada")
    
    DatabaseConfig.inicializar_db()
    print("✅ Base de datos recreada")


def verificar_integridad_db():
    """
    Verifica que la base de datos esté en buen estado.
    
    Retorna:
        bool: True si todo está OK, False si hay problemas
    """
    try:
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        
        # SQLite tiene un comando para verificar integridad
        cursor.execute("PRAGMA integrity_check")
        resultado = cursor.fetchone()
        
        conn.close()
        
        if resultado[0] == 'ok':
            print("✅ Integridad de la base de datos: OK")
            return True
        else:
            print(f"❌ Problemas de integridad: {resultado[0]}")
            return False
            
    except Exception as e:
        print(f"❌ Error al verificar integridad: {e}")
        return False


# ============================================================================
# CÓDIGO QUE SE EJECUTA AL IMPORTAR ESTE MÓDULO
# ============================================================================
# Cuando importemos este archivo, automáticamente inicializará la DB
DatabaseConfig.inicializar_db()