from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
import sys
import os

from inventario import Inventario
from clientes import Clientes
from proveedor import Proveedor
from ventas import Ventas
from reportes import Reportes

class Container(tk.Frame):
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.controlador = controlador
        self.place(x=0, y=0, width=1100, height=650)
        self.frames = {}
        self.buttons = []
        self.widgets()        # Barra superior
        self.init_frames()    # Inicializamos frames hijos

        self.show_frames(Clientes)  # Frame inicial

    def rutas(self, ruta):
        """Obtiene la ruta base para los recursos, compatible con PyInstaller."""
        try:
            rutabase = sys._MEIPASS
        except Exception:
            rutabase = os.path.abspath(".")
        return os.path.join(rutabase, ruta)

    def init_frames(self):
        """Crea todos los frames y los coloca en la posición correcta."""
        for i in (Inventario, Clientes, Proveedor, Ventas, Reportes):
            frame = i(self)
            self.frames[i] = frame
            frame.config(bg="#C6D9E3", highlightbackground="gray", highlightthickness=1)
            frame.place(x=0, y=40, width=1100, height=610)

    def show_frames(self, container):
        """Muestra el frame seleccionado en pantalla."""
        frame = self.frames[container]
        frame.tkraise()

    # Métodos de navegación
    def inventario(self):
        self.show_frames(Inventario)

    def clientes(self):
        self.show_frames(Clientes)

    def proveedor(self):
        self.show_frames(Proveedor)

    def ventas(self):
        self.show_frames(Ventas)

    def reportes(self):
        self.show_frames(Reportes)

    def widgets(self):
        """Crea la barra superior con los botones de navegación."""
        frame2 = tk.Frame(self, bg="white")
        frame2.place(x=0, y=0, width=1100, height=40)

        # Lista de botones y rutas de iconos
        botones_info = [
            ("Ventas", "icono/btnventas.png", self.ventas),        # Primer botón
            ("Inventario", "icono/btninventario.png", self.inventario),
            ("Clientes", "icono/btnclientes.png", self.clientes),
            ("Proveedor", "icono/btnproveedor.png", self.proveedor),
            ("Reportes", "icono/btnreportes.png", self.reportes)  # Último botón
        ]

        ancho_total = 1100
        ancho_boton = ancho_total // len(botones_info)
        x_pos = 0

        for texto, ruta_icono, comando in botones_info:
            ruta = self.rutas(ruta_icono)
            imagen_pil = Image.open(ruta).resize((30, 30))
            imagen_tk = ImageTk.PhotoImage(imagen_pil)
            btn = Button(
                frame2, fg="black", text=texto, font="sans 16 bold",
                image=imagen_tk, compound="left", padx=10, command=comando
            )
            btn.image = imagen_tk  # Evita que Tkinter lo recolecte
            btn.place(x=x_pos, y=0, width=ancho_boton, height=40)
            self.buttons.append(btn)
            x_pos += ancho_boton
