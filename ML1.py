import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd

# Función para cargar el archivo
def cargar_archivo():
    global archivo
    archivo = filedialog.askopenfilename(
        title="Seleccionar archivo"
    )
    if archivo:
        lbl_archivo.config(text=f"Archivo cargado: {archivo.split('/')[-1]}")
    else:
        lbl_archivo.config(text="No se ha cargado ningun archivo")

# Función para aplicar el separador y leer con pandas
def aplicar_separador():
    separador = entry_separador.get()
    if not separador:
        messagebox.showwarning("Debes ingresar un separador.")
        return
    if not archivo:
        messagebox.showwarning("Debes cargar un archivo primero.")
        return
    try:
        # Leer el archivo con pandas
        df = pd.read_csv(archivo, sep=separador)
        messagebox.showinfo("Éxito", f"Archivo leído con éxito con {len(df)} filas y {len(df.columns)} columnas.")
        print(df.head())  # Muestra las primeras filas en la consola para prueba
    except Exception as e:
        messagebox.showerror("Error", f"Error al leer el archivo: {e}")

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Lector de Archivos con Tkinter")
ventana.geometry("500x250")

# Agregar un estilo moderno usando ttk
style = ttk.Style()
style.theme_use("clam")  # Cambiar el tema para diseño moderno

# Botón para cargar el archivo
frame_superior = ttk.Frame(ventana)
frame_superior.pack(pady=10, fill="x", padx=20)

btn_cargar = ttk.Button(frame_superior, text="Cargar Archivo", command=cargar_archivo)
btn_cargar.pack(side="left", padx=10)

lbl_archivo = ttk.Label(frame_superior, text="No se ha cargado ningún archivo", anchor="w")
lbl_archivo.pack(side="top", fill="x", expand=True)

# Separador
frame_separador = ttk.Frame(ventana)
frame_separador.pack(pady=20, padx=20, fill="x")

ttk.Label(frame_separador, text="Separador:").pack(side="left", padx=5)
entry_separador = ttk.Entry(frame_separador, width=10)
entry_separador.pack( padx=5)

btn_aplicar = ttk.Button(frame_separador, text="Aplicar y Leer", command=aplicar_separador)
btn_aplicar.pack( padx=10)

# Añadir un pie de página para estilo
frame_footer = ttk.Frame(ventana)
frame_footer.pack( fill="x", pady=10)

archivo = None

# Ejecutar la ventana principal
ventana.mainloop()
