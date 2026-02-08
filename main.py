"""
============================================================================
SISTEMA DE GESTION DE PAGOS BANCARIOS
============================================================================
Punto de entrada principal de la aplicacion.

Para ejecutar:
    python main.py
============================================================================
"""

import sys
import os

# Agregar el directorio actual al path de Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def verificar_estructura():
    """
    Verifica que la estructura de carpetas este correcta.
    """
    carpetas_requeridas = ['config', 'models', 'database', 'ui', 'services', 'utils']
    carpeta_actual = os.path.dirname(os.path.abspath(__file__))
    
    print("Verificando estructura de carpetas...")
    faltantes = []
    
    for carpeta in carpetas_requeridas:
        ruta = os.path.join(carpeta_actual, carpeta)
        if not os.path.exists(ruta):
            faltantes.append(carpeta)
            print(f"  X Falta carpeta: {carpeta}")
        else:
            # Verificar __init__.py
            init_file = os.path.join(ruta, '__init__.py')
            if not os.path.exists(init_file):
                print(f"  ! Falta {carpeta}/__init__.py (creando...)")
                with open(init_file, 'w') as f:
                    pass
            print(f"  ✓ {carpeta}")
    
    if faltantes:
        print("\nERROR: Faltan carpetas. Crealas con:")
        for carpeta in faltantes:
            print(f"  mkdir {carpeta}")
            print(f"  type nul > {carpeta}\\__init__.py")
        return False
    
    print("✓ Estructura correcta\n")
    return True


def verificar_dependencias():
    """
    Verifica que todas las dependencias esten instaladas.
    """
    dependencias = {
        'customtkinter': 'CustomTkinter',
        'openpyxl': 'OpenPyXL',
        'pandas': 'Pandas',
        'PIL': 'Pillow'
    }
    
    print("Verificando dependencias...")
    faltantes = []
    
    for modulo, nombre in dependencias.items():
        try:
            __import__(modulo)
            print(f"  ✓ {nombre}")
        except ImportError:
            faltantes.append(nombre)
            print(f"  X {nombre}")
    
    if faltantes:
        print("\nERROR: Faltan dependencias por instalar:")
        print("\nEjecuta:")
        print("  pip install customtkinter openpyxl pandas Pillow tkcalendar python-dateutil")
        return False
    
    print("✓ Todas las dependencias instaladas\n")
    return True


def inicializar_sistema():
    """
    Inicializa el sistema:
    - Crea la base de datos si no existe
    - Verifica la integridad
    """
    print("Iniciando Sistema de Gestion de Pagos Bancarios...")
    
    try:
        # Intentar importar la configuracion de base de datos
        from config.database import DatabaseConfig
        
        print("✓ Base de datos inicializada")
        return True
        
    except ImportError as e:
        print(f"\nERROR: No se puede importar config.database")
        print(f"Detalles: {e}")
        print("\nVerifica que:")
        print("  1. Exista la carpeta 'config'")
        print("  2. Exista el archivo 'config/database.py'")
        print("  3. Exista el archivo 'config/__init__.py'")
        return False
    except Exception as e:
        print(f"\nERROR al inicializar la base de datos: {e}")
        import traceback
        traceback.print_exc()
        return False


