from config import get_connection
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from PIL import Image, ImageTk
import threading
import os
import sys
import re
import pyodbc


class Inventario(tk.Frame):

    def __init__(self, padre):
        super().__init__(padre)
        self.con = get_connection()
        self.cur = self.con.cursor()
        self.timer_articulos = None

        # Carpeta para almacenar las imágenes
        self.image_folder = "fotos"
        if not os.path.exists(self.image_folder):
            os.makedirs(self.image_folder)

        self.widgets()
        self.articulos_combobox()
        self.cargar_articulos()

    def rutas(self, ruta):
        try:
            rutabase = sys.__MEIPASS
        except Exception:
            rutabase = os.path.abspath(".")
        return os.path.join(rutabase, ruta)

    # ========================== WIDGETS PRINCIPALES ========================== #
    def widgets(self):
        canva_articulos = tk.LabelFrame(self, text="Articulos", font="arial 14 bold", bg="#C6D9E3")
        canva_articulos.place(x=300, y=10, width=780, height=580)

        self.canvas = tk.Canvas(canva_articulos, bg="#C6D9E3")
        self.scrollbar = tk.Scrollbar(canva_articulos, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#C6D9E3")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # -------------------- Buscar -------------------- #
        lblframe_buscar = LabelFrame(self, text="Buscar", font="arial 14 bold", bg="#C6D9E3")
        lblframe_buscar.place(x=10, y=10, width=280, height=80)

        self.comboboxbuscar = ttk.Combobox(lblframe_buscar, font="arial 12")
        self.comboboxbuscar.place(x=5, y=5, width=260, height=40)
        self.comboboxbuscar.bind("<<ComboboxSelected>>", self.on_combobox_select)
        self.comboboxbuscar.bind("<KeyRelease>", self.filtrar_articulos)

        # -------------------- Selección -------------------- #
        lblframe_seleccion = tk.LabelFrame(self, text="Selección", font="arial 14 bold", bg="#C6D9E3")
        lblframe_seleccion.place(x=10, y=95, width=280, height=190)

        self.label1 = tk.Label(lblframe_seleccion, text="Articulo: ", font="arial 12", bg="#C6D9E3", wraplength=300)
        self.label1.place(x=5, y=5)

        self.label2 = tk.Label(lblframe_seleccion, text="Precio: ", font="arial 12", bg="#C6D9E3")
        self.label2.place(x=5, y=40)

        self.label3 = tk.Label(lblframe_seleccion, text="Costo: ", font="arial 12", bg="#C6D9E3")
        self.label3.place(x=5, y=70)

        self.label4 = tk.Label(lblframe_seleccion, text="Stock: ", font="arial 12", bg="#C6D9E3")
        self.label4.place(x=5, y=100)

        self.label5 = tk.Label(lblframe_seleccion, text="Estado: ", font="arial 12", bg="#C6D9E3")
        self.label5.place(x=5, y=130)

        # -------------------- Botones -------------------- #
        lblframe_botones = LabelFrame(self, bg="#C6D9E3", text="Opciones", font="arial 14 bold")
        lblframe_botones.place(x=10, y=290, width=280, height=300)

        # Botón Agregar
        ruta = self.rutas(r"icono/ingresara.png")
        imagen_pil = Image.open(ruta).resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_pil)
        btn1 = tk.Button(lblframe_botones, text="Agregar", font="arial 14 bold", command=self.agregar_articulo)
        btn1.config(image=imagen_tk, compound=LEFT, padx=10)
        btn1.image = imagen_tk
        btn1.place(x=20, y=10, width=240, height=40)

        # Botón Editar
        ruta = self.rutas(r"icono/editar.png")
        imagen_pil = Image.open(ruta).resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_pil)
        btn2 = tk.Button(lblframe_botones, text="Editar", font="arial 14 bold", command=self.editar_articulo)
        btn2.config(image=imagen_tk, compound=LEFT, padx=10)
        btn2.image = imagen_tk
        btn2.place(x=20, y=60, width=240, height=40)

    # ========================== COMBOBOX ARTICULOS ========================== #
    def articulos_combobox(self):
        self.cur.execute("SELECT articulo FROM Articulos")
        self.articulos = [row[0] for row in self.cur.fetchall()]
        self.comboboxbuscar['values'] = self.articulos

    def filtrar_articulos(self, event):
        if self.timer_articulos:
            self.timer_articulos.cancel()
        self.timer_articulos = threading.Timer(0.5, self._filter_articulos)
        self.timer_articulos.start()

    def _filter_articulos(self):
        typed = self.comboboxbuscar.get()
        if typed == '':
            data = self.articulos
        else:
            data = [item for item in self.articulos if typed.lower() in item.lower()]
        self.comboboxbuscar['values'] = data if data else ['No results found']
        self.comboboxbuscar.event_generate('<Down>')
        self.cargar_articulos(filtro=typed)

    # ========================== CARGAR ARTICULOS ========================== #
    def cargar_articulos(self, filtro=None):
        self.after(0, self._cargar_articulos, filtro)

    def _cargar_articulos(self, filtro=None):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        query = "SELECT articulo, precio, image_path FROM Articulos"
        params = []
        if filtro:
            query += " WHERE articulo LIKE ?"
            params.append(f'%{filtro}%')

        if params:
            self.cur.execute(query, params)
        else:
            self.cur.execute(query)

        articulos = self.cur.fetchall()
        self.row, self.column = 0, 0
        for articulo, precio, image_path in articulos:
            self.mostrar_articulo(articulo, precio, image_path)

    def mostrar_articulo(self, articulo, precio, image_path):
        article_frame = tk.Frame(self.scrollable_frame, bg="white", relief="solid")
        article_frame.grid(row=self.row, column=self.column, padx=10, pady=10)

        if image_path and os.path.exists(image_path):
            image = Image.open(image_path).resize((150, 150), Image.LANCZOS)
            imagen = ImageTk.PhotoImage(image)
            image_label = tk.Label(article_frame, image=imagen)
            image_label.image = imagen
            image_label.pack(expand=True, fill="both")

        name_label = tk.Label(article_frame, text=articulo, bg="white", anchor="w", wraplength=150,
                              font="arial 10 bold")
        name_label.pack(side="top", fill="x")

        price_label = tk.Label(article_frame, text=f"Precio: {precio:,.2f}", bg="white", anchor="w", wraplength=150,
                               font="arial 8 bold")
        price_label.pack(side="bottom", fill="x")

        self.column += 1
        if self.column > 3:
            self.column = 0
            self.row += 1

    # ========================== SELECCIONAR ARTICULO ========================== #
    def on_combobox_select(self, event):
        self.actualizar_label()

    def actualizar_label(self, event=None):
        articulo_seleccionado = self.comboboxbuscar.get()
        try:
            self.cur.execute("SELECT articulo, precio, costo, stock, estado FROM Articulos WHERE articulo=?",
                             (articulo_seleccionado,))
            resultado = self.cur.fetchone()
            if resultado:
                articulo, precio, costo, stock, estado = resultado
                estado_texto = "Habilitado" if estado == 1 else "Deshabilitado"
                self.label1.config(text=f"Artículo: {articulo}")
                self.label2.config(text=f"Precio: {precio}")
                self.label3.config(text=f"Costo: {costo}")
                self.label4.config(text=f"Stock: {stock}")
                self.label5.config(text=f"Estado: {estado_texto}", fg=("green" if estado == 1 else "red"))
            else:
                self.label1.config(text="Artículo: No encontrado")
                self.label2.config(text="Precio: N/A")
                self.label3.config(text="Costo: N/A")
                self.label4.config(text="Stock: N/A")
                self.label5.config(text="Estado: N/A", fg="black")

        except pyodbc.Error as e:
            messagebox.showerror("Error", "Error al obtener los datos del artículo")

    # ========================== CARGAR IMAGEN ========================== #
    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            image = Image.open(file_path).resize((200, 200), Image.LANCZOS)
            image_name = os.path.basename(file_path)
            image_save_path = os.path.join(self.image_folder, image_name)
            image.save(image_save_path)
            self.image_tk = ImageTk.PhotoImage(image)
            self.product_image = self.image_tk
            self.image_path = image_save_path
            img_label = tk.Label(self.frameimg, image=self.image_tk)
            img_label.place(x=0, y=0, width=200, height=200)

    # ========================== AGREGAR ARTICULO ========================== #
    def agregar_articulo(self):
        top = tk.Toplevel(self)
        top.title("Agregar Artículo")
        top.geometry("700x500+200+50")
        top.config(bg="#C6D9E3")
        top.resizable(False, False)
        top.transient(self.master)
        top.grab_set()
        top.focus_set()
        top.lift()

        # ---------------- CAMPOS ---------------- #
        tk.Label(top, text="Artículo: ", font="arial 12 bold", bg="#C6D9E3").place(x=20, y=20)
        entry_articulo = ttk.Entry(top, font="arial 12 bold")
        entry_articulo.place(x=120, y=20, width=250)

        tk.Label(top, text="Precio: ", font="arial 12 bold", bg="#C6D9E3").place(x=20, y=60)
        entry_precio = ttk.Entry(top, font="arial 12 bold")
        entry_precio.place(x=120, y=60, width=250)

        tk.Label(top, text="Costo: ", font="arial 12 bold", bg="#C6D9E3").place(x=20, y=100)
        entry_costo = ttk.Entry(top, font="arial 12 bold")
        entry_costo.place(x=120, y=100, width=250)

        tk.Label(top, text="Stock: ", font="arial 12 bold", bg="#C6D9E3").place(x=20, y=140)
        entry_stock = ttk.Entry(top, font="arial 12 bold")
        entry_stock.place(x=120, y=140, width=250)

        # Estado como Checkbutton
        tk.Label(top, text="Estado: ", font="arial 12 bold", bg="#C6D9E3").place(x=20, y=180)
        estado_var = tk.BooleanVar(value=True)
        chk_estado = tk.Checkbutton(top, text="Habilitado", font="arial 12 bold", bg="#C6D9E3", variable=estado_var)
        chk_estado.place(x=120, y=180)

        # Proveedor
        tk.Label(top, text="Proveedor: ", font="arial 12 bold", bg="#C6D9E3").place(x=20, y=220)
        entry_proveedor = ttk.Combobox(top, font="arial 12 bold")
        entry_proveedor.place(x=120, y=220, width=250)
        self.cur.execute("SELECT id_proveedor, nombre FROM Proveedores")
        proveedores = self.cur.fetchall()
        entry_proveedor['values'] = [prov[1] for prov in proveedores]

        # Imagen
        self.frameimg = tk.Frame(top, bg="white", highlightbackground="gray", highlightthickness=1)
        self.frameimg.place(x=440, y=30, width=200, height=200)

        ruta = self.rutas(r"icono/foto.png")
        imagen_pil = Image.open(ruta).resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_pil)
        btnimagen = tk.Button(top, text="Cargar Imagen", font="arial 12 bold", command=self.load_image)
        btnimagen.config(image=imagen_tk, compound=LEFT, padx=10)
        btnimagen.image = imagen_tk
        btnimagen.place(x=450, y=260, width=200, height=40)

        # Guardar
        def guardar():
            articulo = entry_articulo.get()
            precio = entry_precio.get()
            costo = entry_costo.get()
            stock = entry_stock.get()
            estado = 1 if estado_var.get() else 0
            proveedor_nombre = entry_proveedor.get()

            if not all([articulo, precio, costo, stock, proveedor_nombre]):
                messagebox.showerror("Error", "Todos los campos deben ser completados")
                return
            try:
                precio = float(precio)
                costo = float(costo)
                stock = int(stock)
            except ValueError:
                messagebox.showerror("Error", "Precio, costo y stock deben ser números válidos")
                return

            image_path = getattr(self, 'image_path', self.rutas("fotos/default.png"))

            # Obtener id_proveedor
            self.cur.execute("SELECT id_proveedor FROM Proveedores WHERE nombre=?", (proveedor_nombre,))
            id_proveedor = self.cur.fetchone()[0]

            # Insertar en DB
            self.cur.execute(
                "INSERT INTO Articulos (articulo, precio, costo, stock, estado, image_path, id_proveedor) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (articulo, precio, costo, stock, estado, image_path, id_proveedor)
            )
            self.con.commit()
            messagebox.showinfo("Éxito", "Artículo agregado correctamente")
            top.destroy()
            self.cargar_articulos()
            self.articulos_combobox()

        # Botones Guardar y Cancelar
        ruta = self.rutas(r"icono/guardar.png")
        imagen_pil = Image.open(ruta).resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_pil)
        btnguardar = tk.Button(top, text="Guardar", font="arial 12 bold", command=guardar)
        btnguardar.config(image=imagen_tk, compound=LEFT, padx=10)
        btnguardar.image = imagen_tk
        btnguardar.place(x=50, y=320, width=150, height=40)

        ruta = self.rutas(r"icono/cancelar.png")
        imagen_pil = Image.open(ruta).resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_pil)
        btncancelar = tk.Button(top, text="Cancelar", font="arial 12 bold", command=top.destroy)
        btncancelar.config(image=imagen_tk, compound=LEFT, padx=10)
        btncancelar.image = imagen_tk
        btncancelar.place(x=250, y=320, width=150, height=40)

    # ========================== EDITAR ARTICULO ========================== #
    def editar_articulo(self):
        articulo_seleccionado = self.comboboxbuscar.get()
        if not articulo_seleccionado:
            messagebox.showwarning("Advertencia", "Seleccione un artículo primero")
            return

        # Obtener datos actuales
        self.cur.execute(
            "SELECT articulo, precio, costo, stock, estado, id_proveedor, image_path FROM Articulos WHERE articulo=?",
            (articulo_seleccionado,))
        resultado = self.cur.fetchone()
        if not resultado:
            messagebox.showerror("Error", "No se encontró el artículo seleccionado")
            return

        articulo, precio, costo, stock, estado, id_proveedor, image_path = resultado

        top = tk.Toplevel(self)
        top.title("Editar Artículo")
        top.geometry("700x500+200+50")
        top.config(bg="#C6D9E3")
        top.resizable(False, False)
        top.transient(self.master)
        top.grab_set()
        top.focus_set()
        top.lift()

        # Campos
        tk.Label(top, text="Artículo: ", font="arial 12 bold", bg="#C6D9E3").place(x=20, y=20)
        entry_articulo = ttk.Entry(top, font="arial 12 bold")
        entry_articulo.place(x=120, y=20, width=250)
        entry_articulo.insert(0, articulo)

        tk.Label(top, text="Precio: ", font="arial 12 bold", bg="#C6D9E3").place(x=20, y=60)
        entry_precio = ttk.Entry(top, font="arial 12 bold")
        entry_precio.place(x=120, y=60, width=250)
        entry_precio.insert(0, precio)

        tk.Label(top, text="Costo: ", font="arial 12 bold", bg="#C6D9E3").place(x=20, y=100)
        entry_costo = ttk.Entry(top, font="arial 12 bold")
        entry_costo.place(x=120, y=100, width=250)
        entry_costo.insert(0, costo)

        tk.Label(top, text="Stock: ", font="arial 12 bold", bg="#C6D9E3").place(x=20, y=140)
        entry_stock = ttk.Entry(top, font="arial 12 bold")
        entry_stock.place(x=120, y=140, width=250)
        entry_stock.insert(0, stock)

        # Estado Checkbutton con verificación admin
        tk.Label(top, text="Estado: ", font="arial 12 bold", bg="#C6D9E3").place(x=20, y=180)
        estado_var = tk.BooleanVar(value=bool(estado))

        def toggle_estado():
            if estado_var.get() == False:
                if not self.verificar_admin():
                    estado_var.set(True)

        chk_estado = tk.Checkbutton(top, text="Habilitado" if estado_var.get() else "Deshabilitado",
                                    font="arial 12 bold", bg="#C6D9E3",
                                    variable=estado_var,
                                    command=lambda: chk_estado.config(
                                        text="Habilitado" if estado_var.get() else "Deshabilitado") or toggle_estado())
        chk_estado.place(x=120, y=180)

        # Proveedor
        tk.Label(top, text="Proveedor: ", font="arial 12 bold", bg="#C6D9E3").place(x=20, y=220)
        entry_proveedor = ttk.Combobox(top, font="arial 12 bold")
        entry_proveedor.place(x=120, y=220, width=250)
        self.cur.execute("SELECT id_proveedor, nombre FROM Proveedores")
        proveedores = self.cur.fetchall()
        entry_proveedor['values'] = [prov[1] for prov in proveedores]
        proveedor_actual = [prov[1] for prov in proveedores if prov[0] == id_proveedor][0]
        entry_proveedor.set(proveedor_actual)

        # Imagen
        self.frameimg = tk.Frame(top, bg="white", highlightbackground="gray", highlightthickness=1)
        self.frameimg.place(x=440, y=30, width=200, height=200)
        if image_path and os.path.exists(image_path):
            image = Image.open(image_path).resize((200, 200), Image.LANCZOS)
            self.image_tk = ImageTk.PhotoImage(image)
            img_label = tk.Label(self.frameimg, image=self.image_tk)
            img_label.image = self.image_tk
            img_label.place(x=0, y=0, width=200, height=200)
            self.image_path = image_path

        ruta = self.rutas(r"icono/foto.png")
        imagen_pil = Image.open(ruta).resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_pil)
        btnimagen = tk.Button(top, text="Cargar Imagen", font="arial 12 bold", command=self.load_image)
        btnimagen.config(image=imagen_tk, compound=LEFT, padx=10)
        btnimagen.image = imagen_tk
        btnimagen.place(x=450, y=260, width=200, height=40)

        # Guardar cambios
        def guardar_cambios():
            nuevo_articulo = entry_articulo.get()
            nuevo_precio = entry_precio.get()
            nuevo_costo = entry_costo.get()
            nuevo_stock = entry_stock.get()
            nuevo_estado = 1 if estado_var.get() else 0
            proveedor_nombre = entry_proveedor.get()

            if not all([nuevo_articulo, nuevo_precio, nuevo_costo, nuevo_stock, proveedor_nombre]):
                messagebox.showerror("Error", "Todos los campos deben ser completados")
                return
            try:
                nuevo_precio = float(nuevo_precio)
                nuevo_costo = float(nuevo_costo)
                nuevo_stock = int(nuevo_stock)
            except ValueError:
                messagebox.showerror("Error", "Precio, costo y stock deben ser números válidos")
                return

            image_path_actual = getattr(self, 'image_path', image_path)
            self.cur.execute("SELECT id_proveedor FROM Proveedores WHERE nombre=?", (proveedor_nombre,))
            id_proveedor = self.cur.fetchone()[0]

            self.cur.execute(
                "UPDATE Articulos SET articulo=?, precio=?, costo=?, stock=?, estado=?, image_path=?, id_proveedor=? WHERE articulo=?",
                (nuevo_articulo, nuevo_precio, nuevo_costo, nuevo_stock, nuevo_estado, image_path_actual, id_proveedor, articulo_seleccionado)
            )
            self.con.commit()
            messagebox.showinfo("Éxito", "Artículo actualizado correctamente")
            top.destroy()
            self.cargar_articulos()
            self.articulos_combobox()

        # Botones
        ruta = self.rutas(r"icono/guardar.png")
        imagen_pil = Image.open(ruta).resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_pil)
        btnguardar = tk.Button(top, text="Guardar", font="arial 12 bold", command=guardar_cambios)
        btnguardar.config(image=imagen_tk, compound=LEFT, padx=10)
        btnguardar.image = imagen_tk
        btnguardar.place(x=50, y=320, width=150, height=40)

        ruta = self.rutas(r"icono/cancelar.png")
        imagen_pil = Image.open(ruta).resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_pil)
        btncancelar = tk.Button(top, text="Cancelar", font="arial 12 bold", command=top.destroy)
        btncancelar.config(image=imagen_tk, compound=LEFT, padx=10)
        btncancelar.image = imagen_tk
        btncancelar.place(x=250, y=320, width=150, height=40)

    # ========================== VERIFICACION ADMIN ========================== #
    def verificar_admin(self):
        password = simpledialog.askstring("Autorización requerida", "Ingrese la contraseña del administrador:", show="*")
        if not password:
            messagebox.showwarning("Cancelado", "Operación cancelada.")
            return False
        mi_contraseña = "2024"
        if password == mi_contraseña:
            return True
        else:
            messagebox.showerror("Acceso denegado", "Contraseña incorrecta.")
            return False
