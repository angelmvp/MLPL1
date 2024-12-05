import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Practica 1 ML UyGame")
        self.root.geometry("900x650")
        
        self.archivo = None
        self.dataframe = None
        self.checkboxes = {}

        self.set_styles()
        self.create_widgets()

    def set_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", padding=6, relief="flat", background="#B9F09F")

    def create_widgets(self):
        ###Todo el menu en la izquieda para interactuar 
        self.frame_izquierda = ttk.Frame(self.root)
        self.frame_izquierda.pack(side="left")

        self.frame_info = ttk.Frame(self.frame_izquierda)
        self.frame_info.pack(side="top", pady=5, fill="x", padx=5)
        label_info = ttk.Label(self.frame_info, text="EQUIPO: UyGame\nPractica 1 ML")
        label_info.pack(fill="x", expand=False)

        ##pa cargar los archivos
        self.frame_superior = ttk.Frame(self.frame_izquierda)
        self.frame_superior.pack(side="top", pady=10, padx=20)
        button_cargar_archivo = ttk.Button(self.frame_superior, text="Cargar Archivo", command=self.cargar_archivo)
        button_cargar_archivo.pack(pady=10, padx=10)
        self.label_archivo = ttk.Label(self.frame_superior, text="No se ha cargado ningún archivo", anchor="w")
        self.label_archivo.pack(side="top", fill="y", expand=True)

        # pal separador
        self.frame_separador = ttk.Frame(self.frame_izquierda)
        self.frame_separador.pack(side="bottom", pady=20, padx=20)
        ttk.Label(self.frame_separador, text="Separador:").pack(padx=5)
        self.textBox_separador = ttk.Entry(self.frame_separador, width=10)
        self.textBox_separador.pack(pady=5, padx=10)
        button_aplicar_separador = ttk.Button(self.frame_separador, text="Aplicar y Leer", command=self.aplicar_separador)
        button_aplicar_separador.pack(pady=2, padx=10)

        # donde se mostraran los atributos
        self.frame_atributos = ttk.Frame(self.frame_izquierda)
        self.frame_atributos.pack(side="top", fill="both", expand=True)

        # donde se mostrara toda la data
        self.frame_data = ttk.Frame(self.root)
        self.frame_data.pack(pady=20, padx=20, fill="x")

    def cargar_archivo(self):
        self.archivo = filedialog.askopenfilename(title="Seleccionar archivo de texto")
        if self.archivo:
            self.label_archivo.config(text="Se ha cargado el archivo")
        else:
            self.label_archivo.config(text="No se ha cargado nada")

    def aplicar_separador(self):
        separador = self.textBox_separador.get()
        if not separador:
            messagebox.showwarning("Error", "Ingresa un separador.")
            return
        if not self.archivo:
            messagebox.showwarning("Error", "Primero carga el archivo")
            return
        try:
            self.dataframe = pd.read_csv(self.archivo, sep=separador, header=None)
            self.actualizar_informacion(self.dataframe)
            self.mostrar_atributos(self.dataframe)
            messagebox.showinfo("Éxito", "Archivo leído correctamente")
        except Exception as e:
            messagebox.showerror("Error", "Error al leer el archivo")

    def actualizar_informacion(self, df):
        self.poner_headers(df)
        for widget in self.frame_data.winfo_children():
            widget.destroy()

        ttk.Label(self.frame_data, text=f"Cantidad de Atributos: {len(df.columns)}").pack()
        ttk.Label(self.frame_data, text=f"Cantidad de Patrones: {len(df)}").pack()

        estadisticas = self.obtener_estadisticas(df)
        if estadisticas:
            ttk.Label(self.frame_data, text="Estadísticas de Atributos Cuantitativos:").pack(anchor="w")
            for col, stats in estadisticas.items():
                ttk.Label(self.frame_data, text=f"  {col} : {stats}").pack(anchor="w")

        valores_cualitativos = self.obtener_valores_cualitativos(df)
        if valores_cualitativos:
            ttk.Label(self.frame_data, text="Valores De los Atributos Cualitativos:").pack(anchor="w")
            for col, valores in valores_cualitativos.items():
                ttk.Label(self.frame_data, text=f"  {col}: {', '.join(map(str, valores))}").pack(anchor="w")

    def mostrar_atributos(self, df):
        for widget in self.frame_atributos.winfo_children():
            widget.destroy()

        self.checkboxes = {}
        for col in df.columns:
            var = tk.BooleanVar()
            checkbox = ttk.Checkbutton(self.frame_atributos, text=col, variable=var)
            checkbox.pack(anchor="w")
            self.checkboxes[col] = var

        ttk.Button(self.frame_atributos, text="Generar Vectores Verticales", command=self.generar_vectores_verticales).pack(pady=10)
        ttk.Button(self.frame_atributos, text="Generar Vectores Horizontales", command=self.generar_vectores_horizontales).pack(pady=10)

    def generar_vectores_verticales(self):
        self._generar_vectores(orientacion="vertical")

    def generar_vectores_horizontales(self):
        self._generar_vectores(orientacion="horizontal")

    def _generar_vectores(self, orientacion: str):
        seleccionados = []
        for col, var in self.checkboxes.items(): 
            if var.get():
                seleccionados.append(col)
        if not seleccionados:
            messagebox.showwarning("Advertencia", "Seleccione mínimo un atributo.")
            return

        ventana_vectores = tk.Toplevel(self.root)
        ventana_vectores.title(f"Generación de Vectores {orientacion}")
        ventana_vectores.geometry("500x300")

        ttk.Label(ventana_vectores, text="Atributos Seleccionados:").pack(pady=10)
        dataframe_seleccionado = self.dataframe[seleccionados]
        
        if orientacion == "horizontal":
            texto = dataframe_seleccionado.T.to_string(index=True, header=True) 
        else:
            texto= dataframe_seleccionado.to_string(index=False, header=True)

        text_widget = tk.Text(ventana_vectores, width=80, height=20)
        text_widget.insert(tk.END, texto)
        text_widget.pack(expand=True)

    def obtenerMin(self,columna):
        minimo = columna.iloc[0]  
        for valor in columna:
            if valor < minimo:
                minimo = valor
        return minimo

    def obtenerMax(self,columna):
        maximo = columna.iloc[0]  
        for valor in columna:
            if valor > maximo:
                maximo = valor
        return maximo

    def obtenerMean(self,columna):
        suma = 0
        contador = 0
        for valor in columna:
            suma += valor
            contador += 1
        return suma / contador if contador > 0 else 0
    def obtener_estadisticas(self,df):
        estadisticas = {}
        columnas_numericas = df.select_dtypes(include="number").columns
        
        for col in columnas_numericas:
            min_val = self.obtenerMin(df[col])
            max_val = self.obtenerMax(df[col])
            mean_val = self.obtenerMean(df[col])
            estadisticas[col] = {
                "Min": min_val,
                "Max": max_val,
                "Mean": f"{mean_val:.4f}",
            }
        return estadisticas

    def obtener_valores_cualitativos(self, df):
        valores_cualitativos = {}
        columnas_cualitativas = df.select_dtypes(exclude="number").columns
        for col in columnas_cualitativas:
            print(col)

            valores_cualitativos[col] = df[col].unique()
        return valores_cualitativos

    def poner_headers(self, df):
        headers = [f"Atributo {chr(97 + i)}" for i in range(len(df.columns))]
        df.columns = headers


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
