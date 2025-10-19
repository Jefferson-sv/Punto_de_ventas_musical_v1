from config import get_connection
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import datetime
import sys
import os

class Clientes(Frame):

    def __init__(self, padre):
        super().__init__(padre)
        self.contador = 1  # Contador para el ID
        self.widgets()
        self.cargar_registros()

    def rutas(self,ruta):
        try:
            rutabase=sys.__MEIPASS
        except Exception:
            rutabase=os.path.abspath(".")
        return os.path.join(rutabase,ruta)

    def widgets(self):

        # Ventana de fondo
        self.frame = Frame(self, bg="#C6D9E3",highlightbackground="gray", highlightthickness=1)
        self.frame.place(x=0, y=0, width=1100, height=610)

        #=========LabelFrame con entrys para ingresar datos===================================================================================#
        self.labelframe = tk.LabelFrame(self.frame, text="Clientes", font="sans 22 bold", bg="#C6D9E3")
        self.labelframe.place(x=20,y=30,width=400,height=500)

        lblnombre = tk.Label(self.labelframe, text="Nombre: ", font="sans 14 bold", bg="#C6D9E3")
        lblnombre.place(x=10, y=20)
        self.nombre = ttk.Entry(self.labelframe, font="sans 14 bold")
        self.nombre.place(x=140,y=20,width=240,height=40)

        lblcedula = tk.Label(self.labelframe, text="Cédula: ", font="sans 14 bold", bg="#C6D9E3")
        lblcedula.place(x=10, y=80)
        self.cedula = ttk.Entry(self.labelframe, font="sans 14 bold")
        self.cedula.place(x=140,y=80,width=240,height=40)

        lblcelular = Label(self.labelframe, text="Celular: ", font="sans 14 bold", bg="#C6D9E3")
        lblcelular.place(x=10, y=140)
        self.celular = ttk.Entry(self.labelframe, font="sans 14 bold")
        self.celular.place(x=140,y=140,width=240,height=40)

        lbldireccion = tk.Label(self.labelframe, text="Dirección: ", font="sans 14 bold", bg="#C6D9E3")
        lbldireccion.place(x=10, y=200)
        self.direccion = ttk.Entry(self.labelframe, font="sans 14 bold")
        self.direccion.place(x=140,y=200,width=240,height=40)

        lblcorreo = tk.Label(self.labelframe, text="Correo: ", font="sans 14 bold", bg="#C6D9E3")
        lblcorreo.place(x=10, y=260)
        self.correo = ttk.Entry(self.labelframe, font="sans 14 bold")
        self.correo.place(x=140,y=260,width=240,height=40)

        ruta=self.rutas(r"icono/ingresarc.png")
        imagen_pil = Image.open(ruta)
        imagen_resize = imagen_pil.resize((50, 50))
        imagen_tk = ImageTk.PhotoImage(imagen_resize)

        btn1 = Button(self.labelframe, bg="#dddddd", fg="black", text="Ingresar", font="roboto 12 bold", command=self.registrar)
        btn1.config(image=imagen_tk, compound="top", padx=10)
        btn1.image = imagen_tk
        btn1.place(x=50, y=340,width=80, height=80)

        ruta=self.rutas(r"icono/eliminar.png")
        imagen_pil = Image.open(ruta)
        imagen_resize1 = imagen_pil.resize((50, 50))
        imagen_tk = ImageTk.PhotoImage(imagen_resize1)

        btn_eliminar = Button(self.labelframe, bg="#dddddd", fg="black", text="Eliminar", font="roboto 12 bold", command=self.eliminar)
        btn_eliminar.config(image=imagen_tk, compound="top", padx=10)
        btn_eliminar.image = imagen_tk
        btn_eliminar.place(x=150, y=340,width=80,height=80)

        ruta=self.rutas(r"icono/modificar.png")
        imagen_pil = Image.open(ruta)
        imagen_resize2 = imagen_pil.resize((50, 50))
        imagen_tk = ImageTk.PhotoImage(imagen_resize2)

        btn_modificar = Button(self.labelframe, bg="#dddddd", fg="black", text="Modificar", font="roboto 12 bold", command=self.modificar)
        btn_modificar.config(image=imagen_tk, compound="top", padx=10)
        btn_modificar.image = imagen_tk
        btn_modificar.place(x=250, y=340,width=80, height=80)

        #=========Treeview Tabla=============================================================================================================#
        treFrame=Frame(self.frame,bg="white") #frame recuadro dentro de la ventana ventas
        treFrame.place(x=440,y=50,width=620,height=450)

        # Barra de desplazamiento vertical
        scrol_y = ttk.Scrollbar(treFrame)
        scrol_y.pack(side=RIGHT, fill=Y)

        # Barra de desplazamiento horizontal
        scrol_x = ttk.Scrollbar(treFrame, orient=HORIZONTAL)
        scrol_x.pack(side=BOTTOM, fill=X)

        # Widget Treeview
        self.tre = ttk.Treeview(treFrame, yscrollcommand=scrol_y.set, xscrollcommand=scrol_x.set, height=40,
                                columns=("ID", "Nombre", "Cédula", "Celular", "Dirección", "Correo"),show="headings")
        self.tre.pack(expand=True, fill=BOTH)

        scrol_y.config(command=self.tre.yview)
        scrol_x.config(command=self.tre.xview)

        # Configurar columnas
        self.tre.heading("ID", text="ID")
        self.tre.heading("Nombre", text="Nombre")
        self.tre.heading("Cédula", text="Cédula")
        self.tre.heading("Celular", text="Celular")
        self.tre.heading("Dirección", text="Dirección")
        self.tre.heading("Correo", text="Correo")

        # Formato de las columnas
        self.tre.column("ID", width=50, anchor="center")
        self.tre.column("Nombre", width=150, anchor="center")
        self.tre.column("Cédula", width=120, anchor="center")
        self.tre.column("Celular", width=120, anchor="center")
        self.tre.column("Dirección", width=200, anchor="center")
        self.tre.column("Correo", width=200, anchor="center")

        #==================================================================================================================================#

    def cargar_registros(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            # Seleccionamos explícitamente las columnas en el orden del Treeview
            cursor.execute("SELECT ID, nombre, dui, celular, direccion, correo FROM clientes")
            rows = cursor.fetchall()

            for item in self.tre.get_children():
                self.tre.delete(item)
            for row in rows:
                self.tre.insert("", "end", values=list(row))
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar los registros: {e}")

    def registrar(self):
        if not self.validar_campos(): return
        datos = (self.nombre.get(), self.cedula.get(), self.celular.get(), self.direccion.get(), self.correo.get())
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO clientes (nombre, dui, celular, direccion, correo) VALUES (?, ?, ?, ?, ?)",
                           datos)
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Cliente registrado correctamente.")
            self.limpiar_campos()
            for item in self.tre.get_children(): self.tre.delete(item)
            self.cargar_registros()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el cliente: {e}")

    def eliminar(self):
        if not self.tre.selection():
            messagebox.showerror("Error", "Por favor seleccione un cliente para eliminar.")
            return

        # Mostrar cuadro de entrada para el PIN de seguridad
        pin = simpledialog.askstring("PIN de seguridad", "Ingrese el PIN de seguridad:", show='*')

        if not pin or len(pin) != 4 or not pin.isdigit():
            messagebox.showerror("Error", "PIN inválido. Debe ser un número de 4 dígitos.")
            return

        # Verificar que el PIN sea correcto (aquí puedes definir el PIN que desees)
        if pin != "2024":  # Cambia "1234" por el PIN que prefieras
            messagebox.showerror("Error", "PIN incorrecto.")
            return

        if messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar este cliente?"):
            item = self.tre.selection()[0]
            id_cliente = self.tre.item(item, "values")[0]


            # Eliminar registro de la base de datos
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM clientes WHERE ID=?", (id_cliente,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Éxito", "Cliente eliminado correctamente.")
                self.tre.delete(item)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el cliente: {e}")

    def modificar(self):
        if not self.tre.selection():
            messagebox.showerror("Error", "Seleccione un cliente para modificar.");
            return
        item = self.tre.selection()[0]
        id_cliente, nombre_actual, cedula_actual, celular_actual, direccion_actual, correo_actual = self.tre.item(item,
                                                                                                                  "values")

        top_modificar = Toplevel(self);
        top_modificar.title("Modificar Cliente");
        top_modificar.geometry("400x400");
        top_modificar.config(bg="#C6D9E3")
        labels = ["Nombre", "Cedula", "Celular", "Dirección", "Correo"]
        actuales = [nombre_actual, cedula_actual, celular_actual, direccion_actual, correo_actual]
        entradas = []

        for i, (lab, val) in enumerate(zip(labels, actuales)):
            tk.Label(top_modificar, text=f"{lab}:", font="sans 14 bold", bg="#C6D9E3").grid(row=i, column=0, padx=10,
                                                                                            pady=5)
            entry = tk.Entry(top_modificar, font="sans 14 bold");
            entry.insert(0, val);
            entry.grid(row=i, column=1, padx=10, pady=5)
            entradas.append(entry)

        def actualizar_cliente():
            nuevos = [e.get() for e in entradas]
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE clientes SET nombre=?, dui=?, celular=?, direccion=?, correo=? WHERE ID=?",
                               (*nuevos, id_cliente))
                conn.commit()
                conn.close()
                messagebox.showinfo("Éxito", "Cliente modificado correctamente.")
                self.tre.item(item, values=(id_cliente, *nuevos))
                top_modificar.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo modificar el cliente: {e}")

        ruta = self.rutas(r"icono/guardar.png")
        imagen_pil = Image.open(ruta).resize((30, 30));
        imagen_tk = ImageTk.PhotoImage(imagen_pil)
        btn_guardar = Button(top_modificar, text="Guardar cambios", bg="#dddddd", fg="black", font="sans 14 bold",
                             command=actualizar_cliente)
        btn_guardar.config(image=imagen_tk, compound=LEFT, padx=10);
        btn_guardar.image = imagen_tk
        btn_guardar.place(x=80, y=200, width=240, height=40)

    def limpiar_campos(self):
        self.nombre.delete(0, END)
        self.cedula.delete(0, END)
        self.celular.delete(0, END)
        self.direccion.delete(0, END)
        self.correo.delete(0, END)