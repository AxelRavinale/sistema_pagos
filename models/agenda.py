"""
============================================================================
MODEL - AGENDA (CONTACTOS)
============================================================================
Este módulo maneja los contactos para cheques y transferencias.

VERSIÓN CORREGIDA con explicaciones de los errores comunes.
============================================================================
"""

from config.database import DatabaseConfig
from utils.validators import validar_cuit, validar_cbu


class ContactoCheque:
    """
    Representa un contacto para pagos con cheque.
    
    Atributos:
        id (int): ID único
        nombre (str): Nombre del beneficiario
        cuit (str): CUIT del beneficiario
        notas (str): Notas opcionales
        activo (bool): Si está activo
    """
    
    def __init__(self, id=None, nombre=None, cuit=None, notas=None, activo=True):
        """Constructor de la clase"""
        self.id = id
        self.nombre = nombre
        self.cuit = cuit
        self.notas = notas
        self.activo = activo
    
    @classmethod
    def crear(cls, nombre, cuit, notas=''):
        """
        Crea un nuevo contacto en la base de datos.
        
        ⚠️ ERROR CORREGIDO:
        - Tabla: 'agenda_cheques' (no 'contactos')
        - INSERT debe tener 3 campos en VALUES para 3 valores
        - Campo: 'activo' (no 'activa')
        """
        # 1. Validar formato del CUIT
        cuit = cuit.upper().strip()
        valido, mensaje = validar_cuit(cuit)
        if not valido:
            raise ValueError(mensaje)
        
        # 2. Verificar que no exista
        if cls.existe(cuit):
            raise ValueError(f"Ya existe un contacto con el CUIT {cuit}")
        
        # 3. Insertar en la base de datos
        # ⚠️ CORRECCIÓN: Tabla correcta y campos correctos
        query = """
            INSERT INTO agenda_cheques (nombre, cuit, notas)
            VALUES (?, ?, ?)
        """
        
        try:
            id_nuevo = DatabaseConfig.ejecutar_query(
                query,
                params=(nombre, cuit, notas)
            )
            
            # 4. Retornar objeto creado
            return cls(
                id=id_nuevo,
                nombre=nombre,
                cuit=cuit,
                notas=notas,
                activo=True
            )
        
        except Exception as e:
            raise Exception(f"Error al crear contacto: {e}")
    
    @classmethod
    def existe(cls, cuit):
        """
        Verifica si existe un contacto con ese CUIT.
        
        ⚠️ ERROR CORREGIDO:
        - Buscar por 'cuit', no por 'nombre'
        - Tabla: 'agenda_cheques'
        """
        query = "SELECT COUNT(*) as count FROM agenda_cheques WHERE cuit = ?"
        resultado = DatabaseConfig.ejecutar_query(
            query,
            params=(cuit.upper(),),
            fetch_one=True
        )
        return resultado['count'] > 0
    
    @classmethod
    def obtener_por_id(cls, id):
        """
        Obtiene un contacto por su ID.
        
        ⚠️ ERROR CORREGIDO:
        - Tabla: 'agenda_cheques'
        - Campo: 'activo' (no 'activa')
        """
        query = "SELECT * FROM agenda_cheques WHERE id = ?"
        fila = DatabaseConfig.ejecutar_query(
            query,
            params=(id,),
            fetch_one=True
        )
        
        if fila:
            return cls(
                id=fila['id'],
                nombre=fila['nombre'],
                cuit=fila['cuit'],
                notas=fila['notas'],
                activo=bool(fila['activo'])  # Campo correcto
            )
        
        return None
    
    @classmethod
    def obtener_por_cuit(cls, cuit):
        """
        Obtiene un contacto por su CUIT.
        
        ⚠️ ERROR CORREGIDO: Tabla correcta
        """
        query = "SELECT * FROM agenda_cheques WHERE cuit = ?"
        fila = DatabaseConfig.ejecutar_query(
            query,
            params=(cuit.upper(),),
            fetch_one=True
        )
        
        if fila:
            return cls(
                id=fila['id'],
                nombre=fila['nombre'],
                cuit=fila['cuit'],
                notas=fila['notas'],
                activo=bool(fila['activo'])
            )
        
        return None
    
    @classmethod
    def obtener_todos(cls, solo_activos=True):
        """
        Obtiene todos los contactos.
        
        ⚠️ ERROR CORREGIDO:
        - Tabla: 'agenda_cheques'
        - Campo: 'activo' (no 'activa')
        """
        query = "SELECT * FROM agenda_cheques"
        if solo_activos:
            query += " WHERE activo = 1"
        query += " ORDER BY fecha_creacion DESC"
        
        filas = DatabaseConfig.ejecutar_query(query, fetch_all=True)
        
        return [cls(
            id=fila['id'],
            nombre=fila['nombre'],
            cuit=fila['cuit'],
            notas=fila['notas'],
            activo=bool(fila['activo'])
        ) for fila in filas]
    
    def actualizar(self):
        """
        Actualiza el contacto en la base de datos.
        
        ⚠️ ERRORES CORREGIDOS:
        - Tabla: 'agenda_cheques' (estaba 'contatos' - typo)
        - Campos: nombre, cuit, notas, activo
        - Orden correcto de parámetros
        """
        if not self.id:
            raise ValueError("No se puede actualizar un contacto sin ID")
        
        query = """
            UPDATE agenda_cheques
            SET nombre = ?, cuit = ?, notas = ?, activo = ?
            WHERE id = ?
        """
        
        try:
            DatabaseConfig.ejecutar_query(
                query,
                params=(self.nombre, self.cuit, self.notas, int(self.activo), self.id)
            )
        except Exception as e:
            raise Exception(f"Error al actualizar contacto: {e}")
    
    def desactivar(self):
        """
        Marca el contacto como inactivo.
        
        ✅ ESTE ESTABA BIEN!
        """
        self.activo = False
        self.actualizar()
    
    def __str__(self):
        """Representación en string"""
        return f"{self.nombre} - CUIT: {self.cuit}"
    
    def __repr__(self):
        """Representación técnica"""
        return f"ContactoCheque(id={self.id}, nombre='{self.nombre}', cuit='{self.cuit}')"


