import tkinter as tk
from tkinter import ttk

class Clasificador():
    def __init__(self, matriz_entrenamiento, matriz_prueba, root):
        self.matriz_entrenamiento = matriz_entrenamiento
        self.matriz_prueba = matriz_prueba
        self.root = root
        self.mostrar_ui()
    
    def mostrar_ui(self):
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
        self.clasification_comboBox = ttk.Combobox(
            self.ventana, 
            state="readonly", 
            values=["Mínima Distancia", "KNN"]
        )
        self.clasification_comboBox.bind("<<ComboboxSelected>>", self.on_clasification_change)
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
        self.button_clasificar = ttk.Button(
            self.ventana, 
            text="Aplicar Clasificación", 
            command=self.clasificar
        )
        self.button_clasificar.pack(pady=10)
        
        # Botón para cerrar ventana
        button_cerrar = ttk.Button(self.ventana, text="Cerrar", command=self.ventana.destroy)
        button_cerrar.pack(pady=10)
        
        # Entrada para cantidad de vecinos (oculta inicialmente)
        self.textBox_KnnCantity = ttk.Entry(self.ventana, width=10)
    
    def on_clasification_change(self, event):
        # Mostrar o esconder la entrada de cantidad de vecinos
        selected = self.clasification_comboBox.get()
        if selected == "KNN":
            ttk.Label(self.ventana, text="Cantidad de Vecinos (K)").pack(anchor="w", padx=10)
            self.textBox_KnnCantity.pack(pady=5, padx=10)
        else:
            self.textBox_KnnCantity.pack_forget()
    
    def clasificar(self):
        # Función de clasificación (por implementar)
        print("Aplicando clasificación...")
        print(f"Tipo de clasificación: {self.clasification_comboBox.get()}")
        print(f"Tipo de distancia: {self.typeDistance_comboBox.get()}")
        if self.clasification_comboBox.get() == "KNN":
            k = self.textBox_KnnCantity.get()
            print(f"Cantidad de vecinos (K): {k}")
