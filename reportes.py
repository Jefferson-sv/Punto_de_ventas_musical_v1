from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from tkcalendar import DateEntry
import sys
import os
import datetime
from config import get_connection  # Conexión a SQL Server

class Reportes(tk.Frame):

    def __init__(self, padre):
        super().__init__(padre)
        self.widgets()

    def rutas(self, ruta):
        """Obtiene la ruta base para los recursos, compatible con PyInstaller."""
        try:
            rutabase = sys._MEIPASS
        except Exception:
            rutabase = os.path.abspath(".")
        return os.path.join(rutabase, ruta)

    def widgets(self):
        """Crea la interfaz principal de reportes con botones e iconos."""
        self.frame1 = tk.Frame(self, bg="#C6D9E3", highlightbackground="gray", highlightthickness=1)
        self.frame1.place(x=0, y=0, width=1100, height=610)

        # Botón Reporte ventas totales
        ruta = self.rutas(r"icono/reporte1.png")
        imagen_tk = ImageTk.PhotoImage(Image.open(ruta).resize((100, 100)))
        btn1 = tk.Button(self.frame1, text="Reporte \nventas totales", font="sans 14 bold", bg="#dddddd",
                         command=self.ventas_totales)
        btn1.config(image=imagen_tk, compound="top", pady=10)
        btn1.image = imagen_tk
        btn1.place(x=100, y=120, width=200, height=200)

        # Botón Reporte ganancias
        ruta = self.rutas(r"icono/reporte2.png")
        imagen_tk = ImageTk.PhotoImage(Image.open(ruta).resize((100, 100)))
        btn2 = tk.Button(self.frame1, text="Reporte ganancias", font="sans 14 bold", bg="#dddddd",
                         command=self.reporte_ganancias)
        btn2.config(image=imagen_tk, compound="top", pady=10)
        btn2.image = imagen_tk
        btn2.place(x=330, y=120, width=200, height=200)

        # Botón Costo total inventario
        ruta = self.rutas(r"icono/reporte3.png")
        imagen_tk = ImageTk.PhotoImage(Image.open(ruta).resize((100, 100)))
        btn3 = tk.Button(self.frame1, text="Reporte costo \ntotal inventario", font="sans 14 bold", bg="#dddddd",
                         command=self.costo_total_inventario)
        btn3.config(image=imagen_tk, compound="top", pady=10)
        btn3.image = imagen_tk
        btn3.place(x=560, y=120, width=200, height=200)

        # Botón Costo total ventas
        ruta = self.rutas(r"icono/reporte4.png")
        imagen_tk = ImageTk.PhotoImage(Image.open(ruta).resize((100, 100)))
        btn4 = tk.Button(self.frame1, text="Reporte costo \ntotal ventas", font="sans 14 bold", bg="#dddddd",
                         command=self.costo_total_ventas)
        btn4.config(image=imagen_tk, compound="top", pady=10)
        btn4.image = imagen_tk
        btn4.place(x=790, y=120, width=200, height=200)

    def format_currency(self, amount):
        """Formatea un número como moneda con separador de miles."""
        return f"{amount:,.2f}"

    # --------------------------------- Reporte ventas totales --------------------------------- #
    def ventas_totales(self):
        ventana = tk.Toplevel(self)
        ventana.title("Reporte ventas totales")
        ventana.geometry("550x550+450+80")
        ventana.config(bg="#C6D9E3")
        ventana.resizable(False, False)
        ventana.transient(self.master)
        ventana.grab_set()
        ventana.focus_set()
        ventana.lift()

        tk.Label(ventana, text="Reporte de ventas totales", font="sans 22 bold", bg="#C6D9E3").place(x=110, y=10, height=40)


        self.frame_filtro = tk.LabelFrame(ventana, bg="#dddddd")
        self.frame_filtro.place(x=10, y=60, width=530, height=120)

        tk.Label(self.frame_filtro, text="Desde:", font="sans 14 bold", bg="#dddddd").place(x=0, y=5, width=100, height=40)
        self.entry_desde = DateEntry(self.frame_filtro, font="sans 14 bold", date_pattern="yyyy-mm-dd")
        self.entry_desde.place(x=100, y=5, width=130, height=40)

        tk.Label(self.frame_filtro, text="Hasta:", font="sans 14 bold", bg="#dddddd").place(x=240, y=5, width=100, height=40)
        self.entry_hasta = DateEntry(self.frame_filtro, font="sans 14 bold", date_pattern="yyyy-mm-dd")
        self.entry_hasta.place(x=340, y=5, width=130, height=40)

        ruta = self.rutas(r"icono/filtrar.png")
        imagen_tk = ImageTk.PhotoImage(Image.open(ruta).resize((30, 30)))

        tk.Button(self.frame_filtro, text="Filtrar", font="sans 12 bold", bg="#dddddd",
                  image=imagen_tk, compound=LEFT, padx=10, command=self.generar_reporte).place(x=100, y=60, width=140, height=40)
        self.frame_filtro.image = imagen_tk

        # Tabla
        self.tabla_reporte = ttk.Treeview(ventana, columns=("Cantidad de Ventas", "Total de Ventas"), show="headings", height=5)
        self.tabla_reporte.heading("Cantidad de Ventas", text="Cantidad de productos vendidos", anchor="center")
        self.tabla_reporte.heading("Total de Ventas", text="Total de Ventas", anchor="center")
        self.tabla_reporte.column("Cantidad de Ventas", width=200, anchor="center")
        self.tabla_reporte.column("Total de Ventas", width=200, anchor="center")
        self.tabla_reporte.place(x=10, y=200, width=530, height=200)

        tk.Label(ventana,
                 text="El reporte de ventas totales equivale al total de las ventas de los productos incluyendo costo y ganancia",
                 font="sans 10 bold", bg="#C6D9E3", justify="center", anchor="center", wraplength=450
                 ).place(x=50, y=420, width=450, height=80)

    def generar_reporte(self):
        fecha_desde = self.entry_desde.get()
        fecha_hasta = self.entry_hasta.get()

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*), SUM(total) FROM ventas WHERE fecha BETWEEN ? AND ?", (fecha_desde, fecha_hasta))
            resultado = cursor.fetchone()
            conn.close()

            if not resultado or resultado[0] == 0:
                messagebox.showinfo("Información", "No se encontraron datos para el rango de fechas seleccionado.")
                return

            cantidad_ventas = resultado[0]
            total_ventas = resultado[1] or 0

            for item in self.tabla_reporte.get_children():
                self.tabla_reporte.delete(item)

            self.tabla_reporte.insert("", "end", values=(cantidad_ventas, self.format_currency(total_ventas)))

        except Exception as e:
            messagebox.showerror("Error de Base de Datos", f"Error al generar el reporte: {e}")

    # --------------------------------- Reporte ganancias --------------------------------- #
    def reporte_ganancias(self):
        ventana = tk.Toplevel(self)
        ventana.title("Reporte ganancias")
        ventana.geometry("550x550+450+80")
        ventana.config(bg="#C6D9E3")
        ventana.resizable(False, False)
        ventana.transient(self.master)
        ventana.grab_set()
        ventana.focus_set()
        ventana.lift()

        tk.Label(ventana, text="Reporte de ganancias", font="sans 22 bold", bg="#C6D9E3").place(x=110, y=10, height=40)

        self.frame_filtro1 = tk.LabelFrame(ventana, bg="#dddddd")
        self.frame_filtro1.place(x=10, y=60, width=530, height=120)

        tk.Label(self.frame_filtro1, text="Desde:", font="sans 14 bold", bg="#dddddd").place(x=0, y=5, width=100, height=40)
        self.entry_desde1 = DateEntry(self.frame_filtro1, font="sans 14 bold", date_pattern="yyyy-mm-dd")
        self.entry_desde1.place(x=100, y=5, width=130, height=40)

        tk.Label(self.frame_filtro1, text="Hasta:", font="sans 14 bold", bg="#dddddd").place(x=240, y=5, width=100, height=40)
        self.entry_hasta1 = DateEntry(self.frame_filtro1, font="sans 14 bold", date_pattern="yyyy-mm-dd")
        self.entry_hasta1.place(x=340, y=5, width=130, height=40)

        ruta = self.rutas(r"icono/filtrar.png")
        imagen_tk = ImageTk.PhotoImage(Image.open(ruta).resize((30, 30)))

        tk.Button(self.frame_filtro1, text="Reporte", font="sans 12 bold", bg="#dddddd",
                  image=imagen_tk, compound=LEFT, padx=10, command=self.generar_reporte_ganancias_totales).place(x=100, y=60, width=140, height=40)
        self.frame_filtro1.image = imagen_tk

        self.tabla_ganancias = ttk.Treeview(ventana, columns=("Ganancias Totales",), show="headings", height=5)
        self.tabla_ganancias.heading("Ganancias Totales", text="Ganancias Totales", anchor="center")
        self.tabla_ganancias.column("Ganancias Totales", width=200, anchor="center")
        self.tabla_ganancias.place(x=300, y=300, width=300, height=200, anchor="center")

        tk.Label(ventana,
                 text="El reporte de ganancias equivale a las ventas totales menos el costo de los productos",
                 font="sans 10 bold", bg="#C6D9E3", justify="center", anchor="center", wraplength=450
                 ).place(x=50, y=420, width=450, height=80)

    def generar_reporte_ganancias_totales(self):
        fecha_desde = self.entry_desde1.get()
        fecha_hasta = self.entry_hasta1.get()

        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT SUM(total) FROM ventas WHERE fecha BETWEEN ? AND ?", (fecha_desde, fecha_hasta))
            total_ventas = cursor.fetchone()[0] or 0

            cursor.execute("SELECT SUM(costo) FROM ventas WHERE fecha BETWEEN ? AND ?", (fecha_desde, fecha_hasta))
            total_costos = cursor.fetchone()[0] or 0

            ganancias_totales = total_ventas - total_costos
            conn.close()

            for item in self.tabla_ganancias.get_children():
                self.tabla_ganancias.delete(item)

            self.tabla_ganancias.insert("", "end", values=(self.format_currency(ganancias_totales),))

        except Exception as e:
            messagebox.showerror("Error de Base de Datos", f"Error al generar el reporte de ganancias totales: {e}")

    # --------------------------------- Costo total inventario --------------------------------- #
    def costo_total_inventario(self):
        ventana = tk.Toplevel(self)
        ventana.title("Reporte costo total inventario")
        ventana.geometry("550x550+450+80")
        ventana.config(bg="#C6D9E3")
        ventana.resizable(False, False)
        ventana.transient(self.master)
        ventana.grab_set()
        ventana.focus_set()
        ventana.lift()

        tk.Label(ventana, text="Costo Total de Inventario", font="sans 22 bold", bg="#C6D9E3").pack(pady=10)

        self.tabla_costo_inventario = ttk.Treeview(ventana, columns=("Costo Total",), show="headings", height=5)
        self.tabla_costo_inventario.heading("Costo Total", text="Costo Total", anchor="center")
        self.tabla_costo_inventario.column("Costo Total", width=200, anchor="center")
        self.tabla_costo_inventario.pack(pady=10)

        ruta = self.rutas(r"icono/reporte.png")
        imagen_tk = ImageTk.PhotoImage(Image.open(ruta).resize((30, 30)))

        tk.Button(ventana, text="Generar Reporte", font="sans 12 bold", bg="#dddddd",
                  image=imagen_tk, compound=LEFT, padx=10, command=self.calcular_costo_total).pack(pady=10)
        ventana.image = imagen_tk

        tk.Label(ventana,
                 text="El reporte de costo total de inventario muestra lo que costó adquirir los productos",
                 font="sans 10 bold", bg="#C6D9E3", justify="center", anchor="center", wraplength=450
                 ).place(x=50, y=420, width=450, height=80)

    def calcular_costo_total(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT SUM(costo * stock) FROM articulos")
            total_invertido = cursor.fetchone()[0] or 0
            conn.close()

            for item in self.tabla_costo_inventario.get_children():
                self.tabla_costo_inventario.delete(item)

            self.tabla_costo_inventario.insert("", "end", values=(self.format_currency(total_invertido),))

        except Exception as e:
            messagebox.showerror("Error de Base de Datos", f"Error al calcular el costo total de inventario: {e}")

    # --------------------------------- Costo total ventas --------------------------------- #
    def costo_total_ventas(self):
        ventana = tk.Toplevel(self)
        ventana.title("Reporte costo total ventas")
        ventana.geometry("550x550+450+80")
        ventana.config(bg="#C6D9E3")
        ventana.resizable(False, False)
        ventana.transient(self.master)
        ventana.grab_set()
        ventana.focus_set()
        ventana.lift()

        tk.Label(ventana, text="Reporte de Costo Total de Ventas", font="sans 22 bold", bg="#C6D9E3").pack(pady=10)

        self.lblframe = tk.Frame(ventana, bg="#dddddd", highlightbackground="gray", highlightthickness=1)
        self.lblframe.place(x=20, y=80, width=250, height=200)

        tk.Label(self.lblframe, text="Desde:", font="sans 14 bold", bg="#dddddd").place(x=10, y=15)
        self.entry_desde_ventas = DateEntry(self.lblframe, font="sans 14 bold", date_pattern="yyyy-mm-dd")
        self.entry_desde_ventas.place(x=90, y=15, width=130, height=40)

        tk.Label(self.lblframe, text="Hasta:", font="sans 14 bold", bg="#dddddd").place(x=10, y=70)
        self.entry_hasta_ventas = DateEntry(self.lblframe, font="sans 14 bold", date_pattern="yyyy-mm-dd")
        self.entry_hasta_ventas.place(x=90, y=70, width=130, height=40)

        self.tabla_costo_ventas = ttk.Treeview(ventana, columns=("Costo Total de Ventas",), show="headings", height=5)
        self.tabla_costo_ventas.heading("Costo Total de Ventas", text="Costo Total de Ventas", anchor="center")
        self.tabla_costo_ventas.column("Costo Total de Ventas", width=180, anchor="center")
        self.tabla_costo_ventas.place(x=300, y=80, width=180, height=200)

        ruta = self.rutas(r"icono/reporte.png")
        imagen_tk = ImageTk.PhotoImage(Image.open(ruta).resize((30, 30)))

        tk.Button(self.lblframe, text="Generar Reporte", font="sans 12 bold", bg="#dddddd",
                  image=imagen_tk, compound=LEFT, padx=10, command=self.calcular_costo_total_ventas).place(x=50, y=130, width=180, height=40)
        self.lblframe.image = imagen_tk

        tk.Label(ventana,
                 text="El reporte de costo total de ventas muestra lo que costó únicamente los productos que ya se vendieron",
                 font="sans 10 bold", bg="#C6D9E3", justify="center", anchor="center", wraplength=450
                 ).place(x=50, y=420, width=450, height=80)

    def calcular_costo_total_ventas(self):
        fecha_desde = self.entry_desde_ventas.get()
        fecha_hasta = self.entry_hasta_ventas.get()

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT SUM(costo) FROM ventas WHERE fecha BETWEEN ? AND ?", (fecha_desde, fecha_hasta))
            total_costo_ventas = cursor.fetchone()[0] or 0
            conn.close()

            for item in self.tabla_costo_ventas.get_children():
                self.tabla_costo_ventas.delete(item)

            self.tabla_costo_ventas.insert("", "end", values=(self.format_currency(total_costo_ventas),))

        except Exception as e:
            messagebox.showerror("Error de Base de Datos", f"Error al calcular el costo total de ventas: {e}")
