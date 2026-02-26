"""
Servicio para gestionar la lógica de numeración de cheques
"""
from config.database import DatabaseConfig
from models.cheque import Cheque
from models.rango_cheque import RangoCheque

class ChequeService:
    
    @staticmethod
    def obtener_proximo_numero(tipo):
        """
        Obtiene el próximo número de cheque disponible.
        
        Busca en los rangos activos, en orden de prioridad.
        Si un rango se termina, automáticamente pasa al siguiente.
        
        Args:
            tipo (str): 'diferido' o 'comun'
            
        Returns:
            int: Número de cheque a usar
            
        Raises:
            ValueError: Si no hay rangos disponibles
        """
        # Obtener rangos activos ordenados por prioridad
        query = """
            SELECT * FROM rangos_cheques 
            WHERE tipo = ? AND activo = 1 
            ORDER BY numero_orden ASC
        """
        rangos = DatabaseConfig.ejecutar_query(
            query,
            params=(tipo,),
            fetch_all=True
        )
        
        if not rangos:
            raise ValueError(f"No hay rangos disponibles para cheques {tipo}")
        
        # Buscar el primer rango con números disponibles
        for rango in rangos:
            proximo = rango['proximo_numero']
            final = rango['numero_final']
            
            if proximo is None:
                # Primera vez que se usa este rango
                proximo = rango['numero_inicial']
            
            if proximo <= final:
                # Hay números disponibles en este rango
                # Actualizar el próximo número
                query_update = """
                    UPDATE rangos_cheques 
                    SET proximo_numero = ? 
                    WHERE id = ?
                """
                DatabaseConfig.ejecutar_query(
                    query_update,
                    params=(proximo + 1, rango['id'])
                )
                
                return proximo
        
        # Si llegamos aquí, todos los rangos están agotados
        raise ValueError(f"Todos los rangos de cheques {tipo} están agotados")
    
    @staticmethod
    def asignar_numeros_a_planilla(planilla_id, items_cheques):
        """
        Asigna números de cheque a todos los items de una planilla.
        
        Solo se llama cuando se genera el Excel, no antes.
        
        Args:
            planilla_id (int): ID de la planilla
            items_cheques (list): Lista de items que son cheques
            
        Returns:
            dict: Mapeo de item_id -> numero_cheque
        """
        asignaciones = {}
        
        for item in items_cheques:
            # Determinar tipo de cheque
            modalidad = item['modalidad_pago']
            tipo = 'diferido' if modalidad == 8 else 'comun'
            
            # Obtener próximo número
            numero = ChequeService.obtener_proximo_numero(tipo)
            
            # Crear registro de cheque
            Cheque.crear(
                numero_cheque=numero,
                tipo=tipo,
                planilla_id=planilla_id,
                beneficiario=item['beneficiario'],
                importe=item['importe'],
                fecha_emision=item['fecha_emision'],
                fecha_pago=item.get('fecha_pago_diferido')
            )
            
            asignaciones[item['id']] = numero
        
        return asignaciones