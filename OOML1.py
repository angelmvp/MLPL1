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
        self.df_filtrado=None
        self.matriz_entrenamiento = None
        self.matriz_prueba = None
        self.text_vectores=None
        self.boton_info_vectores=None
        self.vectores_generados=None
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
        self.frame_info.pack(side="top", pady=1, fill="x", padx=5)
        label_info = ttk.Label(self.frame_info, text="EQUIPO: UyGame\nPractica 1 ML")
        label_info.pack(fill="x", expand=False)

        ##pa cargar los archivos
        self.frame_superior = ttk.Frame(self.frame_izquierda)
        self.frame_superior.pack(side="top", pady=2, padx=20)
        button_cargar_archivo = ttk.Button(self.frame_superior, text="Cargar Archivo", command=self.cargar_archivo)
        button_cargar_archivo.pack(pady=5, padx=10)
        self.label_archivo = ttk.Label(self.frame_superior, text="No se ha cargado ningún archivo", anchor="w")
        self.label_archivo.pack(side="top", fill="y", expand=True)

        # pal separador
        self.frame_separador = ttk.Frame(self.frame_izquierda)
        self.frame_separador.pack(side="bottom", pady=5, padx=20)
        ttk.Label(self.frame_separador, text="Separador:").pack(padx=5)
        self.textBox_separador = ttk.Entry(self.frame_separador, width=10)
        self.textBox_separador.pack(pady=5, padx=10)
        button_aplicar_separador = ttk.Button(self.frame_separador, text="Aplicar y Leer", command=self.aplicar_separador)
        button_aplicar_separador.pack(pady=2, padx=10)

        # donde se mostraran los atributos
        self.frame_operaciones = ttk.Frame(self.frame_izquierda)
        self.frame_operaciones.pack(side="top", fill="both", expand=True)

        # donde se mostrara toda la data
        self.frame_data = ttk.Frame(self.root)
        self.frame_data.pack(pady=5, padx=20, fill="x")

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
            self.poner_headers()
            self.mostrar_atributos()
            self.actualizar_informacion(self.dataframe)
            
            messagebox.showinfo("Éxito", "Archivo leído correctamente")
        except Exception as e:
            messagebox.showerror("Error", "Error al realizar las operpaciones")

    def actualizar_informacion(self,df):
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
        if self.vectores_generados is not None:
            if self.text_vectores:
                self.text_vectores.destroy()
            if self.boton_info_vectores:
                self.boton_info_vectores.destroy()
            self.text_vectores = tk.Text(self.frame_data, width=80, height=10)
            self.text_vectores.insert(tk.END, self.texto)
            self.text_vectores.pack(pady=10, padx=10)
    def mostrar_atributos(self):
        for widget in self.frame_operaciones.winfo_children():
            widget.destroy()

        self.checkboxes = {}
        for col in self.dataframe.columns:
            var = tk.BooleanVar()
            checkbox = ttk.Checkbutton(self.frame_operaciones, text=col, variable=var)
            checkbox.pack(anchor="w")
            self.checkboxes[col] = var

        ttk.Button(self.frame_operaciones, text="Generar Vectores Verticales", command=self.generar_vectores_verticales).pack(pady=10)
        ttk.Button(self.frame_operaciones, text="Generar Vectores Horizontales", command=self.generar_vectores_horizontales).pack(pady=10)

        ttk.Label(self.frame_operaciones, text="Inicio de Muestra:").pack(pady=2)
        self.entry_inicio_muestra = ttk.Entry(self.frame_operaciones, width=10)
        self.entry_inicio_muestra.pack(pady=2)

        ttk.Label(self.frame_operaciones, text="Cantidad de Muestras:").pack(pady=2)
        self.entry_cantidad_muestras = ttk.Entry(self.frame_operaciones, width=10)
        self.entry_cantidad_muestras.pack(pady=2)
        ## Botón para asignar nombres a los atributos
        self.button_asignar_nombres = ttk.Button(self.frame_operaciones, text="Asignar Nombre a Atributos", command=self.mostrar_panel_asignar_nombres)
        self.button_asignar_nombres.pack(pady=2)
        ##Boton s pa aplicar matrices entrenamiento
        ttk.Button(
            self.frame_operaciones, text="Aplicar Vector a Matriz de Entrenamiento", command=lambda: self.asignar_dataframe_a_matriz(1)
        ).pack(pady=3)
    
        ttk.Button(
            self.frame_operaciones, text="Aplicar Vector a Matriz de Prueba",  command=lambda: self.asignar_dataframe_a_matriz(2)
        ).pack(pady=3)
    def mostrar_panel_asignar_nombres(self):
        if self.dataframe is None:
            messagebox.showwarning("Error", "Primero carga y lee un archivo.")
            return

        ventana_asignar_nombres = tk.Toplevel(self.root)
        ventana_asignar_nombres.title("Asignar Nombres a Atributos")
        ventana_asignar_nombres.geometry("400x400")

        ttk.Label(ventana_asignar_nombres, text="Editar Nombres de Atributos").pack(pady=10)
        
        entry_widgets = []
        for idx, col in enumerate(self.dataframe.columns):
            frame = ttk.Frame(ventana_asignar_nombres)
            frame.pack(fill="x", pady=2)
            
            ttk.Label(frame, text=f"Atributo {col}").pack(side="left", padx=10)
            entry = ttk.Entry(frame)
            entry.insert(0, col)
            entry.pack(side="right", fill="x", expand=True, padx=10)
            entry_widgets.append(entry)

        def aplicar_nombres():
            nuevos_nombres = [entry.get() for entry in entry_widgets]
            self.dataframe.columns = nuevos_nombres
            ventana_asignar_nombres.destroy()
            messagebox.showinfo("Éxito", "Nombres de atributos actualizados.")
            if self.vectores_generados is not None:
                self.actualizar_informacion(self.vectores_generados)
            else:
                self.actualizar_informacion(self.dataframe)
            self.mostrar_atributos()

        ttk.Button(ventana_asignar_nombres, text="Aplicar Nombres", command=aplicar_nombres).pack(pady=20)
    def generar_vectores_verticales(self):
        self._generar_vectores(orientacion="vertical")

    def generar_vectores_horizontales(self):
        self._generar_vectores(orientacion="horizontal")

    def _generar_vectores(self, orientacion: str):
        try:
            inicio = int(self.entry_inicio_muestra.get())
            cantidad = int(self.entry_cantidad_muestras.get())
            if inicio < 0 or cantidad <= 0:
                raise ValueError("Rangos inválidos.")
            seleccionados = []
            for col, var in self.checkboxes.items():
                if var.get():
                    seleccionados.append(col)
            if not seleccionados:
                messagebox.showwarning("Advertencia", "Seleccione mínimo un atributo.")
                return

            self.df_filtrado = self.dataframe.iloc[inicio:inicio + cantidad, :]
            if orientacion == "horizontal":
                self.texto = self.df_filtrado[seleccionados].T.to_string(index=True, header=True)
            else:
                self.texto = self.df_filtrado[seleccionados].to_string(index=False, header=True)

            # Mostrar los vectores generados en el mismo panel
            if self.text_vectores:
                self.text_vectores.destroy()
            if self.boton_info_vectores:
                self.boton_info_vectores.destroy()

            self.vectores_generados = self.df_filtrado[seleccionados]

            self.text_vectores = tk.Text(self.frame_data, width=80, height=10)
            self.text_vectores.insert(tk.END, self.texto)
            self.text_vectores.pack(pady=10, padx=10)

            # Agregar el botón para obtener información de los vectores
            self.boton_info_vectores = ttk.Button(self.frame_data, text="Obtener Información de los Vectores",
                                                command=self.obtener_info_vectores)
            self.boton_info_vectores.pack(pady=10)

        except ValueError:
            messagebox.showerror("Error", "Por favor, introduce valores válidos para inicio y cantidad.")
    def obtener_info_vectores(self):
        if self.vectores_generados is None:
            messagebox.showwarning("Advertencia", "No se han generado vectores.")
            return
        # Actualizar la información mostrada en pantalla con los vectores generados
        self.actualizar_informacion(self.vectores_generados)
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

    def obtener_valores_cualitativos(self,df):
        valores_cualitativos = {}
        columnas_cualitativas = df.select_dtypes(exclude="number").columns
        for col in columnas_cualitativas:
            print(col)

            valores_cualitativos[col] = df[col].unique()
        return valores_cualitativos
    def asignar_dataframe_a_matriz(self, opcion):
        if opcion == 1:
            self.matriz_entrenamiento =self.df_filtrado.copy()
        elif opcion == 2:
            self.matriz_prueba = self.df_filtrado.copy()
        else:
            messagebox.showerror("Error", "Matriz no válida.")

        messagebox.showinfo("Éxito", f"Vectores asignados.")
        print(self.matriz_entrenamiento)
        print(self.matriz_prueba)
    def poner_headers(self):
        headers = [f"Atributo {chr(97 + i)}" for i in range(len(self.dataframe.columns))]
        self.dataframe.columns = headers

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