class ContactoTransferencia:
    """
    Representa un contacto para transferencias.
    
    Similar a ContactoCheque pero con CBU adicional.
    """
    
    def __init__(self, id=None, nombre=None, cuit=None, cbu=None, notas=None, activo=True):
        """Constructor de la clase"""
        self.id = id
        self.nombre = nombre
        self.cuit = cuit
        self.cbu = cbu
        self.notas = notas
        self.activo = activo
    
    @classmethod
    def crear(cls, nombre, cuit, cbu, notas=''):
        """
        Crea un nuevo contacto en la base de datos.
        
        ⚠️ ERRORES CORREGIDOS:
        - Validar CBU, no CUIT (estabas validando CUIT en la línea del CBU)
        - Validar ambos: CUIT y CBU
        - Tabla: 'agenda_transferencias'
        - 4 campos en VALUES para 4 valores
        """
        # 1. Validar CUIT
        cuit = cuit.upper().strip()
        valido_cuit, mensaje_cuit = validar_cuit(cuit)
        if not valido_cuit:
            raise ValueError(f"CUIT inválido: {mensaje_cuit}")
        
        # 2. Validar CBU
        cbu = cbu.strip()  # CBU no lleva upper() porque son números
        valido_cbu, mensaje_cbu = validar_cbu(cbu)
        if not valido_cbu:
            raise ValueError(f"CBU inválido: {mensaje_cbu}")
        
        # 3. Verificar que no exista
        if cls.existe(cuit, cbu):
            raise ValueError(f"Ya existe un contacto con CUIT {cuit} y CBU {cbu}")
        
        # 4. Insertar en la base de datos
        query = """
            INSERT INTO agenda_transferencias (nombre, cuit, cbu, notas)
            VALUES (?, ?, ?, ?)
        """
        
        try:
            id_nuevo = DatabaseConfig.ejecutar_query(
                query,
                params=(nombre, cuit, cbu, notas)
            )
            
            # 5. Retornar objeto creado
            return cls(
                id=id_nuevo,
                nombre=nombre,
                cuit=cuit,
                cbu=cbu,
                notas=notas,
                activo=True
            )
        
        except Exception as e:
            raise Exception(f"Error al crear contacto: {e}")
    
    @classmethod
    def existe(cls, cuit, cbu):
        """
        Verifica si existe un contacto con ese CUIT y CBU.
        
        ⚠️ ERROR CORREGIDO:
        - Buscar por CUIT AND CBU (ambos campos)
        - Tabla: 'agenda_transferencias'
        """
        query = """
            SELECT COUNT(*) as count 
            FROM agenda_transferencias 
            WHERE cuit = ? AND cbu = ?
        """
        resultado = DatabaseConfig.ejecutar_query(
            query,
            params=(cuit.upper(), cbu),
            fetch_one=True
        )
        return resultado['count'] > 0
    
    @classmethod
    def obtener_por_id(cls, id):
        """Obtiene un contacto por su ID"""
        query = "SELECT * FROM agenda_transferencias WHERE id = ?"
        fila = DatabaseConfig.ejecutar_query(
            query,
            params=(id,),
            fetch_one=True
        )
        
        if fila:
            return cls(
                id=fila['id'],
                nombre=fila['nombre'],
                cuit=fila['cuit'],
                cbu=fila['cbu'],
                notas=fila['notas'],
                activo=bool(fila['activo'])
            )
        
        return None
    
    @classmethod
    def obtener_por_cuit(cls, cuit):
        """
        Obtiene TODOS los contactos con ese CUIT.
        
        ⚠️ CAMBIO IMPORTANTE:
        - Retorna LISTA (no un solo elemento)
        - Porque un CUIT puede tener varios CBUs
        - Usa fetch_all=True
        """
        query = "SELECT * FROM agenda_transferencias WHERE cuit = ?"
        filas = DatabaseConfig.ejecutar_query(
            query,
            params=(cuit.upper(),),
            fetch_all=True  # ← IMPORTANTE: fetch_all
        )
        
        return [cls(
            id=fila['id'],
            nombre=fila['nombre'],
            cuit=fila['cuit'],
            cbu=fila['cbu'],
            notas=fila['notas'],
            activo=bool(fila['activo'])
        ) for fila in filas]
    
    @classmethod
    def obtener_por_cbu(cls, cbu):
        """Obtiene un contacto por su CBU"""
        query = "SELECT * FROM agenda_transferencias WHERE cbu = ?"
        fila = DatabaseConfig.ejecutar_query(
            query,
            params=(cbu,),
            fetch_one=True
        )
        
        if fila:
            return cls(
                id=fila['id'],
                nombre=fila['nombre'],
                cuit=fila['cuit'],
                cbu=fila['cbu'],
                notas=fila['notas'],
                activo=bool(fila['activo'])
            )
        
        return None
    
    @classmethod
    def obtener_todos(cls, solo_activos=True):
        """Obtiene todos los contactos"""
        query = "SELECT * FROM agenda_transferencias"
        if solo_activos:
            query += " WHERE activo = 1"
        query += " ORDER BY fecha_creacion DESC"
        
        filas = DatabaseConfig.ejecutar_query(query, fetch_all=True)
        
        return [cls(
            id=fila['id'],
            nombre=fila['nombre'],
            cuit=fila['cuit'],
            cbu=fila['cbu'],
            notas=fila['notas'],
            activo=bool(fila['activo'])
        ) for fila in filas]
    
    def actualizar(self):
        """
        Actualiza el contacto en la base de datos.
        
        ⚠️ ERROR CORREGIDO:
        - Tabla: 'agenda_transferencias'
        - Incluir el campo CBU
        """
        if not self.id:
            raise ValueError("No se puede actualizar un contacto sin ID")
        
        query = """
            UPDATE agenda_transferencias
            SET nombre = ?, cuit = ?, cbu = ?, notas = ?, activo = ?
            WHERE id = ?
        """
        
        try:
            DatabaseConfig.ejecutar_query(
                query,
                params=(self.nombre, self.cuit, self.cbu, self.notas, int(self.activo), self.id)
            )
        except Exception as e:
            raise Exception(f"Error al actualizar contacto: {e}")
    
    def desactivar(self):
        """Marca el contacto como inactivo"""
        self.activo = False
        self.actualizar()
    
    def __str__(self):
        """Representación en string"""
        return f"{self.nombre} - CUIT: {self.cuit} - CBU: {self.cbu}"
    
    def __repr__(self):
        """Representación técnica"""
        return f"ContactoTransferencia(id={self.id}, nombre='{self.nombre}')"


