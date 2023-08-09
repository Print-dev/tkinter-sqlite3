import tkinter as tk
from tkinter import *
from tkinter import Canvas, messagebox
from PIL import Image, ImageTk
import sqlite3
import random

class Aplicacion:
    dbname = "" #AQUI AGREGA TU PROPIA BASE DE DATOS (SI DESEAS PUEDES USAR LA MISMA EN LA DEL VIDEO POR ESO TE LO DEJO AHI), RECUERDA TAMBIEN COLOCAR EL NOMBRE DE TU TABLA EN LOS METODOS DE CONSULTAS
    def __init__(self, ventana):
        self.pantalla1 = ventana
        self.pantalla1.title("Aplicacion")
        self.pantalla1.geometry("500x300")
        self.pantalla1.configure(bg="#D8F8FC")
        self.pantalla1.resizable(0,0)

        Canvas(self.pantalla1, bg="white", width=228, height=1400).place(x=0, y=0)

        self.image = Image.open("user.png")
        self.resized = self.image.resize((226, 235), Image.LANCZOS)
        self.imagenRender = ImageTk.PhotoImage(self.resized)
        Label(image=self.imagenRender, master=self.pantalla1).pack(side=tk.LEFT, padx=0.5, pady=0)

        Button(text="Iniciar Sesion", fg="black", width="20", height="2", bd=3, bg="#F9E79F", command=self.iniciar_sesion).place(relx=0.6, rely=0.3)
        Button(text="Registrarse", fg="black", width="20", height="2", bd=3, bg="#F9E79F", command=self.registrar).place(relx=0.6, rely=0.6)

        self.obtenerUsuarios()

    def consultar(self, consulta, parametros = ()):
        with sqlite3.connect(self.dbname) as conn:
            cursor = conn.cursor()
            result = cursor.execute(consulta, parametros).fetchall()
            conn.commit()
        return result
    
    def obtenerUsuarios(self):
        self.consulta = 'SELECT * FROM usuarios'
        self.lista = self.consultar(self.consulta)
        for lis in self.lista:
            print(lis)

    def validar_campos_registrar(self):
        return len(self.nombre_entry.get()) != 0 and len(self.contrasena_entry.get()) !=0

    def ingresar_datos_registro(self):
        try:
            if (self.validar_campos_registrar()):
                self.nAleatorio = "123456789"
                self.samp = random.sample(self.nAleatorio, 7)
                self.idAleatorio = "".join(self.samp)
                self.correoConId = self.idAleatorio + "@gmail.com"
                self.consultando = 'INSERT INTO usuarios(ID_USUARIO, NOMBRE, CORREO, CONTRASENA) VALUES (?, ?, ?, ?)'
                self.parametros = (self.idAleatorio, self.nombre_entry.get(), self.correoConId, self.contrasena_entry.get())
                self.db_fila = self.consultar(self.consultando, self.parametros)
                messagebox.showinfo(title="successfully", message="USUARIO REGISTRADO CORRECTAMENTE: \nCORREO: "+self.correoConId+" \nID: "+self.idAleatorio+"")
            else:
                messagebox.showerror(title="Error", message="los campos estan incompletos")
                print("los campos estan incompletos")
        except Exception as error:
            print("un error ha ocurrido: ", error)

    def validar_campos_iniciar(self):
        return len(self.correo_entry.get()) != 0 and len(self.contrasenausuario_verify.get()) != 0
            
    def validar_datos_iniciar(self):

        try:
            if (self.validar_campos_iniciar()):
                self.consultando = "SELECT NOMBRE, CORREO FROM usuarios WHERE CORREO = ? AND CONTRASENA = ?"
                self.parametros = (self.correo_entry.get(), self.contrasenausuario_verify.get())

                self.db_fila = self.consultar(self.consultando, self.parametros)
                
                if(self.db_fila):
                    for usuario in self.db_fila:
                        print(usuario)
                        self.nombreUser = usuario[0]
                        self.iduser =usuario[1]
                        self.id = slice(0, 7)
                        messagebox.showinfo(title="successful", message="SESION INICIADA CORRECTAMENTE: \nNOMBRE: "+self.nombreUser+"\nID: "+self.iduser[self.id]+"")
                else:
                    messagebox.showerror(title="Error", message="Correo o contraseña incorrectos")
            
            else:
                messagebox.showerror(title="Error", message="usuario y contraseña incorrectos")
        except Exception as error:
            print("un error ha ocurrido: " + error)

    def iniciar_sesion(self):
        self.pantalla2 = tk.Toplevel()
        self.pantalla2.title("Aplicacion")
        self.pantalla2.geometry("500x300")
        self.pantalla2.configure(bg="#D8F8FC")
        self.pantalla2.resizable(0,0)

        Canvas(self.pantalla2, bg="white", width=228, height=1400).place(x=0, y=0)

        self.image2 = Image.open("user.png")
        self.resized2 = self.image2.resize((226, 235), Image.LANCZOS)
        self.imagenRender2 = ImageTk.PhotoImage(self.resized2)
        Label(image=self.imagenRender2, master=self.pantalla2).pack(side=tk.LEFT, padx=0.5, pady=0)

        self.correo_entry = StringVar()
        self.contrasenausuario_verify = StringVar()

        Label(self.pantalla2, text="Correo", bg="#D8F8FC").place(relx=0.55, rely=0.18)
        Entry(self.pantalla2, textvariable=self.correo_entry, relief=FLAT, bg="#D8F8FC").place(relx=0.55, rely=0.28)

        Canvas(self.pantalla2, width=164, height=2, bg="black").place(relx=0.55, rely=0.34)

        Label(self.pantalla2, text="Contraseña", bg="#D8F8FC").place(relx=0.55, rely=0.48)
        Entry(self.pantalla2, textvariable=self.contrasenausuario_verify, show="*", relief=FLAT, bg="#D8F8FC").place(relx=0.55, rely=0.58)

        Canvas(self.pantalla2, width=164, height=2, bg="black").place(relx=0.55, rely=0.65)

        Button(self.pantalla2, text="Iniciar Sesion", fg="black", width="14", bd=3, bg="#F9E79F",command=self.validar_datos_iniciar).place(relx=0.72, rely=0.825)
        Button(self.pantalla2, text="Volver", fg="black", width="10", bd=3, bg="#F9E79F", command=self.mostrar_ventana).place(relx=0.53, rely=0.825)

        if(self.pantalla2):
            self.pantalla1.withdraw()

    def registrar(self):
        self.pantalla3 = tk.Toplevel()
        self.pantalla3.title("Aplicacion")
        self.pantalla3.geometry("500x300")
        self.pantalla3.configure(bg="#D8F8FC")
        self.pantalla3.resizable(0,0)

        Canvas(self.pantalla3, bg="white", width=228, height=1400).place(x=0, y=0)

        self.image3 = Image.open("user.png")
        self.resized3 = self.image3.resize((226, 235), Image.LANCZOS)
        self.imagenRender3 = ImageTk.PhotoImage(self.resized3)
        Label(image=self.imagenRender3, master=self.pantalla3).pack(side=tk.LEFT, padx=0.5, pady=0)

        self.nombre_entry = StringVar()
        self.contrasena_entry = StringVar()

        Label(self.pantalla3, text="Nombre de Usuario", bg="#D8F8FC").place(relx=0.55, rely=0.15)
        Entry(self.pantalla3, textvariable=self.nombre_entry, relief=FLAT, bg="#D8F8FC").place(relx=0.55, rely=0.25)
        Canvas(self.pantalla3, width=164, height=2, bg="black").place(relx=0.55, rely=0.33)

        Label(self.pantalla3, text="Contraseña", bg="#D8F8FC").place(relx=0.55, rely=0.38)
        Entry(self.pantalla3, textvariable=self.contrasena_entry, relief=FLAT, bg="#D8F8FC").place(relx=0.55, rely=0.48)
        Canvas(self.pantalla3, width=164, height=2, bg="black").place(relx=0.55, rely=0.55)

        Button(self.pantalla3, text="Registrar", fg="black", width="14", bd=3, bg="#F9E79F", command=self.ingresar_datos_registro).place(relx=0.72, rely=0.825)
        Button(self.pantalla3, text="Volver", fg="black", width="10", bd=3, bg="#F9E79F", command=self.mostrar_ventanaGeneral).place(relx=0.53, rely=0.825)

        if(self.pantalla3):
            self.pantalla1.withdraw()

    def mostrar_ventana(self):
        self.pantalla2.destroy()
        self.pantalla1.deiconify()

    def mostrar_ventanaGeneral(self):
        self.pantalla3.destroy()
        self.pantalla1.deiconify()

ventana = tk.Tk()
app = Aplicacion(ventana)
ventana.mainloop()