import tkinter as tk
from tkinter import ttk,messagebox
import pandas as pd
import numpy as np

class Clasificador:
    def __init__(self, matriz_entrenamiento, matriz_prueba, root):
        self.matriz_entrenamiento = matriz_entrenamiento
        self.matriz_prueba = matriz_prueba
        self.root = root
        self.create_widgets()

    def create_widgets(self):
        # Crear ventana secundaria
        self.ventana = tk.Toplevel(self.root)
        self.ventana.title("Configuración del Clasificador")
        self.ventana.geometry("600x800")
        # Mostrar los vectores
        ttk.Label(self.ventana, text="Vector de Entrenamiento:").pack(anchor="w", padx=10)
        entrenamiento_text = tk.Text(self.ventana, height=5, wrap="word")
        entrenamiento_text.insert("1.0", str(self.matriz_entrenamiento))
        entrenamiento_text.config(state="disabled")
        entrenamiento_text.pack(fill="x", padx=10, pady=5)
        ttk.Label(self.ventana, text="Vector de Prueba:").pack(anchor="w", padx=10)
        prueba_text = tk.Text(self.ventana, height=5, wrap="word")
        prueba_text.insert("1.0", str(self.matriz_prueba))
        prueba_text.config(state="disabled")
        prueba_text.pack(fill="x", padx=10, pady=5)

        # Combobox para tipo de clasificación
        ttk.Label(self.ventana, text="Tipo de Clasificación").pack(anchor="w", padx=10)
        self.clasification_comboBox = ttk.Combobox(self.ventana, state="readonly", values=["Mínima Distancia", "KNN"])
        self.clasification_comboBox.pack(pady=10, padx=10)

        # Combobox para tipo de distancia
        ttk.Label(self.ventana, text="Tipo de Distancia a Utilizar").pack(anchor="w", padx=10)
        self.typeDistance_comboBox = ttk.Combobox(
            self.ventana, 
            state="readonly", 
            values=["Manhattan", "Euclidean"]
        )
        self.typeDistance_comboBox.pack(pady=10, padx=10)

        # Entrada para K en KNN
        ttk.Label(self.ventana, text="Cantidad de Vecinos (K) - Solo para KNN").pack(anchor="w", padx=10)
        self.textBox_KnnCantity = ttk.Entry(self.ventana, width=10)
        self.textBox_KnnCantity.pack(pady=5, padx=10)

        # Botón para aplicar clasificación
        self.button_clasificar = ttk.Button(self.ventana, text="Aplicar Clasificación", command=self.clasificar)
        self.button_clasificar.pack(pady=10)

    def clasificar(self):
        tipo_clasificacion = self.clasification_comboBox.get()
        self.tipo_distancia = self.typeDistance_comboBox.get()
        
        if tipo_clasificacion == "KNN":
            k = self.textBox_KnnCantity.get()
            try:
                self.k = int(k)
                self.clasificar_Knn()
            except ValueError:
                messagebox.showwarning("Error", "ingresa un valor valirdo para K")
        elif tipo_clasificacion == "Mínima Distancia":
            self.clasificar_minima_distancia()

    def clasificar_Knn(self):
        resultados = []
        atributos_entrenamiento = self.matriz_entrenamiento.columns[:-1]
        atributos_prueba = []
        for col in self.matriz_prueba.columns:
            if col in atributos_entrenamiento:
                atributos_prueba.append(col)

        for _, muestra_prueba in self.matriz_prueba.iterrows():
            distancias = []
            for _, muestra_entrenamiento in self.matriz_entrenamiento.iterrows():
                distancia = self.calcular_distancia(muestra_prueba[atributos_prueba],muestra_entrenamiento[atributos_entrenamiento])
                distancias.append((distancia, muestra_entrenamiento.iloc[-1]))
            clase_predicha = self.obtener_clase_mas_cercana(self.k,distancias)
            resultados.append((muestra_prueba.to_dict(), clase_predicha))
        self.mostrar_resultados(resultados)

    def clasificar_minima_distancia(self):
        resultados = []
        promedios_por_clase = self.matriz_entrenamiento.groupby("Clase").mean()
        print(promedios_por_clase)
    
        ##arreglo donde solo nos interesa comparar los atributos que si fueron entrenados
        atributos_prueba = []
        #print(self.matriz_prueba.columns)
        for col in self.matriz_prueba.columns:
            if col in promedios_por_clase.columns:
                atributos_prueba.append(col)

        ### se calculan las distancias de todas las muestras a nuestros promedios de la clase
        for i, muestra_prueba in self.matriz_prueba.iterrows():
            distancias = []
            for clase, promedios in promedios_por_clase.iterrows():
                distancia = self.calcular_distancia(muestra_prueba[atributos_prueba], promedios[atributos_prueba])
                # print(f"distancia: {distancia} a clase {clase}")
                distancias.append((distancia, clase))
            # print(distancias)
            clase_predicha = self.obtener_clase_mas_cercana(1,distancias)
            resultados.append((muestra_prueba.to_dict(), clase_predicha))

        self.mostrar_resultados(resultados)

        ##aqui pa obtener la clase mas cercada comparando n clases cercanas en nuestras distancias desacomodadas
    def obtener_clase_mas_cercana(self, n, distancias):
        for i in range(len(distancias)):
            for j in range(i + 1, len(distancias)):
                if distancias[j][0] < distancias[i][0]:
                    distancias[i], distancias[j] = distancias[j], distancias[i]
        clases_cercanas = [distancias[i][1] for i in range(n)]
        conteo_clases = {}
        for clase in clases_cercanas:
            if clase in conteo_clases:
                conteo_clases[clase] += 1
            else:
                conteo_clases[clase] = 1
        clase_cercana = None
        max_frecuencia = -1
        for clase, frecuencia in conteo_clases.items():
            if frecuencia > max_frecuencia:
                max_frecuencia = frecuencia
                clase_cercana = clase

        return clase_cercana

    def calcular_distancia(self, muestra1, muestra2):
        if self.tipo_distancia == "Euclidean":
            return np.sqrt(np.sum((muestra1 - muestra2) ** 2))
        elif self.tipo_distancia == "Manhattan":
            return np.sum(np.abs(muestra1 - muestra2))

    def mostrar_resultados(self, resultados):
        resultado_ventana = tk.Toplevel(self.ventana)
        resultado_ventana.title("Resultados de Clasificación")

        for muestra, clase in resultados:
            tk.Label(resultado_ventana, text=f"Muestra: {muestra}, Clase Predicha: {clase}").pack(anchor="w", padx=10, pady=2)