# ============================================================================
# FUNCIONES DE UTILIDAD
# ============================================================================

def buscar_contactos_cheque(termino):
    """
    Busca contactos de cheque por nombre o CUIT.
    
    ⚠️ ERROR CORREGIDO:
    - Tabla: 'agenda_cheques'
    - Buscar por 'nombre' o 'cuit' (no 'codigo' ni 'descripcion')
    """
    query = """
        SELECT * FROM agenda_cheques 
        WHERE nombre LIKE ? OR cuit LIKE ?
        ORDER BY fecha_creacion DESC
    """
    
    termino_busqueda = f"%{termino.upper()}%"
    
    filas = DatabaseConfig.ejecutar_query(
        query,
        params=(termino_busqueda, termino_busqueda),
        fetch_all=True
    )
    
    return [ContactoCheque(
        id=fila['id'],
        nombre=fila['nombre'],
        cuit=fila['cuit'],
        notas=fila['notas'],
        activo=bool(fila['activo'])
    ) for fila in filas]


def buscar_contactos_transferencia(termino):
    """
    Busca contactos de transferencia por nombre, CUIT o CBU.
    
    ⚠️ ERROR CORREGIDO: Buscar por los campos correctos
    """
    query = """
        SELECT * FROM agenda_transferencias 
        WHERE nombre LIKE ? OR cuit LIKE ? OR cbu LIKE ?
        ORDER BY fecha_creacion DESC
    """
    
    termino_busqueda = f"%{termino}%"
    
    filas = DatabaseConfig.ejecutar_query(
        query,
        params=(termino_busqueda, termino_busqueda, termino_busqueda),
        fetch_all=True
    )
    
    return [ContactoTransferencia(
        id=fila['id'],
        nombre=fila['nombre'],
        cuit=fila['cuit'],
        cbu=fila['cbu'],
        notas=fila['notas'],
        activo=bool(fila['activo'])
    ) for fila in filas]


