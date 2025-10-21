import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
import threading
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from collections import defaultdict
import sys
import os
import re

from config import get_connection


class Ventas(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        # numero_factura se obtiene del servidor (tabla ventas)
        self.numero_factura = self.obtener_numero_factura_actual()
        # productos_seleccionados: lista de tuplas (factura, cliente, producto, precio_float, cantidad_int, total_float, costo_float)
        self.productos_seleccionados = []
        self.clientes = []
        self.products = []
        self.timer_cliente = None
        self.timer_producto = None

        self.widgets()
        self.cargar_productos()
        self.cargar_clientes()

    # Ruta compatible con PyInstaller
    def rutas(self, ruta):
        base = getattr(sys, "_MEIPASS", None)
        if not base:
            base = os.path.abspath(".")
        return os.path.join(base, ruta)

    # ------- UTILIDADES -------
    def _parse_currency(self, s):
        """Convierte una cadena formateada (ej: '1,234.56' o '$1,234.56') a float seguro."""
        if s is None:
            return 0.0
        try:
            # remover símbolos y espacios
            clean = re.sub(r"[^\d\.\-]", "", str(s))
            return float(clean) if clean != "" else 0.0
        except Exception:
            return 0.0

    # ------- DB: número de factura -------
    def obtener_numero_factura_actual(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            # Si la tabla usa IDENTITY o un campo 'factura', MAX funciona igual en SQL Server
            cur.execute("SELECT MAX(factura) FROM ventas")
            row = cur.fetchone()
            conn.close()
            last = row[0] if row else None
            return int(last) + 1 if last is not None else 1
        except Exception as e:
            print("Error obteniendo número de factura:", e)
            return 1

    # ------- CARGA DATOS (clientes / productos) -------
    def cargar_clientes(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT nombre FROM clientes")
            rows = cur.fetchall()
            conn.close()
            self.clientes = [r[0] for r in rows]
            # si el widget aún no existe, ignorar
            if hasattr(self, "entry_cliente"):
                self.entry_cliente["values"] = self.clientes
        except Exception as e:
            print("Error cargando clientes:", e)

    def filtrar_clientes(self, event):
        if self.timer_cliente:
            self.timer_cliente.cancel()
        self.timer_cliente = threading.Timer(0.5, self._filter_clientes)
        self.timer_cliente.start()

    def _filter_clientes(self):
        typed = self.entry_cliente.get()
        if typed == "":
            data = self.clientes
        else:
            data = [item for item in self.clientes if typed.lower() in item.lower()]
        if data:
            self.entry_cliente["values"] = data
            self.entry_cliente.event_generate("<Down>")
        else:
            self.entry_cliente["values"] = ["No results found"]
            self.entry_cliente.event_generate("<Down>")
            # no borrar el entry aquí — el usuario quizás quisiera corregir texto

    def cargar_productos(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT articulo FROM articulos")
            rows = cur.fetchall()
            conn.close()
            self.products = [r[0] for r in rows]
            if hasattr(self, "entry_producto"):
                self.entry_producto["values"] = self.products
        except Exception as e:
            print("Error cargando productos:", e)

    def filtrar_productos(self, event):
        if self.timer_producto:
            self.timer_producto.cancel()
        self.timer_producto = threading.Timer(0.5, self._filter_products)
        self.timer_producto.start()

    def _filter_products(self):
        typed = self.entry_producto.get()
        if typed == "":
            data = self.products
        else:
            data = [item for item in self.products if typed.lower() in item.lower()]
        if data:
            self.entry_producto["values"] = data
            self.entry_producto.event_generate("<Down>")
        else:
            self.entry_producto["values"] = ["No results found"]
            self.entry_producto.event_generate("<Down>")

    # ------- AGREGAR / EDITAR / ELIMINAR ARTÍCULO EN LA FACTURA EN MEMORIA -------
    def agregar_articulo(self):
        cliente = self.entry_cliente.get()
        producto = self.entry_producto.get()
        cantidad_txt = self.entry_cantidad.get()

        if not cliente:
            messagebox.showerror("Error", "Por favor seleccione un cliente.")
            return

        if not producto:
            messagebox.showerror("Error", "Por favor seleccione un producto.")
            return

        if not cantidad_txt.isdigit() or int(cantidad_txt) <= 0:
            messagebox.showerror("Error", "Por favor ingrese una cantidad válida.")
            return

        cantidad = int(cantidad_txt)

        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT precio, costo, stock FROM articulos WHERE articulo = ?", (producto,))
            row = cur.fetchone()
            conn.close()

            if row is None:
                messagebox.showerror("Error", "Producto no encontrado.")
                return

            precio, costo, stock = row
            precio = float(precio)
            costo = float(costo)
            stock = int(stock)

            if cantidad > stock:
                messagebox.showerror("Error", f"Stock insuficiente. Solo hay {stock} unidades disponibles.")
                return

            total = precio * cantidad
            total_formatted = "{:,.2f}".format(total)

            # Insertar visualmente en el Treeview (formateado)
            self.tre.insert("", "end", values=(self.numero_factura, cliente, producto,
                                              "{:,.2f}".format(precio), cantidad, total_formatted))
            # Guardar datos numéricos en la lista interna
            self.productos_seleccionados.append((self.numero_factura, cliente, producto, precio, cantidad, total, costo))

            # Limpiar entrys
            self.entry_cantidad.delete(0, "end")
            self.entry_producto.set("")

        except Exception as e:
            print("Error al agregar artículo:", e)

        self.calcular_precio_total()

    def calcular_precio_total(self):
        total_pagar = 0.0
        for item in self.productos_seleccionados:
            # item[5] es total en float
            try:
                total_pagar += float(item[5])
            except Exception:
                pass
        total_pagar_cop = "{:,.2f}".format(total_pagar)
        self.label_precio_total.config(text=f"Precio a Pagar: {total_pagar_cop}")

    def actualizar_stock(self, event=None):
        producto_seleccionado = self.entry_producto.get()
        if not producto_seleccionado:
            self.label_stock.config(text="Stock: -")
            return
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT stock FROM articulos WHERE articulo = ?", (producto_seleccionado,))
            row = cur.fetchone()
            conn.close()
            stock = int(row[0]) if row and row[0] is not None else 0
            self.label_stock.config(text=f"Stock: {stock}")
        except Exception as e:
            print("Error al obtener el stock del producto:", e)
            self.label_stock.config(text="Stock: -")

    # ------- PAGO / REGISTRO EN BD -------
    def realizar_pago(self):
        if not self.productos_seleccionados:
            messagebox.showerror("Error", "No hay productos seleccionados para realizar el pago.")
            return

        total_venta = sum(item[5] for item in self.productos_seleccionados)
        total_formateado = "{:,.2f}".format(total_venta)

        # Ventana para introducir monto pagado
        ventana_pago = tk.Toplevel(self)
        ventana_pago.title("Realizar pago")
        ventana_pago.geometry("400x400+450+80")
        ventana_pago.config(bg="#C6D9E3")
        ventana_pago.resizable(False, False)
        ventana_pago.transient(self.master)
        ventana_pago.grab_set()
        ventana_pago.focus_set()
        ventana_pago.lift()

        label_titulo = tk.Label(ventana_pago, text="Realizar pago", font="sans 30 bold", bg="#C6D9E3")
        label_titulo.place(x=70, y=10)

        label_total = tk.Label(ventana_pago, text=f"Total a pagar: {total_formateado}", font="sans 14 bold", bg="#C6D9E3")
        label_total.place(x=80, y=100)

        label_monto = tk.Label(ventana_pago, text="Ingrese el monto pagado:", font="sans 14 bold", bg="#C6D9E3")
        label_monto.place(x=80, y=160)

        entry_monto = ttk.Entry(ventana_pago, font="sans 14 bold")
        entry_monto.place(x=80, y=210, width=240, height=40)

        ruta = self.rutas(r"icono/pago.png")
        try:
            imagen_pil = Image.open(ruta)
            imagen_resize10 = imagen_pil.resize((30, 30))
            imagen_tk = ImageTk.PhotoImage(imagen_resize10)
        except Exception:
            imagen_tk = None

        button_confirmar_pago = tk.Button(ventana_pago, text="Confirmar Pago",
                                          font="sans 14 bold",
                                          bg="#dddddd",
                                          fg="black",
                                          command=lambda: self.procesar_pago(entry_monto.get(), ventana_pago, total_venta))
        if imagen_tk:
            button_confirmar_pago.config(image=imagen_tk, compound="left", padx=10)
            button_confirmar_pago.image = imagen_tk
        button_confirmar_pago.place(x=80, y=270, width=240, height=40)

    def procesar_pago(self, cantidad_pagada, ventana_pago, total_venta):
        # Validaciones
        if "," in cantidad_pagada:
            messagebox.showwarning("Advertencia", "No coloque comas. Solo utilice punto si requiere decimales.")
            return

        decimal_pattern = r"^\d+(\.\d{1,2})?$"
        if not re.match(decimal_pattern, cantidad_pagada):
            messagebox.showwarning("Advertencia", "Cantidad pagada debe tener un máximo de dos decimales.")
            return

        try:
            cantidad_pagada = float(cantidad_pagada)
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese una cantidad válida.")
            return

        if cantidad_pagada < total_venta:
            messagebox.showerror("Error", "La cantidad pagada es insuficiente.")
            return

        cambio = cantidad_pagada - total_venta
        total_formateado = "{:,.2f}".format(total_venta)
        mensaje = f"Total: {total_formateado} \nCantidad pagada: {cantidad_pagada:,.2f} \nCambio: {cambio:,.2f} "
        messagebox.showinfo("Pago Realizado", mensaje)

        cliente = self.entry_cliente.get()
        try:
            conn = get_connection()
            cur = conn.cursor()

            fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d")
            hora_actual = datetime.datetime.now().strftime("%H:%M:%S")

            # Insertar cada item en ventas y actualizar stock
            for item in self.productos_seleccionados:
                _, cliente_item, producto, precio, cantidad, total_item, costo = item
                # Insert en SQL Server, sin incluir la columna IDENTITY (factura)
                cur.execute(
                    "INSERT INTO ventas (cliente, articulo, precio, cantidad, total, costo, fecha, hora) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (cliente_item, producto, precio, cantidad, total_item, costo * cantidad, fecha_actual, hora_actual)
                )

                # Reducir stock
                cur.execute("UPDATE articulos SET stock = stock - ? WHERE articulo = ?", (cantidad, producto))

            conn.commit()
            conn.close()

            # Generar PDF usando self.productos_seleccionados actuales
            self.generar_factura_pdf(total_venta, cliente, cantidad_pagada, cambio)

        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar la venta: {e}")
            return

        # Actualizar número de factura y limpiar
        self.numero_factura += 1
        if hasattr(self, "label_numero_factura"):
            self.label_numero_factura.config(text=str(self.numero_factura))

        self.productos_seleccionados = []
        self.limpiar_campos()
        ventana_pago.destroy()

    # ------- VENTANAS / VIEWS -------
    def limpiar_campos(self):
        for item in self.tre.get_children():
            self.tre.delete(item)
        self.label_precio_total.config(text="Precio a Pagar: 0")
        self.entry_producto.set("")
        self.entry_cantidad.delete(0, "end")

    def ver_ventas_realizadas(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT factura, cliente, articulo, precio, cantidad, total, fecha, hora, costo FROM ventas")
            ventas = cur.fetchall()
            conn.close()

            ventana_ventas = tk.Toplevel(self)
            ventana_ventas.title("Ventas Realizadas")
            ventana_ventas.geometry("1100x650+120+20")
            ventana_ventas.configure(bg="#C6D9E3")
            ventana_ventas.resizable(False, False)
            ventana_ventas.transient(self.master)
            ventana_ventas.grab_set()
            ventana_ventas.focus_set()
            ventana_ventas.lift()
            try:
                ruta = self.rutas(r"icono.ico")
                ventana_ventas.iconbitmap(ruta)
            except Exception:
                pass

            # Función para filtrar y mostrar ventas agrupadas
            def filtrar_ventas():
                factura_a_buscar = entry_factura.get().strip()
                cliente_a_buscar = entry_cliente.get().strip().lower()

                # limpiar tree
                for it in tree.get_children():
                    tree.delete(it)

                ventas_filtradas = [
                    venta for venta in ventas
                    if (str(venta[0]) == factura_a_buscar or not factura_a_buscar) and
                       (venta[1].lower() == cliente_a_buscar or not cliente_a_buscar)
                ]

                ventas_por_factura = defaultdict(lambda: {'cliente': '', 'fecha': '', 'hora': '', 'total': 0.0})

                for venta in ventas_filtradas:
                    factura = venta[0]
                    cliente = venta[1]
                    fecha = venta[6]
                    hora = venta[7]
                    total_item = float(venta[5])
                    ventas_por_factura[factura]['cliente'] = cliente
                    ventas_por_factura[factura]['fecha'] = fecha
                    ventas_por_factura[factura]['hora'] = hora
                    ventas_por_factura[factura]['total'] += total_item

                for factura, datos in ventas_por_factura.items():
                    try:
                        datos_fecha = datetime.datetime.strptime(datos['fecha'], "%Y-%m-%d").strftime("%d-%m-%Y")
                    except Exception:
                        datos_fecha = datos['fecha']
                    datos_total = "{:,.2f}".format(datos['total'])
                    tree.insert("", "end", values=(factura, datos['cliente'], datos_total, datos_fecha, datos['hora']))

            # Header
            label_ventas_realizadas = tk.Label(ventana_ventas, text="Ventas Realizadas", font="sans 26 bold", bg="#C6D9E3")
            label_ventas_realizadas.place(x=350, y=20)

            # Filtro
            filtro_frame = tk.Frame(ventana_ventas, bg="#C6D9E3")
            filtro_frame.place(x=20, y=60, width=1060, height=60)

            label_factura = tk.Label(filtro_frame, text="Número de Factura:", bg="#C6D9E3", font="sans 14 bold")
            label_factura.place(x=10, y=15)
            entry_factura = ttk.Entry(filtro_frame, font="sans 14 bold")
            entry_factura.place(x=200, y=10, width=200, height=40)

            label_cliente = tk.Label(filtro_frame, text="Nombre del Cliente:", bg="#C6D9E3", font="sans 14 bold")
            label_cliente.place(x=420, y=15)
            entry_cliente = ttk.Entry(filtro_frame, font="sans 14 bold")
            entry_cliente.place(x=620, y=10, width=200, height=40)

            # Botón filtrar
            try:
                ruta_img = self.rutas(r"icono/filtrar.png")
                img_p = Image.open(ruta_img).resize((30, 30))
                img_t = ImageTk.PhotoImage(img_p)
            except Exception:
                img_t = None

            btn_filtrar = tk.Button(filtro_frame, text="Filtrar", font="sans 14 bold", bg="#dddddd", command=filtrar_ventas)
            if img_t:
                btn_filtrar.config(image=img_t, compound="left", padx=10)
                btn_filtrar.image = img_t
            btn_filtrar.place(x=840, y=10)

            # Treeview
            tree_frame = tk.Frame(ventana_ventas, bg="gray")
            tree_frame.place(x=20, y=130, width=1060, height=500)

            scrol_y = ttk.Scrollbar(tree_frame)
            scrol_y.pack(side="right", fill="y")
            scrol_x = ttk.Scrollbar(tree_frame, orient=HORIZONTAL)
            scrol_x.pack(side=BOTTOM, fill=X)

            tree = ttk.Treeview(tree_frame, columns=("Factura", "Cliente", "Total", "Fecha", "Hora"), show="headings")
            tree.pack(expand=True, fill=BOTH)
            scrol_y.config(command=tree.yview)
            scrol_x.config(command=tree.xview)

            tree.heading("Factura", text="Factura")
            tree.heading("Cliente", text="Cliente")
            tree.heading("Total", text="Total")
            tree.heading("Fecha", text="Fecha")
            tree.heading("Hora", text="Hora")

            tree.column("Factura", width=50, anchor="center")
            tree.column("Cliente", width=180, anchor="center")
            tree.column("Total", width=100, anchor="center")
            tree.column("Fecha", width=100, anchor="center")
            tree.column("Hora", width=80, anchor="center")

            # Mostrar todas las ventas agrupadas
            ventas_por_factura = defaultdict(lambda: {'cliente': '', 'fecha': '', 'hora': '', 'total': 0.0})
            for venta in ventas:
                factura = venta[0]
                cliente = venta[1]
                fecha = venta[6]
                hora = venta[7]
                total = float(venta[5])
                ventas_por_factura[factura]['cliente'] = cliente
                ventas_por_factura[factura]['fecha'] = fecha
                ventas_por_factura[factura]['hora'] = hora
                ventas_por_factura[factura]['total'] += total

            for factura, datos in ventas_por_factura.items():
                try:
                    fecha_fmt = datetime.datetime.strptime(datos['fecha'], "%Y-%m-%d").strftime("%d-%m-%Y")
                except Exception:
                    fecha_fmt = datos['fecha']
                datos_total = "{:,.2f}".format(datos['total'])
                tree.insert("", "end", values=(factura, datos['cliente'], datos_total, fecha_fmt, datos['hora']))

            # Detalle de factura al doble clic
            def ver_detalles_factura(event):
                sel = tree.selection()
                if not sel:
                    return
                item = sel[0]
                factura_seleccionada = tree.item(item, "values")[0]

                ventana_detalles = tk.Toplevel(self)
                ventana_detalles.title(f"Detalles de la Factura {factura_seleccionada}")
                ventana_detalles.geometry("1100x650+120+20")
                ventana_detalles.configure(bg="#C6D9E3")
                ventana_detalles.resizable(False, False)
                ventana_detalles.transient(self.master)
                ventana_detalles.grab_set()
                ventana_detalles.focus_set()
                ventana_detalles.lift()

                label_detalle_ventas = tk.Label(ventana_detalles, text=f"Detalles de la Factura No.{factura_seleccionada}",
                                                font="sans 30 bold", bg="#C6D9E3")
                label_detalle_ventas.place(x=300, y=40)

                tree_frame1 = tk.Frame(ventana_detalles, bg="gray")
                tree_frame1.place(x=20, y=130, width=1060, height=500)

                scrol_y_det = ttk.Scrollbar(tree_frame1)
                scrol_y_det.pack(side="right", fill="y")
                scrol_x_det = ttk.Scrollbar(tree_frame1, orient=HORIZONTAL)
                scrol_x_det.pack(side=BOTTOM, fill=X)

                tree_detalles = ttk.Treeview(tree_frame1, columns=("Factura", "Cliente", "Producto", "Precio", "Cantidad", "Total", "Fecha", "Hora", "Costo"), show="headings")
                tree_detalles.pack(expand=True, fill=BOTH)

                scrol_y_det.config(command=tree_detalles.yview)
                scrol_x_det.config(command=tree_detalles.xview)

                # Encabezados columnas
                cols = [("Factura", 50), ("Cliente", 180), ("Producto", 150), ("Precio", 80),
                        ("Cantidad", 80), ("Total", 100), ("Fecha", 100), ("Hora", 80), ("Costo", 80)]
                for col, w in cols:
                    tree_detalles.heading(col, text=col)
                    tree_detalles.column(col, width=w, anchor="center")

                # Consultar detalles de la factura
                try:
                    conn = get_connection()
                    cur = conn.cursor()
                    cur.execute("SELECT factura, cliente, articulo, precio, cantidad, total, fecha, hora, costo FROM ventas WHERE factura = ?", (factura_seleccionada,))
                    detalles_venta = cur.fetchall()
                    conn.close()
                except Exception as e:
                    detalles_venta = []
                    print("Error consultando detalles:", e)

                for detalle in detalles_venta:
                    detalle_list = list(detalle)
                    # Formatear precio/total/costo
                    detalle_list[3] = "{:,.2f}".format(float(detalle_list[3])) if detalle_list[3] is not None else "0.00"
                    detalle_list[5] = "{:,.2f}".format(float(detalle_list[5])) if detalle_list[5] is not None else "0.00"
                    detalle_list[8] = "{:,.2f}".format(float(detalle_list[8])) if detalle_list[8] is not None else "0.00"
                    tree_detalles.insert("", "end", values=detalle_list)

            tree.bind("<Double-1>", ver_detalles_factura)

        except Exception as e:
            print("Error al obtener las ventas:", e)

    # ------- GENERAR FACTURA (PDF) -------
    def generar_factura_pdf(self, total_venta, cliente, cantidad_pagada, cambio):
        try:
            # Asegurarse de que exista la carpeta facturas
            os.makedirs("facturas", exist_ok=True)
            factura_path = f"facturas/Factura_{self.numero_factura}.pdf"
            c = canvas.Canvas(factura_path, pagesize=letter)

            # Datos empresa (puedes parametrizar)
            empresa_nombre = "Mini Market Version 1.0"
            empresa_direccion = "Calle 1 # 1A - 01, Neiva, Colombia"
            empresa_telefono = "+57 3002385798"
            empresa_email = "info@marketsystem.com"
            empresa_website = "www.marketsystem.com"

            c.setFont("Helvetica-Bold", 18)
            c.setFillColor(colors.darkblue)
            c.drawCentredString(300, 750, "FACTURA DE SERVICIOS")

            c.setFillColor(colors.black)
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, 710, f"{empresa_nombre}")
            c.setFont("Helvetica", 12)
            c.drawString(50, 690, f"Dirección: {empresa_direccion}")
            c.drawString(50, 670, f"Teléfono: {empresa_telefono}")
            c.drawString(50, 650, f"Email: {empresa_email}")
            c.drawString(50, 630, f"Website: {empresa_website}")

            c.setLineWidth(0.5)
            c.setStrokeColor(colors.grey)
            c.line(50, 620, 550, 620)

            c.setFont("Helvetica", 12)
            c.drawString(50, 600, f"Número de Factura: {self.numero_factura}")
            c.drawString(50, 580, f"Fecha: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

            c.line(50, 560, 550, 560)

            c.drawString(50, 540, f"Cliente: {cliente}")
            c.drawString(50, 520, "Descripción de Productos:")

            y_offset = 500
            c.setFont("Helvetica-Bold", 12)
            c.drawString(70, y_offset, "Producto")
            c.drawString(270, y_offset, "Cantidad")
            c.drawString(370, y_offset, "Precio")
            c.drawString(470, y_offset, "Total")

            c.line(50, y_offset - 10, 550, y_offset - 10)
            y_offset -= 30
            c.setFont("Helvetica", 12)

            for item in self.productos_seleccionados:
                factura, cliente_item, producto, precio, cantidad, total, costo = item
                c.drawString(70, y_offset, str(producto))
                c.drawString(270, y_offset, str(cantidad))
                c.drawString(370, y_offset, "{:,.2f}".format(precio))
                c.drawString(470, y_offset, "{:,.2f}".format(total))
                y_offset -= 20
                # Salto de página si se llena la hoja
                if y_offset < 80:
                    c.showPage()
                    y_offset = 750

            c.line(50, y_offset, 550, y_offset)
            y_offset -= 20

            c.setFont("Helvetica-Bold", 14)
            c.setFillColor(colors.darkblue)
            c.drawString(50, y_offset, f"Total a Pagar: {total_venta:,.2f}")
            c.drawString(50, y_offset - 20, f"Cantidad pagada: {cantidad_pagada:,.2f}")
            c.drawString(50, y_offset - 40, f"Cambio: {cambio:,.2f}")
            c.setFillColor(colors.black)
            c.setFont("Helvetica", 12)

            y_offset -= 20
            c.line(50, y_offset, 550, y_offset)

            c.setFont("Helvetica-Bold", 16)
            c.drawString(150, y_offset - 60, "¡Gracias por tu compra, vuelve pronto!")

            y_offset -= 100
            c.setFont("Helvetica", 10)
            c.drawString(50, y_offset, "Términos y Condiciones:")
            c.drawString(50, y_offset - 20, "1. Los productos comprados no tienen devolución.")
            c.drawString(50, y_offset - 40, "2. Conserve esta factura como comprobante de su compra.")
            c.drawString(50, y_offset - 60, "3. Para más información, visite nuestro sitio web o contacte a servicio al cliente.")

            c.setFont("Helvetica", 10)
            c.drawString(50, 50, "Para más información, visite nuestro sitio web o síganos en nuestras redes sociales:")
            c.drawString(50, 40, f"Website: www.innovasoftcode.com / Software creado por Kevin Arboleda / InnovaSoft Code @ 2024")

            c.save()

            messagebox.showinfo("Factura Generada", f"Se ha generado la factura en: {factura_path}")

            try:
                os.startfile(os.path.abspath(factura_path))
            except Exception:
                pass

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar la factura: {e}")

    # ------- Eliminar / Editar -------
    def limpiar_lista(self):
        self.tre.delete(*self.tre.get_children())
        self.productos_seleccionados.clear()
        self.calcular_precio_total()

    def eliminar_articulo(self):
        item_seleccionado = self.tre.selection()
        if not item_seleccionado:
            messagebox.showerror("Error", "No hay ningún artículo seleccionado.")
            return

        item_id = item_seleccionado[0]
        valores_item = self.tre.item(item_id)["values"]
        if not valores_item:
            return
        articulo = valores_item[2]

        # Eliminar visualmente
        self.tre.delete(item_id)
        # Eliminar de la lista interna (comparando por nombre de artículo)
        self.productos_seleccionados = [p for p in self.productos_seleccionados if p[2] != articulo]
        self.calcular_precio_total()

    def editar_articulo(self):
        selected_item = self.tre.selection()
        if not selected_item:
            messagebox.showerror("Error", "Por favor seleccione un artículo para editar.")
            return

        item_values = self.tre.item(selected_item[0], "values")
        if not item_values:
            return

        current_producto = item_values[2]
        current_cantidad = int(item_values[4])

        new_cantidad = simpledialog.askinteger("Editar Artículo", "Ingrese la nueva cantidad:", initialvalue=current_cantidad)
        if new_cantidad is None:
            return

        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT precio, costo, stock FROM articulos WHERE articulo = ?", (current_producto,))
            row = cur.fetchone()
            conn.close()

            if row is None:
                messagebox.showerror("Error", "Producto no encontrado.")
                return

            precio, costo, stock = row
            precio = float(precio)
            costo = float(costo)
            stock = int(stock)

            if new_cantidad > stock:
                messagebox.showerror("Error", f"Stock insuficiente. Solo hay {stock} unidades disponibles.")
                return

            total = precio * new_cantidad
            total_formatted = "{:,.2f}".format(total)

            # Actualizar Treeview
            self.tre.item(selected_item[0], values=(self.numero_factura, self.entry_cliente.get(), current_producto,
                                                   "{:,.2f}".format(precio), new_cantidad, total_formatted))

            # Actualizar lista interna
            for idx, producto in enumerate(self.productos_seleccionados):
                if producto[2] == current_producto:
                    self.productos_seleccionados[idx] = (self.numero_factura, self.entry_cliente.get(), current_producto,
                                                         precio, new_cantidad, total, costo)
                    break

            self.calcular_precio_total()

        except Exception as e:
            print("Error al editar el artículo:", e)

    # ------- INTERFAZ -------
    def widgets(self):
        # LabelFrame con entrys para ingresar datos
        labelframe = tk.LabelFrame(self, font="sans 12 bold", bg="#C6D9E3")
        labelframe.place(x=25, y=30, width=1045, height=180)

        label_cliente = tk.Label(labelframe, text="Cliente:", font="sans 14 bold", bg="#C6D9E3")
        label_cliente.place(x=10, y=11)
        self.entry_cliente = ttk.Combobox(labelframe, font="sans 14 bold")
        self.entry_cliente.place(x=120, y=8, width=260, height=40)
        self.entry_cliente.bind("<KeyRelease>", self.filtrar_clientes)

        try:
            ruta = self.rutas(r"icono/actualizar.png")
            imagen_pil = Image.open(ruta)
            imagen_resize = imagen_pil.resize((30, 30))
            imagen_tk = ImageTk.PhotoImage(imagen_resize)
        except Exception:
            imagen_tk = None

        self.btn_actualizarc = tk.Button(labelframe, command=self.cargar_clientes)
        if imagen_tk:
            self.btn_actualizarc.config(image=imagen_tk, compound="left", padx=10)
            self.btn_actualizarc.image = imagen_tk
        self.btn_actualizarc.place(x=400, y=8, width=40, height=40)

        label_producto = tk.Label(labelframe, text="Producto:", font="sans 14 bold", bg="#C6D9E3")
        label_producto.place(x=10, y=70)
        self.entry_producto = ttk.Combobox(labelframe, font="sans 14 bold")
        self.entry_producto.place(x=120, y=66, width=260, height=40)
        self.entry_producto.bind("<KeyRelease>", self.filtrar_productos)

        self.btn_actualizar = tk.Button(labelframe, command=self.cargar_productos)
        if imagen_tk:
            self.btn_actualizar.config(image=imagen_tk, compound="left", padx=10)
            self.btn_actualizar.image = imagen_tk
        self.btn_actualizar.place(x=400, y=66, width=40, height=40)

        label_cantidad = tk.Label(labelframe, text="Cantidad:", font="sans 14 bold", bg="#C6D9E3")
        label_cantidad.place(x=500, y=11)
        self.entry_cantidad = ttk.Entry(labelframe, font="sans 14 bold")
        self.entry_cantidad.place(x=610, y=8, width=100, height=40)

        self.label_stock = tk.Label(labelframe, text="Stock:", font="sans 14 bold", bg="#C6D9E3")
        self.label_stock.place(x=500, y=70)

        self.entry_producto.bind("<<ComboboxSelected>>", self.actualizar_stock)

        try:
            ruta = self.rutas(r"icono/factura.png")
            imagen_pil = Image.open(ruta)
            imagen_resize11 = imagen_pil.resize((30, 30))
            imagen_tk = ImageTk.PhotoImage(imagen_resize11)
        except Exception:
            imagen_tk = None

        label_factura = tk.Label(labelframe, text="Factura:", font="sans 14 bold", bg="#C6D9E3")
        if imagen_tk:
            label_factura.config(image=imagen_tk, compound="left", padx=10)
            label_factura.image = imagen_tk
        label_factura.place(x=800, y=11)

        self.label_numero_factura = tk.Label(labelframe, text=f"{self.numero_factura}", font="sans 14 bold", bg="#C6D9E3")
        self.label_numero_factura.place(x=950, y=15)

        # botones (agregar, eliminar, editar, limpiar)
        def make_button(frame, x, y, text, cmd, icon_path):
            try:
                ruta = self.rutas(icon_path)
                img = Image.open(ruta).resize((30, 30))
                ik = ImageTk.PhotoImage(img)
            except Exception:
                ik = None
            btn = tk.Button(frame, text=text, font="sans 14 bold", command=cmd)
            if ik:
                btn.config(image=ik, compound="left", padx=10)
                btn.image = ik
            btn.place(x=x, y=y, width=200, height=40)
            return btn

        make_button(labelframe, 90, 120, "Agregar", self.agregar_articulo, r"icono/agregar.png")
        make_button(labelframe, 310, 120, "Eliminar", self.eliminar_articulo, r"icono/eliminar.png")
        make_button(labelframe, 530, 120, "Editar", self.editar_articulo, r"icono/modificar.png")
        make_button(labelframe, 750, 120, "Limpiar", self.limpiar_lista, r"icono/limpiar.png")

        # TreeView Tabla
        treFrame = tk.Frame(self, bg="white")
        treFrame.place(x=70, y=220, width=980, height=300)

        scrol_y = ttk.Scrollbar(treFrame)
        scrol_y.pack(side=RIGHT, fill=Y)
        scrol_x = ttk.Scrollbar(treFrame, orient=HORIZONTAL)
        scrol_x.pack(side=BOTTOM, fill=X)

        self.tre = ttk.Treeview(treFrame, yscrollcommand=scrol_y.set, xscrollcommand=scrol_x.set, height=40,
                                columns=("Factura", "Cliente", "Producto", "Precio", "Cantidad", "Total"), show="headings")
        self.tre.pack(expand=True, fill=BOTH)
        scrol_y.config(command=self.tre.yview)
        scrol_x.config(command=self.tre.xview)

        cols = [("Factura", 70), ("Cliente", 250), ("Producto", 250), ("Precio", 120), ("Cantidad", 120), ("Total", 150)]
        for col, w in cols:
            self.tre.heading(col, text=col)
            self.tre.column(col, width=w, anchor="center")

        # Label precio total
        try:
            ruta = self.rutas(r"icono/precio.png")
            imagen_pil = Image.open(ruta)
            imagen_resize11 = imagen_pil.resize((50, 50))
            imagen_tk = ImageTk.PhotoImage(imagen_resize11)
        except Exception:
            imagen_tk = None

        self.label_precio_total = tk.Label(self, text="Precio a Pagar: 0", font="sans 22 bold", bg="#C6D9E3")
        if imagen_tk:
            self.label_precio_total.config(image=imagen_tk, compound="left", padx=10)
            self.label_precio_total.image = imagen_tk
        self.label_precio_total.place(x=580, y=540)

        # Botones pagar y ver ventas
        try:
            ruta = self.rutas(r"icono/pago.png")
            imagen_pil = Image.open(ruta)
            imagen_resize1 = imagen_pil.resize((30, 30))
            imagen_tk = ImageTk.PhotoImage(imagen_resize1)
        except Exception:
            imagen_tk = None

        boton_pagar = tk.Button(self, text="Pagar", font="sans 14 bold", command=self.realizar_pago)
        if imagen_tk:
            boton_pagar.config(image=imagen_tk, compound="left", padx=10)
            boton_pagar.image = imagen_tk
        boton_pagar.place(x=20, y=550, width=180, height=40)

        try:
            ruta = self.rutas(r"icono/ver.png")
            imagen_pil = Image.open(ruta)
            imagen_resize2 = imagen_pil.resize((30, 30))
            imagen_tk2 = ImageTk.PhotoImage(imagen_resize2)
        except Exception:
            imagen_tk2 = None

        boton_ver_ventas = tk.Button(self, text="Ver Ventas", font="sans 14 bold", bg="#dddddd", command=self.ver_ventas_realizadas)
        if imagen_tk2:
            boton_ver_ventas.config(image=imagen_tk2, compound="left", padx=10)
            boton_ver_ventas.image = imagen_tk2
        boton_ver_ventas.place(x=220, y=550, width=180, height=40)
