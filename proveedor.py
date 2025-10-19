from config import get_connection
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
import datetime
import sys
import os


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

    #               SECCIÓN DE WIDGETS / INTERFAZ
    def widgets(self):
        self.frame = Frame(self, bg="#C6D9E3", highlightbackground="gray", highlightthickness=1)
        self.frame.place(x=0, y=0, width=1100, height=610)

        self.labelframe = tk.LabelFrame(self.frame, text="Proveedores", font="sans 22 bold", bg="#C6D9E3")
        self.labelframe.place(x=20, y=30, width=400, height=500)

        lblnombre = tk.Label(self.labelframe, text="Nombre:", font="sans 14 bold", bg="#C6D9E3")
        lblnombre.place(x=10, y=20)
        self.nombre = ttk.Entry(self.labelframe, font="sans 14 bold")
        self.nombre.place(x=140, y=20, width=240, height=40)

        lblid = tk.Label(self.labelframe, text="Identificación:", font="sans 14 bold", bg="#C6D9E3")
        lblid.place(x=10, y=80)
        self.identificacion = ttk.Entry(self.labelframe, font="sans 14 bold")
        self.identificacion.place(x=140, y=80, width=240, height=40)

        lblcelular = Label(self.labelframe, text="Celular:", font="sans 14 bold", bg="#C6D9E3")
        lblcelular.place(x=10, y=140)
        self.celular = ttk.Entry(self.labelframe, font="sans 14 bold")
        self.celular.place(x=140, y=140, width=240, height=40)

        lbldireccion = tk.Label(self.labelframe, text="Dirección:", font="sans 14 bold", bg="#C6D9E3")
        lbldireccion.place(x=10, y=200)
        self.direccion = ttk.Entry(self.labelframe, font="sans 14 bold")
        self.direccion.place(x=140, y=200, width=240, height=40)

        lblcorreo = tk.Label(self.labelframe, text="Correo:", font="sans 14 bold", bg="#C6D9E3")
        lblcorreo.place(x=10, y=260)
        self.correo = ttk.Entry(self.labelframe, font="sans 14 bold")
        self.correo.place(x=140, y=260, width=240, height=40)

        # -------------------- Botones --------------------
        ruta = self.rutas(r"icono/ingresarc.png")
        img = ImageTk.PhotoImage(Image.open(ruta).resize((50, 50)))
        btn1 = Button(self.labelframe, bg="#dddddd", fg="black", text="Ingresar", font="roboto 12 bold", image=img, compound="top", padx=10, command=self.registrar)
        btn1.image = img
        btn1.place(x=50, y=340, width=80, height=80)

        ruta = self.rutas(r"icono/eliminar.png")
        img2 = ImageTk.PhotoImage(Image.open(ruta).resize((50, 50)))
        btn_eliminar = Button(self.labelframe, bg="#dddddd", fg="black", text="Eliminar", font="roboto 12 bold", image=img2, compound="top", padx=10, command=self.eliminar)
        btn_eliminar.image = img2
        btn_eliminar.place(x=150, y=340, width=80, height=80)

        ruta = self.rutas(r"icono/modificar.png")
        img3 = ImageTk.PhotoImage(Image.open(ruta).resize((50, 50)))
        btn_modificar = Button(self.labelframe, bg="#dddddd", fg="black", text="Modificar", font="roboto 12 bold", image=img3, compound="top", padx=10, command=self.modificar)
        btn_modificar.image = img3
        btn_modificar.place(x=250, y=340, width=80, height=80)

        # -------------------- Treeview --------------------
        treFrame = Frame(self.frame, bg="white")
        treFrame.place(x=440, y=50, width=620, height=450)

        scrol_y = ttk.Scrollbar(treFrame)
        scrol_y.pack(side=RIGHT, fill=Y)

        scrol_x = ttk.Scrollbar(treFrame, orient=HORIZONTAL)
        scrol_x.pack(side=BOTTOM, fill=X)

        self.tre = ttk.Treeview(
            treFrame,
            yscrollcommand=scrol_y.set,
            xscrollcommand=scrol_x.set,
            height=40,
            columns=("ID", "Nombre", "Identificación", "Celular", "Dirección", "Correo"),
            show="headings"
        )
        self.tre.pack(expand=True, fill=BOTH)
        scrol_y.config(command=self.tre.yview)
        scrol_x.config(command=self.tre.xview)

        self.tre.heading("ID", text="ID")
        self.tre.heading("Nombre", text="Nombre")
        self.tre.heading("Identificación", text="Identificación")
        self.tre.heading("Celular", text="Celular")
        self.tre.heading("Dirección", text="Dirección")
        self.tre.heading("Correo", text="Correo")

        self.tre.column("ID", width=50, anchor="center")
        self.tre.column("Nombre", width=150, anchor="center")
        self.tre.column("Identificación", width=120, anchor="center")
        self.tre.column("Celular", width=120, anchor="center")
        self.tre.column("Dirección", width=200, anchor="center")
        self.tre.column("Correo", width=200, anchor="center")

    #                 SECCIÓN BASE DE DATOS (SQL SERVER)
    def crear_tabla(self):
        # Crea la tabla 'proveedores' si no existe.
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
                correo NVARCHAR(100)
            )
            """)
            conn.commit()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear la tabla: {e}")

    def cargar_registros(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id_proveedor, nombre, identificacion, celular, direccion, correo FROM proveedores")
            rows = cursor.fetchall()
            self.tre.delete(*self.tre.get_children())
            for row in rows:
                self.tre.insert("", "end", values=list(row))

            conn.close()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los registros: {e}")

    def registrar(self):
        #Inserta un nuevo proveedor.
        if not self.nombre.get() or not self.identificacion.get() or not self.celular.get() or not self.direccion.get() or not self.correo.get():
            messagebox.showerror("Error", "Todos los campos son requeridos.")
            return
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO proveedores (nombre, identificacion, celular, direccion, correo)
            VALUES (?, ?, ?, ?, ?)
            """, (self.nombre.get(), self.identificacion.get(), self.celular.get(), self.direccion.get(), self.correo.get()))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Proveedor registrado correctamente.")
            self.limpiar_campos()
            self.cargar_registros()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el proveedor: {e}")

    def eliminar(self):
        #Elimina un proveedor seleccionado.
        if not self.tre.selection():
            messagebox.showerror("Error", "Seleccione un proveedor para eliminar.")
            return

        pin = simpledialog.askstring("PIN de seguridad", "Ingrese el PIN de seguridad:", show="*")
        if not pin or pin != "2024":
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

    def modificar(self):
        """Permite editar un proveedor seleccionado."""
        if not self.tre.selection():
            messagebox.showerror("Error", "Seleccione un proveedor para modificar.")
            return

        item = self.tre.selection()[0]
        datos = self.tre.item(item, "values")
        id_proveedor = datos[0]

        top_modificar = Toplevel(self)
        top_modificar.title("Modificar Proveedor")
        top_modificar.geometry("400x400")
        top_modificar.config(bg="#C6D9E3")

        labels = ["Nombre", "Identificación", "Celular", "Dirección", "Correo"]
        entries = []
        for i, campo in enumerate(datos[1:], start=0):
            tk.Label(top_modificar, text=f"{labels[i]}:", font="sans 14 bold", bg="#C6D9E3").grid(row=i, column=0, padx=10, pady=5)
            entry = tk.Entry(top_modificar, font="sans 14 bold")
            entry.insert(0, campo)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries.append(entry)

        def guardar_cambios():
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE proveedores
                    SET nombre=?, identificacion=?, celular=?, direccion=?, correo=?
                    WHERE id_proveedor=?
                """, (entries[0].get(), entries[1].get(), entries[2].get(), entries[3].get(), entries[4].get(), id_proveedor))
                conn.commit()
                conn.close()
                messagebox.showinfo("Éxito", "Proveedor modificado correctamente.")
                top_modificar.destroy()
                self.cargar_registros()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo modificar el proveedor: {e}")

        ruta = self.rutas(r"icono/guardar.png")
        img_save = ImageTk.PhotoImage(Image.open(ruta).resize((30, 30)))
        btn_guardar = Button(top_modificar, text="Guardar cambios", bg="#dddddd", fg="black", font="sans 14 bold", image=img_save, compound=LEFT, padx=10, command=guardar_cambios)
        btn_guardar.image = img_save
        btn_guardar.place(x=80, y=200, width=240, height=40)

    def limpiar_campos(self):
        self.nombre.delete(0, END)
        self.identificacion.delete(0, END)
        self.celular.delete(0, END)
        self.direccion.delete(0, END)
        self.correo.delete(0, END)
