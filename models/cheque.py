"""
============================================================================
MODEL - CHEQUE (VERSIÓN CORREGIDA)
============================================================================
Este modelo maneja los cheques individuales emitidos.
============================================================================
"""

from config.database import DatabaseConfig
from datetime import datetime


class Cheque:
    """Representa un cheque emitido"""
    
    # Estados posibles (constantes de clase)
    ESTADO_PENDIENTE = 'emitido_pendiente'
    ESTADO_CORRECTO = 'emitido_correcto'
    ESTADO_CARGADO = 'cargado_sistema'
    ESTADO_SIN_USAR = 'sin_usar'
    
    ESTADOS_VALIDOS = [ESTADO_PENDIENTE, ESTADO_CORRECTO, ESTADO_CARGADO, ESTADO_SIN_USAR]
    
    def __init__(self, id=None, numero_cheque=None, tipo=None, estado=None,
                 referencia_id=None, planilla_id=None, beneficiario=None,
                 importe=None, fecha_emision=None, fecha_pago=None, fecha_creacion=None):
        """Constructor de la clase"""
        self.id = id
        self.numero_cheque = numero_cheque
        self.tipo = tipo
        self.estado = estado or self.ESTADO_PENDIENTE
        self.referencia_id = referencia_id
        self.planilla_id = planilla_id
        self.beneficiario = beneficiario
        self.importe = importe
        self.fecha_emision = fecha_emision
        self.fecha_pago = fecha_pago
        self.fecha_creacion = fecha_creacion
    
    @classmethod
    def crear(cls, numero_cheque, tipo, planilla_id=None, referencia_id=None,
              beneficiario=None, importe=None, fecha_emision=None, fecha_pago=None):
        """
        Crea un nuevo cheque en la base de datos.
        
        ⚠️ CORRECCIONES:
        1. Validación de importe corregida (debe ser > 0, no ≤ 0)
        2. INSERT incluye todos los campos necesarios
        3. NO hay campo 'activo' en cheques_emitidos (lo confundiste con rangos)
        """
        # 1. Validar tipo
        tipo = tipo.lower().strip()
        if tipo not in ['diferido', 'comun']:
            raise ValueError("El tipo debe ser 'diferido' o 'comun'")
        
        # 2. Verificar que no exista
        if cls.existe(numero_cheque, tipo):
            raise ValueError(f"Ya existe un cheque con número {numero_cheque} y tipo {tipo}")
        
        # 3. Validar importe (si se proporciona)
        # ⚠️ CORRECCIÓN: Debe ser > 0 (no <= 0)
        if importe is not None and importe <= 0:
            raise ValueError("El importe debe ser mayor a 0")
        
        # 4. Insertar en la base de datos
        # ⚠️ CORRECCIÓN: Incluir campo 'estado' y NO incluir 'activo' (no existe)
        query = """
            INSERT INTO cheques_emitidos (numero_cheque, tipo, estado, referencia_id, planilla_id, 
                                         beneficiario, importe, fecha_emision, fecha_pago)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        try:
            id_nuevo = DatabaseConfig.ejecutar_query(
                query, 
                params=(numero_cheque, tipo, cls.ESTADO_PENDIENTE, referencia_id, planilla_id,
                       beneficiario, importe, fecha_emision, fecha_pago)
            )
            
            # 5. Retornar objeto creado
            return cls(
                id=id_nuevo,
                numero_cheque=numero_cheque,
                tipo=tipo,
                estado=cls.ESTADO_PENDIENTE,
                referencia_id=referencia_id,
                planilla_id=planilla_id,
                beneficiario=beneficiario,
                importe=importe,
                fecha_emision=fecha_emision,
                fecha_pago=fecha_pago,
                fecha_creacion=datetime.now()
            )
            
        except Exception as e:
            raise Exception(f"Error al crear cheque: {e}")

    @classmethod
    def existe(cls, numero_cheque, tipo):
        """
        Verifica si existe un cheque con ese número y tipo.
        
        ✅ ESTE ESTABA BIEN!
        """
        query = "SELECT COUNT(*) as count FROM cheques_emitidos WHERE numero_cheque = ? AND tipo = ?"
        resultado = DatabaseConfig.ejecutar_query(
            query, 
            params=(numero_cheque, tipo.lower()), 
            fetch_one=True
        )
        return resultado['count'] > 0
    
    @classmethod
    def obtener_por_id(cls, id):
        """
        Obtiene un cheque por su ID.
        
        ⚠️ CORRECCIÓN: NO hay campo 'activo'
        """
        query = "SELECT * FROM cheques_emitidos WHERE id = ?"
        fila = DatabaseConfig.ejecutar_query(
            query,
            params=(id,),
            fetch_one=True
        )
        
        if fila:
            return cls(
                id=fila['id'],
                numero_cheque=fila['numero_cheque'],
                tipo=fila['tipo'],
                estado=fila['estado'],
                referencia_id=fila['referencia_id'],
                planilla_id=fila['planilla_id'],
                beneficiario=fila['beneficiario'],
                importe=fila['importe'],
                fecha_emision=fila['fecha_emision'],
                fecha_pago=fila['fecha_pago'],
                fecha_creacion=fila['fecha_creacion']
            )
        
        return None
    
    @classmethod
    def obtener_por_numero(cls, numero_cheque, tipo):
        """
        Obtiene un cheque por su número y tipo.
        
        ✅ ESTE ESTABA CASI BIEN - Solo quitamos 'activo'
        """
        query = "SELECT * FROM cheques_emitidos WHERE numero_cheque = ? AND tipo = ?"
        fila = DatabaseConfig.ejecutar_query(
            query,
            params=(numero_cheque, tipo.lower()),
            fetch_one=True
        )
        
        if fila:
            return cls(
                id=fila['id'],
                numero_cheque=fila['numero_cheque'],
                tipo=fila['tipo'],
                estado=fila['estado'],
                referencia_id=fila['referencia_id'],
                planilla_id=fila['planilla_id'],
                beneficiario=fila['beneficiario'],
                importe=fila['importe'],
                fecha_emision=fila['fecha_emision'],
                fecha_pago=fila['fecha_pago'],
                fecha_creacion=fila['fecha_creacion']
            )
        
        return None

    @classmethod
    def obtener_por_planilla(cls, planilla_id):
        """
        Obtiene todos los cheques de una planilla.
        
        ⚠️ CORRECCIÓN: Debe usar fetch_all (retorna LISTA, no uno solo)
        """
        query = "SELECT * FROM cheques_emitidos WHERE planilla_id = ?"
        
        # ⚠️ CORRECCIÓN: fetch_all=True (no fetch_one)
        filas = DatabaseConfig.ejecutar_query(
            query,
            params=(planilla_id,),
            fetch_all=True
        )
        
        return [cls(
            id=fila['id'],
            numero_cheque=fila['numero_cheque'],
            tipo=fila['tipo'],
            estado=fila['estado'],
            referencia_id=fila['referencia_id'],
            planilla_id=fila['planilla_id'],
            beneficiario=fila['beneficiario'],
            importe=fila['importe'],
            fecha_emision=fila['fecha_emision'],
            fecha_pago=fila['fecha_pago'],
            fecha_creacion=fila['fecha_creacion']
        ) for fila in filas]
    
    @classmethod
    def obtener_por_estado(cls, estado, tipo=None):
        """
        Obtiene todos los cheques en un estado específico.
        
        ⚠️ CORRECCIÓN: Lógica de filtros y fetch_all
        """
        query = "SELECT * FROM cheques_emitidos WHERE estado = ?"
        params = [estado]
        
        if tipo:
            query += " AND tipo = ?"
            params.append(tipo.lower())
        
        query += " ORDER BY fecha_creacion DESC"
        
        filas = DatabaseConfig.ejecutar_query(
            query,
            params=tuple(params),
            fetch_all=True
        )
        
        return [cls(
            id=fila['id'],
            numero_cheque=fila['numero_cheque'],
            tipo=fila['tipo'],
            estado=fila['estado'],
            referencia_id=fila['referencia_id'],
            planilla_id=fila['planilla_id'],
            beneficiario=fila['beneficiario'],
            importe=fila['importe'],
            fecha_emision=fila['fecha_emision'],
            fecha_pago=fila['fecha_pago'],
            fecha_creacion=fila['fecha_creacion']
        ) for fila in filas]
    
    @classmethod
    def obtener_todos(cls, tipo=None, estado=None):
        """
        Obtiene todos los cheques con filtros opcionales.
        
        ⚠️ CORRECCIÓN COMPLETA: Lógica de filtros incorrecta
        """
        query = "SELECT * FROM cheques_emitidos WHERE 1=1"
        params = []
        
        if tipo:
            query += " AND tipo = ?"
            params.append(tipo.lower())
        
        if estado:
            query += " AND estado = ?"
            params.append(estado)
        
        query += " ORDER BY fecha_creacion DESC"
        
        filas = DatabaseConfig.ejecutar_query(
            query, 
            params=tuple(params) if params else None,
            fetch_all=True
        )
        
        return [cls(
            id=fila['id'],
            numero_cheque=fila['numero_cheque'],
            tipo=fila['tipo'],
            estado=fila['estado'],
            referencia_id=fila['referencia_id'],
            planilla_id=fila['planilla_id'],
            beneficiario=fila['beneficiario'],
            importe=fila['importe'],
            fecha_emision=fila['fecha_emision'],
            fecha_pago=fila['fecha_pago'],
            fecha_creacion=fila['fecha_creacion']
        ) for fila in filas]
    
    def actualizar(self):
        """
        Actualiza el cheque en la base de datos.
        
        ⚠️ CORRECCIÓN: NO hay campo 'activa'
        """
        if not self.id:
            raise ValueError("No se puede actualizar un cheque sin ID")
        
        query = """
            UPDATE cheques_emitidos 
            SET estado = ?, beneficiario = ?, importe = ?, fecha_emision = ?,
                fecha_pago = ?, planilla_id = ?, referencia_id = ?
            WHERE id = ?
        """
        
        try:
            DatabaseConfig.ejecutar_query(
                query,
                params=(self.estado, self.beneficiario, self.importe, self.fecha_emision, 
                       self.fecha_pago, self.planilla_id, self.referencia_id, self.id)
            )
        except Exception as e:
            raise Exception(f"Error al actualizar cheque: {e}")
    
    # ========================================================================
    # MÉTODOS DE CAMBIO DE ESTADO
    # ========================================================================
    
    def marcar_como_correcto(self):
        """
        Cambia el estado a 'emitido_correcto'.
        
        ⚠️ CORRECCIÓN: Debes actualizar self.estado también
        """
        if self.estado != self.ESTADO_PENDIENTE:
            raise ValueError(f"Solo se puede marcar como correcto desde estado pendiente. Estado actual: {self.estado}")
        
        self.estado = self.ESTADO_CORRECTO
        self.actualizar()
    
    def marcar_como_cargado(self):
        """
        Cambia el estado a 'cargado_sistema'.
        
        ⚠️ CORRECCIÓN: Debes actualizar self.estado también
        """
        if self.estado != self.ESTADO_CORRECTO:
            raise ValueError(f"Solo se puede cargar desde estado correcto. Estado actual: {self.estado}")
        
        self.estado = self.ESTADO_CARGADO
        self.actualizar()
    
    def marcar_como_sin_usar(self):
        """
        Cambia el estado a 'sin_usar'.
        
        ⚠️ CORRECCIÓN: Lógica y actualización de self.estado
        """
        if self.estado == self.ESTADO_CARGADO:
            raise ValueError("No se puede marcar como sin usar un cheque ya cargado en el sistema")
        
        self.estado = self.ESTADO_SIN_USAR
        self.actualizar()
    
    # ========================================================================
    # MÉTODOS DE CONSULTA
    # ========================================================================
    
    def es_diferido(self):
        """Verifica si el cheque es diferido"""
        return self.tipo == 'diferido'
    
    def es_comun(self):
        """Verifica si el cheque es común"""
        return self.tipo == 'comun'
    
    def esta_pendiente(self):
        """Verifica si está en estado pendiente"""
        return self.estado == self.ESTADO_PENDIENTE
    
    def esta_disponible(self):
        """Verifica si está disponible para reutilizar"""
        return self.estado == self.ESTADO_SIN_USAR
    
    def puede_cambiar_estado(self, nuevo_estado):
        """
        Verifica si se puede cambiar al nuevo estado.
        
        ⚠️ CORRECCIÓN COMPLETA: La lógica estaba muy confusa
        """
        # Validar que el nuevo estado sea válido
        if nuevo_estado not in self.ESTADOS_VALIDOS:
            return False
        
        # Reglas de transición
        transiciones_validas = {
            self.ESTADO_PENDIENTE: [self.ESTADO_CORRECTO, self.ESTADO_SIN_USAR],
            self.ESTADO_CORRECTO: [self.ESTADO_CARGADO, self.ESTADO_SIN_USAR],
            self.ESTADO_CARGADO: [],  # No se puede cambiar
            self.ESTADO_SIN_USAR: []  # No se puede cambiar
        }
        
        return nuevo_estado in transiciones_validas.get(self.estado, [])
    
    def __str__(self):
        """Representación en string"""
        return f"Cheque {self.tipo} #{self.numero_cheque} - Estado: {self.estado}"
    
    def __repr__(self):
        """Representación técnica"""
        return f"Cheque(id={self.id}, numero={self.numero_cheque}, tipo='{self.tipo}')"
    
    def to_dict(self):
        """Convierte el cheque a diccionario"""
        return {
            'id': self.id,
            'numero_cheque': self.numero_cheque,
            'tipo': self.tipo,
            'estado': self.estado,
            'referencia_id': self.referencia_id,
            'planilla_id': self.planilla_id,
            'beneficiario': self.beneficiario,
            'importe': self.importe,
            'fecha_emision': self.fecha_emision,
            'fecha_pago': self.fecha_pago,
            'fecha_creacion': self.fecha_creacion
        }


# ============================================================================
# FUNCIONES DE UTILIDAD
# ============================================================================

def buscar_cheques(termino):
    """
    Busca cheques por número, beneficiario o cualquier campo.
    
    ⚠️ CORRECCIÓN: Búsqueda por número debe ser exacta (es un int)
    """
    query = """
        SELECT * FROM cheques_emitidos 
        WHERE CAST(numero_cheque AS TEXT) LIKE ? 
           OR tipo LIKE ? 
           OR estado LIKE ? 
           OR beneficiario LIKE ?
        ORDER BY fecha_creacion DESC
    """
    
    termino_busqueda = f"%{termino}%"
    
    filas = DatabaseConfig.ejecutar_query(
        query,
        params=(termino_busqueda, termino_busqueda, termino_busqueda, termino_busqueda),
        fetch_all=True
    )

    return [Cheque(
        id=fila['id'],
        numero_cheque=fila['numero_cheque'],
        tipo=fila['tipo'],
        estado=fila['estado'],
        referencia_id=fila['referencia_id'],
        planilla_id=fila['planilla_id'],
        beneficiario=fila['beneficiario'],
        importe=fila['importe'],
        fecha_emision=fila['fecha_emision'],
        fecha_pago=fila['fecha_pago'],
        fecha_creacion=fila['fecha_creacion']
    ) for fila in filas]    

def contar_por_estado(tipo=None):
    """
    Cuenta cuántos cheques hay en cada estado.
    
    ⚠️ CORRECCIÓN COMPLETA: Debe retornar un dict con todos los estados
    """
    resultado = {}
    
    for estado in Cheque.ESTADOS_VALIDOS:
        query = "SELECT COUNT(*) as count FROM cheques_emitidos WHERE estado = ?"
        params = [estado]
        
        if tipo:
            query += " AND tipo = ?"
            params.append(tipo.lower())
        
        fila = DatabaseConfig.ejecutar_query(
            query,
            params=tuple(params),
            fetch_one=True
        )
        
        resultado[estado] = fila['count']
    
    return resultado


# ============================================================================
# TESTING
# ============================================================================

def test_cheque():
    """Función de testing"""
    print("=== TESTING MODELO CHEQUE ===\n")
    
    try:
        # 1. Crear cheque
        print("1. Creando cheque diferido...")
        cheque1 = Cheque.crear(
            numero_cheque=91181444,
            tipo='diferido',
            beneficiario='Juan Pérez',
            importe=50000.00,
            fecha_emision='01/03/2026',
            fecha_pago='15/04/2026'
        )
        print(f"   ✓ Creado: {cheque1}")
        
        # 2. Cambiar estado
        print("\n2. Marcando como emitido correcto...")
        cheque1.marcar_como_correcto()
        print(f"   ✓ Estado: {cheque1.estado}")
        
        # 3. Obtener por número
        print("\n3. Buscando por número...")
        encontrado = Cheque.obtener_por_numero(91181444, 'diferido')
        print(f"   ✓ Encontrado: {encontrado}")
        
        # 4. Crear cheque común
        print("\n4. Creando cheque común...")
        cheque2 = Cheque.crear(
            numero_cheque=91181244,
            tipo='comun',
            beneficiario='María González',
            importe=25000.00
        )
        print(f"   ✓ Creado: {cheque2}")
        
        # 5. Obtener todos
        print("\n5. Obteniendo todos los cheques...")
        todos = Cheque.obtener_todos()
        print(f"   ✓ Total: {len(todos)} cheques")
        for c in todos:
            print(f"      - {c}")
        
        # 6. Filtrar por estado
        print("\n6. Cheques pendientes...")
        pendientes = Cheque.obtener_por_estado(Cheque.ESTADO_PENDIENTE)
        print(f"   ✓ Pendientes: {len(pendientes)}")
        
        # 7. Contar por estado
        print("\n7. Conteo por estado...")
        conteo = contar_por_estado()
        for estado, cantidad in conteo.items():
            print(f"   - {estado}: {cantidad}")
        
        print("\n=== TESTS COMPLETADOS ===")
        
    except Exception as e:
        print(f"\n❌ Error en test: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_cheque()