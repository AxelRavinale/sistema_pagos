"""
============================================================================
VALIDATORS - VALIDADORES DE DATOS
============================================================================
Este módulo contiene funciones para validar diferentes tipos de datos
que usamos en el sistema (CUIT, CBU, referencias, etc.).

¿Por qué validar? Para asegurarnos de que los datos sean correctos ANTES
de guardarlos en la base de datos. Es mejor prevenir que curar.
============================================================================
"""

import re


def validar_cuit(cuit):
    """
    Valida si un CUIT/CUIL es válido según el algoritmo oficial.
    
    El CUIT tiene el formato: XX-XXXXXXXX-X
    - Primeros 2 dígitos: tipo (20, 23, 24, 27, 30, 33, 34)
    - Siguientes 8 dígitos: DNI
    - Último dígito: verificador (se calcula con un algoritmo)
    
    Args:
        cuit (str): El CUIT a validar (puede tener o no guiones)
        
    Returns:
        tuple: (es_valido: bool, mensaje: str)
        
    Ejemplo:
        valido, msg = validar_cuit("20-12345678-9")
        if valido:
            print("CUIT válido")
        else:
            print(f"Error: {msg}")
    """
    # Eliminar guiones y espacios
    cuit_limpio = cuit.replace('-', '').replace(' ', '').strip()
    
    # Verificar que tenga 11 dígitos
    if len(cuit_limpio) != 11:
        return False, "El CUIT debe tener 11 dígitos"
    
    # Verificar que sean todos números
    if not cuit_limpio.isdigit():
        return False, "El CUIT debe contener solo números"
    
    # Verificar que el tipo sea válido
    tipo = cuit_limpio[:2]
    tipos_validos = ['20', '23', '24', '27', '30', '33', '34']
    if tipo not in tipos_validos:
        return False, f"Tipo de CUIT inválido: {tipo}. Debe ser uno de: {', '.join(tipos_validos)}"
    
    # Calcular dígito verificador
    # Este es el algoritmo oficial de la AFIP
    multiplicadores = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]
    suma = 0
    
    for i in range(10):
        suma += int(cuit_limpio[i]) * multiplicadores[i]
    
    resto = suma % 11
    digito_verificador = 11 - resto
    
    # Casos especiales del algoritmo
    if digito_verificador == 11:
        digito_verificador = 0
    elif digito_verificador == 10:
        digito_verificador = 9
    
    # Comparar con el dígito verificador ingresado
    if int(cuit_limpio[10]) != digito_verificador:
        return False, f"Dígito verificador inválido. Debería ser {digito_verificador}"
    
    return True, "CUIT válido"


def validar_cbu(cbu):
    """
    Valida si un CBU es válido según el algoritmo bancario.
    
    El CBU tiene 22 dígitos divididos en dos bloques:
    - Bloque 1 (8 dígitos): Banco (3) + Sucursal (4) + Verificador (1)
    - Bloque 2 (14 dígitos): Cuenta (13) + Verificador (1)
    
    Args:
        cbu (str): El CBU a validar
        
    Returns:
        tuple: (es_valido: bool, mensaje: str)
    """
    # Limpiar espacios y guiones
    cbu_limpio = cbu.replace(' ', '').replace('-', '').strip()
    
    # Verificar longitud
    if len(cbu_limpio) != 22:
        return False, "El CBU debe tener exactamente 22 dígitos"
    
    # Verificar que sean todos números
    if not cbu_limpio.isdigit():
        return False, "El CBU debe contener solo números"
    
    # Validar primer bloque (8 dígitos)
    bloque1 = cbu_limpio[:8]
    verificador1 = int(cbu_limpio[7])
    
    # Algoritmo para el primer verificador
    suma1 = (int(bloque1[0]) * 7 + 
             int(bloque1[1]) * 1 + 
             int(bloque1[2]) * 3 + 
             int(bloque1[3]) * 9 + 
             int(bloque1[4]) * 7 + 
             int(bloque1[5]) * 1 + 
             int(bloque1[6]) * 3)
    
    diferencia1 = 10 - (suma1 % 10)
    if diferencia1 == 10:
        diferencia1 = 0
    
    if verificador1 != diferencia1:
        return False, f"Dígito verificador del primer bloque inválido. Debería ser {diferencia1}"
    
    # Validar segundo bloque (14 dígitos)
    bloque2 = cbu_limpio[8:22]
    verificador2 = int(cbu_limpio[21])
    
    # Algoritmo para el segundo verificador
    suma2 = (int(bloque2[0]) * 3 + 
             int(bloque2[1]) * 9 + 
             int(bloque2[2]) * 7 + 
             int(bloque2[3]) * 1 + 
             int(bloque2[4]) * 3 + 
             int(bloque2[5]) * 9 + 
             int(bloque2[6]) * 7 + 
             int(bloque2[7]) * 1 + 
             int(bloque2[8]) * 3 + 
             int(bloque2[9]) * 9 + 
             int(bloque2[10]) * 7 + 
             int(bloque2[11]) * 1 + 
             int(bloque2[12]) * 3)
    
    diferencia2 = 10 - (suma2 % 10)
    if diferencia2 == 10:
        diferencia2 = 0
    
    if verificador2 != diferencia2:
        return False, f"Dígito verificador del segundo bloque inválido. Debería ser {diferencia2}"
    
    return True, "CBU válido"


