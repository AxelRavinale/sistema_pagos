"""
============================================================================
MODEL - REFERENCIA
============================================================================
Este modelo maneja todo lo relacionado con las referencias de las planillas.

Las referencias son códigos únicos que identifican cada planilla.
Formato: 5 letras + 7 números (Ej: LABSEM0000118)

CONCEPTOS CLAVE:
- CRUD: Create, Read, Update, Delete (operaciones básicas en BD)
- Class methods (@classmethod): Métodos que trabajan con la clase, no con instancias
- Instance methods: Métodos que trabajan con una instancia específica
============================================================================
"""

from config.database import DatabaseConfig
from utils.validators import validar_referencia
from datetime import datetime


class Referencia:
    """
    Representa una referencia de planilla en el sistema.
    
    Atributos:
        id (int): ID único en la base de datos
        codigo (str): Código de la referencia (Ej: LABSEM0000118)
        descripcion (str): Descripción opcional
        fecha_creacion (datetime): Cuándo se creó
        activa (bool): Si está activa o no
    """
    
    def __init__(self, id=None, codigo=None, descripcion=None, 
                 fecha_creacion=None, activa=True):
        """
        Constructor de la clase.
        
        Args:
            id (int, optional): ID de la referencia
            codigo (str, optional): Código de la referencia
            descripcion (str, optional): Descripción
            fecha_creacion (datetime, optional): Fecha de creación
            activa (bool, optional): Si está activa. Defaults to True.
        """
        self.id = id
        self.codigo = codigo
        self.descripcion = descripcion
        self.fecha_creacion = fecha_creacion
        self.activa = activa
    
    # ========================================================================
    # MÉTODOS DE CLASE (CREATE, READ)
    # ========================================================================
    
    @classmethod
    def crear(cls, codigo, descripcion=''):
        """
        Crea una nueva referencia en la base de datos.
        
        Este es un método de CREACIÓN (la C en CRUD).
        
        Args:
            codigo (str): Código de la referencia (5 letras + 7 números)
            descripcion (str, optional): Descripción. Defaults to ''.
            
        Returns:
            Referencia: Objeto con la referencia creada
            
        Raises:
            ValueError: Si el código es inválido o ya existe
            
        Ejemplo:
            ref = Referencia.crear("LABSEM0000118", "Laboratorio Seminario")
            print(f"Creada referencia: {ref.codigo}")
        """
        # 1. Validar formato del código
        codigo = codigo.upper().strip()
        valido, mensaje = validar_referencia(codigo)
        if not valido:
            raise ValueError(mensaje)
        
        # 2. Verificar que no exista
        if cls.existe(codigo):
            raise ValueError(f"Ya existe una referencia con el código {codigo}")
        
        # 3. Insertar en la base de datos
        query = """
            INSERT INTO referencias (codigo, descripcion, activa)
            VALUES (?, ?, ?)
        """
        
        try:
            id_nuevo = DatabaseConfig.ejecutar_query(
                query, 
                params=(codigo, descripcion, 1)
            )
            
            # 4. Retornar objeto creado
            return cls(
                id=id_nuevo,
                codigo=codigo,
                descripcion=descripcion,
                fecha_creacion=datetime.now(),
                activa=True
            )
            
        except Exception as e:
            raise Exception(f"Error al crear referencia: {e}")
    
    @classmethod
    def existe(cls, codigo):
        """
        Verifica si existe una referencia con ese código.
        
        Args:
            codigo (str): Código a verificar
            
        Returns:
            bool: True si existe, False si no
            
        Ejemplo:
            if Referencia.existe("LABSEM0000118"):
                print("Ya existe")
        """
        query = "SELECT COUNT(*) as count FROM referencias WHERE codigo = ?"
        resultado = DatabaseConfig.ejecutar_query(
            query, 
            params=(codigo.upper(),), 
            fetch_one=True
        )
        return resultado['count'] > 0
    
    @classmethod
    def obtener_por_id(cls, id):
        """
        Obtiene una referencia por su ID.
        
        Este es un método de LECTURA (la R en CRUD).
        
        Args:
            id (int): ID de la referencia
            
        Returns:
            Referencia or None: Objeto Referencia o None si no existe
            
        Ejemplo:
            ref = Referencia.obtener_por_id(5)
            if ref:
                print(ref.codigo)
        """
        query = "SELECT * FROM referencias WHERE id = ?"
        fila = DatabaseConfig.ejecutar_query(
            query,
            params=(id,),
            fetch_one=True
        )
        
        if fila:
            return cls(
                id=fila['id'],
                codigo=fila['codigo'],
                descripcion=fila['descripcion'],
                fecha_creacion=fila['fecha_creacion'],
                activa=bool(fila['activa'])
            )
        
        return None
    
    @classmethod
    def obtener_por_codigo(cls, codigo):
        """
        Obtiene una referencia por su código.
        
        Args:
            codigo (str): Código de la referencia
            
        Returns:
            Referencia or None: Objeto Referencia o None si no existe
        """
        query = "SELECT * FROM referencias WHERE codigo = ?"
        fila = DatabaseConfig.ejecutar_query(
            query,
            params=(codigo.upper(),),
            fetch_one=True
        )
        
        if fila:
            return cls(
                id=fila['id'],
                codigo=fila['codigo'],
                descripcion=fila['descripcion'],
                fecha_creacion=fila['fecha_creacion'],
                activa=bool(fila['activa'])
            )
        
        return None
    
    @classmethod
    def obtener_todas(cls, solo_activas=True):
        """
        Obtiene todas las referencias de la base de datos.
        
        Args:
            solo_activas (bool, optional): Si True, solo activas. Defaults to True.
            
        Returns:
            list: Lista de objetos Referencia
            
        Ejemplo:
            todas = Referencia.obtener_todas()
            for ref in todas:
                print(f"{ref.codigo} - {ref.descripcion}")
        """
        query = "SELECT * FROM referencias"
        if solo_activas:
            query += " WHERE activa = 1"
        query += " ORDER BY fecha_creacion DESC"
        
        filas = DatabaseConfig.ejecutar_query(query, fetch_all=True)
        
        # Convertir filas en objetos Referencia
        return [cls(
            id=fila['id'],
            codigo=fila['codigo'],
            descripcion=fila['descripcion'],
            fecha_creacion=fila['fecha_creacion'],
            activa=bool(fila['activa'])
        ) for fila in filas]
    
    @classmethod
    def generar_siguiente_codigo(cls, prefijo):
        """
        Genera el siguiente código de referencia basado en un prefijo.
        
        IMPORTANTE: Esta función es clave para evitar códigos duplicados.
        
        Lógica:
        1. Busca el último código con ese prefijo
        2. Si existe, toma la parte numérica y le suma 1
        3. Si no existe, empieza en 1
        4. Formatea con 7 dígitos (con ceros a la izquierda)
        
        Args:
            prefijo (str): Las 5 letras del código (Ej: "LABSEM")
            
        Returns:
            str: Código completo generado (Ej: "LABSEM0000119")
            
        Raises:
            ValueError: Si el prefijo no tiene 5 letras
            
        Ejemplo:
            # Si existe LABSEM0000118
            nuevo = Referencia.generar_siguiente_codigo("LABSEM")
            print(nuevo)  # Output: LABSEM0000119
        """
        # Validar prefijo
        prefijo = prefijo.upper().strip()
        if len(prefijo) != 5 or not prefijo.isalpha():
            raise ValueError("El prefijo debe tener exactamente 5 letras")
        
        # Buscar el último código con ese prefijo
        query = """
            SELECT codigo FROM referencias 
            WHERE codigo LIKE ? 
            ORDER BY codigo DESC 
            LIMIT 1
        """
        resultado = DatabaseConfig.ejecutar_query(
            query,
            params=(f"{prefijo}%",),
            fetch_one=True
        )
        
        if resultado:
            # Extraer la parte numérica (últimos 7 caracteres)
            parte_numerica = int(resultado['codigo'][5:])
            nueva_parte_numerica = parte_numerica + 1
        else:
            # Es la primera con este prefijo
            nueva_parte_numerica = 1
        
        # Formatear con 7 dígitos (completar con ceros a la izquierda)
        # Ejemplo: 118 → 0000118
        return f"{prefijo}{nueva_parte_numerica:07d}"
    
    # ========================================================================
    # MÉTODOS DE INSTANCIA (UPDATE, DELETE)
    # ========================================================================
    
    def actualizar(self):
        """
        Actualiza la referencia en la base de datos.
        
        Este es un método de ACTUALIZACIÓN (la U en CRUD).
        Solo actualiza descripción y estado activa.
        El código NO se puede cambiar (es único e inmutable).
        
        Raises:
            ValueError: Si la referencia no tiene ID (no fue guardada)
            
        Ejemplo:
            ref = Referencia.obtener_por_id(5)
            ref.descripcion = "Nueva descripción"
            ref.actualizar()
        """
        if not self.id:
            raise ValueError("No se puede actualizar una referencia sin ID")
        
        query = """
            UPDATE referencias 
            SET descripcion = ?, activa = ?
            WHERE id = ?
        """
        
        try:
            DatabaseConfig.ejecutar_query(
                query,
                params=(self.descripcion, int(self.activa), self.id)
            )
        except Exception as e:
            raise Exception(f"Error al actualizar referencia: {e}")
    
    def desactivar(self):
        """
        Marca la referencia como inactiva (soft delete).
        
        NO eliminamos el registro de la base de datos (hard delete),
        solo lo marcamos como inactivo. Esto mantiene el historial.
        
        Ejemplo:
            ref = Referencia.obtener_por_id(5)
            ref.desactivar()
        """
        self.activa = False
        self.actualizar()
    
    def activar(self):
        """
        Marca la referencia como activa nuevamente.
        
        Ejemplo:
            ref = Referencia.obtener_por_id(5)
            ref.activar()
        """
        self.activa = True
        self.actualizar()
    
    def eliminar_permanentemente(self):
        """
        Elimina la referencia de la base de datos PERMANENTEMENTE.
        
        ⚠️ CUIDADO: Esta acción NO se puede deshacer.
        
        Solo usar si:
        - La referencia fue creada por error
        - No tiene planillas asociadas
        
        Raises:
            ValueError: Si tiene planillas asociadas
            
        Ejemplo:
            ref = Referencia.obtener_por_id(5)
            if not ref.tiene_planillas():
                ref.eliminar_permanentemente()
        """
        if not self.id:
            raise ValueError("No se puede eliminar una referencia sin ID")
        
        # Verificar que no tenga planillas asociadas
        if self.tiene_planillas():
            raise ValueError(
                "No se puede eliminar una referencia con planillas asociadas. "
                "Use desactivar() en su lugar."
            )
        
        query = "DELETE FROM referencias WHERE id = ?"
        
        try:
            DatabaseConfig.ejecutar_query(query, params=(self.id,))
            self.id = None  # Marcar como eliminada
        except Exception as e:
            raise Exception(f"Error al eliminar referencia: {e}")
    
    # ========================================================================
    # MÉTODOS DE CONSULTA ADICIONALES
    # ========================================================================
    
    def tiene_planillas(self):
        """
        Verifica si esta referencia tiene planillas asociadas.
        
        Returns:
            bool: True si tiene planillas, False si no
        """
        query = "SELECT COUNT(*) as count FROM planillas WHERE referencia_id = ?"
        resultado = DatabaseConfig.ejecutar_query(
            query,
            params=(self.id,),
            fetch_one=True
        )
        return resultado['count'] > 0
    
    def contar_planillas(self):
        """
        Cuenta cuántas planillas tiene esta referencia.
        
        Returns:
            int: Cantidad de planillas
        """
        query = "SELECT COUNT(*) as count FROM planillas WHERE referencia_id = ?"
        resultado = DatabaseConfig.ejecutar_query(
            query,
            params=(self.id,),
            fetch_one=True
        )
        return resultado['count']
    
    # ========================================================================
    # MÉTODOS ESPECIALES DE PYTHON
    # ========================================================================
    
    def __str__(self):
        """
        Representación en string de la referencia.
        
        Se usa cuando haces print(referencia) o str(referencia)
        
        Returns:
            str: Representación legible
        """
        estado = "✓ Activa" if self.activa else "✗ Inactiva"
        return f"{self.codigo} - {self.descripcion or 'Sin descripción'} [{estado}]"
    
    def __repr__(self):
        """
        Representación técnica de la referencia.
        
        Se usa en debugging y en consola interactiva.
        
        Returns:
            str: Representación técnica
        """
        return f"Referencia(id={self.id}, codigo='{self.codigo}')"
    
    def to_dict(self):
        """
        Convierte la referencia a diccionario.
        
        Útil para:
        - Serialización JSON
        - Pasar datos a la interfaz gráfica
        - Logging
        
        Returns:
            dict: Diccionario con todos los atributos
        """
        return {
            'id': self.id,
            'codigo': self.codigo,
            'descripcion': self.descripcion,
            'fecha_creacion': self.fecha_creacion,
            'activa': self.activa
        }


