"""
Ventana principal con pestañas
"""
import customtkinter as ctk

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configuración de la ventana
        self.title("Sistema de Gestión de Pagos Bancarios")
        self.geometry("1200x700")
        
        # Configurar tema (dark/light)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Crear el TabView (pestañas)
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Agregar las 6 pestañas
        self.tab_carga = self.tabview.add("📝 Carga")
        self.tab_rangos = self.tabview.add("🔢 Rangos")
        self.tab_referencias = self.tabview.add("📋 Referencias")
        self.tab_agenda_cheques = self.tabview.add("👥 Agenda Cheques")
        self.tab_agenda_trans = self.tabview.add("💳 Agenda Transfer.")
        self.tab_planillas = self.tabview.add("📄 Planillas")
        
        # Inicializar cada pestaña
        self.setup_tab_carga()
        self.setup_tab_rangos()
        self.setup_tab_referencias()
        # ... etc
    
    def setup_tab_carga(self):
        """Configura la pestaña de carga de información"""
        # Frame principal
        frame = ctk.CTkFrame(self.tab_carga)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título
        titulo = ctk.CTkLabel(
            frame, 
            text="Nueva Planilla", 
            font=("Arial", 20, "bold")
        )
        titulo.pack(pady=10)
        
        # Frame para referencia
        frame_ref = ctk.CTkFrame(frame)
        frame_ref.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(frame_ref, text="Referencia:").pack(side="left", padx=5)
        
        # ComboBox para seleccionar referencia
        self.combo_referencia = ctk.CTkComboBox(
            frame_ref,
            values=self.cargar_referencias(),
            width=200
        )
        self.combo_referencia.pack(side="left", padx=5)
        
        # Botón para nueva referencia
        btn_nueva_ref = ctk.CTkButton(
            frame_ref,
            text="+ Nueva",
            width=100,
            command=self.crear_nueva_referencia
        )
        btn_nueva_ref.pack(side="left", padx=5)
        
        # ... más elementos de la interfaz
    
    def cargar_referencias(self):
        """Carga las referencias desde la base de datos"""
        from models.referencia import Referencia
        referencias = Referencia.obtener_todas()
        return [ref.codigo for ref in referencias]
    
    def crear_nueva_referencia(self):
        """Abre diálogo para crear nueva referencia"""
        # Aquí abrirías una ventana modal con un formulario
        pass