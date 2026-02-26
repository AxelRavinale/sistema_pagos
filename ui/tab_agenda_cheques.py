"""
============================================================================
UI - PESTAÑA AGENDA CHEQUES (PLANTILLA PARA COMPLETAR)
============================================================================
EJERCICIO: Completar esta interfaz siguiendo el ejemplo de tab_referencias.py

Funcionalidades a implementar:
- Formulario para agregar contactos (nombre + CUIT)
- Validar CUIT antes de guardar
- Listar todos los contactos
- Buscar contactos
- Desactivar contactos
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
        
        # TODO: Configurar grid para responsive
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Pista: Mira como lo hace tab_referencias.py
        
        self.crear_interfaz()
        self.cargar_contactos()
    
    def crear_interfaz(self):
        """Crea todos los elementos de la interfaz"""
        
        # ====================================================================
        # SECCIÓN 1: NUEVO CONTACTO
        # ====================================================================
        
        # TODO: Crear frame para nuevo contacto
        frame_nueva = ctk.CTkFrame(self)
        frame_nueva.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        # Pista: frame_nueva = ctk.CTkFrame(self)
        # Pista: frame_nueva.grid(row=0, column=0, ...)
        
        # TODO: Agregar título "👥 Nuevo Contacto"
        label_titulo = ctk.CTkLabel(
            frame_nueva,
            text="👥 Nuevo Contacto",
            font=("Arial", 18, "bold")
        )
        label_titulo.pack(pady=10)
        # TODO: Crear frame para el formulario
        form_frame = ctk.CTkFrame(frame_nueva)
        form_frame.pack(fill="x", padx=20, pady=10)

        # --- Campo: Nombre ---
        # TODO: Label "Nombre:"
        ctk.CTkLabel(
            form_frame,
            text="Nombre:",
            font=("Arial", 12)
        ).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        # TODO: Entry para nombre (self.entry_nombre)
        # Pista: self.entry_nombre = ctk.CTkEntry(form_frame, width=300)
        self.entry_nombre = ctk.CTkEntry(
            form_frame,
            width=150,
            placeholder_text="Ej: Axel Ravinale"
        )
        self.entry_nombre.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # --- Campo: CUIT ---
        # TODO: Label "CUIT:"
        ctk.CTkLabel(
            form_frame,
            text="CUIT:",
            font=("Arial", 12)
        ).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        
        # Entry para el CUIT
        self.entry_cuit = ctk.CTkEntry(
            form_frame,
            width=200,
            placeholder_text="20-12345678-9"
        )
        self.entry_cuit.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        
        # Botón para validar (llama al método validar_cuit)
        btn_validar_cuit = ctk.CTkButton(
            form_frame,
            text="Validar",
            width=100,
            command=self.validar_cuit  # ← Acá lo llamás
        )
        btn_validar_cuit.grid(row=1, column=2, padx=10, pady=10)
        
        # Label para mostrar el resultado
        self.label_cuit_valido = ctk.CTkLabel(
            form_frame,
            text="",  # Vacío al principio
            font=("Arial", 12)
        )
        self.label_cuit_valido.grid(row=1, column=3, padx=10, pady=10)
        # --- Campo: Notas (opcional) ---
        # TODO: Label "Notas:"
        ctk.CTkLabel(
            form_frame,
            text="Notas:",
            font=("Arial", 12)
        ).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        # TODO: Entry para notas (self.entry_notas)
        self.entry_notas = ctk.CTkEntry(
            form_frame,
            width=150,
            placeholder_text="Opcional Ej: Empleado"
        )
        self.entry_notas.grid(row=2, column=1, padx=10, pady=10, sticky="w")  
        # TODO: Botón "✅ Agregar Contacto" que llame a self.agregar_contacto()
        self.btn_crear = ctk.CTkButton(
            frame_nueva,
            text="✅ Crear contacto echeq",
            font=("Arial", 14, "bold"),
            height=40,
            command=self.agregar_contacto
        )
        self.btn_crear.pack(pady=15)
        
        
        # ====================================================================
        # SECCIÓN 2: CONTACTOS EXISTENTES
        # ====================================================================

        # TODO: Crear frame para lista de contactos
        # Pista: Similar a tab_referencias.py
        frame_lista = ctk.CTkFrame(self)
        frame_lista.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        frame_lista.grid_columnconfigure(0, weight=1)
        frame_lista.grid_rowconfigure(1, weight=1)


        # TODO: Agregar título "📚 Contactos Existentes"
        label_titulo_lista = ctk.CTkLabel(
            frame_lista,
            text="📚 Contactos Echeqs Existentes",
            font=("Arial", 18, "bold")
        )
        label_titulo_lista.grid(row=0, column=0, pady=10, sticky="w", padx=20)

        # TODO: Crear barra de búsqueda
        # Pista: self.entry_busqueda = ctk.CTkEntry(...)
        # Pista: self.entry_busqueda.bind('<KeyRelease>', lambda e: self.buscar_contactos())
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
            placeholder_text="Buscar por nombre, cuit o notas..."
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

        # TODO: Crear ScrollableFrame para los contactos
        # Pista: self.frame_items = ctk.CTkScrollableFrame(...)

        frame_scroll = ctk.CTkScrollableFrame(
            frame_lista,
            label_text=""
        )
        frame_scroll.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        frame_scroll.grid_columnconfigure(0, weight=1)
        
        # Aquí se agregarán las referencias dinámicamente
        self.frame_items = frame_scroll
        
    
    def validar_cuit(self):
        """
        Valida el CUIT ingresado y muestra el resultado.
        
        TODO: Implementar este método
        
        Pasos:
        1. Obtener el CUIT del entry
        2. Llamar a validar_cuit() de utils.validators
        3. Actualizar self.label_cuit_valido con ✅ o ❌
        4. Cambiar color del label (verde o rojo)
        """
        # TU CÓDIGO AQUÍ
        # Pista: cuit = self.entry_cuit.get()
        # Pista: valido, mensaje = validar_cuit(cuit)
        # Pista: if valido:
        #            self.label_cuit_valido.configure(text="✅ Válido", text_color="green")
        """
        Valida el CUIT ingresado y muestra el resultado en pantalla.
        
        Este método:
        1. Obtiene el CUIT del entry
        2. Llama a la función validar_cuit() de utils.validators
        3. Muestra ✅ verde si es válido, ❌ rojo si no
        """
        # 1. Obtener el texto del entry
        cuit = self.entry_cuit.get().strip()
        
        # 2. Verificar que no esté vacío
        if not cuit:
            self.label_cuit_valido.configure(
                text="⚠️ Ingresa un CUIT",
                text_color="orange"
            )
            return
        
        # 3. Llamar a la función validadora (de utils/validators.py)
        valido, mensaje = validar_cuit(cuit)
        
        # 4. Mostrar resultado
        if valido:
            # Es válido → Verde con ✅
            self.label_cuit_valido.configure(
                text="✅ CUIT válido",
                text_color="green"
            )
        else:
            # No es válido → Rojo con ❌ y el error
            self.label_cuit_valido.configure(
                text=f"❌ {mensaje}",
                text_color="red"
            )
    
    def agregar_contacto(self):
        """
        Agrega un nuevo contacto a la base de datos.
        
        TODO: Implementar este método
        
        Pasos:
        1. Obtener datos del formulario (nombre, cuit, notas)
        2. Validar que el nombre no esté vacío
        3. Validar el CUIT
        4. Llamar a ContactoCheque.crear()
        5. Mostrar mensaje de éxito
        6. Limpiar formulario
        7. Recargar la lista
        """
        # TU CÓDIGO AQUÍ
        # Pista: nombre = self.entry_nombre.get().strip()
        # Pista: if not nombre:
        #            messagebox.showwarning("Campo Requerido", "Ingresa un nombre")
        #            return
        # Pista: try:
        #            contacto = ContactoCheque.crear(nombre, cuit, notas)
        #            messagebox.showinfo("✅ Contacto Creado", ...)
        #        except Exception as e:
        #            messagebox.showerror("Error", str(e))
        nombre = self.entry_nombre.get().title().strip()
        cuit = self.entry_cuit.get().strip()
        notas = self.entry_notas.get().lower().strip()

        if not nombre:
            messagebox.showwarning(
                "Campo Requerido",
                "Por favor ingresa un nombre."
            )
            self.entry_nombre.focus()
            return

        if not cuit:
            messagebox.showwarning(
                "Campo Requerido",
                "Por favor ingresa un cuit."
            )
            self.entry_cuit.focus()
            return

        if len(cuit) != 13:
            messagebox.showwarning(
                "Cuit Inválido",
                "El prefijo debe tener exactamente 11 numeros y 2 guiones." \
                "xx-xxxxxxxx-x"
            )
            self.entry_cuit.focus()
            return
        
        try:
            #Crear contacto
            contacto_echeq = ContactoCheque.crear(nombre, cuit, notas)

            #Mensaje de exito
            messagebox.showinfo(
                "✅ Contacto echeq Creado",
                f"Contacto '{nombre}' creado exitosamente!"
            )

            # Limpiar formulario
            self.limpiar_formulario()
            
            # Recargar la lista
            self.cargar_contactos()

        except ValueError as e:
            messagebox.showerror(
                "Error de Validación",
                str(e)
            )
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error al crear contacto: {e}"
            )

    def limpiar_formulario(self):
        """
        Limpia todos los campos del formulario.
        
        TODO: Implementar este método
        """
        # TU CÓDIGO AQUÍ
        # Pista: self.entry_nombre.delete(0, "end")
        # Pista: self.entry_cuit.delete(0, "end")
        # Pista: self.entry_notas.delete(0, "end")
        # Pista: self.label_cuit_valido.configure(text="")
        pass
    
    def cargar_contactos(self):
        """
        Carga todos los contactos de la base de datos.
        
        TODO: Implementar este método
        
        Pasos:
        1. Limpiar widgets existentes en self.frame_items
        2. Obtener contactos con ContactoCheque.obtener_todos()
        3. Si no hay contactos, mostrar mensaje
        4. Si hay, crear un item por cada contacto con self.crear_item_contacto()
        """
        # TU CÓDIGO AQUÍ
        # Pista: for widget in self.frame_items.winfo_children():
        #            widget.destroy()
        # Pista: contactos = ContactoCheque.obtener_todos()
        # Pista: for idx, contacto in enumerate(contactos):
        #            self.crear_item_contacto(contacto, idx)
        pass
    
    def crear_item_contacto(self, contacto, index):
        """
        Crea un widget que muestra un contacto individual.
        
        TODO: Implementar este método
        
        El widget debe mostrar:
        - Icono de estado (✅ o ❌)
        - Nombre del contacto (grande, bold)
        - CUIT formateado (más chico, gris)
        - Botón "Desactivar" (si está activo)
        - Botón "Activar" (si está inactivo)
        
        Args:
            contacto (ContactoCheque): Objeto contacto
            index (int): Índice para colores alternados
        """
        # TU CÓDIGO AQUÍ
        # Pista: Mira self.crear_item_referencia() en tab_referencias.py
        # Pista: item_frame = ctk.CTkFrame(self.frame_items, fg_color=...)
        # Pista: label_nombre = ctk.CTkLabel(item_frame, text=contacto.nombre, ...)
        # Pista: label_cuit = ctk.CTkLabel(item_frame, text=formatear_cuit(contacto.cuit), ...)
        pass
    
    def desactivar_contacto(self, contacto):
        """
        Desactiva un contacto.
        
        TODO: Implementar este método
        """
        # TU CÓDIGO AQUÍ
        # Pista: Similar a desactivar_referencia() en tab_referencias.py
        # Pista: respuesta = messagebox.askyesno("Confirmar", ...)
        # Pista: if respuesta:
        #            contacto.desactivar()
        #            self.cargar_contactos()
        pass
    
    def activar_contacto(self, contacto):
        """
        Activa un contacto.
        
        TODO: Implementar este método
        """
        # TU CÓDIGO AQUÍ
        pass
    
    def buscar_contactos(self):
        """
        Busca contactos por término.
        
        TODO: Implementar este método
        """
        # TU CÓDIGO AQUÍ
        # Pista: termino = self.entry_busqueda.get().strip()
        # Pista: if not termino:
        #            self.cargar_contactos()
        #            return
        # Pista: resultados = buscar_contactos_cheque(termino)
        pass
    
    def limpiar_busqueda(self):
        """Limpia la búsqueda"""
        # TU CÓDIGO AQUÍ
        pass


# ============================================================================
# AYUDA Y PISTAS
# ============================================================================

"""
PISTAS GENERALES:

