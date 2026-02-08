-- ============================================================================
-- ESQUEMA DE BASE DE DATOS - Sistema de Gestión de Pagos Bancarios
-- ============================================================================
-- Este archivo define todas las tablas necesarias para el sistema
-- SQLite creará automáticamente esta estructura cuando iniciemos la app

-- ============================================================================
-- TABLA: referencias
-- Propósito: Almacenar códigos de referencia para las planillas
-- Formato: 5 letras + 7 números (Ej: LABSEM0118)
-- ============================================================================
CREATE TABLE IF NOT EXISTS referencias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- ID único auto-generado
    codigo TEXT UNIQUE NOT NULL,           -- Código de referencia (único!)
    descripcion TEXT,                      -- Descripción opcional
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,  -- Cuándo se creó
    activa BOOLEAN DEFAULT 1               -- 1 = activa, 0 = inactiva
);

-- Índice para búsquedas rápidas por código
CREATE INDEX IF NOT EXISTS idx_referencias_codigo ON referencias(codigo);


-- ============================================================================
-- TABLA: rangos_cheques
-- Propósito: Gestionar rangos de numeración de cheques (4 rangos por tipo)
-- ============================================================================
CREATE TABLE IF NOT EXISTS rangos_cheques (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT NOT NULL,                    -- 'diferido' o 'comun'
    numero_orden INTEGER NOT NULL,         -- 1, 2, 3 o 4 (prioridad de uso)
    numero_inicial INTEGER NOT NULL,       -- Primer número del rango
    numero_final INTEGER NOT NULL,         -- Último número del rango
    cantidad_total INTEGER NOT NULL,       -- Total de cheques en el rango
    proximo_numero INTEGER,                -- Próximo número a asignar
    activo BOOLEAN DEFAULT 1,              -- Si está disponible para usar
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    -- Restricción: cada tipo puede tener solo un rango con cada número de orden
    UNIQUE(tipo, numero_orden)
);

-- Índices para búsquedas rápidas
CREATE INDEX IF NOT EXISTS idx_rangos_tipo ON rangos_cheques(tipo);
CREATE INDEX IF NOT EXISTS idx_rangos_activo ON rangos_cheques(activo);


-- ============================================================================
-- TABLA: cheques_emitidos
-- Propósito: Registro de todos los cheques emitidos con su estado
-- ============================================================================
CREATE TABLE IF NOT EXISTS cheques_emitidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_cheque INTEGER NOT NULL,        -- Número del cheque
    tipo TEXT NOT NULL,                    -- 'diferido' o 'comun'
    
    -- Estados posibles:
    -- 'emitido_pendiente': Cheque asignado pero aún no confirmado
    -- 'emitido_correcto': Usuario confirmó que se emitió correctamente
    -- 'cargado_sistema': Ya fue cargado en el sistema bancario
    -- 'sin_usar': Falló y quedó disponible (pero NO se reutiliza automáticamente)
    estado TEXT DEFAULT 'emitido_pendiente',
    
    referencia_id INTEGER,                 -- A qué referencia pertenece
    planilla_id INTEGER,                   -- En qué planilla se emitió
    beneficiario TEXT,                     -- Nombre del beneficiario
    importe DECIMAL(12,2),                 -- Monto del cheque
    fecha_emision DATE,                    -- Fecha de emisión
    fecha_pago DATE,                       -- Fecha de pago (si es diferido)
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    -- Relaciones con otras tablas
    FOREIGN KEY (referencia_id) REFERENCES referencias(id),
    FOREIGN KEY (planilla_id) REFERENCES planillas(id),
    
    -- Restricción: un número de cheque + tipo debe ser único
    UNIQUE(numero_cheque, tipo)
);

-- Índices para búsquedas rápidas
CREATE INDEX IF NOT EXISTS idx_cheques_numero ON cheques_emitidos(numero_cheque);
CREATE INDEX IF NOT EXISTS idx_cheques_estado ON cheques_emitidos(estado);
CREATE INDEX IF NOT EXISTS idx_cheques_planilla ON cheques_emitidos(planilla_id);


-- ============================================================================
-- TABLA: agenda_cheques
-- Propósito: Contactos para pagos con cheque (nombre + CUIT)
-- ============================================================================
CREATE TABLE IF NOT EXISTS agenda_cheques (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,                  -- Nombre del beneficiario
    cuit TEXT NOT NULL UNIQUE,             -- CUIT (debe ser único)
    notas TEXT,                            -- Notas adicionales opcionales
    activo BOOLEAN DEFAULT 1,              -- 1 = activo, 0 = inactivo
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Índice para búsquedas por nombre o CUIT
CREATE INDEX IF NOT EXISTS idx_agenda_cheques_cuit ON agenda_cheques(cuit);
CREATE INDEX IF NOT EXISTS idx_agenda_cheques_nombre ON agenda_cheques(nombre);


-- ============================================================================
-- TABLA: agenda_transferencias
-- Propósito: Contactos para transferencias (nombre + CUIT + CBU)
-- ============================================================================
CREATE TABLE IF NOT EXISTS agenda_transferencias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,                  -- Nombre del beneficiario
    cuit TEXT NOT NULL,                    -- CUIT
    cbu TEXT NOT NULL,                     -- CBU (22 dígitos)
    notas TEXT,                            -- Notas adicionales opcionales
    activo BOOLEAN DEFAULT 1,              -- 1 = activo, 0 = inactivo
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    -- Restricción: la combinación CUIT + CBU debe ser única
    UNIQUE(cuit, cbu)
);

-- Índices para búsquedas rápidas
CREATE INDEX IF NOT EXISTS idx_agenda_trans_cuit ON agenda_transferencias(cuit);
CREATE INDEX IF NOT EXISTS idx_agenda_trans_nombre ON agenda_transferencias(nombre);


