"""
============================================================================
MODEL - RANGO CHEQUE (VERSIÓN CORREGIDA)
============================================================================
Este modelo maneja los rangos de numeración de cheques.
============================================================================
"""

from config.database import DatabaseConfig
from datetime import datetime


class RangoCheque:
    """
    Representa un rango de numeración de cheques.
    """
    
    def __init__(self, id=None, tipo=None, numero_orden=None, 
                 numero_inicial=None, numero_final=None, cantidad_total=None,
                 proximo_numero=None, activo=True, fecha_creacion=None):
        """Constructor de la clase"""
        self.id = id
        self.tipo = tipo
        self.numero_orden = numero_orden
        self.numero_inicial = numero_inicial
        self.numero_final = numero_final
        self.cantidad_total = cantidad_total
        self.proximo_numero = proximo_numero
        self.activo = activo
        self.fecha_creacion = fecha_creacion
    
    @classmethod
    def crear(cls, tipo, numero_orden, numero_inicial, numero_final):
        """
        Crea un nuevo rango de cheques.
        
        ⚠️ CORRECCIONES:
        1. NO necesita validar_referencia (es para rangos, no referencias)
        2. Validar tipo sea 'diferido' o 'comun'
        3. Validar numero_orden sea 1, 2, 3 o 4
        4. Validar numero_inicial < numero_final
        5. Calcular cantidad_total
        6. Inicializar proximo_numero = numero_inicial
        7. Tabla: 'rangos_cheques' (plural)
        """
        # 1. Validar tipo
        tipo = tipo.lower().strip()
        if tipo not in ['diferido', 'comun']:
            raise ValueError("El tipo debe ser 'diferido' o 'comun'")
        
        # 2. Validar numero_orden
        if numero_orden not in [1, 2, 3, 4]:
            raise ValueError("El número de orden debe ser 1, 2, 3 o 4")
        
        # 3. Validar rangos
        if numero_inicial >= numero_final:
            raise ValueError("El número inicial debe ser menor que el número final")
        
        # 4. Verificar que no exista
        if cls.existe(tipo, numero_orden):
            raise ValueError(f"Ya existe un rango {tipo} con orden {numero_orden}")
        
        # 5. Calcular cantidad_total
        cantidad_total = numero_final - numero_inicial + 1
        
        # 6. Insertar en la base de datos
        # ⚠️ CORRECCIÓN: Tabla 'rangos_cheques' (plural) y campo 'activo' (no 'activa')
        query = """
            INSERT INTO rangos_cheques (tipo, numero_orden, numero_inicial, numero_final, cantidad_total, proximo_numero, activo)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        
        try:
            id_nuevo = DatabaseConfig.ejecutar_query(
                query, 
                params=(tipo, numero_orden, numero_inicial, numero_final, cantidad_total, numero_inicial, 1)
            )
            
            # 7. Retornar objeto creado
            return cls(
                id=id_nuevo,
                tipo=tipo,
                numero_orden=numero_orden, 
                numero_inicial=numero_inicial,
                numero_final=numero_final,
                cantidad_total=cantidad_total,
                proximo_numero=numero_inicial,  # ← Importante!
                activo=True
            )
            
        except Exception as e:
            raise Exception(f"Error al crear rango: {e}")
    
    @classmethod
    def existe(cls, tipo, numero_orden):
        """
        Verifica si existe un rango con ese tipo y orden.
        
        ⚠️ CORRECCIÓN: SQL correcto con AND
        """
        query = "SELECT COUNT(*) as count FROM rangos_cheques WHERE tipo = ? AND numero_orden = ?"
        resultado = DatabaseConfig.ejecutar_query(
            query, 
            params=(tipo.lower(), numero_orden), 
            fetch_one=True
        )
        return resultado['count'] > 0
    
    @classmethod
    def obtener_por_id(cls, id):
        """
        Obtiene un rango por su ID.
        
        ⚠️ CORRECCIÓN: Tabla y nombres de campos correctos
        """
        query = "SELECT * FROM rangos_cheques WHERE id = ?"
        fila = DatabaseConfig.ejecutar_query(
            query,
            params=(id,),
            fetch_one=True
        )
        
        if fila:
            return cls(
                id=fila['id'],
                tipo=fila['tipo'],
                numero_orden=fila['numero_orden'], 
                numero_inicial=fila['numero_inicial'],
                numero_final=fila['numero_final'],
                cantidad_total=fila['cantidad_total'],
                proximo_numero=fila['proximo_numero'],
                activo=bool(fila['activo']),
                fecha_creacion=fila['fecha_creacion']
            )
        
        return None
    
    @classmethod
    def obtener_todos(cls, tipo=None, solo_activos=True):
        """
        Obtiene todos los rangos, opcionalmente filtrados por tipo.
        
        ⚠️ CORRECCIÓN: Lógica de filtros correcta
        """
        query = "SELECT * FROM rangos_cheques WHERE 1=1"
        params = []
        
        # Filtrar por activos
        if solo_activos:
            query += " AND activo = 1"
        
        # Filtrar por tipo (opcional)
        if tipo:
            query += " AND tipo = ?"
            params.append(tipo.lower())
        
        # Ordenar por tipo y numero_orden
        query += " ORDER BY tipo, numero_orden"
        
        filas = DatabaseConfig.ejecutar_query(query, params=tuple(params) if params else None, fetch_all=True)
        
        return [cls(
            id=fila['id'],
            tipo=fila['tipo'],
            numero_orden=fila['numero_orden'], 
            numero_inicial=fila['numero_inicial'],
            numero_final=fila['numero_final'],
            cantidad_total=fila['cantidad_total'],
            proximo_numero=fila['proximo_numero'],
            activo=bool(fila['activo']),
            fecha_creacion=fila['fecha_creacion']
        ) for fila in filas]
    
    @classmethod
    def obtener_rango_activo(cls, tipo):
        """
        Obtiene el primer rango activo con números disponibles.
        
        ⚠️ CORRECCIÓN COMPLETA: Lógica correcta de selección
        """
        # Buscar rangos activos del tipo especificado, ordenados por prioridad
        query = """
            SELECT * FROM rangos_cheques 
            WHERE tipo = ? AND activo = 1
            ORDER BY numero_orden ASC
        """
        
        filas = DatabaseConfig.ejecutar_query(
            query,
            params=(tipo.lower(),),
            fetch_all=True
        )
        
        # Buscar el primer rango con números disponibles
        for fila in filas:
            proximo = fila['proximo_numero']
            final = fila['numero_final']
            
            # Si proximo_numero es None, usar numero_inicial
            if proximo is None:
                proximo = fila['numero_inicial']
            
            # Verificar si tiene disponibles
            if proximo <= final:
                return cls(
                    id=fila['id'],
                    tipo=fila['tipo'],
                    numero_orden=fila['numero_orden'], 
                    numero_inicial=fila['numero_inicial'],
                    numero_final=fila['numero_final'],
                    cantidad_total=fila['cantidad_total'],
                    proximo_numero=proximo,
                    activo=bool(fila['activo']),
                    fecha_creacion=fila['fecha_creacion']
                )
        
        # No hay rangos disponibles
        return None
    
    def actualizar(self):
        """
        Actualiza el rango en la base de datos.
        
        ⚠️ CORRECCIÓN: Campos y tabla correctos
        """
        if not self.id:
            raise ValueError("No se puede actualizar un rango sin ID")
        
        query = """
            UPDATE rangos_cheques 
            SET numero_inicial = ?, numero_final = ?, cantidad_total = ?, 
                proximo_numero = ?, activo = ?
            WHERE id = ?
        """
        
        try:
            DatabaseConfig.ejecutar_query(
                query,
                params=(self.numero_inicial, self.numero_final, self.cantidad_total, 
                       self.proximo_numero, int(self.activo), self.id)
            )
        except Exception as e:
            raise Exception(f"Error al actualizar rango: {e}")
    
    def desactivar(self):
        """Marca el rango como inactivo - ✅ ESTE ESTABA BIEN"""
        self.activo = False
        self.actualizar()
    
    def activar(self):
        """Marca el rango como activo - ✅ ESTE ESTABA BIEN"""
        self.activo = True
        self.actualizar()
    
    # ========================================================================
    # MÉTODOS DE CONSULTA (PROPIEDADES) - ⚠️ FALTABAN IMPLEMENTAR
    # ========================================================================
    
    def numeros_usados(self):
        """
        Calcula cuántos números se han usado de este rango.
        
        ⚠️ IMPLEMENTADO
        """
        if self.proximo_numero is None:
            return 0
        return self.proximo_numero - self.numero_inicial
    
    def numeros_disponibles(self):
        """
        Calcula cuántos números quedan disponibles.
        
        ⚠️ IMPLEMENTADO
        """
        if self.proximo_numero is None:
            return self.cantidad_total
        
        disponibles = self.numero_final - self.proximo_numero + 1
        return max(0, disponibles)  # No puede ser negativo
    
    def porcentaje_usado(self):
        """
        Calcula el porcentaje de uso del rango.
        
        ⚠️ IMPLEMENTADO
        """
        if self.cantidad_total == 0:
            return 0
        return (self.numeros_usados() / self.cantidad_total) * 100
    
    def tiene_disponibles(self):
        """
        Verifica si el rango tiene números disponibles.
        
        ⚠️ IMPLEMENTADO
        """
        return self.numeros_disponibles() > 0
    
    # ========================================================================
    # MÉTODOS DE ASIGNACIÓN - ⚠️ FALTABA IMPLEMENTAR
    # ========================================================================
    
    def obtener_siguiente_numero(self):
        """
        Obtiene y reserva el siguiente número disponible.
        
        ⚠️ IMPLEMENTADO - ESTE ES CRÍTICO!
        
        Este método:
        1. Verifica que esté activo y tenga disponibles
        2. Obtiene el número actual
        3. Incrementa proximo_numero en la BD
        4. Retorna el número
        """
        # 1. Verificar que esté activo
        if not self.activo:
            raise ValueError(f"El rango {self.tipo} #{self.numero_orden} está inactivo")
        
        # 2. Obtener proximo_numero
        if self.proximo_numero is None:
            self.proximo_numero = self.numero_inicial
        
        numero_actual = self.proximo_numero
        
        # 3. Verificar que tenga disponibles
        if numero_actual > self.numero_final:
            raise ValueError(f"El rango {self.tipo} #{self.numero_orden} está agotado")
        
        # 4. Incrementar proximo_numero en la BD
        nuevo_proximo = numero_actual + 1
        
        query = """
            UPDATE rangos_cheques 
            SET proximo_numero = ?
            WHERE id = ?
        """
        
        try:
            DatabaseConfig.ejecutar_query(
                query,
                params=(nuevo_proximo, self.id)
            )
            
            # Actualizar el objeto en memoria
            self.proximo_numero = nuevo_proximo
            
            # 5. Retornar el número asignado
            return numero_actual
            
        except Exception as e:
            raise Exception(f"Error al obtener siguiente número: {e}")
    
    def __str__(self):
        """Representación en string"""
        usado = self.numeros_usados()
        disponible = self.numeros_disponibles()
        return f"Rango {self.tipo} #{self.numero_orden}: {self.numero_inicial}-{self.numero_final} (Usados: {usado}, Disponibles: {disponible})"
    
    def __repr__(self):
        """Representación técnica"""
        return f"RangoCheque(id={self.id}, tipo='{self.tipo}', orden={self.numero_orden})"
    
    def to_dict(self):
        """Convierte el rango a diccionario"""
        return {
            'id': self.id,
            'tipo': self.tipo,
            'numero_orden': self.numero_orden,
            'numero_inicial': self.numero_inicial,
            'numero_final': self.numero_final,
            'cantidad_total': self.cantidad_total,
            'proximo_numero': self.proximo_numero,
            'numeros_usados': self.numeros_usados(),
            'numeros_disponibles': self.numeros_disponibles(),
            'porcentaje_usado': self.porcentaje_usado(),
            'activo': self.activo
        }


# ============================================================================
# FUNCIONES DE UTILIDAD
# ============================================================================

def inicializar_rangos_ejemplo():
    """Crea rangos de ejemplo para testing"""
    try:
        # Rango 1: Cheques diferidos
        if not RangoCheque.existe('diferido', 1):
            RangoCheque.crear('diferido', 1, 91181444, 91181843)
            print("✓ Rango diferido 1 creado")
        
        # Rango 2: Cheques comunes
        if not RangoCheque.existe('comun', 1):
            RangoCheque.crear('comun', 1, 91181244, 91181443)
            print("✓ Rango común 1 creado")
        
    except Exception as e:
        print(f"Error al inicializar rangos: {e}")


# ============================================================================
# TESTING
# ============================================================================

def test_rango_cheque():
    """Función de testing"""
    print("=== TESTING MODELO RANGO CHEQUE ===\n")
    
    try:
        # 1. Crear rango de cheques diferidos
        print("1. Creando rango de cheques diferidos...")
        rango1 = RangoCheque.crear(
            tipo='diferido',
            numero_orden=1,
            numero_inicial=91181444,
            numero_final=91181843
        )
        print(f"   ✓ Creado: {rango1}")
        print(f"   Info: {rango1.to_dict()}")
        
        # 2. Crear rango de cheques comunes
        print("\n2. Creando rango de cheques comunes...")
        rango2 = RangoCheque.crear(
            tipo='comun',
            numero_orden=1,
            numero_inicial=91181244,
            numero_final=91181443
        )
        print(f"   ✓ Creado: {rango2}")
        
        # 3. Obtener rango activo
        print("\n3. Obteniendo rango activo para diferidos...")
        activo = RangoCheque.obtener_rango_activo('diferido')
        print(f"   ✓ Rango activo: {activo}")
        
        # 4. Asignar algunos números
        print("\n4. Asignando números de cheque...")
        for i in range(5):
            numero = rango1.obtener_siguiente_numero()
            print(f"   ✓ Número asignado: {numero}")
        
        print(f"\n   Estado del rango: {rango1}")
        print(f"   Porcentaje usado: {rango1.porcentaje_usado():.2f}%")
        
        # 5. Obtener todos
        print("\n5. Obteniendo todos los rangos...")
        todos = RangoCheque.obtener_todos()
        print(f"   ✓ Total rangos: {len(todos)}")
        for r in todos:
            print(f"      - {r}")
        
        print("\n=== TESTS COMPLETADOS ===")
        
    except Exception as e:
        print(f"\n❌ Error en test: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_rango_cheque()