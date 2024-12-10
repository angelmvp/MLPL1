import tkinter as tk
from tkinter import ttk

class Clasificador():
    def __init__(self, matriz_entrenamiento, matriz_prueba, root):
        self.matriz_entrenamiento = matriz_entrenamiento
        self.matriz_prueba = matriz_prueba
        self.root = root
        self.create_widgets()
    
    def create_widgets(self):
        # Crear ventana secundaria
        self.ventana = tk.Toplevel(self.root)
        self.ventana.title("Configuración del Clasificador")
        
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
        
        # Botón para aplicar clasificación
        self.button_clasificar = ttk.Button(self.ventana,text="Aplicar Clasificación",command=self.clasificar)
        self.button_clasificar.pack(pady=10)
        self.label_Knn=ttk.Label(self.ventana, text="Cantidad de Vecinos (K)").pack(anchor="w", padx=10)
        self.textBox_KnnCantity = ttk.Entry(self.ventana, width=10)
    
    def clasificar(self):
        print("Aplicando clasificación...")
        tipo_clasificacion= self.clasification_comboBox.get()
        self.tipo_distancia=self.typeDistance_comboBox.get()
        if tipo_clasificacion == "KNN":
            self.clasificar_Knn()
        else:
            self.clasificar_minima_distancia()
        if self.clasification_comboBox.get() == "KNN":
            self.k = self.textBox_KnnCantity.get()
            print(f"Cantidad de vecinos (K): {self.k}")
    def clasificar_Knn(self):
        print(f"Knn con distancia {self.tipo_distancia} y vecinos {self.k}")
        pass
    def clasificar_minima_distancia(self):
        print(f"minimaDistancia con distancia {self.tipo_distancia}")
        pass
    def calcular_distancia_euclidiana(self,muestra1, muestras):
        pass
    def calcular_distancia_manhattan(self,muestra1, muestra2):
        pass