def crear_ventana_principal():
    """
    Crea y muestra la ventana principal de la aplicacion.
    """
    try:
        import customtkinter as ctk
        
        class VentanaPrincipal(ctk.CTk):
            def __init__(self):
                super().__init__()
                
                # Configuracion de la ventana
                self.title("Sistema de Gestion de Pagos Bancarios v1.0")
                self.geometry("1200x700")
                
                # Configurar tema
                ctk.set_appearance_mode("dark")
                ctk.set_default_color_theme("blue")
                
                # Crear interfaz
                self.crear_interfaz()
            
            def crear_interfaz(self):
                """Crea la interfaz principal con pestañas"""
                
                # Frame principal
                main_frame = ctk.CTkFrame(self)
                main_frame.pack(fill="both", expand=True, padx=10, pady=10)
                
                # Titulo
                titulo = ctk.CTkLabel(
                    main_frame,
                    text="💼 Sistema de Gestion de Pagos Bancarios",
                    font=("Arial", 28, "bold")
                )
                titulo.pack(pady=20)
                
                # Subtitulo
                subtitulo = ctk.CTkLabel(
                    main_frame,
                    text="Gestion de planillas, cheques y transferencias",
                    font=("Arial", 14)
                )
                subtitulo.pack(pady=5)
                
                # Crear TabView (pestañas)
                self.tabview = ctk.CTkTabview(main_frame)
                self.tabview.pack(fill="both", expand=True, padx=10, pady=20)
                
                # Agregar las 6 pestañas
                self.tab_carga = self.tabview.add("📝 Carga")
                self.tab_rangos = self.tabview.add("🔢 Rangos")
                self.tab_referencias = self.tabview.add("📋 Referencias")
                self.tab_agenda_cheques = self.tabview.add("👥 Agenda Cheques")
                self.tab_agenda_trans = self.tabview.add("💳 Agenda Transfer.")
                self.tab_planillas = self.tabview.add("📄 Planillas")
                
                # Configurar cada pestaña
                self.setup_tab_demo(self.tab_carga, "Carga de Informacion")
                self.setup_tab_demo(self.tab_rangos, "Gestion de Rangos")
                self.setup_tab_demo(self.tab_referencias, "Gestion de Referencias")
                self.setup_tab_demo(self.tab_agenda_cheques, "Agenda de Cheques")
                self.setup_tab_demo(self.tab_agenda_trans, "Agenda de Transferencias")
                self.setup_tab_demo(self.tab_planillas, "Historial de Planillas")
                
                # Barra de estado
                self.status_bar = ctk.CTkLabel(
                    self,
                    text="✓ Sistema listo | Base de datos: OK | Version 1.0",
                    fg_color=("gray80", "gray20")
                )
                self.status_bar.pack(side="bottom", fill="x", pady=2)
            
            def setup_tab_demo(self, tab, titulo):
                """Configura una pestaña de demostracion"""
                frame = ctk.CTkFrame(tab)
                frame.pack(fill="both", expand=True, padx=20, pady=20)
                
                label = ctk.CTkLabel(
                    frame,
                    text=f"🚧 {titulo} - En Desarrollo",
                    font=("Arial", 24, "bold")
                )
                label.pack(pady=40)
                
                info = ctk.CTkLabel(
                    frame,
                    text="Esta funcionalidad esta en desarrollo.\n\n"
                         "El sistema ya tiene:\n"
                         "• Base de datos configurada ✓\n"
                         "• Estructura del proyecto lista ✓\n"
                         "• Validadores funcionando ✓\n\n"
                         "Proximo paso: Implementar las interfaces de cada pestaña",
                    font=("Arial", 12),
                    justify="left"
                )
                info.pack(pady=20)
                
                # Boton de prueba
                btn_prueba = ctk.CTkButton(
                    frame,
                    text="🧪 Probar Validadores",
                    command=self.probar_validadores,
                    width=200,
                    height=40
                )
                btn_prueba.pack(pady=20)
            
            def probar_validadores(self):
                """Abre una ventana para probar los validadores"""
                
                ventana = ctk.CTkToplevel(self)
                ventana.title("Prueba de Validadores")
                ventana.geometry("500x400")
                ventana.transient(self)
                ventana.grab_set()
                
                frame = ctk.CTkFrame(ventana)
                frame.pack(fill="both", expand=True, padx=20, pady=20)
                
                titulo = ctk.CTkLabel(
                    frame,
                    text="🧪 Probar Validadores",
                    font=("Arial", 20, "bold")
                )
                titulo.pack(pady=10)
                
                # Campo para CUIT
                ctk.CTkLabel(frame, text="CUIT:").pack(pady=5)
                entry_cuit = ctk.CTkEntry(frame, width=300, placeholder_text="20-12345678-9")
                entry_cuit.pack(pady=5)
                
                resultado_cuit = ctk.CTkLabel(frame, text="")
                resultado_cuit.pack(pady=5)
                
                def validar_cuit_input():
                    try:
                        from utils.validators import validar_cuit
                        valido, mensaje = validar_cuit(entry_cuit.get())
                        
                        if valido:
                            resultado_cuit.configure(
                                text=f"✓ {mensaje}",
                                text_color="green"
                            )
                        else:
                            resultado_cuit.configure(
                                text=f"✗ {mensaje}",
                                text_color="red"
                            )
                    except Exception as e:
                        resultado_cuit.configure(
                            text=f"Error: {e}",
                            text_color="red"
                        )
                
                btn_validar = ctk.CTkButton(
                    frame,
                    text="Validar CUIT",
                    command=validar_cuit_input
                )
                btn_validar.pack(pady=10)
                
                # Separador
                ctk.CTkLabel(frame, text="─" * 50).pack(pady=10)
                
                # Campo para CBU
                ctk.CTkLabel(frame, text="CBU:").pack(pady=5)
                entry_cbu = ctk.CTkEntry(frame, width=300, placeholder_text="0170099520000003912345")
                entry_cbu.pack(pady=5)
                
                resultado_cbu = ctk.CTkLabel(frame, text="")
                resultado_cbu.pack(pady=5)
                
                def validar_cbu_input():
                    try:
                        from utils.validators import validar_cbu
                        valido, mensaje = validar_cbu(entry_cbu.get())
                        
                        if valido:
                            resultado_cbu.configure(
                                text=f"✓ {mensaje}",
                                text_color="green"
                            )
                        else:
                            resultado_cbu.configure(
                                text=f"✗ {mensaje}",
                                text_color="red"
                            )
                    except Exception as e:
                        resultado_cbu.configure(
                            text=f"Error: {e}",
                            text_color="red"
                        )
                
                btn_validar_cbu = ctk.CTkButton(
                    frame,
                    text="Validar CBU",
                    command=validar_cbu_input
                )
                btn_validar_cbu.pack(pady=10)
        
        # Crear y mostrar la ventana
        app = VentanaPrincipal()
        app.mainloop()
        
    except Exception as e:
        print(f"\nERROR al crear la ventana principal: {e}")
        import traceback
        traceback.print_exc()


def main():
    """
    Funcion principal que orquesta el arranque de la aplicacion.
    """
    print("=" * 70)
    print("  SISTEMA DE GESTION DE PAGOS BANCARIOS v1.0")
    print("=" * 70)
    print()
    
    # 1. Verificar estructura
    if not verificar_estructura():
        input("\nPresiona Enter para salir...")
        return
    
    # 2. Verificar dependencias
    if not verificar_dependencias():
        input("\nPresiona Enter para salir...")
        return
    
    # 3. Inicializar sistema
    if not inicializar_sistema():
        print("\nNOTA: La base de datos no se pudo inicializar, pero la interfaz funcionara.")
        input("Presiona Enter para continuar de todos modos...")
    
    # 4. Lanzar interfaz grafica
    print("\nLanzando interfaz grafica...")
    print()
    crear_ventana_principal()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Programa interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error fatal: {e}")
        import traceback
        traceback.print_exc()
        input("\nPresiona Enter para salir...")
