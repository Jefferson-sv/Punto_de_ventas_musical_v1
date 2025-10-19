from config import get_connection
from tkinter import *
import tkinter as tk
from tkinter import ttk,messagebox
from PIL import Image, ImageTk
from container import Container
import sys
import os

class Login(tk.Frame):  # Define la clase Login que hereda de tk.Frame, un contenedor en tkinter
    image = None  # Variable de clase para almacenar una imagen, inicializada como None

    def __init__(self, padre, controlador):  # Método constructor de la clase Login
        super().__init__(padre)  # Llama al constructor de la clase base tk.Frame
        self.pack()  # Empaqueta el frame dentro de su contenedor padre
        self.place(x=0, y=0, width=1100, height=650)  # Coloca el frame en la posición especificada y establece su tamaño
        self.controlador = controlador  # Almacena la referencia al controlador (ventana principal)
        self.widgets()  # Llama al método widgets para crear los elementos de la interfaz
        
    def rutas(self, ruta):  # Método para obtener la ruta del archivo de manera segura
        try:
            rutabase = sys.__MEIPASS  # Intenta obtener la ruta base si se está ejecutando en un entorno empaquetado (por ejemplo, con PyInstaller)
        except Exception:
            rutabase = os.path.abspath(".")  # Si no es un entorno empaquetado, usa la ruta actual
        return os.path.join(rutabase, ruta)  # Combina la ruta base con el nombre del archivo y lo devuelve

    def validacion(self, user, pas):  # Método para validar que el nombre de usuario y la contraseña no estén vacíos
        return len(user) > 0 and len(pas) > 0  # Retorna True si ambos campos tienen longitud mayor a 0

    def login(self):
        user = self.username.get()
        pas = self.password.get()

        if self.validacion(user, pas):
            consulta = "SELECT * FROM usuarios WHERE username=? AND password=?"
            parametros = (user, pas)

            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute(consulta, parametros)
                result = cursor.fetchall()
                conn.close()

                if result:
                    self.control1()
                else:
                    self.username.delete(0, 'end')
                    self.password.delete(0, 'end')
                    messagebox.showerror(title="Error", message="Usuario y/o contraseña incorrecta")
            except Exception as e:
                messagebox.showerror(title="Error", message=f"No se conectó a la base de datos: {e}")
        else:
            messagebox.showerror(title="Error", message="Llene todas las casillas")

    def control1(self):  # Método para cambiar a la pantalla del contenedor
        self.controlador.show_frame(Container)  # Llama al método show_frame del controlador con el frame del contenedor

    def control2(self):  # Método para cambiar a la pantalla de registro
        self.controlador.show_frame(Registro)  # Llama al método show_frame del controlador con el frame de registro

    def widgets(self):  # Método para crear y configurar los widgets de la interfaz
