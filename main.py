import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp

class CalculadoraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora Avanzada")
        self.root.geometry("1200x700")
        self.root.configure(bg='whitesmoke')

        self.funcion_str = tk.StringVar(value="")
        self.x1_str = tk.StringVar(value="")
        self.x2_str = tk.StringVar(value="")
        self.resultado = tk.StringVar()

        self.crear_widgets()
        self.configurar_layout()

    def crear_widgets(self):
        # Entradas y etiquetas
        ttk.Label(self.root, text="Ingrese la función de X:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10)
        ttk.Entry(self.root, textvariable=self.funcion_str, width=50, font=("Arial", 12)).grid(row=0, column=1, padx=10, pady=10, columnspan=3)

        ttk.Label(self.root, text="Ingrese el rango de X:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10)
        ttk.Entry(self.root, textvariable=self.x1_str, width=10, font=("Arial", 12)).grid(row=1, column=1, padx=10, pady=10)
        ttk.Entry(self.root, textvariable=self.x2_str, width=10, font=("Arial", 12)).grid(row=1, column=2, padx=10, pady=10)

        ttk.Label(self.root, text="Resultado:", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=10)
        ttk.Label(self.root, textvariable=self.resultado, width=50, font=("Arial", 14, "bold"), foreground="blue").grid(row=2, column=1, padx=10, pady=10, columnspan=4)

        # Botones
        botones_info = [
            ("Tabla", self.mostrar_tabla),
            ("Pendiente", self.calcular_pendiente),
            ("Valor de X", self.calcular_valor),
            ("Derivar", self.derivar_funcion),
            ("Extremos", self.calcular_extremos),
            ("Limpiar", self.limpiar_campos),
            ("Igualar a 0", self.igualar_a_cero),
            ("Derivar y Igualar a 0", self.derivar_igualar_a_cero),
            ("Créditos", self.mostrar_creditos),
            ("Salir", self.salir)
        ]

        for i, (text, command) in enumerate(botones_info):
            tk.Button(self.root, text=text, command=command, width=15, font=("Arial", 12), foreground="black").grid(row=3, column=i, padx=5, pady=10, sticky="nsew")

        # Tabla de valores
        self.tree = ttk.Treeview(self.root, columns=("X", "f(X)"), show="headings", height=15)
        self.tree.heading("X", text="X")
        self.tree.heading("f(X)", text="f(X)")
        self.tree.grid(row=4, column=0, columnspan=5, padx=10, pady=10, sticky='nsew')

        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        self.scrollbar.grid(row=4, column=5, sticky="ns")
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # Gráfica
        self.figure = plt.Figure(figsize=(6, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().grid(row=4, column=6, columnspan=4, padx=10, pady=10, sticky='nsew')

    def configurar_layout(self):
        # Expandir filas y columnas
        self.root.grid_rowconfigure(4, weight=1)
        self.root.grid_columnconfigure(4, weight=1)

    def limpiar_campos(self):
        self.funcion_str.set("")
        self.x1_str.set("")
        self.x2_str.set("")
        self.resultado.set("")
        self.tree.delete(*self.tree.get_children())
        self.ax.clear()
        self.canvas.draw()

    def mostrar_tabla(self):
        try:
            x = sp.symbols('x')
            funcion = sp.sympify(self.funcion_str.get())
            x1 = int(self.x1_str.get())
            x2 = int(self.x2_str.get())
            self.tree.delete(*self.tree.get_children())
            for x_val in range(x1, x2 + 1):
                f_valor = funcion.subs(x, x_val)
                self.tree.insert("", "end", values=(x_val, f_valor))
            
            # Graficar función
            self.graficar_funcion()
        except Exception as e:
            self.resultado.set(f"Error: {e}")

    def calcular_pendiente(self):
        try:
            x1 = float(simpledialog.askstring("Input", "Ingrese el valor de X1:"))
            x2 = float(simpledialog.askstring("Input", "Ingrese el valor de X2:"))
            x = sp.symbols('x')
            funcion = sp.sympify(self.funcion_str.get())
            f_x1 = funcion.subs(x, x1)
            f_x2 = funcion.subs(x, x2)
            pendiente = (f_x2 - f_x1) / (x2 - x1)
            self.resultado.set(f"Pendiente entre {x1} y {x2}: {pendiente}")
        except Exception as e:
            self.resultado.set(f"Error: {e}")

    def calcular_valor(self):
        try:
            x_val = float(simpledialog.askstring("Input", "Ingrese el valor de X:"))
            x = sp.symbols('x')
            funcion = sp.sympify(self.funcion_str.get())
            f_valor = funcion.subs(x, x_val)
            self.resultado.set(f"f({x_val}) = {f_valor}")
        except Exception as e:
            self.resultado.set(f"Error: {e}")

    def derivar_funcion(self):
        try:
            x = sp.symbols('x')
            funcion = sp.sympify(self.funcion_str.get())
            derivada = sp.diff(funcion, x)
            self.resultado.set(f"Derivada: {derivada}")
        except Exception as e:
            self.resultado.set(f"Error: {e}")

    def graficar_funcion(self):
        try:
            self.ax.clear()
            x_vals = np.linspace(int(self.x1_str.get()), int(self.x2_str.get()), 400)
            funcion = sp.lambdify(sp.symbols('x'), sp.sympify(self.funcion_str.get()), 'numpy')
            y_vals = funcion(x_vals)
            self.ax.plot(x_vals, y_vals, label=self.funcion_str.get())
            self.ax.set_xlabel('x')
            self.ax.set_ylabel('f(x)')
            self.ax.set_title(f'Función f(x) = {self.funcion_str.get()}')
            self.ax.legend()
            self.ax.grid(True)
            self.canvas.draw()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo graficar la función: {e}")

    def calcular_extremos(self):
        try:
            x = sp.symbols('x')
            funcion = sp.sympify(self.funcion_str.get())
            derivada = sp.diff(funcion, x)
            extremos = sp.solve(derivada, x)
            maximos_minimos = [(punto, funcion.subs(x, punto)) for punto in extremos]
            self.resultado.set(f"Extremos: {maximos_minimos}")
        except Exception as e:
            self.resultado.set(f"Error: {e}")

    def igualar_a_cero(self):
        try:
            x = sp.symbols('x')
            funcion = sp.sympify(self.funcion_str.get())
            soluciones = sp.solve(funcion, x)
            self.resultado.set(f"Soluciones: {soluciones}")
        except Exception as e:
            self.resultado.set(f"Error: {e}")

    def derivar_igualar_a_cero(self):
        try:
            x = sp.symbols('x')
            funcion = sp.sympify(self.funcion_str.get())
            derivada = sp.diff(funcion, x)
            soluciones = sp.solve(derivada, x)
            self.resultado.set(f"Soluciones derivada: {soluciones}")
        except Exception as e:
            self.resultado.set(f"Error: {e}")

    def mostrar_creditos(self):
        messagebox.showinfo("Créditos", "Esta calculadora fue desarrollada por Javier Armando Sarmiento Gil.")

    def salir(self):
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraApp(root)
    root.mainloop()