# ============================================================================
# FUNCIONES DE UTILIDAD
# ============================================================================

def buscar_referencias(termino):
    """
    Busca referencias por código o descripción.
    
    Args:
        termino (str): Término de búsqueda
        
    Returns:
        list: Lista de referencias que coinciden
        
    Ejemplo:
        resultados = buscar_referencias("LAB")
        for ref in resultados:
            print(ref)
    """
    query = """
        SELECT * FROM referencias 
        WHERE codigo LIKE ? OR descripcion LIKE ?
        ORDER BY fecha_creacion DESC
    """
    
    # Agregar % para búsqueda parcial
    termino_busqueda = f"%{termino.upper()}%"
    
    filas = DatabaseConfig.ejecutar_query(
        query,
        params=(termino_busqueda, termino_busqueda),
        fetch_all=True
    )
    
    return [Referencia(
        id=fila['id'],
        codigo=fila['codigo'],
        descripcion=fila['descripcion'],
        fecha_creacion=fila['fecha_creacion'],
        activa=bool(fila['activa'])
    ) for fila in filas]


# ============================================================================
# TESTING
# ============================================================================

def test_referencia():
    """
    Función de testing para probar la clase Referencia.
    """
    print("=== TESTING MODELO REFERENCIA ===\n")
    
    try:
        # 1. Crear referencia
        print("1. Creando referencia...")
        ref = Referencia.crear("LABSEM0000118", "Laboratorio Seminario")
        print(f"   ✅ Creada: {ref}")
        
        # 2. Verificar que existe
        print("\n2. Verificando existencia...")
        existe = Referencia.existe("LABSEM0000118")
        print(f"   ✅ Existe: {existe}")
        
        # 3. Obtener todas
        print("\n3. Obteniendo todas las referencias...")
        todas = Referencia.obtener_todas()
        print(f"   ✅ Total: {len(todas)} referencias")
        for r in todas:
            print(f"      - {r}")
        
        # 4. Generar siguiente código
        print("\n4. Generando siguiente código...")
        siguiente = Referencia.generar_siguiente_codigo("LABSEM")
        print(f"   ✅ Siguiente: {siguiente}")
        
        # 5. Actualizar descripción
        print("\n5. Actualizando descripción...")
        ref.descripcion = "Lab Seminario Actualizado"
        ref.actualizar()
        print(f"   ✅ Actualizada: {ref}")
        
        # 6. Desactivar
        print("\n6. Desactivando...")
        ref.desactivar()
        print(f"   ✅ Desactivada: {ref}")
        
        # 7. Buscar
        print("\n7. Buscando por término...")
        resultados = buscar_referencias("LAB")
        print(f"   ✅ Encontradas: {len(resultados)}")
        
        print("\n=== TESTS COMPLETADOS ===")
        
    except Exception as e:
        print(f"\n❌ Error en test: {e}")
        import traceback
        traceback.print_exc()


# Si ejecutamos este archivo directamente, correr los tests
if __name__ == "__main__":
    test_referencia()