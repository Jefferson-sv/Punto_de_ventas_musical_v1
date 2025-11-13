from config import get_connection
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
import os
import sys

class Proveedor(Frame):
    def __init__(self, padre):
        super().__init__(padre)
        self.widgets()
        self.crear_tabla()
        self.cargar_registros()

    def rutas(self, ruta):
        try:
            rutabase = sys._MEIPASS
        except Exception:
            rutabase = os.path.abspath(".")
        return os.path.join(rutabase, ruta)

    def widgets(self):
        self.frame = Frame(self, bg="#C6D9E3", highlightbackground="gray", highlightthickness=1)
        self.frame.place(x=0, y=0, width=1100, height=610)

        # LabelFrame con entradas
        self.labelframe = tk.LabelFrame(self.frame, text="Proveedores", font="sans 22 bold", bg="#C6D9E3")
        self.labelframe.place(x=20, y=30, width=400, height=550)

        campos = ["Nombre", "Identificación", "Celular", "Dirección", "Correo"]
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

        # Treeview
        treFrame = Frame(self.frame, bg="white")
        treFrame.place(x=440, y=50, width=620, height=450)

        scrol_y = ttk.Scrollbar(treFrame)
        scrol_y.pack(side=RIGHT, fill=Y)
        scrol_x = ttk.Scrollbar(treFrame, orient=HORIZONTAL)
        scrol_x.pack(side=BOTTOM, fill=X)

        columnas = ("ID", "Nombre", "Identificación", "Celular", "Dirección", "Correo", "Estado")
        self.tre = ttk.Treeview(treFrame, yscrollcommand=scrol_y.set, xscrollcommand=scrol_x.set, height=40,
                                columns=columnas, show="headings")
        self.tre.pack(expand=True, fill=BOTH)
        scrol_y.config(command=self.tre.yview)
        scrol_x.config(command=self.tre.xview)

        width_map = {
            "ID": 50, "Nombre": 150, "Identificación": 120,
            "Celular": 120, "Dirección": 200, "Correo": 200, "Estado": 100
        }
        for col in columnas:
            self.tre.heading(col, text=col)
            self.tre.column(col, width=width_map[col], anchor="center")

    # ========================== TABLA ========================== #
    def crear_tabla(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='proveedores' AND xtype='U')
            CREATE TABLE proveedores (
                id_proveedor INT IDENTITY(1,1) PRIMARY KEY,
                nombre NVARCHAR(100),
                identificacion NVARCHAR(50),
                celular NVARCHAR(20),
                direccion NVARCHAR(150),
                correo NVARCHAR(100),
                estado BIT DEFAULT 1
            )
            """)
            conn.commit()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear la tabla: {e}")

    # ========================== CARGAR REGISTROS ========================== #
    def cargar_registros(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id_proveedor, nombre, identificacion, celular, direccion, correo, estado FROM proveedores")
            rows = cursor.fetchall()
            self.tre.delete(*self.tre.get_children())
            for row in rows:
                id_proveedor, nombre, ident, celular, direccion, correo, estado = row
                estado_texto = "Habilitado" if estado == 1 else "Deshabilitado"
                item_id = self.tre.insert("", "end", values=(id_proveedor, nombre, ident, celular, direccion, correo, estado_texto))
                if estado == 0:
                    self.tre.item(item_id, tags=("deshabilitado",))
            self.tre.tag_configure("deshabilitado", foreground="red")
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los registros: {e}")

    # ========================== REGISTRAR ========================== #
    def registrar(self):
        datos = [self.entries[c].get() for c in ["nombre","identificación","celular","dirección","correo"]]
        if any(d == "" for d in datos):
            messagebox.showerror("Error", "Todos los campos son requeridos.")
            return
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO proveedores (nombre, identificacion, celular, direccion, correo, estado)
                VALUES (?, ?, ?, ?, ?, 1)
            """, tuple(datos))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Proveedor registrado correctamente.")
            self.limpiar_campos()
            self.cargar_registros()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el proveedor: {e}")

    # ========================== ELIMINAR ========================== #
    def eliminar(self):
        if not self.tre.selection():
            messagebox.showerror("Error", "Seleccione un proveedor para eliminar.")
            return
        pin = simpledialog.askstring("PIN de seguridad", "Ingrese el PIN de seguridad:", show="*")
        if pin != "2024":
            messagebox.showerror("Error", "PIN incorrecto.")
            return
        item = self.tre.selection()[0]
        id_proveedor = self.tre.item(item, "values")[0]
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM proveedores WHERE id_proveedor=?", (id_proveedor,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Proveedor eliminado correctamente.")
            self.cargar_registros()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el proveedor: {e}")

    # ========================== MODIFICAR ========================== #
    def modificar(self):
        if not self.tre.selection():
            messagebox.showerror("Error", "Seleccione un proveedor para modificar.")
            return
        item = self.tre.selection()[0]
        id_proveedor = self.tre.item(item, "values")[0]

        # Traer datos de DB
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT nombre, identificacion, celular, direccion, correo, estado FROM proveedores WHERE id_proveedor=?", (id_proveedor,))
            row = cursor.fetchone()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los datos: {e}")
            return

        nombre_actual, ident_actual, celular_actual, dir_actual, correo_actual, estado_actual = row

        top_mod = Toplevel(self)
        top_mod.title("Modificar Proveedor")
        top_mod.geometry("400x450")
        top_mod.config(bg="#C6D9E3")

        labels = ["Nombre", "Identificación", "Celular", "Dirección", "Correo"]
        actuales = [nombre_actual, ident_actual, celular_actual, dir_actual, correo_actual]
        entries = []
        for i, val in enumerate(actuales):
            tk.Label(top_mod, text=f"{labels[i]}:", font="sans 14 bold", bg="#C6D9E3").grid(row=i, column=0, padx=10, pady=5)
            entry = tk.Entry(top_mod, font="sans 14 bold")
            entry.insert(0, val)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries.append(entry)

        # Estado Checkbutton
        estado_var = tk.BooleanVar(value=bool(estado_actual))
        chk = tk.Checkbutton(top_mod, text="Habilitado" if estado_var.get() else "Deshabilitado",
                             variable=estado_var,
                             font="sans 14 bold", bg="#C6D9E3",
                             command=lambda: chk.config(text="Habilitado" if estado_var.get() else "Deshabilitado"))
        chk.grid(row=5, column=1, pady=10)

        # Guardar cambios con verificación de PIN si cambia estado
        def guardar_cambios():
            nuevos = [e.get() for e in entries]
            if bool(estado_actual) != estado_var.get():
                pin = simpledialog.askstring("PIN de seguridad", "Ingrese PIN de administrador para cambiar estado:", show="*")
                if pin != "2024":
                    messagebox.showerror("Error", "PIN incorrecto. No se puede cambiar el estado.")
                    estado_var.set(bool(estado_actual))
                    return
            nuevo_estado = 1 if estado_var.get() else 0
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE proveedores SET nombre=?, identificacion=?, celular=?, direccion=?, correo=?, estado=?
                    WHERE id_proveedor=?
                """, (*nuevos, nuevo_estado, id_proveedor))
                conn.commit()
                conn.close()
                self.cargar_registros()
                top_mod.destroy()
                messagebox.showinfo("Éxito", "Proveedor modificado correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo modificar el proveedor: {e}")

        ruta = self.rutas(r"icono/guardar.png")
        img_save = ImageTk.PhotoImage(Image.open(ruta).resize((30, 30)))
        btn_guardar = Button(top_mod, text="Guardar cambios", bg="#dddddd", font="sans 14 bold",
                             image=img_save, compound=LEFT, padx=10, command=guardar_cambios)
        btn_guardar.image = img_save
        btn_guardar.place(x=80, y=300, width=240, height=40)

    # ========================== LIMPIAR CAMPOS ========================== #
    def limpiar_campos(self):
        for ent in self.entries.values():
            ent.delete(0, END)