# ============================================================================
# TESTING
# ============================================================================

def test_agenda():
    """Función de testing para probar las clases"""
    print("=== TESTING MODELO AGENDA ===\n")
    
    try:
        # 1. Crear contacto de cheque
        print("1. Creando contacto de cheque...")
        contacto_ch = ContactoCheque.crear("Juan Pérez", "20-12345678-9", "Cliente VIP")
        print(f"   ✓ Creado: {contacto_ch}")
        
        # 2. Crear contacto de transferencia
        print("\n2. Creando contacto de transferencia...")
        contacto_tr = ContactoTransferencia.crear(
            "María González", 
            "27-98765432-1", 
            "0170099520000003912345",
            "Proveedor"
        )
        print(f"   ✓ Creado: {contacto_tr}")
        
        # 3. Obtener todos
        print("\n3. Obteniendo todos los contactos...")
        cheques = ContactoCheque.obtener_todos()
        print(f"   ✓ Contactos cheque: {len(cheques)}")
        for c in cheques:
            print(f"      - {c}")
        
        transferencias = ContactoTransferencia.obtener_todos()
        print(f"   ✓ Contactos transferencia: {len(transferencias)}")
        for t in transferencias:
            print(f"      - {t}")
        
        print("\n=== TESTS COMPLETADOS ===")
        
    except Exception as e:
        print(f"\n❌ Error en test: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_agenda()