#===============Frame izquierdo=================================================================================#
        # Crear un Frame para el fondo
        fondo = tk.Frame(self, bg="#C6D9E3")  # Crea un frame con un color de fondo específico
        fondo.pack()  # Empaqueta el frame dentro del frame principal
        fondo.place(x=0, y=0, width=1250, height=680)  # Coloca el frame en la posición especificada y establece su tamaño

        # Agregar imagen de fondo
        ruta = self.rutas(r"imagenes/fondo.png")  # Obtiene la ruta de la imagen de fondo
        self.bg_image = Image.open(ruta)  # Abre la imagen con PIL
        self.bg_image = self.bg_image.resize((1100, 650))  # Redimensiona la imagen
        self.bg_image = ImageTk.PhotoImage(self.bg_image)  # Convierte la imagen a un formato compatible con tkinter
        self.bg_label = ttk.Label(fondo, image=self.bg_image)  # Crea una etiqueta con la imagen de fondo
        self.bg_label.place(x=0, y=0, width=1100, height=650)  # Coloca la etiqueta en el frame de fondo

        frame1 = tk.Frame(self, bg="#FFFFFF", highlightbackground="black", highlightthickness=1)  # Crea un frame para el contenido de inicio de sesión
        frame1.place(x=350, y=70, width=400, height=560)  # Coloca el frame en la posición especificada y establece su tamaño
        
        # Crear widgets encima del fondo
        ruta = self.rutas(r"imagenes/logo1.png")  # Obtiene la ruta de la imagen del logo
        self.logo_image = Image.open(ruta)  # Abre la imagen del logo con PIL
        self.logo_image = self.logo_image.resize((200, 200))  # Redimensiona la imagen del logo
        self.logo_image = ImageTk.PhotoImage(self.logo_image)  # Convierte la imagen a un formato compatible con tkinter
        self.logo_label = ttk.Label(frame1, image=self.logo_image, background="#FFFFFF")  # Crea una etiqueta con el logo
        self.logo_label.place(x=100, y=20)  # Coloca la etiqueta en el frame del contenido

        user = ttk.Label(frame1, text="Nombre de usuario", font="arial 16 bold", background="#FFFFFF")  # Crea una etiqueta para el nombre de usuario
        user.place(x=100, y=250)  # Coloca la etiqueta en el frame del contenido
        self.username = ttk.Entry(frame1, font="arial 16 bold")  # Crea un campo de entrada para el nombre de usuario
        self.username.place(x=80, y=290, width=240, height=40)  # Coloca el campo de entrada en el frame del contenido

        pas = ttk.Label(frame1, text="Contraseña", font="arial 16 bold", background="#FFFFFF")  # Crea una etiqueta para la contraseña
        pas.place(x=100, y=340)  # Coloca la etiqueta en el frame del contenido
        self.password = ttk.Entry(frame1, show="*", font="arial 16 bold")  # Crea un campo de entrada para la contraseña con caracteres ocultos
        self.password.place(x=80, y=380, width=240, height=40)  # Coloca el campo de entrada en el frame del contenido

        ruta = self.rutas(r"icono/iniciar.png")  # Obtiene la ruta del icono de iniciar sesión
        imagen_pil = Image.open(ruta)  # Abre la imagen del icono con PIL
        imagen_resize = imagen_pil.resize((30, 30))  # Redimensiona la imagen del icono
        imagen_tk = ImageTk.PhotoImage(imagen_resize)  # Convierte la imagen a un formato compatible con tkinter

        btn1 = tk.Button(frame1, text="Iniciar", image=imagen_tk, compound=tk.LEFT, command=self.login, font=("arial", 16, "bold"))  # Crea un botón para iniciar sesión
        btn1.image = imagen_tk  # Almacena la imagen del botón para evitar que sea recolectada por el recolector de basura
        btn1.place(x=80, y=440, width=240, height=40)  # Coloca el botón en el frame del contenido

        ruta = self.rutas(r"icono/registrar.png")  # Obtiene la ruta del icono de registrar
        imagen_pil1 = Image.open(ruta)  # Abre la imagen del icono con PIL
        imagen_resize1 = imagen_pil1.resize((30, 30))  # Redimensiona la imagen del icono
        imagen_tk1 = ImageTk.PhotoImage(imagen_resize1)  # Convierte la imagen a un formato compatible con tkinter

        btn2 = tk.Button(frame1, text="Registrar", image=imagen_tk1, compound=tk.LEFT, command=self.control2, font=("arial", 16, "bold"))  # Crea un botón para ir al registro
        btn2.image = imagen_tk1  # Almacena la imagen del botón para evitar que sea recolectada por el recolector de basura
        btn2.place(x=80, y=500, width=240, height=40)  # Coloca el botón en el frame del contenido

