"""
============================================================================
MAIN - SISTEMA DE GESTIÓN DE PAGOS BANCARIOS
============================================================================
Versión actualizada con la pestaña Referencias funcionando.
============================================================================
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def verificar_dependencias():
    """Verifica que todas las dependencias estén instaladas"""
    dependencias = {
        'customtkinter': 'CustomTkinter',
        'openpyxl': 'OpenPyXL',
        'pandas': 'Pandas',
        'PIL': 'Pillow'
    }
    
    faltantes = []
    for modulo, nombre in dependencias.items():
        try:
            __import__(modulo)
        except ImportError:
            faltantes.append(nombre)
    
    if faltantes:
        print("❌ ERROR: Faltan dependencias:")
        for dep in faltantes:
            print(f"   • {dep}")
        print("\n💡 Ejecuta: pip install -r requirements.txt")
        return False
    
    return True


def inicializar_sistema():
    """Inicializa la base de datos"""
    try:
        from config.database import DatabaseConfig
        print("✅ Base de datos lista")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def crear_ventana_principal():
    """Crea la ventana principal con todas las pestañas"""
    import customtkinter as ctk
    from ui.tab_referencias import TabReferencias
    from ui.tab_agenda_cheques import TabAgendaCheques
    from ui.tab_agenda_transferencias import TabAgendaTransferencias

    
    class VentanaPrincipal(ctk.CTk):
        def __init__(self):
            super().__init__()
            
            # Configuración
            self.title("Sistema de Gestión de Pagos Bancarios v1.0")
            self.geometry("1400x800")
            
            # Tema
            ctk.set_appearance_mode("dark")
            ctk.set_default_color_theme("blue")
            
            # Crear interfaz
            self.crear_interfaz()
        
        def crear_interfaz(self):
            """Crea la interfaz con pestañas"""
            
            # Frame principal
            main_frame = ctk.CTkFrame(self)
            main_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Título
            titulo = ctk.CTkLabel(
                main_frame,
                text="💼 Sistema de Gestión de Pagos Bancarios",
                font=("Arial", 28, "bold")
            )
            titulo.pack(pady=15)
            
            # TabView
            self.tabview = ctk.CTkTabview(main_frame)
            self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Pestaña 1: Referencias (FUNCIONANDO) ✅
            self.tab_referencias = self.tabview.add("📋 Referencias")
            referencias_ui = TabReferencias(self.tab_referencias)
            referencias_ui.pack(fill="both", expand=True)
            
            # Pestaña 2: Rangos (Temporal)
            self.tab_rangos = self.tabview.add("🔢 Rangos")
            self.crear_tab_temporal(self.tab_rangos, "Rangos de Cheques")
            
            # Pestaña 3: Agenda Cheques (Temporal)
            self.tab_agenda_ch = self.tabview.add("👥 Agenda Cheques")
            agenda_ch_ui = TabAgendaCheques(self.tab_agenda_ch)
            agenda_ch_ui.pack(fill="both", expand=True)
            
            # Pestaña 4: Agenda Transferencias (Temporal)
            self.tab_agenda_tr = self.tabview.add("💳 Agenda Transfer.")
            agenda_tr_ui = TabAgendaTransferencias(self.tab_agenda_tr)
            agenda_tr_ui.pack(fill="both", expand=True)
            
            # Pestaña 5: Carga (Temporal)
            self.tab_carga = self.tabview.add("📝 Carga")
            self.crear_tab_temporal(self.tab_carga, "Carga de Planillas")
            
            # Pestaña 6: Planillas (Temporal)
            self.tab_planillas = self.tabview.add("📄 Planillas")
            self.crear_tab_temporal(self.tab_planillas, "Historial de Planillas")
            
            # Barra de estado
            self.status_bar = ctk.CTkLabel(
                self,
                text="✅ Sistema listo | Referencias: Funcionando | Otras pestañas: En desarrollo",
                fg_color=("gray80", "gray20")
            )
            self.status_bar.pack(side="bottom", fill="x", pady=2)
        
        def crear_tab_temporal(self, tab, nombre):
            """Crea una pestaña temporal (placeholder)"""
            frame = ctk.CTkFrame(tab)
            frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            label = ctk.CTkLabel(
                frame,
                text=f"🚧 {nombre}",
                font=("Arial", 24, "bold")
            )
            label.pack(pady=40)
            
            info = ctk.CTkLabel(
                frame,
                text=f"La pestaña {nombre} estará disponible próximamente.\n\n"
                     "✅ Pestaña Referencias ya está funcionando!\n"
                     "Podés crear y gestionar referencias allí.",
                font=("Arial", 14),
                justify="center"
            )
            info.pack(pady=20)
    
    # Crear y mostrar la ventana
    app = VentanaPrincipal()
    app.mainloop()


def main():
    """Función principal"""
    print("=" * 70)
    print("  SISTEMA DE GESTIÓN DE PAGOS BANCARIOS v1.0")
    print("=" * 70)
    print()
    
    # Verificar dependencias
    if not verificar_dependencias():
        input("\nPresiona Enter para salir...")
        return
    
    print("✅ Dependencias OK")
    
    # Inicializar sistema
    if not inicializar_sistema():
        input("\nPresiona Enter para salir...")
        return
    
    print()
    print("🎨 Lanzando interfaz gráfica...")
    print()
    crear_ventana_principal()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Programa interrumpido")
    except Exception as e:
        print(f"\n❌ Error fatal: {e}")
        import traceback
        traceback.print_exc()
        input("\nPresiona Enter para salir...")