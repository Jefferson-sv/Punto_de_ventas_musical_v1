from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
import sys
import os

from inventario import Inventario
from clientes import Clientes
from proveedor import Proveedor


class Container(tk.Frame):
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.controlador = controlador
        self.pack()
        self.place(x=0, y=0, width=1100, height=650)
        self.widgets()
        self.frames = {}
        self.buttons = []  

        for i in (Inventario, Clientes, Proveedor):
            frame = i(self)
            self.frames[i] = frame
            frame.pack()
            frame.config(bg="#C6D9E3", highlightbackground="gray", highlightthickness=1)
            frame.place(x=0, y=40, width=1100, height=610)

        self.show_frames(Clientes)

    def rutas(self, ruta):
        """Obtiene la ruta base para los recursos, compatible con PyInstaller."""
        try:
            rutabase = sys._MEIPASS
        except Exception:
            rutabase = os.path.abspath(".")
        return os.path.join(rutabase, ruta)

    def show_frames(self, container):
        """Muestra el frame seleccionado en pantalla."""
        frame = self.frames[container]
        frame.tkraise()

    def inventario(self):
        self.show_frames(Inventario)

    def clientes(self):
        self.show_frames(Clientes)

    def proveedor(self):
        self.show_frames(Proveedor)

    def widgets(self):
        """Crea la barra superior con los botones de navegación."""
        frame2 = tk.Frame(self, bg="white")
        frame2.place(x=0, y=0, width=1100, height=40)

        ruta = self.rutas(r"icono/btninventario.png")
        imagen_pil = Image.open(ruta).resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_pil)
        self.btn_inventario = Button(
            frame2, fg="black", text="Inventario", font="sans 16 bold",
            image=imagen_tk, compound="left", padx=10, command=self.inventario
        )
        self.btn_inventario.image = imagen_tk
        self.btn_inventario.place(x=0, y=0, width=367, height=40)

        ruta = self.rutas(r"icono/btnclientes.png")
        imagen_pil = Image.open(ruta).resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_pil)
        self.btn_clientes = Button(
            frame2, fg="black", text="Clientes", font="sans 16 bold",
            image=imagen_tk, compound="left", padx=10, command=self.clientes
        )
        self.btn_clientes.image = imagen_tk
        self.btn_clientes.place(x=367, y=0, width=367, height=40)

        ruta = self.rutas(r"icono/btnproveedor.png")
        imagen_pil = Image.open(ruta).resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_pil)
        self.btn_proveedor = Button(
            frame2, fg="black", text="Proveedor", font="sans 16 bold",
            image=imagen_tk, compound="left", padx=10, command=self.proveedor
        )
        self.btn_proveedor.image = imagen_tk
        self.btn_proveedor.place(x=734, y=0, width=366, height=40)

        self.buttons = [self.btn_inventario, self.btn_clientes, self.btn_proveedor]
