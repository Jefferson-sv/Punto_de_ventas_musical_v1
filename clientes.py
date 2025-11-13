from config import get_connection
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
import os

class Clientes(Frame):

    def __init__(self, padre):
        super().__init__(padre)
        self.widgets()
        self.cargar_registros()

    def rutas(self, ruta):
        try:
            rutabase = sys.__MEIPASS
        except Exception:
            rutabase = os.path.abspath(".")
        return os.path.join(rutabase, ruta)

    def widgets(self):
        self.frame = Frame(self, bg="#C6D9E3", highlightbackground="gray", highlightthickness=1)
        self.frame.place(x=0, y=0, width=1100, height=610)

        #========= LabelFrame con entradas ===================================================================================#
        self.labelframe = tk.LabelFrame(self.frame, text="Clientes", font="sans 22 bold", bg="#C6D9E3")
        self.labelframe.place(x=20, y=30, width=400, height=550)

        campos = ["Nombre", "Cédula", "Celular", "Dirección", "Correo"]
        self.entries = {}
        for i, campo in enumerate(campos):
            lbl = tk.Label(self.labelframe, text=f"{campo}:", font="sans 14 bold", bg="#C6D9E3")
            lbl.place(x=10, y=20 + i*60)
            ent = ttk.Entry(self.labelframe, font="sans 14 bold")
            ent.place(x=140, y=20 + i*60, width=240, height=40)
            self.entries[campo.lower()] = ent

        # Botones
        botones_info = [("Ingresar", self.registrar, "icono/ingresarc.png"),
                        ("Eliminar", self.eliminar, "icono/eliminar.png"),
                        ("Modificar", self.modificar, "icono/modificar.png")]

        for i, (text, cmd, icono) in enumerate(botones_info):
            ruta = self.rutas(icono)
            imagen_pil = Image.open(ruta).resize((50, 50))
            imagen_tk = ImageTk.PhotoImage(imagen_pil)
            btn = Button(self.labelframe, text=text, bg="#dddddd", fg="black", font="roboto 12 bold", command=cmd)
            btn.config(image=imagen_tk, compound="top", padx=10)
            btn.image = imagen_tk
            btn.place(x=50 + i*100, y=400, width=80, height=80)

        #========= Treeview ===================================================================================================#
        treFrame = Frame(self.frame, bg="white")
        treFrame.place(x=440, y=50, width=620, height=450)

        scrol_y = ttk.Scrollbar(treFrame)
        scrol_y.pack(side=RIGHT, fill=Y)
        scrol_x = ttk.Scrollbar(treFrame, orient=HORIZONTAL)
        scrol_x.pack(side=BOTTOM, fill=X)

        columnas = ("ID", "Nombre", "Cédula", "Celular", "Dirección", "Correo", "Estado")
        self.tre = ttk.Treeview(treFrame, yscrollcommand=scrol_y.set, xscrollcommand=scrol_x.set, height=40,
                                columns=columnas, show="headings")
        self.tre.pack(expand=True, fill=BOTH)
        scrol_y.config(command=self.tre.yview)
        scrol_x.config(command=self.tre.xview)

        for col in columnas:
            self.tre.heading(col, text=col)
            if col == "ID":
                self.tre.column(col, width=50, anchor="center")
            elif col in ["Nombre", "Cédula", "Celular", "Dirección", "Correo", "Estado"]:
                # Centrar todas las demás columnas
                width_map = {
                    "Nombre": 150,
                    "Cédula": 120,
                    "Celular": 120,
                    "Dirección": 200,
                    "Correo": 200,
                    "Estado": 100
                }
                self.tre.column(col, width=width_map[col], anchor="center")

    # ========================== CARGAR REGISTROS ========================== #
    def cargar_registros(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            # Seleccionamos columnas incluyendo el estado
            cursor.execute("SELECT ID, nombre, dui, celular, direccion, correo, estado FROM clientes")
            rows = cursor.fetchall()

            # Limpiamos Treeview
            for item in self.tre.get_children():
                self.tre.delete(item)

            # Insertamos filas
            for row in rows:
                id_cliente, nombre, dui, celular, direccion, correo, estado = row
                estado_texto = "Habilitado" if estado == 1 else "Deshabilitado"
                item_id = self.tre.insert("", "end",
                                          values=(id_cliente, nombre, dui, celular, direccion, correo, estado_texto))

                # Aplicar color rojo si está deshabilitado
                if estado == 0:
                    self.tre.item(item_id, tags=("deshabilitado",))

            self.tre.tag_configure("deshabilitado", foreground="red")
            conn.close()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar los registros: {e}")

    # ========================== REGISTRAR CLIENTE ========================== #
    def registrar(self):
        # Recopilar datos directamente
        nombre = self.entries["nombre"].get()
        cedula = self.entries["cédula"].get()
        celular = self.entries["celular"].get()
        direccion = self.entries["dirección"].get()
        correo = self.entries["correo"].get()

        try:
            conn = get_connection()
            cursor = conn.cursor()
            # Insertamos el estado habilitado por defecto (1)
            cursor.execute(
                "INSERT INTO clientes (nombre, dui, celular, direccion, correo, estado) VALUES (?, ?, ?, ?, ?, 1)",
                (nombre, cedula, celular, direccion, correo)
            )
            conn.commit()
            conn.close()

            messagebox.showinfo("Éxito", "Cliente registrado correctamente.")
            self.limpiar_campos()
            # Recargar registros en Treeview
            for item in self.tre.get_children():
                self.tre.delete(item)
            self.cargar_registros()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el cliente: {e}")

    # ========================== ELIMINAR CLIENTE ========================== #
    def eliminar(self):
        if not self.tre.selection():
            messagebox.showerror("Error", "Por favor seleccione un cliente para eliminar.")
            return
        pin = simpledialog.askstring("PIN de seguridad", "Ingrese el PIN de seguridad:", show='*')
        if pin != "2024":
            messagebox.showerror("Error", "PIN incorrecto.")
            return
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este cliente?"):
            item = self.tre.selection()[0]
            id_cliente = self.tre.item(item, "values")[0]
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM clientes WHERE ID=?", (id_cliente,))
                conn.commit()
                conn.close()
                self.tre.delete(item)
                messagebox.showinfo("Éxito", "Cliente eliminado correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el cliente: {e}")

    # ========================== MODIFICAR CLIENTE ========================== #
    def modificar(self):
        if not self.tre.selection():
            messagebox.showerror("Error", "Seleccione un cliente para modificar.")
            return

        item = self.tre.selection()[0]
        id_cliente = self.tre.item(item, "values")[0]  # Solo obtenemos el ID

        # Traer los datos reales desde la base de datos
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT nombre, dui, celular, direccion, correo, estado FROM clientes WHERE ID=?",
                           (id_cliente,))
            row = cursor.fetchone()
            conn.close()
            if not row:
                messagebox.showerror("Error", "No se encontró el cliente en la base de datos.")
                return
            nombre_actual, cedula_actual, celular_actual, direccion_actual, correo_actual, estado_actual = row
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo obtener los datos del cliente: {e}")
            return

        top_mod = Toplevel(self)
        top_mod.title("Modificar Cliente")
        top_mod.geometry("400x500")
        top_mod.config(bg="#C6D9E3")

        labels = ["Nombre", "Cédula", "Celular", "Dirección", "Correo"]
        actuales = [nombre_actual, cedula_actual, celular_actual, direccion_actual, correo_actual]
        entradas = []

        for i, (lab, val) in enumerate(zip(labels, actuales)):
            tk.Label(top_mod, text=f"{lab}:", font="sans 14 bold", bg="#C6D9E3").grid(row=i, column=0, padx=10, pady=5)
            entry = tk.Entry(top_mod, font="sans 14 bold")
            entry.insert(0, val)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entradas.append(entry)

        # ===================== Checkbutton Estado ===================== #
        estado_var = tk.BooleanVar(value=bool(estado_actual))
        chk = tk.Checkbutton(top_mod, text="Habilitado" if estado_var.get() else "Deshabilitado",
                             variable=estado_var,
                             font="sans 14 bold", bg="#C6D9E3",
                             command=lambda: chk.config(text="Habilitado" if estado_var.get() else "Deshabilitado"))
        chk.grid(row=5, column=1, pady=10)

        # ===================== Guardar cambios ===================== #
        def guardar_cambios():
            nuevos = [e.get() for e in entradas]

            if bool(estado_actual) != estado_var.get():
                pin = simpledialog.askstring("PIN de seguridad", "Ingrese PIN de administrador para cambiar estado:",
                                             show="*")
                if pin != "2024":
                    messagebox.showerror("Error", "PIN incorrecto. No se puede cambiar el estado.")
                    estado_var.set(bool(estado_actual))  # Revertir valor
                    return

            nuevo_estado = 1 if estado_var.get() else 0

            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE clientes SET nombre=?, dui=?, celular=?, direccion=?, correo=?, estado=? WHERE ID=?",
                    (*nuevos, nuevo_estado, id_cliente)
                )
                conn.commit()
                conn.close()
                self.cargar_registros()
                top_mod.destroy()
                messagebox.showinfo("Éxito", "Cliente modificado correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo modificar el cliente: {e}")

        # Botón Guardar
        ruta = self.rutas(r"icono/guardar.png")
        imagen_pil = Image.open(ruta).resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_pil)
        btn_guardar = Button(top_mod, text="Guardar cambios", bg="#dddddd", font="sans 14 bold",
                             command=guardar_cambios)
        btn_guardar.config(image=imagen_tk, compound=LEFT, padx=10)
        btn_guardar.image = imagen_tk
        btn_guardar.place(x=80, y=350, width=240, height=40)

    def limpiar_campos(self):
        for ent in self.entries.values():
            ent.delete(0, END)