#==================================================================================================================# 
class Registro(tk.Frame):  # Define la clase Registro que hereda de tk.Frame
    image = None  # Variable de clase para almacenar una imagen, inicializada como None

    def __init__(self, padre, controlador):  # Método constructor de la clase Registro
        super().__init__(padre)  # Llama al constructor de la clase base tk.Frame
        self.pack()  # Empaqueta el frame dentro de su contenedor padre
        self.place(x=0, y=0, width=1100, height=650)  # Coloca el frame en la posición especificada y establece su tamaño
        self.controlador = controlador  # Almacena la referencia al controlador (ventana principal)
        self.widgets()  # Llama al método widgets para crear los elementos de la interfaz
        
    def rutas(self, ruta):  # Método para obtener la ruta del archivo de manera segura
        try:
            rutabase = sys.__MEIPASS  # Intenta obtener la ruta base si se está ejecutando en un entorno empaquetado (por ejemplo, con PyInstaller)
        except Exception:
            rutabase = os.path.abspath(".")  # Si no es un entorno empaquetado, usa la ruta actual
        return os.path.join(rutabase, ruta)  # Combina la ruta base con el nombre del archivo y lo devuelve

    def validacion(self, user, pas):  # Método para validar que el nombre de usuario y la contraseña no estén vacíos
        return len(user) > 0 and len(pas) > 0  # Retorna True si ambos campos tienen longitud mayor a 0

    def create_table(self):
        consulta = '''
          IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='usuarios' AND xtype='U')
          CREATE TABLE usuarios (
              id INT IDENTITY(1,1) PRIMARY KEY,
              username NVARCHAR(50),
              password NVARCHAR(50)
          )
          '''
        self.eje_consulta(consulta)

    def eje_consulta(self, consulta, parametros=()):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(consulta, parametros)
            conn.commit()
            conn.close()
        except Exception as e:
            messagebox.showerror(title="Error", message=f"Error al ejecutar la consulta: {e}")

    def registro(self):  # Método para manejar el registro de un nuevo usuario
        user = self.username.get()  # Obtiene el nombre de usuario del campo de entrada
        pas = self.password.get()  # Obtiene la contraseña del campo de entrada
        key = self.key.get()  # Obtiene el código de registro del campo de entrada
        if self.validacion(user, pas):  # Verifica si los datos de entrada son válidos
            if len(pas) < 6:  # Verifica si la contraseña es demasiado corta
                messagebox.showinfo(title="Error", message="Contraseña demasiado corta")  # Muestra un mensaje de advertencia
                self.username.delete(0, 'end')  # Limpia el campo de nombre de usuario
                self.password.delete(0, 'end')  # Limpia el campo de contraseña
            else:
                if key == "1234":  # Verifica si el código de registro es correcto
                    self.create_table()  # Asegura que la tabla de usuarios exista
                    consulta = "INSERT INTO usuarios VALUES (?,?)"  # Consulta SQL para insertar un nuevo usuario
                    parametros = (user, pas)  # Parámetros para la consulta SQL
                    self.eje_consulta(consulta, parametros)  # Llama al método eje_consulta para ejecutar la consulta
                    self.control1()  # Cambia a la pantalla del contenedor
                else:
                    messagebox.showerror(title="Registro", message="Error al ingresar el código de registro")  # Muestra un mensaje de error si el código es incorrecto
        else:
            messagebox.showerror(title="Error", message="Llene sus datos")  # Muestra un mensaje de error si los campos están vacíos

    def control1(self):  # Método para cambiar a la pantalla del contenedor
        self.controlador.show_frame(Container)  # Llama al método show_frame del controlador con el frame del contenedor

    def control2(self):  # Método para cambiar a la pantalla de inicio de sesión
        self.controlador.show_frame(Login)  # Llama al método show_frame del controlador con el frame de inicio de sesión

    def widgets(self):  # Método para crear y configurar los widgets de la interfaz