def validar_referencia(codigo):
    """
    Valida el formato de un código de referencia.
    
    Formato esperado: 5 letras mayúsculas + 7 números
    Ejemplo: LABSEM0118
    
    Args:
        codigo (str): El código de referencia
        
    Returns:
        tuple: (es_valido: bool, mensaje: str)
    """
    # Limpiar espacios
    codigo = codigo.strip().upper()
    
    # Verificar longitud
    if len(codigo) != 12:
        return False, "La referencia debe tener 12 caracteres (5 letras + 7 números)"
    
    # Verificar formato con expresión regular
    # ^: inicio de la cadena
    # [A-Z]{5}: exactamente 5 letras mayúsculas
    # [0-9]{7}: exactamente 7 números
    # $: fin de la cadena
    patron = r'^[A-Z]{5}[0-9]{7}$'
    
    if not re.match(patron, codigo):
        return False, "Formato inválido. Debe ser: 5 letras mayúsculas + 7 números (Ej: LABSEM0000118)"
    
    return True, "Referencia válida"


def validar_importe(importe_str):
    """
    Valida que un importe sea un número válido y positivo.
    
    Args:
        importe_str (str): El importe como string
        
    Returns:
        tuple: (es_valido: bool, valor_float: float or None, mensaje: str)
    """
    # Limpiar espacios y reemplazar coma por punto
    importe = importe_str.strip().replace(',', '.')
    
    try:
        valor = float(importe)
        
        if valor <= 0:
            return False, None, "El importe debe ser mayor a 0"
        
        if valor > 999999999.99:
            return False, None, "El importe es demasiado grande"
        
        # Redondear a 2 decimales
        valor = round(valor, 2)
        
        return True, valor, "Importe válido"
        
    except ValueError:
        return False, None, "Importe inválido. Debe ser un número"


def validar_fecha(fecha_str):
    """
    Valida que una fecha tenga el formato DD/MM/AAAA.
    
    Args:
        fecha_str (str): La fecha como string
        
    Returns:
        tuple: (es_valido: bool, mensaje: str)
    """
    from datetime import datetime
    
    if not fecha_str or fecha_str.strip() == '':
        return True, "Fecha vacía (opcional)"
    
    # Verificar formato con expresión regular
    patron = r'^\d{2}/\d{2}/\d{4}$'
    if not re.match(patron, fecha_str):
        return False, "Formato inválido. Debe ser DD/MM/AAAA"
    
    # Intentar parsear la fecha
    try:
        datetime.strptime(fecha_str, '%d/%m/%Y')
        return True, "Fecha válida"
    except ValueError:
        return False, "Fecha inválida. Verifique día y mes"


def formatear_cuit(cuit):
    """
    Formatea un CUIT al formato estándar XX-XXXXXXXX-X.
    
    Args:
        cuit (str): CUIT sin formato
        
    Returns:
        str: CUIT formateado
    """
    cuit_limpio = cuit.replace('-', '').replace(' ', '').strip()
    
    if len(cuit_limpio) == 11:
        return f"{cuit_limpio[:2]}-{cuit_limpio[2:10]}-{cuit_limpio[10]}"
    
    return cuit


def formatear_cbu(cbu):
    """
    Formatea un CBU agrupando los dígitos para mejor lectura.
    
    Args:
        cbu (str): CBU sin formato
        
    Returns:
        str: CBU formateado
    """
    cbu_limpio = cbu.replace(' ', '').replace('-', '').strip()
    
    if len(cbu_limpio) == 22:
        # Formato: XXX XXXX X XXXXXXXXXXXXX X
        return f"{cbu_limpio[:3]} {cbu_limpio[3:7]} {cbu_limpio[7]} {cbu_limpio[8:21]} {cbu_limpio[21]}"
    
    return cbu


def limpiar_numero(numero_str):
    """
    Limpia un string de números eliminando todo lo que no sea dígito.
    
    Útil para limpiar inputs de usuario.
    
    Args:
        numero_str (str): String con números y posibles otros caracteres
        
    Returns:
        str: Solo los dígitos
    """
    return ''.join(filter(str.isdigit, numero_str))


# ============================================================================
# FUNCIONES DE TESTING
# ============================================================================

def test_validadores():
    """
    Función para probar todos los validadores.
    Útil para verificar que todo funciona correctamente.
    """
    print("=== TESTING VALIDADORES ===\n")
    
    # Test CUIT
    print("1. Validando CUIT:")
    cuits_test = [
        "20-12345678-9",  # Formato con guiones
        "20123456789",    # Formato sin guiones
        "27-98765432-1",  # Otro tipo válido
        "20-12345678-0",  # Verificador incorrecto
        "123456789",      # Muy corto
    ]
    
    for cuit in cuits_test:
        valido, msg = validar_cuit(cuit)
        print(f"   {cuit}: {'✅' if valido else '❌'} {msg}")
    
    # Test CBU
    print("\n2. Validando CBU:")
    cbus_test = [
        "0170099520000003912345",  # Ejemplo válido
        "123456789",               # Muy corto
        "0170099520000003912340",  # Verificador incorrecto
    ]
    
    for cbu in cbus_test:
        valido, msg = validar_cbu(cbu)
        print(f"   {cbu}: {'✅' if valido else '❌'} {msg}")
    
    # Test Referencia
    print("\n3. Validando Referencias:")
    refs_test = [
        "LABSEM0118",     # Válida
        "GAB2009",        # Muy corta
        "LABSEM01234",    # Solo 5 números
        "labsem0000118",  # Minúsculas
    ]
    
    for ref in refs_test:
        valido, msg = validar_referencia(ref)
        print(f"   {ref}: {'✅' if valido else '❌'} {msg}")
    
    print("\n=== FIN TESTS ===")


# Si ejecutamos este archivo directamente, correr los tests
if __name__ == "__main__":
    test_validadores()
