"""
============================================================================
UI - PESTAÑA REFERENCIAS
============================================================================
Interfaz gráfica para gestionar referencias de planillas.

Esta pestaña permite:
- Crear nuevas referencias con auto-incremento
- Ver listado de referencias existentes
- Buscar referencias
- Activar/Desactivar referencias
============================================================================
"""

import customtkinter as ctk
from tkinter import messagebox
from models.referencia import Referencia, buscar_referencias


class TabReferencias(ctk.CTkFrame):
    """
    Pestaña de gestión de referencias.
    
    Esta clase hereda de CTkFrame y se inserta en el TabView principal.
    """
    
    def __init__(self, parent):
        """
        Constructor de la pestaña.
        
        Args:
            parent: El widget padre (normalmente el tab del TabView)
        """
        super().__init__(parent)
        
        # Configurar el grid para que sea responsive
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Crear la interfaz
        self.crear_interfaz()
        
        # Cargar datos iniciales
        self.cargar_referencias()
    
    def crear_interfaz(self):
        """Crea todos los elementos de la interfaz"""
        
        # ====================================================================
        # SECCIÓN 1: NUEVA REFERENCIA
        # ====================================================================
        
        frame_nueva = ctk.CTkFrame(self)
        frame_nueva.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        
        # Título
        label_titulo = ctk.CTkLabel(
            frame_nueva,
            text="📋 Nueva Referencia",
            font=("Arial", 18, "bold")
        )
        label_titulo.pack(pady=10)
        
        # Frame para el formulario
        form_frame = ctk.CTkFrame(frame_nueva)
        form_frame.pack(fill="x", padx=20, pady=10)
        
        # Campo: Prefijo (5 letras)
        ctk.CTkLabel(
            form_frame,
            text="Prefijo (5 letras):",
            font=("Arial", 12)
        ).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.entry_prefijo = ctk.CTkEntry(
            form_frame,
            width=150,
            placeholder_text="Ej: LABSEM"
        )
        self.entry_prefijo.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        # Bind para actualizar vista previa
        self.entry_prefijo.bind('<KeyRelease>', self.actualizar_vista_previa)
        
        # Botón para generar automático
        btn_generar = ctk.CTkButton(
            form_frame,
            text="📝 Generar Automático",
            width=150,
            command=self.generar_codigo_automatico
        )
        btn_generar.grid(row=0, column=2, padx=10, pady=10)
        
        # Vista previa del código completo
        ctk.CTkLabel(
            form_frame,
            text="Código completo:",
            font=("Arial", 12)
        ).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        
        self.label_vista_previa = ctk.CTkLabel(
            form_frame,
            text="_____0000000",
            font=("Arial", 14, "bold"),
            text_color="gray"
        )
        self.label_vista_previa.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        
        # Campo: Descripción
        ctk.CTkLabel(
            form_frame,
            text="Descripción:",
            font=("Arial", 12)
        ).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        
        self.entry_descripcion = ctk.CTkEntry(
            form_frame,
            width=400,
            placeholder_text="Descripción opcional de la referencia"
        )
        self.entry_descripcion.grid(row=2, column=1, columnspan=2, padx=10, pady=10, sticky="w")
        
        # Botón crear
        self.btn_crear = ctk.CTkButton(
            frame_nueva,
            text="✅ Crear Referencia",
            font=("Arial", 14, "bold"),
            height=40,
            command=self.crear_referencia
        )
        self.btn_crear.pack(pady=15)
        
        # ====================================================================
        # SECCIÓN 2: REFERENCIAS EXISTENTES
        # ====================================================================
        
        frame_lista = ctk.CTkFrame(self)
        frame_lista.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        frame_lista.grid_columnconfigure(0, weight=1)
        frame_lista.grid_rowconfigure(1, weight=1)
        
        # Título
        label_titulo_lista = ctk.CTkLabel(
            frame_lista,
            text="📚 Referencias Existentes",
            font=("Arial", 18, "bold")
        )
        label_titulo_lista.grid(row=0, column=0, pady=10, sticky="w", padx=20)
        
        # Barra de búsqueda
        frame_busqueda = ctk.CTkFrame(frame_lista)
        frame_busqueda.grid(row=0, column=0, sticky="e", padx=20, pady=10)
        
        ctk.CTkLabel(
            frame_busqueda,
            text="🔍",
            font=("Arial", 16)
        ).pack(side="left", padx=5)
        
        self.entry_busqueda = ctk.CTkEntry(
            frame_busqueda,
            width=250,
            placeholder_text="Buscar por código o descripción..."
        )
        self.entry_busqueda.pack(side="left", padx=5)
        self.entry_busqueda.bind('<KeyRelease>', lambda e: self.buscar_referencias())
        
        btn_buscar = ctk.CTkButton(
            frame_busqueda,
            text="Buscar",
            width=100,
            command=self.buscar_referencias
        )
        btn_buscar.pack(side="left", padx=5)
        
        btn_limpiar = ctk.CTkButton(
            frame_busqueda,
            text="Limpiar",
            width=100,
            command=self.limpiar_busqueda
        )
        btn_limpiar.pack(side="left", padx=5)
        
        # Frame con scrollbar para la tabla
        frame_scroll = ctk.CTkScrollableFrame(
            frame_lista,
            label_text=""
        )
        frame_scroll.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        frame_scroll.grid_columnconfigure(0, weight=1)
        
        # Aquí se agregarán las referencias dinámicamente
        self.frame_items = frame_scroll
    
    def actualizar_vista_previa(self, event=None):
        """
        Actualiza la vista previa del código completo.
        
        Se ejecuta cada vez que el usuario escribe en el campo prefijo.
        """
        prefijo = self.entry_prefijo.get().upper().strip()
        
        if len(prefijo) == 0:
            self.label_vista_previa.configure(text="_____0000000", text_color="gray")
            return
        
        if len(prefijo) > 5:
            prefijo = prefijo[:5]
            self.entry_prefijo.delete(5, "end")
        
        # Generar el código completo
        try:
            codigo_completo = Referencia.generar_siguiente_codigo(prefijo)
            self.label_vista_previa.configure(
                text=codigo_completo,
                text_color="green"
            )
        except Exception:
            self.label_vista_previa.configure(
                text=f"{prefijo}_______",
                text_color="orange"
            )
    
    def generar_codigo_automatico(self):
        """
        Genera automáticamente el siguiente número correlativo.
        
        Se llama cuando el usuario hace clic en "Generar Automático".
        """
        prefijo = self.entry_prefijo.get().upper().strip()
        
        if not prefijo:
            messagebox.showwarning(
                "Prefijo Requerido",
                "Por favor ingresa un prefijo de 5 letras primero."
            )
            return
        
        if len(prefijo) != 5:
            messagebox.showwarning(
                "Prefijo Inválido",
                "El prefijo debe tener exactamente 5 letras."
            )
            return
        
        if not prefijo.isalpha():
            messagebox.showwarning(
                "Prefijo Inválido",
                "El prefijo debe contener solo letras."
            )
            return
        
        try:
            codigo_completo = Referencia.generar_siguiente_codigo(prefijo)
            self.label_vista_previa.configure(
                text=codigo_completo,
                text_color="green"
            )
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error al generar código: {e}"
            )
    
    def crear_referencia(self):
        """
        Crea una nueva referencia en la base de datos.
        
        Valida los datos y muestra mensajes de éxito/error.
        """
        # Obtener datos del formulario
        prefijo = self.entry_prefijo.get().upper().strip()
        descripcion = self.entry_descripcion.get().strip()
        
        # Validaciones
        if not prefijo:
            messagebox.showwarning(
                "Campo Requerido",
                "Por favor ingresa un prefijo."
            )
            self.entry_prefijo.focus()
            return
        
        if len(prefijo) != 5:
            messagebox.showwarning(
                "Prefijo Inválido",
                "El prefijo debe tener exactamente 5 letras."
            )
            self.entry_prefijo.focus()
            return
        
        if not prefijo.isalpha():
            messagebox.showwarning(
                "Prefijo Inválido",
                "El prefijo debe contener solo letras."
            )
            self.entry_prefijo.focus()
            return
        
        try:
            # Generar código completo
            codigo_completo = Referencia.generar_siguiente_codigo(prefijo)
            
            # Crear la referencia
            referencia = Referencia.crear(codigo_completo, descripcion)
            
            # Mensaje de éxito
            messagebox.showinfo(
                "✅ Referencia Creada",
                f"Referencia '{codigo_completo}' creada exitosamente!"
            )
            
            # Limpiar formulario
            self.limpiar_formulario()
            
            # Recargar la lista
            self.cargar_referencias()
            
        except ValueError as e:
            messagebox.showerror(
                "Error de Validación",
                str(e)
            )
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error al crear referencia: {e}"
            )
    
    def limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        self.entry_prefijo.delete(0, "end")
        self.entry_descripcion.delete(0, "end")
        self.label_vista_previa.configure(text="_____0000000", text_color="gray")
        self.entry_prefijo.focus()
    
    def cargar_referencias(self):
        """
        Carga todas las referencias de la base de datos y las muestra.
        
        Se llama al iniciar y después de crear/editar una referencia.
        """
        # Limpiar items existentes
        for widget in self.frame_items.winfo_children():
            widget.destroy()
        
        try:
            # Obtener referencias
            referencias = Referencia.obtener_todas(solo_activas=False)
            
            if not referencias:
                # Mostrar mensaje si no hay referencias
                label_vacio = ctk.CTkLabel(
                    self.frame_items,
                    text="No hay referencias creadas aún.\nCrea tu primera referencia arriba. 👆",
                    font=("Arial", 14),
                    text_color="gray"
                )
                label_vacio.pack(pady=50)
                return
            
            # Crear un item por cada referencia
            for idx, ref in enumerate(referencias):
                self.crear_item_referencia(ref, idx)
        
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error al cargar referencias: {e}"
            )
    
    def crear_item_referencia(self, referencia, index):
        """
        Crea un widget que muestra una referencia individual.
        
        Args:
            referencia (Referencia): Objeto referencia
            index (int): Índice en la lista (para alternar colores)
        """
        # Frame para el item
        color = ("gray90", "gray20") if index % 2 == 0 else ("gray95", "gray25")
        
        item_frame = ctk.CTkFrame(
            self.frame_items,
            fg_color=color
        )
        item_frame.pack(fill="x", pady=2, padx=5)
        item_frame.grid_columnconfigure(1, weight=1)
        
        # Indicador de estado (activa/inactiva)
        estado_symbol = "✅" if referencia.activa else "❌"
        label_estado = ctk.CTkLabel(
            item_frame,
            text=estado_symbol,
            font=("Arial", 20)
        )
        label_estado.grid(row=0, column=0, padx=10, pady=10, rowspan=2)
        
        # Código de la referencia
        label_codigo = ctk.CTkLabel(
            item_frame,
            text=referencia.codigo,
            font=("Arial", 16, "bold"),
            anchor="w"
        )
        label_codigo.grid(row=0, column=1, sticky="w", padx=10, pady=(10, 0))
        
        # Descripción
        descripcion_texto = referencia.descripcion if referencia.descripcion else "Sin descripción"
        label_descripcion = ctk.CTkLabel(
            item_frame,
            text=descripcion_texto,
            font=("Arial", 11),
            text_color="gray",
            anchor="w"
        )
        label_descripcion.grid(row=1, column=1, sticky="w", padx=10, pady=(0, 10))
        
        # Botones de acción
        btn_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        btn_frame.grid(row=0, column=2, rowspan=2, padx=10)
        
        # Botón activar/desactivar
        if referencia.activa:
            btn_toggle = ctk.CTkButton(
                btn_frame,
                text="Desactivar",
                width=100,
                fg_color="orange",
                hover_color="darkorange",
                command=lambda r=referencia: self.desactivar_referencia(r)
            )
        else:
            btn_toggle = ctk.CTkButton(
                btn_frame,
                text="Activar",
                width=100,
                fg_color="green",
                hover_color="darkgreen",
                command=lambda r=referencia: self.activar_referencia(r)
            )
        btn_toggle.pack(side="left", padx=5)
    
    def desactivar_referencia(self, referencia):
        """
        Desactiva una referencia.
        
        Args:
            referencia (Referencia): Referencia a desactivar
        """
        respuesta = messagebox.askyesno(
            "Confirmar Desactivación",
            f"¿Estás seguro de desactivar la referencia '{referencia.codigo}'?\n\n"
            "Nota: No podrás crear nuevas planillas con esta referencia."
        )
        
        if respuesta:
            try:
                referencia.desactivar()
                messagebox.showinfo(
                    "✅ Desactivada",
                    f"Referencia '{referencia.codigo}' desactivada."
                )
                self.cargar_referencias()
            except Exception as e:
                messagebox.showerror(
                    "Error",
                    f"Error al desactivar: {e}"
                )
    
    def activar_referencia(self, referencia):
        """
        Activa una referencia.
        
        Args:
            referencia (Referencia): Referencia a activar
        """
        try:
            referencia.activar()
            messagebox.showinfo(
                "✅ Activada",
                f"Referencia '{referencia.codigo}' activada."
            )
            self.cargar_referencias()
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error al activar: {e}"
            )
    
    def buscar_referencias(self):
        """Busca referencias por término"""
        termino = self.entry_busqueda.get().strip()
        
        if not termino:
            self.cargar_referencias()
            return
        
        # Limpiar items existentes
        for widget in self.frame_items.winfo_children():
            widget.destroy()
        
        try:
            resultados = buscar_referencias(termino)
            
            if not resultados:
                label_vacio = ctk.CTkLabel(
                    self.frame_items,
                    text=f"No se encontraron resultados para '{termino}'",
                    font=("Arial", 14),
                    text_color="gray"
                )
                label_vacio.pack(pady=50)
                return
            
            # Mostrar resultados
            for idx, ref in enumerate(resultados):
                self.crear_item_referencia(ref, idx)
        
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error al buscar: {e}"
            )
    
    def limpiar_busqueda(self):
        """Limpia la búsqueda y recarga todas las referencias"""
        self.entry_busqueda.delete(0, "end")
        self.cargar_referencias()