1. ESTRUCTURA:
   - Mira tab_referencias.py como guía
   - La estructura es MUY similar
   - Solo cambias: Referencias → Contactos, codigo → nombre/cuit

2. VALIDACIÓN DE CUIT:
   from utils.validators import validar_cuit, formatear_cuit
   valido, mensaje = validar_cuit(cuit_ingresado)
   if valido:
       # Mostrar ✅
   else:
       # Mostrar ❌ y mensaje

3. FORMATEO:
   cuit_formateado = formatear_cuit("20123456789")
   # Retorna: "20-12345678-9"

4. GRID LAYOUT:
   # Para 3 columnas:
   label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
   entry.grid(row=0, column=1, padx=10, pady=10)
   button.grid(row=0, column=2, padx=10, pady=10)

5. COLORES ALTERNADOS:
   color = ("gray90", "gray20") if index % 2 == 0 else ("gray95", "gray25")

6. MESSAGEBOX:
   from tkinter import messagebox
   messagebox.showinfo("Título", "Mensaje")
   messagebox.showwarning("Título", "Mensaje")
   messagebox.showerror("Título", "Mensaje")
   respuesta = messagebox.askyesno("Título", "¿Pregunta?")

ERRORES COMUNES A EVITAR:

❌ Olvidar llamar .strip() en los strings
❌ No validar que los campos no estén vacíos
❌ No actualizar la lista después de agregar/modificar
❌ No usar try-except al llamar métodos del modelo
❌ No limpiar el formulario después de crear
"""