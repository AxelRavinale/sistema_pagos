Readme · MDCopiar💼 Sistema de Gestión de Pagos Bancarios
Sistema de escritorio para gestionar planillas de pagos bancarios, cheques y transferencias.
📋 Características

✅ Gestión de planillas de pagos (cheques y transferencias)
✅ Control de rangos de numeración de cheques
✅ Sistema de referencias único para cada planilla
✅ Agendas de contactos (cheques y transferencias)
✅ Validación automática de CUIT y CBU
✅ Generación de archivos Excel con formato bancario
✅ Interfaz gráfica moderna y atractiva
✅ Base de datos local (no requiere servidor)

🚀 Instalación
Requisitos Previos

Python 3.8 o superior
pip (gestor de paquetes de Python)

Pasos de Instalación

Crear la estructura de carpetas

cmdmkdir sistema_pagos
cd sistema_pagos
mkdir config models database ui services utils

Crear archivos init.py vacíos

cmdtype nul > config\__init__.py
type nul > models\__init__.py
type nul > database\__init__.py
type nul > ui\__init__.py
type nul > services\__init__.py
type nul > utils\__init__.py

Copiar todos los archivos descargados en sus respectivas carpetas
Instalar dependencias

cmdpip install -r requirements.txt

Ejecutar la aplicación

cmdpython main.py
📂 Estructura del Proyecto
sistema_pagos/
│
├── main.py                 # Archivo principal (ejecutar este)
├── requirements.txt        # Dependencias del proyecto
├── README.md              # Este archivo
│
├── config/
│   ├── __init__.py
│   └── database.py        # Configuración de base de datos
│
├── models/
│   ├── __init__.py
│   └── referencia.py     # Modelo de ejemplo completo
│
├── database/
│   ├── __init__.py
│   └── schema.sql        # Estructura de tablas
│
├── ui/
│   └── __init__.py       # Interfaces (por completar)
│
├── services/
│   └── __init__.py       # Servicios (por completar)
│
└── utils/
    ├── __init__.py
    └── validators.py     # Validadores (CUIT, CBU, etc.)
🎯 Funcionalidades por Pestaña
1️⃣ Carga de Información

Crear nuevas planillas de pago
Agregar múltiples pagos (cheques o transferencias)
Validación automática de datos

2️⃣ Rangos de Cheques

Configurar hasta 4 rangos por tipo
Control automático de numeración
Cambio manual de estados

3️⃣ Referencias

Crear códigos únicos (5 letras + 7 números)
Auto-incremento inteligente

4️⃣ Agenda de Cheques

Contactos con CUIT y nombre
Búsqueda rápida

5️⃣ Agenda de Transferencias

Contactos con CUIT, nombre y CBU
Validación de CBU

6️⃣ Planillas

Ver historial
Descargar Excel
Cargar planilla vieja para editar

🔐 Validaciones Implementadas
CUIT/CUIL

Formato: XX-XXXXXXXX-X
Verifica tipo y dígito verificador

CBU

22 dígitos
Valida ambos bloques

Referencia

5 letras mayúsculas + 7 números
Unicidad garantizada

🗄️ Base de Datos
SQLite local en: ~/.sistema_pagos/pagos.db
Tablas:

referencias
rangos_cheques
cheques_emitidos
agenda_cheques
agenda_transferencias
planillas
items_planilla
configuracion

🧪 Probar Validadores
cmdpython utils\validators.py
O desde la interfaz: Botón "🧪 Probar Validadores"
🛠️ Estado del Desarrollo
✅ Completado

 Estructura del proyecto
 Base de datos y esquema
 Validadores (CUIT, CBU, Referencias)
 Modelo de ejemplo (Referencia)
 Interfaz básica

🚧 Por Completar

 Resto de modelos
 Servicios de negocio
 Interfaces de cada pestaña
 Generación de Excel

📖 Documentación Adicional

PLAN_DEL_PROYECTO.md - Diseño completo
GUIA_CONTINUACION.md - Cómo continuar
LEEME_PRIMERO.md - Guía de inicio

🐛 Solución de Problemas
Error: "No module named 'customtkinter'"
cmdpip install -r requirements.txt
Error: Carpeta no encontrada
Verificá que estés en la carpeta correcta con cd
🎓 Aprendizaje
Este proyecto enseña:

Python orientado a objetos
Bases de datos SQLite
Interfaces gráficas CustomTkinter
Manejo de Excel
Validación de datos
Arquitectura MVC

📞 Soporte
Lee la documentación en los archivos .md incluidos.

¡Buena suerte con tu desarrollo! 🚀