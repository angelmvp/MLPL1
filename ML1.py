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
        dataframe = pd.read_csv(archivo, sep=separador, header=None)
        actualizar_informacion(dataframe)
        mostrar_atributos(dataframe)
        messagebox.showinfo("Éxito", "Archivo correctamente leído")
    except Exception as e:
        messagebox.showerror("Error", "Error al leer el archivo")


# Funciones adicionales para estadísticas y cualitativos
def obtener_estadisticas(df):
    estadisticas = {}
    columnas_numericas = df.select_dtypes(include="number").columns
    for col in columnas_numericas:
        min_val = df[col].min()
        max_val = df[col].max()
        mean_val = df[col].mean()
        estadisticas[col] = {
            "Min": min_val,
            "Max": max_val,
            "Mean": f"{mean_val:.4f}",
        }
    return estadisticas

def obtener_valores_cualitativos(df):
    valores_cualitativos = {}
    columnas_cualitativas = df.select_dtypes(exclude="number").columns
    for col in columnas_cualitativas:
        valores_cualitativos[col] = df[col].unique()
    return valores_cualitativos

def poner_headers(df):
    headers = []
    for i in range(len(df.columns)):
        headers.append(f"Atributo {chr(97 + i)}")
    df.columns = headers

# Función para actualizar la información
def actualizar_informacion(df):
    poner_headers(df)
    for widget in frame_data.winfo_children():
        widget.destroy()

    ttk.Label(frame_data, text=f"Cantidad de Atributos: {len(df.columns)}").pack()
    ttk.Label(frame_data, text=f"Cantidad de Patrones: {len(df)}").pack()

    estadisticas = obtener_estadisticas(df)
    if estadisticas:
        ttk.Label(frame_data, text="Estadísticas de Atributos Cuantitativos:").pack(anchor="w")
        for col, stats in estadisticas.items():
            ttk.Label(frame_data, text=f"  {col} : {stats}").pack(anchor="w")

    valores_cualitativos = obtener_valores_cualitativos(df)
    if valores_cualitativos:
        ttk.Label(frame_data, text="Valores Únicos de Atributos Cualitativos:").pack(anchor="w")
        for col, valores in valores_cualitativos.items():
            ttk.Label(frame_data, text=f"  {col}: {', '.join(map(str, valores))}").pack(anchor="w")

def mostrar_atributos(df):
    global checkboxes
    for widget in frame_atributos.winfo_children():
        widget.destroy()
    
    checkboxes = {}
    for col in df.columns:
        var = tk.BooleanVar()
        checkbox = ttk.Checkbutton(frame_atributos, text=col, variable=var)
        checkbox.pack(anchor="w")
        checkboxes[col] = var

    button_generar_vectores = ttk.Button(frame_atributos, text="Generar Vectores", command=generar_vectores)
    button_generar_vectores.pack(pady=10)



def generar_vectores():
    seleccionados = []
    for col, var in checkboxes.items():
        if var.get(): 
            seleccionados.append(col) 
    if not seleccionados:
        messagebox.showwarning("Advertencia", "Seleccione minumo un atributo.")
        return
    #print(seleccionados)
    ventana_vectores = tk.Toplevel(ventana)
    ventana_vectores.title("Generación de Vectores")
    ventana_vectores.geometry("500x300")

    ttk.Label(ventana_vectores, text="Atributos Seleccionados:").pack(pady=10)
    dataframe_seleccionado = dataframe[seleccionados]
    print(dataframe_seleccionado)
    texto = dataframe_seleccionado.to_string(index=False, header=True)
    print(texto)
    text_widget = tk.Text(ventana_vectores, width=80, height=20)
    text_widget.insert(tk.END, texto)
    text_widget.pack(expand=True)

ventana = tk.Tk()
ventana.title("Practica 1 ML UyGame")
ventana.geometry("900x650")

style = ttk.Style()
style.theme_use("clam")

frame_izquierda = ttk.Frame(ventana)
frame_izquierda.pack(side="left")

frame_info = ttk.Frame(frame_izquierda)
frame_info.pack(side="top", pady=5, fill="x", padx=5)
label_info = ttk.Label(frame_info, text="EQUIPO: UyGame\nPractica 1 ML")
label_info.pack(fill="x", expand=False)

frame_superior = ttk.Frame(frame_izquierda)
frame_superior.pack(side="top", pady=10, padx=20)

button_cargar_archivo = ttk.Button(frame_superior, text="Cargar Archivo", command=cargar_archivo)
button_cargar_archivo.pack(pady=10, padx=10)

label_archivo = ttk.Label(frame_superior, text="No se ha cargado ningún archivo", anchor="w")
label_archivo.pack(side="top", fill="y", expand=True)

# Separador
frame_separador = ttk.Frame(frame_izquierda)
frame_separador.pack(side="bottom", pady=20, padx=20)

ttk.Label(frame_separador, text="Separador:").pack(padx=5)
textBox_separador = ttk.Entry(frame_separador, width=10)
textBox_separador.pack(pady=5, padx=10)

button_aplicar_separador = ttk.Button(frame_separador, text="Aplicar y Leer", command=aplicar_separador)
button_aplicar_separador.pack(pady=2, padx=10)

style.configure("TLabel", padding=6, relief="flat", background="#B9F09F")

frame_atributos = ttk.Frame(frame_izquierda)
frame_atributos.pack(side="top", fill="both", expand=True)

archivo = None
dataframe = None
checkboxes = {}

frame_data = ttk.Frame(ventana)
frame_data.pack(pady=20, padx=20, fill="x")

ventana.mainloop()
