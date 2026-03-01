"""
============================================================================
UI - PESTAÑA AGENDA CHEQUES (CORREGIDA)
============================================================================
"""

import customtkinter as ctk
from tkinter import messagebox
from models.agenda import ContactoCheque, buscar_contactos_cheque
from utils.validators import validar_cuit, formatear_cuit


class TabAgendaCheques(ctk.CTkFrame):
    """Pestaña de gestión de agenda de cheques"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        # Configurar grid para responsive
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.crear_interfaz()
        self.cargar_contactos()
    
    def crear_interfaz(self):
        """Crea todos los elementos de la interfaz"""
        
        # ====================================================================
        # SECCIÓN 1: NUEVO CONTACTO
        # ====================================================================
        
        frame_nueva = ctk.CTkFrame(self)
        frame_nueva.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        
        # Título
        label_titulo = ctk.CTkLabel(
            frame_nueva,
            text="👥 Nuevo Contacto",
            font=("Arial", 18, "bold")
        )
        label_titulo.pack(pady=10)
        
        # Frame del formulario
        form_frame = ctk.CTkFrame(frame_nueva)
        form_frame.pack(fill="x", padx=20, pady=10)

        # Campo: Nombre
        ctk.CTkLabel(
            form_frame,
            text="Nombre:",
            font=("Arial", 12)
        ).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.entry_nombre = ctk.CTkEntry(
            form_frame,
            width=300,
            placeholder_text="Ej: Axel Ravinale"
        )
        self.entry_nombre.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky="w")

        # Campo: CUIT
        ctk.CTkLabel(
            form_frame,
            text="CUIT:",
            font=("Arial", 12)
        ).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        
        self.entry_cuit = ctk.CTkEntry(
            form_frame,
            width=200,
            placeholder_text="20-12345678-9"
        )
        self.entry_cuit.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        
        btn_validar_cuit = ctk.CTkButton(
            form_frame,
            text="Validar",
            width=100,
            command=self.validar_cuit
        )
        btn_validar_cuit.grid(row=1, column=2, padx=10, pady=10)
        
        self.label_cuit_valido = ctk.CTkLabel(
            form_frame,
            text="",
            font=("Arial", 12)
        )
        self.label_cuit_valido.grid(row=1, column=3, padx=10, pady=10)
        
        # Campo: Notas
        ctk.CTkLabel(
            form_frame,
            text="Notas:",
            font=("Arial", 12)
        ).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        
        self.entry_notas = ctk.CTkEntry(
            form_frame,
            width=400,
            placeholder_text="Opcional - Ej: Empleado"
        )
        self.entry_notas.grid(row=2, column=1, columnspan=3, padx=10, pady=10, sticky="w")  
        
        # Botón Crear
        self.btn_crear = ctk.CTkButton(
            frame_nueva,
            text="✅ Agregar Contacto",
            font=("Arial", 14, "bold"),
            height=40,
            command=self.agregar_contacto
        )
        self.btn_crear.pack(pady=15)
        
        # ====================================================================
        # SECCIÓN 2: CONTACTOS EXISTENTES
        # ====================================================================

        frame_lista = ctk.CTkFrame(self)
        frame_lista.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        frame_lista.grid_columnconfigure(0, weight=1)
        frame_lista.grid_rowconfigure(1, weight=1)

        # Título
        label_titulo_lista = ctk.CTkLabel(
            frame_lista,
            text="📚 Contactos Existentes",
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
            placeholder_text="Buscar por nombre, CUIT o notas..."
        )
        self.entry_busqueda.pack(side="left", padx=5)
        self.entry_busqueda.bind('<KeyRelease>', lambda e: self.buscar_contactos())
        
        btn_buscar = ctk.CTkButton(
            frame_busqueda,
            text="Buscar",
            width=100,
            command=self.buscar_contactos
        )
        btn_buscar.pack(side="left", padx=5)
        
        btn_limpiar = ctk.CTkButton(
            frame_busqueda,
            text="Limpiar",
            width=100,
            command=self.limpiar_busqueda
        )
        btn_limpiar.pack(side="left", padx=5)

        # ScrollableFrame
        frame_scroll = ctk.CTkScrollableFrame(
            frame_lista,
            label_text=""
        )
        frame_scroll.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        frame_scroll.grid_columnconfigure(0, weight=1)
        
        self.frame_items = frame_scroll
    
    def validar_cuit(self):
        """Valida el CUIT ingresado y muestra el resultado"""
        cuit = self.entry_cuit.get().strip()
        
        if not cuit:
            self.label_cuit_valido.configure(
                text="⚠️ Ingresa un CUIT",
                text_color="orange"
            )
            return
        
        valido, mensaje = validar_cuit(cuit)
        
        if valido:
            self.label_cuit_valido.configure(
                text="✅ CUIT válido",
                text_color="green"
            )
        else:
            self.label_cuit_valido.configure(
                text=f"❌ {mensaje}",
                text_color="red"
            )
    
    def agregar_contacto(self):
        """Agrega un nuevo contacto a la base de datos"""
        nombre = self.entry_nombre.get().strip()
        cuit = self.entry_cuit.get().strip()
        notas = self.entry_notas.get().strip()

        # Validar nombre
        if not nombre:
            messagebox.showwarning(
                "Campo Requerido",
                "Por favor ingresa un nombre."
            )
            self.entry_nombre.focus()
            return

        # Validar CUIT
        if not cuit:
            messagebox.showwarning(
                "Campo Requerido",
                "Por favor ingresa un CUIT."
            )
            self.entry_cuit.focus()
            return
        
        # Validar formato y dígito verificador
        valido, mensaje = validar_cuit(cuit)
        if not valido:
            messagebox.showerror(
                "CUIT Inválido",
                mensaje
            )
            self.entry_cuit.focus()
            return
        
        try:
            # Crear contacto
            contacto = ContactoCheque.crear(nombre, cuit, notas)

            # Mensaje de éxito
            messagebox.showinfo(
                "✅ Contacto Creado",
                f"Contacto '{nombre}' creado exitosamente!"
            )

            # Limpiar formulario
            self.limpiar_formulario()
            
            # Recargar la lista
            self.cargar_contactos()

        except ValueError as e:
            # ✅ MEJORA: Detectar si el contacto existe pero está inactivo
            error_msg = str(e)
            
            if "Ya existe un contacto" in error_msg and "CUIT" in error_msg:
                # ✅ CORRECCIÓN: obtener_por_cuit retorna UN objeto o None, NO una lista
                contacto_existente = ContactoCheque.obtener_por_cuit(cuit)
                
                if contacto_existente and not contacto_existente.activo:
                    # Preguntar si quiere reactivarlo
                    respuesta = messagebox.askyesno(
                        "Contacto Inactivo",
                        f"Ya existe un contacto con el CUIT {formatear_cuit(cuit)}, pero está INACTIVO.\n\n"
                        f"Nombre: {contacto_existente.nombre}\n"
                        f"Notas: {contacto_existente.notas or 'Sin notas'}\n\n"
                        "¿Querés reactivar este contacto?"
                    )
                    
                    if respuesta:
                        # Reactivar y actualizar datos
                        contacto_existente.nombre = nombre
                        contacto_existente.notas = notas
                        contacto_existente.activo = True
                        contacto_existente.actualizar()
                        
                        messagebox.showinfo(
                            "✅ Contacto Reactivado",
                            f"Contacto '{nombre}' reactivado exitosamente!"
                        )
                        
                        self.limpiar_formulario()
                        self.cargar_contactos()
                    return
            
            # Si no es el caso anterior, mostrar el error normal
            messagebox.showerror(
                "Error de Validación",
                error_msg
            )
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error al crear contacto: {e}"
            )

    def limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        self.entry_nombre.delete(0, "end")
        self.entry_cuit.delete(0, "end")
        self.entry_notas.delete(0, "end")
        self.label_cuit_valido.configure(text="")
        self.entry_nombre.focus()
    
    def cargar_contactos(self):
        """Carga todos los contactos de la base de datos"""
        # Limpiar items existentes
        for widget in self.frame_items.winfo_children():
            widget.destroy()
        
        try:
            # ✅ CAMBIO: solo_activos=False para mostrar TODOS
            contactos = ContactoCheque.obtener_todos(solo_activos=False)

            if not contactos:
                label_vacio = ctk.CTkLabel(
                    self.frame_items,
                    text="No hay contactos creados aún.\nCrea tu primer contacto arriba. 👆",
                    font=("Arial", 14),
                    text_color="gray"
                )
                label_vacio.pack(pady=50)
                return
            
            # ✅ CORRECCIÓN: self.crear_item_contacto (no self-self)
            for idx, contacto in enumerate(contactos):
                self.crear_item_contacto(contacto, idx)
            
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error al cargar contactos: {e}"
            )
    
    def crear_item_contacto(self, contacto, index):
        """Crea un widget que muestra un contacto individual"""
        # Color alternado
        color = ("gray90", "gray20") if index % 2 == 0 else ("gray95", "gray25")
        
        item_frame = ctk.CTkFrame(
            self.frame_items,
            fg_color=color
        )
        item_frame.pack(fill="x", pady=2, padx=5)
        item_frame.grid_columnconfigure(1, weight=1)

        # ✅ CORRECCIÓN: Calcular rowspan ANTES de crear los widgets
        tiene_notas = bool(contacto.notas)
        rowspan_value = 3 if tiene_notas else 2

        # Indicador de estado (activo/inactivo)
        estado_symbol = "✅" if contacto.activo else "❌"
        label_estado = ctk.CTkLabel(
            item_frame,
            text=estado_symbol,
            font=("Arial", 20)
        )
        # ✅ Usar el rowspan correcto desde el principio
        label_estado.grid(row=0, column=0, padx=10, pady=10, rowspan=rowspan_value)

        # Nombre
        label_nombre = ctk.CTkLabel(
            item_frame,
            text=contacto.nombre,
            font=("Arial", 16, "bold"),
            anchor="w"
        )
        label_nombre.grid(row=0, column=1, sticky="w", padx=10, pady=(10, 0))

        # CUIT formateado
        cuit_formateado = formatear_cuit(contacto.cuit)
        label_cuit = ctk.CTkLabel(
            item_frame,
            text=f"CUIT: {cuit_formateado}",
            font=("Arial", 11),
            text_color="gray",
            anchor="w"
        )
        label_cuit.grid(row=1, column=1, sticky="w", padx=10, pady=(0, 5))

        # Notas (si existen)
        if tiene_notas:
            label_notas = ctk.CTkLabel(
                item_frame,
                text=f"Notas: {contacto.notas}",
                font=("Arial", 10),
                text_color="gray60",
                anchor="w"
            )
            label_notas.grid(row=2, column=1, sticky="w", padx=10, pady=(0, 10))

        # Botones de acción
        btn_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        btn_frame.grid(row=0, column=2, rowspan=rowspan_value, padx=10)

        # Botón activar/desactivar
        if contacto.activo:
            btn_toggle = ctk.CTkButton(
                btn_frame,
                text="Desactivar",
                width=100,
                fg_color="orange",
                hover_color="darkorange",
                command=lambda c=contacto: self.desactivar_contacto(c)
            )
        else:
            btn_toggle = ctk.CTkButton(
                btn_frame,
                text="Activar",
                width=100,
                fg_color="green",
                hover_color="darkgreen",
                command=lambda c=contacto: self.activar_contacto(c)
            )
        btn_toggle.pack(side="left", padx=5)

    def desactivar_contacto(self, contacto):
        """Desactiva un contacto"""
        respuesta = messagebox.askyesno(
            "Confirmar Desactivación",
            f"¿Estás seguro de desactivar el contacto '{contacto.nombre}'?\n\n"
            "Nota: No podrás usar este contacto en nuevos cheques."
        )

        if respuesta:
            try:
                # ✅ CORRECCIÓN: No usar .desactivar() sino actualizar directamente
                contacto.activo = False
                contacto.actualizar()
                
                messagebox.showinfo(
                    "✅ Desactivado",
                    f"Contacto '{contacto.nombre}' desactivado."
                )
                self.cargar_contactos()
            except Exception as e:
                messagebox.showerror(
                    "Error",
                    f"Error al desactivar: {e}"
                )
    
    def activar_contacto(self, contacto):
        """Activa un contacto"""
        try:
            # ✅ CORRECCIÓN: No usar .activar() sino actualizar directamente
            contacto.activo = True
            contacto.actualizar()
            
            messagebox.showinfo(
                "✅ Activado",
                f"Contacto '{contacto.nombre}' activado."
            )
            self.cargar_contactos()
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error al activar: {e}"
            )
    
    def buscar_contactos(self):
        """Busca contactos por término"""
        termino = self.entry_busqueda.get().strip()
        
        if not termino:
            self.cargar_contactos()
            return
        
        # Limpiar items existentes
        for widget in self.frame_items.winfo_children():
            widget.destroy()
        
        try:
            # ✅ CORRECCIÓN: buscar_contactos_cheque() del modelo (no self.buscar_contactos)
            resultados = buscar_contactos_cheque(termino)
            
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
            for idx, contacto in enumerate(resultados):
                self.crear_item_contacto(contacto, idx)
        
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error al buscar: {e}"
            )
    
    def limpiar_busqueda(self):
        """Limpia la búsqueda y recarga todos los contactos"""
        self.entry_busqueda.delete(0, "end")
        self.cargar_contactos()