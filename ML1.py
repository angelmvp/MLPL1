import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd

# Función para cargar el archivo
def cargar_archivo():
    global archivo
    archivo = filedialog.askopenfilename(
        title="Seleccionar archivo de texto"
    )
    if archivo:
        label_archivo.config(text="Archivo cargado")
    else:
        label_archivo.config(text="No se ha cargado ningun archivo")

# Función para aplicar el separador y leer con pandas
def aplicar_separador():
    separador = textBox_separador.get()
    if not separador:
        messagebox.showwarning("Error","Se debe de ingresar un separador.")
        return
    if not archivo:
        messagebox.showwarning("Error","Se debe decargar un archivo primero.")
        return
    try:
        data = pd.read_csv(archivo, sep=separador)
        actualizar_informacion(data)
        messagebox.showinfo("Éxito", "archivo correctamente leido")
    except Exception as e:
        messagebox.showerror("Error", "error al leer el archivo")

def obtener_cantidad_atributos(data):
    return data.shape[1]

# Función para obtener y mostrar la cantidad de patrones
def obtener_cantidad_patrones(data):
    return data.shape[0] + 1

# Función para mostrar una vista previa de la matriz (primeros 5 registros)
def cargar_matriz(data):
    return data.head().to_string(index=False)

# Función para obtener información cuantitativa básica
def obtener_info_cuantitativos(data):
    return data.describe().to_string()

def actualizar_informacion(data):
    for widget in frame_data.winfo_children():
        widget.destroy()

    # Cantidad de atributos
    atributos = obtener_cantidad_atributos(data)
    label_atributos = ttk.Label(frame_data, text=f"Cantidad de Atributos: {atributos}")
    label_atributos.pack()

    # Cantidad de patrones
    patrones = obtener_cantidad_patrones(data)
    label_patrones = ttk.Label(frame_data, text=f"Cantidad de Patrones: {patrones}")
    label_patrones.pack()

    # Matriz de datos
    matriz = cargar_matriz(data)
    label_matriz = ttk.Label(frame_data, text=f"Matriz de Datos:\n{matriz}", justify="left")
    label_matriz.pack(anchor="w")

    # Información cuantitativa
    info_cuantitativa = obtener_info_cuantitativos(data)
    label_info_cuantitativa = ttk.Label(frame_data, text=f"Información Cuantitativa:\n{info_cuantitativa}", justify="left")
    label_info_cuantitativa.pack(anchor="w")

ventana = tk.Tk()
ventana.title("Lector de Archivos con Tkinter")
ventana.geometry("800x450")

style = ttk.Style()
style.theme_use("clam") 



frame_info = ttk.Frame(ventana)
frame_info.pack(pady=18, fill="x",padx=5)
label_info= ttk.Label(frame_info,text="EQUIPO: UyGame\nPractica 1 ML")
label_info.pack(fill="x",expand=False)
frame_superior = ttk.Frame(ventana)
frame_superior.pack(pady=20, fill="y", padx=20)

button_cargar_archivo = ttk.Button(frame_superior, text="Cargar Archivo", command=cargar_archivo)
button_cargar_archivo.pack(pady=10,padx=10)

label_archivo = ttk.Label(frame_superior, text="No se ha cargado ningún archivo", anchor="w")
label_archivo.pack(side="top", fill="y", expand=True)

# Separador
frame_separador = ttk.Frame(ventana)
frame_separador.pack(pady=20, padx=20, fill="y")

ttk.Label(frame_separador, text="Separador:").pack( padx=5)
textBox_separador = ttk.Entry(frame_separador, width=10)
textBox_separador.pack(pady=10,padx=10)

button_aplicar_separador = ttk.Button(frame_separador, text="Aplicar y Leer", command=aplicar_separador)
button_aplicar_separador.pack(pady=10,padx=10)
# style.configure("TButton", padding=6, relief="flat",
#    background="#ABCDEF")
style.configure("TLabel", padding=6, relief="flat",
   background="#B9F09F")

archivo = None

frame_data= ttk.Frame(ventana)
frame_data.pack(pady=20,padx=20,fill="x")


###Aqui va toda la data de las funciones que estan definidas
# Ejecutar la ventana principal
ventana.mainloop()