-- ============================================================================
-- TABLA: planillas
-- Propósito: Registro de planillas generadas
-- ============================================================================
CREATE TABLE IF NOT EXISTS planillas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    referencia_id INTEGER NOT NULL,        -- Qué referencia usa
    numero_planilla INTEGER,               -- Número correlativo de la planilla
    sucursal TEXT,                         -- Sucursal bancaria
    cuenta_debito TEXT,                    -- Cuenta de débito
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    archivo_excel TEXT,                    -- Ruta del archivo Excel generado
    
    -- Estados posibles:
    -- 'borrador': Planilla en construcción
    -- 'generada': Excel generado pero no descargado
    -- 'descargada': Usuario descargó el archivo
    estado TEXT DEFAULT 'borrador',
    
    -- Relación con referencias
    FOREIGN KEY (referencia_id) REFERENCES referencias(id)
);

-- Índices para búsquedas
CREATE INDEX IF NOT EXISTS idx_planillas_referencia ON planillas(referencia_id);
CREATE INDEX IF NOT EXISTS idx_planillas_fecha ON planillas(fecha_creacion);


-- ============================================================================
-- TABLA: items_planilla
-- Propósito: Items individuales dentro de cada planilla (los pagos)
-- ============================================================================
CREATE TABLE IF NOT EXISTS items_planilla (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    planilla_id INTEGER NOT NULL,          -- A qué planilla pertenece
    tipo_documento TEXT,                   -- 'CUIT' o 'CUIL'
    numero_documento TEXT,                 -- Número de documento
    identificacion_pago TEXT,              -- Identificación del pago
    beneficiario TEXT,                     -- Nombre del beneficiario
    importe DECIMAL(12,2),                 -- Monto a pagar
    cuenta_pago TEXT,                      -- CBU o número de cheque
    
    -- Modalidad de pago:
    -- 2 = TRANSFERENCIA BANCO MACRO
    -- 4 = TRANSFERENCIA OTROS BANCOS
    -- 6 = ECHEQ COMÚN
    -- 8 = ECHEQ DIFERIDO
    modalidad_pago INTEGER,
    
    marca_registracion TEXT,               -- Marca de registración del cheque
    fecha_emision DATE,                    -- Fecha de emisión
    fecha_pago_diferido DATE,              -- Fecha de pago (si es diferido)
    cheque_id INTEGER,                     -- Si es cheque, referencia al cheque
    
    -- Relaciones
    FOREIGN KEY (planilla_id) REFERENCES planillas(id) ON DELETE CASCADE,
    FOREIGN KEY (cheque_id) REFERENCES cheques_emitidos(id)
);

-- Índices para búsquedas
CREATE INDEX IF NOT EXISTS idx_items_planilla ON items_planilla(planilla_id);


-- ============================================================================
-- TABLA: configuracion
-- Propósito: Guardar configuraciones generales del sistema
-- ============================================================================
CREATE TABLE IF NOT EXISTS configuracion (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    clave TEXT UNIQUE NOT NULL,            -- Nombre de la configuración
    valor TEXT NOT NULL,                   -- Valor de la configuración
    descripcion TEXT,                      -- Descripción de para qué sirve
    fecha_modificacion DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Insertar configuraciones por defecto
INSERT OR IGNORE INTO configuracion (clave, valor, descripcion) VALUES
    ('sucursal_default', '', 'Sucursal bancaria por defecto'),
    ('cuenta_debito_default', '', 'Cuenta de débito por defecto'),
    ('proximo_numero_planilla', '1', 'Próximo número de planilla a asignar'),
    ('version_db', '1.0', 'Versión del esquema de base de datos');


-- ============================================================================
-- VISTAS ÚTILES (Consultas pre-armadas para facilitar el trabajo)
-- ============================================================================

-- Vista: Resumen de rangos de cheques con disponibilidad
CREATE VIEW IF NOT EXISTS v_rangos_disponibles AS
SELECT 
    r.id,
    r.tipo,
    r.numero_orden,
    r.numero_inicial,
    r.numero_final,
    r.cantidad_total,
    r.proximo_numero,
    r.activo,
    -- Calcular cuántos se usaron
    COALESCE(r.proximo_numero - r.numero_inicial, 0) as usados,
    -- Calcular cuántos quedan disponibles
    COALESCE(r.numero_final - r.proximo_numero + 1, r.cantidad_total) as disponibles
FROM rangos_cheques r
WHERE r.activo = 1
ORDER BY r.tipo, r.numero_orden;


-- Vista: Planillas con información completa
CREATE VIEW IF NOT EXISTS v_planillas_completas AS
SELECT 
    p.id,
    p.numero_planilla,
    r.codigo as referencia,
    r.descripcion as referencia_desc,
    p.sucursal,
    p.cuenta_debito,
    p.estado,
    p.fecha_creacion,
    -- Contar items en la planilla
    COUNT(i.id) as cantidad_items,
    -- Sumar total de importes
    COALESCE(SUM(i.importe), 0) as total_importe
FROM planillas p
JOIN referencias r ON p.referencia_id = r.id
LEFT JOIN items_planilla i ON p.id = i.planilla_id
GROUP BY p.id;


-- ============================================================================
-- TRIGGERS (Acciones automáticas)
-- ============================================================================

-- Trigger: Actualizar fecha de modificación en configuracion
CREATE TRIGGER IF NOT EXISTS trg_config_fecha_mod
AFTER UPDATE ON configuracion
BEGIN
    UPDATE configuracion 
    SET fecha_modificacion = CURRENT_TIMESTAMP 
    WHERE id = NEW.id;
END;


-- ============================================================================
-- FIN DEL ESQUEMA
-- ============================================================================