#==============Frame izquierdo========================================================================================# 
        # Crear un Frame para el fondo
        fondo = tk.Frame(self, bg="#C6D9E3")  # Crea un frame con un color de fondo específico
        fondo.pack()  # Empaqueta el frame dentro del frame principal
        fondo.place(x=0, y=0, width=1100, height=650)  # Coloca el frame en la posición especificada y establece su tamaño

        # Agregar imagen de fondo
        ruta = self.rutas(r"imagenes/fondo.png")  # Obtiene la ruta de la imagen de fondo
        self.bg_image = Image.open(ruta)  # Abre la imagen con PIL
        self.bg_image = self.bg_image.resize((1100, 650))  # Redimensiona la imagen
        self.bg_image = ImageTk.PhotoImage(self.bg_image)  # Convierte la imagen a un formato compatible con tkinter
        self.bg_label = ttk.Label(fondo, image=self.bg_image)  # Crea una etiqueta con la imagen de fondo
        self.bg_label.place(x=0, y=0, width=1100, height=650)  # Coloca la etiqueta en el frame de fondo

        frame1 = tk.Frame(self, bg="#FFFFFF", highlightbackground="black", highlightthickness=1)  # Crea un frame para el contenido de registro
        frame1.place(x=350, y=10, width=400, height=630)  # Coloca el frame en la posición especificada y establece su tamaño
        
        # Crear widgets encima del fondo
        ruta = self.rutas(r"imagenes/logo1.png")  # Obtiene la ruta de la imagen del logo
        self.logo_image = Image.open(ruta)  # Abre la imagen del logo con PIL
        self.logo_image = self.logo_image.resize((200, 200))  # Redimensiona la imagen del logo
        self.logo_image = ImageTk.PhotoImage(self.logo_image)  # Convierte la imagen a un formato compatible con tkinter
        self.logo_label = ttk.Label(frame1, image=self.logo_image, background="#FFFFFF")  # Crea una etiqueta con el logo
        self.logo_label.place(x=100, y=20)  # Coloca la etiqueta en el frame del contenido
        
        user = Label(frame1, text="Nombre de usuario", font="sans 16 bold", bg="#FFFFFF")  # Crea una etiqueta para el nombre de usuario
        user.place(x=100, y=250)  # Coloca la etiqueta en el frame del contenido
        self.username = ttk.Entry(frame1, font="sans 16 bold")  # Crea un campo de entrada para el nombre de usuario
        self.username.place(x=80, y=290, width=240, height=40)  # Coloca el campo de entrada en el frame del contenido
        
        pas = Label(frame1, text="Contraseña", font="sans 16 bold", bg="#FFFFFF")  # Crea una etiqueta para la contraseña
        pas.place(x=100, y=340)  # Coloca la etiqueta en el frame del contenido
        self.password = ttk.Entry(frame1, show="*", font="16")  # Crea un campo de entrada para la contraseña con caracteres ocultos
        self.password.place(x=80, y=380, width=240, height=40)  # Coloca el campo de entrada en el frame del contenido
        
        key = Label(frame1, text="Código de registro", font="sans 16 bold", bg="#FFFFFF")  # Crea una etiqueta para el código de registro
        key.place(x=100, y=430)  # Coloca la etiqueta en el frame del contenido
        self.key = ttk.Entry(frame1, show="*", font="16")  # Crea un campo de entrada para el código de registro con caracteres ocultos
        self.key.place(x=80, y=470, width=240, height=40)  # Coloca el campo de entrada en el frame del contenido

        ruta = self.rutas(r"icono/registrar.png")  # Obtiene la ruta del icono para el botón de registro
        imagen_pil = Image.open(ruta)  # Abre la imagen del icono con PIL
        imagen_resize3 = imagen_pil.resize((30, 30))  # Redimensiona la imagen del icono
        imagen_tk = ImageTk.PhotoImage(imagen_resize3)  # Convierte la imagen a un formato compatible con tkinter
        
        btn3 = Button(frame1, fg="black", text="Registrarse", font="sans 16 bold", command=self.registro)  # Crea un botón para registrar un nuevo usuario
        btn3.config(image=imagen_tk, compound=LEFT, padx=10)  # Configura la imagen del botón
        btn3.image = imagen_tk  # Almacena la imagen del botón para evitar que sea recolectada por el recolector de basura
        btn3.place(x=80, y=520, width=240, height=40)  # Coloca el botón en el frame del contenido

        ruta = self.rutas(r"icono/regresar.png")  # Obtiene la ruta del icono para el botón de regresar
        imagen_pil = Image.open(ruta)  # Abre la imagen del icono con PIL
        imagen_resize4 = imagen_pil.resize((30, 30))  # Redimensiona la imagen del icono
        imagen_tk = ImageTk.PhotoImage(imagen_resize4)  # Convierte la imagen a un formato compatible con tkinter

        btn4 = Button(frame1, fg="black", text="Regresar", font="sans 16 bold", command=self.control2)  # Crea un botón para regresar a la pantalla de inicio de sesión
        btn4.config(image=imagen_tk, compound=LEFT, padx=10)  # Configura la imagen del botón
        btn4.image = imagen_tk  # Almacena la imagen del botón para evitar que sea recolectada por el recolector de basura
        btn4.place(x=80, y=570, width=240, height=40)  # Coloca el botón en el frame del contenido

#======================================================================================================================#


