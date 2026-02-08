"""
============================================================================
TEST - SCRIPT DE PRUEBAS
============================================================================
Script para probar todas las funcionalidades del sistema.

Ejecutar desde la raiz del proyecto:
    python test.py
============================================================================
"""

import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_validadores():
    """Prueba los validadores de CUIT, CBU y referencias"""
    print("=" * 70)
    print("TEST 1: VALIDADORES")
    print("=" * 70)
    
    try:
        from utils.validators import validar_cuit, validar_cbu, validar_referencia
        
        # Test CUIT
        print("\n1. Validando CUIT:")
        cuits_test = [
            "20-12345678-9",
            "27-98765432-1",
            "20-00000000-0",  # Invalido
        ]
        
        for cuit in cuits_test:
            valido, msg = validar_cuit(cuit)
            simbolo = "✓" if valido else "✗"
            print(f"   {simbolo} {cuit}: {msg}")
        
        # Test CBU
        print("\n2. Validando CBU:")
        cbus_test = [
            "0170099520000003912345",
            "123456789",  # Muy corto
        ]
        
        for cbu in cbus_test:
            valido, msg = validar_cbu(cbu)
            simbolo = "✓" if valido else "✗"
            print(f"   {simbolo} {cbu}: {msg}")
        
        # Test Referencia
        print("\n3. Validando Referencias:")
        refs_test = [
            "LABSEM0000118",
            "TEST0001234",
            "CORTO",  # Muy corta
        ]
        
        for ref in refs_test:
            valido, msg = validar_referencia(ref)
            simbolo = "✓" if valido else "✗"
            print(f"   {simbolo} {ref}: {msg}")
        
        print("\n✓ Test de validadores completado")
        return True
        
    except Exception as e:
        print(f"\n✗ Error en test de validadores: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_base_datos():
    """Prueba la conexion a la base de datos"""
    print("\n" + "=" * 70)
    print("TEST 2: BASE DE DATOS")
    print("=" * 70)
    
    try:
        from config.database import DatabaseConfig
        
        # Verificar que se puede conectar
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        
        # Listar tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tablas = cursor.fetchall()
        
        print("\nTablas en la base de datos:")
        for tabla in tablas:
            print(f"   ✓ {tabla[0]}")
        
        conn.close()
        
        print("\n✓ Test de base de datos completado")
        return True
        
    except Exception as e:
        print(f"\n✗ Error en test de base de datos: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_modelo_referencia():
    """Prueba el modelo Referencia"""
    print("\n" + "=" * 70)
    print("TEST 3: MODELO REFERENCIA")
    print("=" * 70)
    
    try:
        from models.referencia import Referencia
        
        # 1. Crear referencia
        print("\n1. Creando referencia de prueba...")
        codigo_test = "TEST0000001"
        
        # Verificar si ya existe
        if Referencia.existe(codigo_test):
            print(f"   ℹ La referencia {codigo_test} ya existe, saltando creacion")
            ref = Referencia.obtener_por_codigo(codigo_test)
        else:
            ref = Referencia.crear(codigo_test, "Referencia de prueba")
            print(f"   ✓ Creada: {ref}")
        
        # 2. Obtener todas
        print("\n2. Obteniendo todas las referencias...")
        todas = Referencia.obtener_todas()
        print(f"   ✓ Total: {len(todas)} referencias")
        for r in todas[:3]:  # Mostrar solo las primeras 3
            print(f"      - {r}")
        
        # 3. Generar siguiente codigo
        print("\n3. Generando siguiente codigo...")
        siguiente = Referencia.generar_siguiente_codigo("TEST")
        print(f"   ✓ Siguiente codigo: {siguiente}")
        
        # 4. Buscar
        print("\n4. Buscando referencias con 'TEST'...")
        from models.referencia import buscar_referencias
        resultados = buscar_referencias("TEST")
        print(f"   ✓ Encontradas: {len(resultados)}")
        
        print("\n✓ Test de modelo Referencia completado")
        return True
        
    except Exception as e:
        print(f"\n✗ Error en test de modelo: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_interfaz():
    """Prueba que la interfaz grafica se pueda crear"""
    print("\n" + "=" * 70)
    print("TEST 4: INTERFAZ GRAFICA")
    print("=" * 70)
    
    try:
        import customtkinter as ctk
        
        print("\n✓ CustomTkinter importado correctamente")
        print("   (No se abrira ventana, solo verificacion de import)")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Error en test de interfaz: {e}")
        return False


def main():
    """Ejecuta todos los tests"""
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "SISTEMA DE TESTS - PAGOS BANCARIOS" + " " * 19 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    resultados = []
    
    # Ejecutar tests
    resultados.append(("Validadores", test_validadores()))
    resultados.append(("Base de Datos", test_base_datos()))
    resultados.append(("Modelo Referencia", test_modelo_referencia()))
    resultados.append(("Interfaz Grafica", test_interfaz()))
    
    # Resumen
    print("\n" + "=" * 70)
    print("RESUMEN DE TESTS")
    print("=" * 70)
    
    for nombre, resultado in resultados:
        simbolo = "✓" if resultado else "✗"
        estado = "PASS" if resultado else "FAIL"
        print(f"   {simbolo} {nombre}: {estado}")
    
    # Resultado final
    todos_ok = all(r for _, r in resultados)
    
    print("\n" + "=" * 70)
    if todos_ok:
        print("✓ TODOS LOS TESTS PASARON")
    else:
        print("✗ ALGUNOS TESTS FALLARON")
    print("=" * 70)
    print()
    
    input("Presiona Enter para salir...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Tests interrumpidos")
    except Exception as e:
        print(f"\n✗ Error fatal: {e}")
        import traceback
        traceback.print_exc()
        input("\nPresiona Enter para salir...")
