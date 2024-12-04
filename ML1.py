import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd

# Función para cargar el archivo
def cargar_archivo():
    global archivo
    archivo = filedialog.askopenfilename(
        title="Seleccionar archivo de texto",
    )
    if archivo:
        label_archivo.config(text="Se ha cargado el archivo")
    else:
        label_archivo.config(text="No se ha cargado ningún archivo")

# Función para aplicar el separador y leer el archivo
def aplicar_separador():
    separador = textBox_separador.get()
    if not separador:
        messagebox.showwarning("Error", "Se debe ingresar un separador.")
        return
    if not archivo:
        messagebox.showwarning("Error", "Se debe cargar un archivo primero.")
        return
    try:
        global dataframe
        dataframe = pd.read_csv(archivo, sep=separador)
        actualizar_informacion(dataframe)
        messagebox.showinfo("Éxito", "Archivo correctamente leído")
    except Exception as e:
        messagebox.showerror("Error", "Error al leer el archivo")


def obtener_tipos_atributos(df):
    return {col: "Cuantitativo" if pd.api.types.is_numeric_dtype(df[col]) else "Cualitativo" for col in df.columns}

def obtener_valores_cualitativos(df):
    valores_cualitativos = {}

    columnas_cualitativas = df.select_dtypes(exclude="number").columns
    for col in columnas_cualitativas:
        # Guardar los valores únicos de la columna en el diccionario
        valores_cualitativos[col] = df[col].unique()  
    return valores_cualitativos

# Función para obtener estadísticas de atributos cuantitativos
def obtenerMin(columna):
    minimo = columna.iloc[0]  
    for valor in columna:
        if valor < minimo:
            minimo = valor
    return minimo

def obtenerMax(columna):
    maximo = columna.iloc[0]  
    for valor in columna:
        if valor > maximo:
            maximo = valor
    return maximo

def obtenerMean(columna):
    suma = 0
    contador = 0
    for valor in columna:
        suma += valor
        contador += 1
    return suma / contador if contador > 0 else 0
def obtener_estadisticas(df):
    estadisticas = {}
    columnas_numericas = df.select_dtypes(include="number").columns
    
    for col in columnas_numericas:
        min_val = obtenerMin(df[col])
        max_val = obtenerMax(df[col])
        mean_val = obtenerMean(df[col])
        estadisticas[col] = {
            "Min": min_val,
            "Max": max_val,
            "Mean": mean_val,
        }
    return estadisticas
def poner_headers(df):
    headers = []
    for i in range(len(df.columns)):
        headers.append(f"Atributo {i}")
    df.columns = headers
# Función para actualizar la información en el frame_data
def actualizar_informacion(df):
    poner_headers(df)
    print(df.columns)
    for widget in frame_data.winfo_children():
        widget.destroy()

    # Cantidad de atributos
    ttk.Label(frame_data, text=f"Cantidad de Atributos: {len(df.columns)}").pack()
    # Cantidad de patrones
    ttk.Label(frame_data, text=f"Cantidad de Patrones: {len(df)+1}").pack()

    # Estadísticas de atributos cuantitativos
    estadisticas = obtener_estadisticas(df)
    if estadisticas:
        ttk.Label(frame_data, text="Estadísticas de Atributos Cuantitativos:").pack(anchor="w")
        for col, stats in estadisticas.items():
            ttk.Label(frame_data, text=f"  {col} : Estadisticas: {stats}").pack(anchor="w")

    # Valores de atributos cualitativos
    valores_cualitativos = obtener_valores_cualitativos(df)
    if valores_cualitativos:
        ttk.Label(frame_data, text="Valores Únicos de Atributos Cualitativos:").pack(anchor="w")
        for col, valores in valores_cualitativos.items():
            ttk.Label(frame_data, text=f"  {col}: {', '.join(map(str, valores[:]))}").pack(anchor="w", padx=20)



ventana = tk.Tk()
ventana.title("Practica 1 ML UyGame")
ventana.geometry("800x450")

style = ttk.Style()
style.theme_use("clam")

frame_info = ttk.Frame(ventana)
frame_info.pack(pady=5, fill="x", padx=5)
label_info = ttk.Label(frame_info, text="EQUIPO: UyGame\nPractica 1 ML")
label_info.pack(fill="x", expand=False)

frame_superior = ttk.Frame(ventana)
frame_superior.pack(pady=10, fill="y", padx=20)

button_cargar_archivo = ttk.Button(frame_superior, text="Cargar Archivo", command=cargar_archivo)
button_cargar_archivo.pack(pady=10, padx=10)

label_archivo = ttk.Label(frame_superior, text="No se ha cargado ningún archivo", anchor="w")
label_archivo.pack(side="top", fill="y", expand=True)

# Separador
frame_separador = ttk.Frame(ventana)
frame_separador.pack(pady=20, padx=20, fill="y")

ttk.Label(frame_separador, text="Separador:").pack(padx=5)
textBox_separador = ttk.Entry(frame_separador, width=10)
textBox_separador.pack(pady=5, padx=10)

button_aplicar_separador = ttk.Button(frame_separador, text="Aplicar y Leer", command=aplicar_separador)
button_aplicar_separador.pack(pady=2, padx=10)

style.configure("TLabel", padding=6, relief="flat", background="#B9F09F")

archivo = None
dataframe = None

frame_data = ttk.Frame(ventana)
frame_data.pack(pady=20, padx=20, fill="x")

# Ejecutar la ventana principal
ventana.mainloop()
