"""
============================================================================
MODEL - PLANILLA (COMPLETO)
============================================================================
Este es el modelo MÁS IMPORTANTE del sistema.

Una planilla contiene múltiples items (pagos individuales).
Cada item puede ser un cheque o una transferencia.
============================================================================
"""

from config.database import DatabaseConfig
from datetime import datetime


class Planilla:
    """
    Representa una planilla de pagos.
    
    Atributos:
        id (int): ID único
        referencia_id (int): ID de la referencia
        numero_planilla (int): Número correlativo
        sucursal (str): Sucursal bancaria
        cuenta_debito (str): Cuenta de débito
        estado (str): 'borrador', 'generada', 'descargada'
        archivo_excel (str): Ruta del archivo generado
        fecha_creacion (datetime): Fecha de creación
    """
    
    # Estados posibles
    ESTADO_BORRADOR = 'borrador'
    ESTADO_GENERADA = 'generada'
    ESTADO_DESCARGADA = 'descargada'
    
    def __init__(self, id=None, referencia_id=None, numero_planilla=None,
                 sucursal=None, cuenta_debito=None, estado=None,
                 archivo_excel=None, fecha_creacion=None):
        """Constructor de la clase"""
        self.id = id
        self.referencia_id = referencia_id
        self.numero_planilla = numero_planilla
        self.sucursal = sucursal
        self.cuenta_debito = cuenta_debito
        self.estado = estado or self.ESTADO_BORRADOR
        self.archivo_excel = archivo_excel
        self.fecha_creacion = fecha_creacion
    
    @classmethod
    def crear(cls, referencia_id, sucursal, cuenta_debito):
        """
        Crea una nueva planilla en estado borrador.
        
        Este método:
        1. Valida que la referencia existe
        2. Obtiene el próximo número de planilla de configuracion
        3. Crea la planilla
        4. Incrementa el contador
        """
        # 1. Validar que la referencia existe
        from models.referencia import Referencia
        ref = Referencia.obtener_por_id(referencia_id)
        if not ref:
            raise ValueError(f"No existe la referencia con ID {referencia_id}")
        
        # 2. Obtener el próximo número de planilla
        query_get = "SELECT valor FROM configuracion WHERE clave = 'proximo_numero_planilla'"
        resultado = DatabaseConfig.ejecutar_query(query_get, fetch_one=True)
        
        if resultado:
            numero_planilla = int(resultado['valor'])
        else:
            # Si no existe, crear el registro
            query_insert = "INSERT INTO configuracion (clave, valor, descripcion) VALUES (?, ?, ?)"
            DatabaseConfig.ejecutar_query(
                query_insert,
                params=('proximo_numero_planilla', '1', 'Próximo número de planilla')
            )
            numero_planilla = 1
        
        # 3. Crear la planilla
        query = """
            INSERT INTO planillas (referencia_id, numero_planilla, sucursal, cuenta_debito, estado)
            VALUES (?, ?, ?, ?, ?)
        """
        
        try:
            id_nuevo = DatabaseConfig.ejecutar_query(
                query,
                params=(referencia_id, numero_planilla, sucursal, cuenta_debito, cls.ESTADO_BORRADOR)
            )
            
            # 4. Incrementar el contador
            query_update = "UPDATE configuracion SET valor = ? WHERE clave = 'proximo_numero_planilla'"
            DatabaseConfig.ejecutar_query(query_update, params=(str(numero_planilla + 1),))
            
            # 5. Retornar objeto creado
            return cls(
                id=id_nuevo,
                referencia_id=referencia_id,
                numero_planilla=numero_planilla,
                sucursal=sucursal,
                cuenta_debito=cuenta_debito,
                estado=cls.ESTADO_BORRADOR,
                fecha_creacion=datetime.now()
            )
            
        except Exception as e:
            raise Exception(f"Error al crear planilla: {e}")
    
    @classmethod
    def obtener_por_id(cls, id):
        """Obtiene una planilla por su ID"""
        query = "SELECT * FROM planillas WHERE id = ?"
        fila = DatabaseConfig.ejecutar_query(query, params=(id,), fetch_one=True)
        
        if fila:
            return cls(
                id=fila['id'],
                referencia_id=fila['referencia_id'],
                numero_planilla=fila['numero_planilla'],
                sucursal=fila['sucursal'],
                cuenta_debito=fila['cuenta_debito'],
                estado=fila['estado'],
                archivo_excel=fila['archivo_excel'],
                fecha_creacion=fila['fecha_creacion']
            )
        
        return None
    
    @classmethod
    def obtener_todas(cls, referencia_id=None, estado=None):
        """
        Obtiene todas las planillas con filtros opcionales.
        """
        query = "SELECT * FROM planillas WHERE 1=1"
        params = []
        
        if referencia_id:
            query += " AND referencia_id = ?"
            params.append(referencia_id)
        
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
            referencia_id=fila['referencia_id'],
            numero_planilla=fila['numero_planilla'],
            sucursal=fila['sucursal'],
            cuenta_debito=fila['cuenta_debito'],
            estado=fila['estado'],
            archivo_excel=fila['archivo_excel'],
            fecha_creacion=fila['fecha_creacion']
        ) for fila in filas]
    
    def actualizar(self):
        """Actualiza la planilla en la base de datos"""
        if not self.id:
            raise ValueError("No se puede actualizar una planilla sin ID")
        
        query = """
            UPDATE planillas 
            SET referencia_id = ?, numero_planilla = ?, sucursal = ?, 
                cuenta_debito = ?, estado = ?, archivo_excel = ?
            WHERE id = ?
        """
        
        try:
            DatabaseConfig.ejecutar_query(
                query,
                params=(self.referencia_id, self.numero_planilla, self.sucursal,
                       self.cuenta_debito, self.estado, self.archivo_excel, self.id)
            )
        except Exception as e:
            raise Exception(f"Error al actualizar planilla: {e}")
    
    # ========================================================================
    # MÉTODOS DE GESTIÓN DE ITEMS
    # ========================================================================
    
    def agregar_item(self, tipo_documento, numero_documento, identificacion_pago,
                     beneficiario, importe, modalidad_pago, cuenta_pago=None,
                     marca_registracion=None, fecha_emision=None, fecha_pago_diferido=None):
        """
        Agrega un item (pago) a la planilla.
        
        IMPORTANTE: NO asigna número de cheque aquí.
        Los números se asignan cuando se genera el Excel.
        
        Args:
            tipo_documento (str): 'CUIT' o 'CUIL'
            numero_documento (str): Número de documento
            identificacion_pago (str): Identificación del pago
            beneficiario (str): Nombre del beneficiario
            importe (float): Monto a pagar
            modalidad_pago (int): 2, 4, 6, 8
            cuenta_pago (str, optional): CBU o número de cheque
            marca_registracion (str, optional): Marca del cheque
            fecha_emision (str, optional): Fecha de emisión
            fecha_pago_diferido (str, optional): Fecha de pago diferido
            
        Returns:
            int: ID del item creado
        """
        # Validar que la planilla esté en borrador
        if not self.puede_editar():
            raise ValueError("Solo se pueden agregar items a planillas en borrador")
        
        # Validar modalidad de pago
        if modalidad_pago not in [2, 4, 6, 8]:
            raise ValueError("Modalidad de pago debe ser 2, 4, 6 u 8")
        
        # Validar importe
        if importe <= 0:
            raise ValueError("El importe debe ser mayor a 0")
        
        # Insertar en la base de datos
        query = """
            INSERT INTO items_planilla 
            (planilla_id, tipo_documento, numero_documento, identificacion_pago,
             beneficiario, importe, cuenta_pago, modalidad_pago, marca_registracion,
             fecha_emision, fecha_pago_diferido)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        try:
            id_item = DatabaseConfig.ejecutar_query(
                query,
                params=(self.id, tipo_documento, numero_documento, identificacion_pago,
                       beneficiario, importe, cuenta_pago, modalidad_pago, marca_registracion,
                       fecha_emision, fecha_pago_diferido)
            )
            return id_item
            
        except Exception as e:
            raise Exception(f"Error al agregar item: {e}")
    
    def obtener_items(self):
        """
        Obtiene todos los items de esta planilla.
        
        Returns:
            list: Lista de diccionarios con los items
        """
        query = "SELECT * FROM items_planilla WHERE planilla_id = ? ORDER BY id"
        filas = DatabaseConfig.ejecutar_query(
            query,
            params=(self.id,),
            fetch_all=True
        )
        
        # Convertir filas a diccionarios
        items = []
        for fila in filas:
            items.append({
                'id': fila['id'],
                'planilla_id': fila['planilla_id'],
                'tipo_documento': fila['tipo_documento'],
                'numero_documento': fila['numero_documento'],
                'identificacion_pago': fila['identificacion_pago'],
                'beneficiario': fila['beneficiario'],
                'importe': fila['importe'],
                'cuenta_pago': fila['cuenta_pago'],
                'modalidad_pago': fila['modalidad_pago'],
                'marca_registracion': fila['marca_registracion'],
                'fecha_emision': fila['fecha_emision'],
                'fecha_pago_diferido': fila['fecha_pago_diferido'],
                'cheque_id': fila['cheque_id']
            })
        
        return items
    
    def eliminar_item(self, item_id):
        """
        Elimina un item de la planilla.
        
        Solo se puede si la planilla está en borrador.
        """
        if not self.puede_editar():
            raise ValueError("Solo se pueden eliminar items de planillas en borrador")
        
        query = "DELETE FROM items_planilla WHERE id = ? AND planilla_id = ?"
        
        try:
            DatabaseConfig.ejecutar_query(query, params=(item_id, self.id))
        except Exception as e:
            raise Exception(f"Error al eliminar item: {e}")
    
    def contar_items(self):
        """
        Cuenta cuántos items tiene la planilla.
        
        Returns:
            int: Cantidad de items
        """
        query = "SELECT COUNT(*) as count FROM items_planilla WHERE planilla_id = ?"
        resultado = DatabaseConfig.ejecutar_query(
            query,
            params=(self.id,),
            fetch_one=True
        )
        return resultado['count']
    
    def calcular_total(self):
        """
        Calcula el total de importes de la planilla.
        
        Returns:
            float: Suma de todos los importes
        """
        query = "SELECT SUM(importe) as total FROM items_planilla WHERE planilla_id = ?"
        resultado = DatabaseConfig.ejecutar_query(
            query,
            params=(self.id,),
            fetch_one=True
        )
        
        total = resultado['total']
        return float(total) if total else 0.0
    
    # ========================================================================
    # MÉTODOS DE CAMBIO DE ESTADO
    # ========================================================================
    
    def marcar_como_generada(self, archivo_excel):
        """
        Marca la planilla como generada.
        
        Args:
            archivo_excel (str): Ruta del archivo Excel generado
        """
        self.estado = self.ESTADO_GENERADA
        self.archivo_excel = archivo_excel
        self.actualizar()
    
    def marcar_como_descargada(self):
        """Marca la planilla como descargada"""
        if self.estado != self.ESTADO_GENERADA:
            raise ValueError("Solo se puede marcar como descargada una planilla generada")
        
        self.estado = self.ESTADO_DESCARGADA
        self.actualizar()
    
    # ========================================================================
    # MÉTODOS DE CONSULTA
    # ========================================================================
    
    def es_borrador(self):
        """Verifica si está en borrador"""
        return self.estado == self.ESTADO_BORRADOR
    
    def puede_editar(self):
        """Verifica si se puede editar"""
        return self.es_borrador()
    
    def tiene_items(self):
        """Verifica si tiene items"""
        return self.contar_items() > 0
    
    def obtener_referencia(self):
        """
        Obtiene el objeto Referencia asociado.
        
        Returns:
            Referencia: Objeto de la referencia
        """
        from models.referencia import Referencia
        return Referencia.obtener_por_id(self.referencia_id)
    
    def __str__(self):
        """Representación en string"""
        items = self.contar_items()
        return f"Planilla #{self.numero_planilla} - Estado: {self.estado} ({items} items)"
    
    def __repr__(self):
        """Representación técnica"""
        return f"Planilla(id={self.id}, numero={self.numero_planilla})"
    
    def to_dict(self):
        """Convierte la planilla a diccionario"""
        return {
            'id': self.id,
            'referencia_id': self.referencia_id,
            'numero_planilla': self.numero_planilla,
            'sucursal': self.sucursal,
            'cuenta_debito': self.cuenta_debito,
            'estado': self.estado,
            'archivo_excel': self.archivo_excel,
            'fecha_creacion': self.fecha_creacion,
            'cantidad_items': self.contar_items(),
            'total_importe': self.calcular_total()
        }


class ItemPlanilla:
    """
    Clase opcional para representar un item individual.
    
    Esta clase es OPCIONAL - puedes trabajar con diccionarios directamente
    o usar esta clase si querés más estructura.
    """
    
    def __init__(self, id=None, planilla_id=None, tipo_documento=None,
                 numero_documento=None, identificacion_pago=None,
                 beneficiario=None, importe=None, cuenta_pago=None,
                 modalidad_pago=None, marca_registracion=None,
                 fecha_emision=None, fecha_pago_diferido=None, cheque_id=None):
        """Constructor de la clase"""
        self.id = id
        self.planilla_id = planilla_id
        self.tipo_documento = tipo_documento
        self.numero_documento = numero_documento
        self.identificacion_pago = identificacion_pago
        self.beneficiario = beneficiario
        self.importe = importe
        self.cuenta_pago = cuenta_pago
        self.modalidad_pago = modalidad_pago
        self.marca_registracion = marca_registracion
        self.fecha_emision = fecha_emision
        self.fecha_pago_diferido = fecha_pago_diferido
        self.cheque_id = cheque_id
    
    def es_cheque(self):
        """Verifica si es un cheque (modalidad 6 o 8)"""
        return self.modalidad_pago in [6, 8]
    
    def es_transferencia(self):
        """Verifica si es una transferencia (modalidad 2 o 4)"""
        return self.modalidad_pago in [2, 4]
    
    def es_diferido(self):
        """Verifica si es diferido (modalidad 8)"""
        return self.modalidad_pago == 8
    
    def __str__(self):
        """Representación en string"""
        tipo = "Cheque" if self.es_cheque() else "Transferencia"
        return f"{tipo} - {self.beneficiario} - ${self.importe}"


# ============================================================================
# FUNCIONES DE UTILIDAD
# ============================================================================

def obtener_estadisticas():
    """
    Obtiene estadísticas generales de planillas.
    
    Returns:
        dict: {
            'total_planillas': 10,
            'borradores': 2,
            'generadas': 5,
            'descargadas': 3
        }
    """
    estadisticas = {
        'total_planillas': 0,
        'borradores': 0,
        'generadas': 0,
        'descargadas': 0
    }
    
    # Total
    query_total = "SELECT COUNT(*) as count FROM planillas"
    resultado = DatabaseConfig.ejecutar_query(query_total, fetch_one=True)
    estadisticas['total_planillas'] = resultado['count']
    
    # Por estado
    for estado in [Planilla.ESTADO_BORRADOR, Planilla.ESTADO_GENERADA, Planilla.ESTADO_DESCARGADA]:
        query = "SELECT COUNT(*) as count FROM planillas WHERE estado = ?"
        resultado = DatabaseConfig.ejecutar_query(query, params=(estado,), fetch_one=True)
        
        if estado == Planilla.ESTADO_BORRADOR:
            estadisticas['borradores'] = resultado['count']
        elif estado == Planilla.ESTADO_GENERADA:
            estadisticas['generadas'] = resultado['count']
        else:
            estadisticas['descargadas'] = resultado['count']
    
    return estadisticas


# ============================================================================
# TESTING
# ============================================================================

def test_planilla():
    """Función de testing"""
    print("=== TESTING MODELO PLANILLA ===\n")
    
    try:
        # Primero necesitas una referencia
        from models.referencia import Referencia
        
        # Crear referencia si no existe
        if not Referencia.existe("TEST0000001"):
            ref = Referencia.crear("TEST0000001", "Test Planilla")
        else:
            ref = Referencia.obtener_por_codigo("TEST0000001")
        
        print(f"Usando referencia: {ref}")
        
        # 1. Crear planilla
        print("\n1. Creando planilla...")
        planilla = Planilla.crear(
            referencia_id=ref.id,
            sucursal="001",
            cuenta_debito="0170099520000003912345"
        )
        print(f"   ✓ Creada: {planilla}")
        print(f"   Info: {planilla.to_dict()}")
        
        # 2. Agregar items
        print("\n2. Agregando items...")
        
        # Item 1: Cheque común
        item1_id = planilla.agregar_item(
            tipo_documento='CUIT',
            numero_documento='20-12345678-9',
            identificacion_pago='OP001',
            beneficiario='Juan Pérez',
            importe=50000.00,
            modalidad_pago=6,  # Cheque común
            fecha_emision='01/03/2026'
        )
        print(f"   ✓ Item 1 agregado: ID {item1_id}")
        
        # Item 2: Transferencia
        item2_id = planilla.agregar_item(
            tipo_documento='CUIT',
            numero_documento='27-98765432-1',
            identificacion_pago='OP002',
            beneficiario='María González',
            importe=25000.00,
            modalidad_pago=2,  # Transferencia Macro
            cuenta_pago='0170099520000003912345'
        )
        print(f"   ✓ Item 2 agregado: ID {item2_id}")
        
        # Item 3: Cheque diferido
        item3_id = planilla.agregar_item(
            tipo_documento='CUIT',
            numero_documento='30-11111111-1',
            identificacion_pago='OP003',
            beneficiario='Pedro Rodríguez',
            importe=75000.00,
            modalidad_pago=8,  # Cheque diferido
            fecha_emision='01/03/2026',
            fecha_pago_diferido='15/04/2026'
        )
        print(f"   ✓ Item 3 agregado: ID {item3_id}")
        
        # 3. Ver items
        print(f"\n3. Items de la planilla ({planilla.contar_items()}):")
        items = planilla.obtener_items()
        for item in items:
            modalidad = {2: 'Transfer Macro', 4: 'Transfer Otros', 6: 'Echeq Común', 8: 'Echeq Diferido'}
            print(f"   - {item['beneficiario']}: ${item['importe']:,.2f} ({modalidad[item['modalidad_pago']]})")
        
        # 4. Calcular total
        print(f"\n4. Total planilla: ${planilla.calcular_total():,.2f}")
        
        # 5. Obtener todas
        print("\n5. Todas las planillas:")
        todas = Planilla.obtener_todas()
        print(f"   ✓ Total: {len(todas)}")
        for p in todas[:3]:  # Mostrar solo las primeras 3
            print(f"      - {p}")
        
        # 6. Estadísticas
        print("\n6. Estadísticas:")
        stats = obtener_estadisticas()
        for clave, valor in stats.items():
            print(f"   - {clave}: {valor}")
        
        print("\n=== TESTS COMPLETADOS ===")
        
    except Exception as e:
        print(f"\n❌ Error en test: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_planilla()