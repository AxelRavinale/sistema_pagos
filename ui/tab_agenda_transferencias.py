"""
============================================================================
UI - PESTAÑA AGENDA TRANSFERENCIAS (PLANTILLA PARA COMPLETAR)
============================================================================
EJERCICIO: Completar esta interfaz.

Diferencias con Agenda Cheques:
- Tiene campo adicional: CBU
- Necesita validar tanto CUIT como CBU
- Muestra CBU en la lista de contactos

Es casi idéntica a tab_agenda_cheques.py, solo con un campo extra.
============================================================================
"""

import customtkinter as ctk
from tkinter import messagebox
from models.agenda import ContactoTransferencia, buscar_contactos_transferencia
from utils.validators import validar_cuit, validar_cbu, formatear_cuit, formatear_cbu


class TabAgendaTransferencias(ctk.CTkFrame):
    """Pestaña de gestión de agenda de transferencias"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        # TODO: Configurar grid
        
        self.crear_interfaz()
        self.cargar_contactos()
    
    def crear_interfaz(self):
        """Crea todos los elementos de la interfaz"""
        
        # ====================================================================
        # SECCIÓN 1: NUEVO CONTACTO
        # ====================================================================
        
        # TODO: Frame para nuevo contacto
        
        # TODO: Título "💳 Nuevo Contacto"
        
        # TODO: Frame del formulario
        
        # --- Campo: Nombre ---
        # TODO: Label y Entry (self.entry_nombre)
        
        # --- Campo: CUIT ---
        # TODO: Label y Entry (self.entry_cuit)
        # TODO: Botón "Validar CUIT" → self.validar_cuit()
        # TODO: Label resultado (self.label_cuit_valido)
        
        # --- Campo: CBU (NUEVO!) ---
        # TODO: Label "CBU:"
        # TODO: Entry para CBU (self.entry_cbu)
        # TODO: Botón "Validar CBU" → self.validar_cbu()
        # TODO: Label resultado (self.label_cbu_valido)
        
        # --- Campo: Notas ---
        # TODO: Label y Entry (self.entry_notas)
        
        # TODO: Botón "✅ Agregar Contacto" → self.agregar_contacto()
        
        pass
        
        # ====================================================================
        # SECCIÓN 2: CONTACTOS EXISTENTES
        # ====================================================================
        
        # TODO: Frame para lista
        # TODO: Título "📚 Contactos Existentes"
        # TODO: Barra de búsqueda
        # TODO: ScrollableFrame para items (self.frame_items)
        
        pass
    
    def validar_cuit(self):
        """
        Valida el CUIT ingresado.
        
        TODO: Implementar - Idéntico a tab_agenda_cheques.py
        """
        # TU CÓDIGO AQUÍ
        pass
    
    def validar_cbu(self):
        """
        Valida el CBU ingresado.
        
        TODO: Implementar - Similar a validar_cuit() pero con validar_cbu()
        
        Pasos:
        1. Obtener CBU del entry
        2. Llamar a validar_cbu()
        3. Actualizar self.label_cbu_valido con resultado
        """
        # TU CÓDIGO AQUÍ
        # Pista: cbu = self.entry_cbu.get().strip()
        # Pista: valido, mensaje = validar_cbu(cbu)
        # Pista: if valido:
        #            self.label_cbu_valido.configure(text="✅ Válido", text_color="green")
        #        else:
        #            self.label_cbu_valido.configure(text=f"❌ {mensaje}", text_color="red")
        """Valida el CBU ingresado"""
        cbu = self.entry_cbu.get().strip()
        
        if not cbu:
            self.label_cbu_valido.configure(
                text="⚠️ Ingresa un CBU",
                text_color="orange"
            )
            return
        
        valido, mensaje = validar_cbu(cbu)  # ← Solo cambia la función
        
        if valido:
            self.label_cbu_valido.configure(
                text="✅ CBU válido",
                text_color="green"
            )
        else:
            self.label_cbu_valido.configure(
                text=f"❌ {mensaje}",
                text_color="red"
            )
    
    def agregar_contacto(self):
        """
        Agrega un nuevo contacto.
        
        TODO: Implementar
        
        Diferencia con Cheques: También pasa el CBU a crear()
        """
        # TU CÓDIGO AQUÍ
        # Pista: nombre = self.entry_nombre.get().strip()
        # Pista: cuit = self.entry_cuit.get().strip()
        # Pista: cbu = self.entry_cbu.get().strip()  ← NUEVO
        # Pista: notas = self.entry_notas.get().strip()
        
        # Validaciones
        # Pista: if not nombre:
        #            messagebox.showwarning(...)
        #            return
        
        # Validar CUIT
        # Pista: valido_cuit, msg_cuit = validar_cuit(cuit)
        # Pista: if not valido_cuit:
        #            messagebox.showerror("CUIT Inválido", msg_cuit)
        #            return
        
        # Validar CBU (NUEVO!)
        # Pista: valido_cbu, msg_cbu = validar_cbu(cbu)
        # Pista: if not valido_cbu:
        #            messagebox.showerror("CBU Inválido", msg_cbu)
        #            return
        
        # Crear contacto
        # Pista: try:
        #            contacto = ContactoTransferencia.crear(nombre, cuit, cbu, notas)
        #            messagebox.showinfo("✅", f"Contacto '{nombre}' creado")
        #            self.limpiar_formulario()
        #            self.cargar_contactos()
        #        except Exception as e:
        #            messagebox.showerror("Error", str(e))
        pass
    
    def limpiar_formulario(self):
        """
        Limpia el formulario.
        
        TODO: Implementar - Similar a Cheques pero incluye entry_cbu
        """
        # TU CÓDIGO AQUÍ
        # Pista: self.entry_nombre.delete(0, "end")
        # Pista: self.entry_cuit.delete(0, "end")
        # Pista: self.entry_cbu.delete(0, "end")  ← NUEVO
        # Pista: self.entry_notas.delete(0, "end")
        # Pista: self.label_cuit_valido.configure(text="")
        # Pista: self.label_cbu_valido.configure(text="")  ← NUEVO
        pass
    
    def cargar_contactos(self):
        """
        Carga todos los contactos.
        
        TODO: Implementar - Casi idéntico a Cheques
        """
        # TU CÓDIGO AQUÍ
        # Pista: for widget in self.frame_items.winfo_children():
        #            widget.destroy()
        # Pista: contactos = ContactoTransferencia.obtener_todos()
        # Pista: if not contactos:
        #            # Mostrar mensaje "No hay contactos"
        # Pista: for idx, contacto in enumerate(contactos):
        #            self.crear_item_contacto(contacto, idx)
        pass
    
    def crear_item_contacto(self, contacto, index):
        """
        Crea un widget para un contacto.
        
        TODO: Implementar
        
        Diferencia con Cheques: También muestra el CBU
        
        Layout sugerido:
        ┌───────────────────────────────────────┐
        │ ✅  Nombre del Contacto    [Botones] │
        │     CUIT: 20-12345678-9              │
        │     CBU: 0170 0995 2 0000003912345 6 │
        └───────────────────────────────────────┘
        """
        # TU CÓDIGO AQUÍ
        # Pista: Similar a tab_agenda_cheques pero con 3 filas
        
        # item_frame = ctk.CTkFrame(...)
        
        # Row 0: Estado y Nombre
        # label_estado.grid(row=0, column=0, rowspan=3, ...)
        # label_nombre.grid(row=0, column=1, ...)
        
        # Row 1: CUIT
        # label_cuit.grid(row=1, column=1, ...)
        
        # Row 2: CBU (NUEVO!)
        # label_cbu.grid(row=2, column=1, ...)
        
        # Botones en column=2, rowspan=3
        pass
    
    def desactivar_contacto(self, contacto):
        """TODO: Implementar - Idéntico a Cheques"""
        # TU CÓDIGO AQUÍ
        pass
    
    def activar_contacto(self, contacto):
        """TODO: Implementar - Idéntico a Cheques"""
        # TU CÓDIGO AQUÍ
        pass
    
    def buscar_contactos(self):
        """TODO: Implementar - Casi idéntico a Cheques"""
        # TU CÓDIGO AQUÍ
        # Pista: termino = self.entry_busqueda.get().strip()
        # Pista: resultados = buscar_contactos_transferencia(termino)
        pass
    
    def limpiar_busqueda(self):
        """TODO: Implementar"""
        # TU CÓDIGO AQUÍ
        pass


# ============================================================================
# PISTAS ESPECÍFICAS PARA TRANSFERENCIAS
# ============================================================================

"""
DIFERENCIAS CLAVE CON AGENDA CHEQUES:

1. CAMPO ADICIONAL - CBU:
   - Agregar Entry para CBU
   - Agregar botón "Validar CBU"
   - Agregar Label para resultado de validación
   
2. VALIDACIÓN DOBLE:
   def agregar_contacto(self):
       # Validar CUIT
       valido_cuit, msg = validar_cuit(cuit)
       if not valido_cuit:
           return
       
       # Validar CBU (NUEVO!)
       valido_cbu, msg = validar_cbu(cbu)
       if not valido_cbu:
           return
       
       # Crear con ambos
       ContactoTransferencia.crear(nombre, cuit, cbu, notas)

3. MOSTRAR CBU EN LA LISTA:
   - En crear_item_contacto(), agregar una fila más
   - Usar formatear_cbu() para mostrarlo bonito
   
   label_cbu = ctk.CTkLabel(
       item_frame,
       text=f"CBU: {formatear_cbu(contacto.cbu)}",
       font=("Arial", 10),
       text_color="gray"
   )
   label_cbu.grid(row=2, column=1, sticky="w", padx=10)

4. LAYOUT DEL ITEM:
   ┌──────────────────────────────────────┐
   │ [✅] Nombre Grande         [Botones] │
   │      CUIT: 20-12345678-9            │
   │      CBU: 0170 0995...              │
   └──────────────────────────────────────┘
   
   Usa rowspan=3 para el estado y los botones

TIPS:

- Copiá tab_agenda_cheques.py completo
- Agregá el campo CBU en el formulario
- Agregá validación de CBU
- En crear_item_contacto(), agregá la tercera fila para CBU
- ¡Listo!

El 90% del código es idéntico a Agenda Cheques.
"""