"""
=====================================================================
CALCULADORA DE AUMENTOS Y DESCUENTOS SUCESIVOS
Versión 3.0 - Robusta (funciona con o sin voz)
=====================================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
import threading

# ============================================================
# INTENTAR CARGAR LA VOZ DE FORMA SEGURA
# ============================================================
VOZ_ACTIVA = False
motor_voz = None

try:
    import pythoncom
    import pywintypes
    import pyttsx3
    motor_voz = pyttsx3.init()
    VOZ_ACTIVA = True
    print("✅ Voz inicializada correctamente")
except Exception as e:
    print(f"⚠️  Voz no disponible: {e}")
    print("   El aplicativo funcionará en modo silencioso.")


# ============================================================
# FUNCIONES DE VOZ (simplificadas)
# ============================================================
def hablar(texto):
    """Habla solo si la voz está activa"""
    if not VOZ_ACTIVA or not motor_voz:
        return
    def _hablar():
        try:
            motor_voz.say(texto)
            motor_voz.runAndWait()
        except:
            pass
    threading.Thread(target=_hablar, daemon=True).start()

def voz_bienvenida():
    hablar("Bienvenido a la Calculadora de Aumentos y Descuentos Sucesivos.")

def voz_resultado(vi, vf, mu, variacion, tipo):
    if "AUMENTO" in tipo.upper():
        hablar(f"Partimos de {vi} soles. Precio final {vf} soles. Aumento del {variacion} por ciento.")
    elif "DESCUENTO" in tipo.upper():
        hablar(f"Partimos de {vi} soles. Precio final {vf} soles. Descuento del {variacion} por ciento.")
    else:
        hablar(f"Precio final {vf} soles. Sin variación.")

def voz_acierto():
    frases = ["¡Excelente!", "¡Muy bien!", "¡Correcto!", "¡Perfecto!", "¡Buen trabajo!"]
    hablar(random.choice(frases))

def voz_error():
    hablar("No es correcto. Recuerda usar multiplicadores, no sumar porcentajes.")

def voz_consejo():
    consejos = [
        "Nunca sumes los porcentajes directamente. Usa multiplicadores.",
        "El multiplicador único es el producto de todos los multiplicadores.",
        "Para aumentos: multiplicador = 1 + porcentaje/100",
        "Para descuentos: multiplicador = 1 - porcentaje/100",
        "Dos descuentos del 20 y 10 por ciento no equivalen al 30 por ciento."
    ]
    hablar(random.choice(consejos))


# ============================================================
# CLASE PRINCIPAL
# ============================================================
class CalculadoraAumentosDescuentos:
    def __init__(self, root):
        self.root = root
        self.root.title("🌽 Calculadora de Aumentos y Descuentos - Feria Rural")
        self.root.geometry("850x700")
        self.root.configure(bg="#f5f0e1")

        self.vi = tk.DoubleVar(value=0.0)
        self.c1 = tk.DoubleVar(value=0.0)
        self.c2 = tk.DoubleVar(value=0.0)
        self.c3 = tk.DoubleVar(value=0.0)

        self.resultado_vf = tk.StringVar(value="")
        self.resultado_mu = tk.StringVar(value="")
        self.resultado_var = tk.StringVar(value="")
        self.resultado_tipo = tk.StringVar(value="")

        self.problema_actual = None
        self.solucion_actual = None

        self.crear_interfaz()
        self.root.after(500, voz_bienvenida)
        self.root.protocol("WM_DELETE_WINDOW", self.cerrar)

    def crear_interfaz(self):
        # Título
        ft = tk.Frame(self.root, bg="#5d4037", padx=10, pady=10)
        ft.pack(fill="x")
        tk.Label(ft, text="🌽 CALCULADORA DE AUMENTOS Y DESCUENTOS SUCESIVOS",
                font=("Arial", 16, "bold"), bg="#5d4037", fg="#fff8e1").pack()
        tk.Label(ft, text='"Decisiones inteligentes para la feria y la chacra"',
                font=("Arial", 11, "italic"), bg="#5d4037", fg="#ffcc80").pack()
        if not VOZ_ACTIVA:
            tk.Label(ft, text="🔇 Modo silencioso", font=("Arial", 8),
                    bg="#5d4037", fg="#ffcc80").pack()

        # Pestañas
        estilo = ttk.Style()
        estilo.theme_use('default')
        estilo.configure('TNotebook.Tab', font=("Arial", 11, "bold"), padding=[15, 5])

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, padx=15, fill="both", expand=True)

        self.tab1 = tk.Frame(self.notebook, bg="#f5f0e1")
        self.tab2 = tk.Frame(self.notebook, bg="#f5f0e1")
        self.tab3 = tk.Frame(self.notebook, bg="#f5f0e1")
        self.tab4 = tk.Frame(self.notebook, bg="#f5f0e1")

        self.notebook.add(self.tab1, text="🧮 CALCULAR")
        self.notebook.add(self.tab2, text="📚 ENSEÑAR")
        self.notebook.add(self.tab3, text="🎲 PRACTICAR")
        self.notebook.add(self.tab4, text="📈 DIAGRAMA")

        self.pestana_calcular()
        self.pestana_ensenar()
        self.pestana_practicar()
        self.pestana_diagrama()

        self.estado = tk.Label(self.root, text="✅ Listo | Presiona CALCULAR",
                              font=("Arial", 9), bg="#e8e0d5", fg="#5d4037",
                              anchor="w", padx=15, pady=5)
        self.estado.pack(side="bottom", fill="x")

    def pestana_calcular(self):
        f = self.tab1
        fe = tk.LabelFrame(f, text="📥 DATOS DE ENTRADA", font=("Arial", 12, "bold"),
                          bg="#f5f0e1", fg="#5d4037", padx=15, pady=15)
        fe.pack(pady=10, padx=20, fill="x")

        tk.Label(fe, text="Valor inicial (S/):", bg="#f5f0e1", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=8)
        tk.Entry(fe, textvariable=self.vi, font=("Arial", 11), width=15, justify="center", bg="white").grid(row=0, column=1, padx=10)

        tk.Label(fe, text="Cambio 1 (%):", bg="#f5f0e1", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=8)
        tk.Entry(fe, textvariable=self.c1, font=("Arial", 11), width=15, justify="center", bg="white").grid(row=1, column=1, padx=10)
        tk.Label(fe, text="(+ aumento, - descuento)", bg="#f5f0e1", font=("Arial", 8), fg="#8d6e63").grid(row=1, column=2, sticky="w")

        tk.Label(fe, text="Cambio 2 (%):", bg="#f5f0e1", font=("Arial", 10)).grid(row=2, column=0, sticky="w", pady=8)
        tk.Entry(fe, textvariable=self.c2, font=("Arial", 11), width=15, justify="center", bg="white").grid(row=2, column=1, padx=10)
        tk.Label(fe, text="(0 si no hay)", bg="#f5f0e1", font=("Arial", 8), fg="#8d6e63").grid(row=2, column=2, sticky="w")

        tk.Label(fe, text="Cambio 3 (%):", bg="#f5f0e1", font=("Arial", 10)).grid(row=3, column=0, sticky="w", pady=8)
        tk.Entry(fe, textvariable=self.c3, font=("Arial", 11), width=15, justify="center", bg="white").grid(row=3, column=1, padx=10)
        tk.Label(fe, text="(0 si no hay)", bg="#f5f0e1", font=("Arial", 8), fg="#8d6e63").grid(row=3, column=2, sticky="w")

        fb = tk.Frame(f, bg="#f5f0e1")
        fb.pack(pady=10)
        tk.Button(fb, text="🧮 CALCULAR", font=("Arial", 12, "bold"), bg="#4caf50", fg="white",
                padx=20, pady=10, command=self.calcular).pack(side="left", padx=5)
        tk.Button(fb, text="🔄 LIMPIAR", font=("Arial", 11), bg="#ff9800", fg="white",
                padx=15, pady=10, command=self.limpiar).pack(side="left", padx=5)
        tk.Button(fb, text="📋 VER TABLA", font=("Arial", 11), bg="#2196f3", fg="white",
                padx=15, pady=10, command=self.ver_tabla).pack(side="left", padx=5)
        tk.Button(fb, text="💡 CONSEJO", font=("Arial", 11), bg="#9c27b0", fg="white",
                padx=15, pady=10, command=voz_consejo).pack(side="left", padx=5)

        fr = tk.LabelFrame(f, text="📊 RESULTADOS", font=("Arial", 12, "bold"),
                          bg="#f5f0e1", fg="#5d4037", padx=15, pady=15)
        fr.pack(pady=10, padx=20, fill="x")
        tk.Label(fr, text="Precio final:", bg="#f5f0e1", font=("Arial", 11, "bold")).grid(row=0, column=0, sticky="w", pady=8)
        tk.Label(fr, textvariable=self.resultado_vf, bg="#f5f0e1", font=("Arial", 16, "bold"), fg="#2e7d32").grid(row=0, column=1, padx=20, pady=8)
        tk.Label(fr, text="Multiplicador único:", bg="#f5f0e1", font=("Arial", 11, "bold")).grid(row=1, column=0, sticky="w", pady=8)
        tk.Label(fr, textvariable=self.resultado_mu, bg="#f5f0e1", font=("Arial", 14), fg="#1565c0").grid(row=1, column=1, padx=20, pady=8)
        tk.Label(fr, text="Variación total:", bg="#f5f0e1", font=("Arial", 11, "bold")).grid(row=2, column=0, sticky="w", pady=8)
        self.lbl_var = tk.Label(fr, textvariable=self.resultado_var, bg="#f5f0e1", font=("Arial", 16, "bold"))
        self.lbl_var.grid(row=2, column=1, padx=20, pady=8)
        tk.Label(fr, text="Tipo:", bg="#f5f0e1", font=("Arial", 11, "bold")).grid(row=3, column=0, sticky="w", pady=8)
        self.lbl_tipo = tk.Label(fr, textvariable=self.resultado_tipo, bg="#f5f0e1", font=("Arial", 14, "bold"))
        self.lbl_tipo.grid(row=3, column=1, padx=20, pady=8)

    def pestana_ensenar(self):
        f = self.tab2
        tk.Label(f, text="📚 MODO ENSEÑANZA", font=("Arial", 14, "bold"),
                bg="#f5f0e1", fg="#5d4037").pack(pady=15)
        self.txt_ensenar = tk.Text(f, height=22, width=90, font=("Consolas", 10),
                                   bg="#fff8e1", fg="#3e2723", padx=15, pady=15,
                                   state="disabled", wrap="word")
        self.txt_ensenar.pack(pady=10, padx=20)
        tk.Button(f, text="▶️ INICIAR EJEMPLO GUIADO", font=("Arial", 13, "bold"),
                bg="#4caf50", fg="white", padx=25, pady=12,
                command=self.modo_ensenar).pack(pady=15)

    def pestana_practicar(self):
        f = self.tab3
        tk.Label(f, text="🎲 MODO PRÁCTICA", font=("Arial", 14, "bold"),
                bg="#f5f0e1", fg="#5d4037").pack(pady=15)
        self.txt_enunciado = tk.Text(f, height=5, width=85, font=("Arial", 12),
                                     bg="#fff8e1", fg="#3e2723", padx=15, pady=15,
                                     state="disabled", wrap="word")
        self.txt_enunciado.pack(pady=10, padx=20)

        fr = tk.Frame(f, bg="#f5f0e1")
        fr.pack(pady=15)
        tk.Label(fr, text="Tu respuesta (S/):", bg="#f5f0e1",
                font=("Arial", 12, "bold")).pack(side="left", padx=10)
        self.entrada_respuesta = tk.Entry(fr, font=("Arial", 14), width=15,
                                          justify="center", bg="white")
        self.entrada_respuesta.pack(side="left", padx=10)
        self.entrada_respuesta.bind("<Return>", lambda e: self.verificar())

        fb = tk.Frame(f, bg="#f5f0e1")
        fb.pack(pady=15)
        tk.Button(fb, text="🎲 NUEVO PROBLEMA", font=("Arial", 13, "bold"),
                bg="#9c27b0", fg="white", padx=25, pady=12,
                command=self.nuevo_problema).pack(side="left", padx=10)
        tk.Button(fb, text="✅ VERIFICAR", font=("Arial", 13, "bold"),
                bg="#4caf50", fg="white", padx=25, pady=12,
                command=self.verificar).pack(side="left", padx=10)
        tk.Button(fb, text="💡 SOLUCIÓN", font=("Arial", 12),
                bg="#2196f3", fg="white", padx=20, pady=12,
                command=self.ver_solucion).pack(side="left", padx=10)

    def pestana_diagrama(self):
        f = self.tab4
        tk.Label(f, text="📈 DIAGRAMA DE FLUJO", font=("Arial", 14, "bold"),
                bg="#f5f0e1", fg="#5d4037").pack(pady=15)
        self.canvas = tk.Canvas(f, width=800, height=450, bg="#fff8e1",
                               highlightthickness=2, highlightbackground="#5d4037")
        self.canvas.pack(pady=10, padx=20)
        tk.Button(f, text="🔄 ACTUALIZAR", font=("Arial", 12, "bold"),
                bg="#2196f3", fg="white", padx=20, pady=10,
                command=self.dibujar).pack(pady=10)

    # ============================================================
    # LÓGICA DE CÁLCULO
    # ============================================================
    def _calcular(self):
        vi = self.vi.get()
        multiplicadores = []
        valores = [vi]
        actual = vi
        for c in [self.c1.get(), self.c2.get(), self.c3.get()]:
            if c != 0:
                m = 1 + c/100
                multiplicadores.append(m)
                actual *= m
                valores.append(round(actual, 2))
        if not multiplicadores:
            return None
        mu = round(eval('*'.join(map(str, multiplicadores))), 4)
        vf = round(vi * mu, 2)
        if mu > 1:
            var = round((mu-1)*100, 2)
            tipo = f"📈 AUMENTO del {var}%"
            color = "#2e7d32"
        elif mu < 1:
            var = round((1-mu)*100, 2)
            tipo = f"📉 DESCUENTO del {var}%"
            color = "#c62828"
        else:
            var = 0
            tipo = "➡️ SIN VARIACIÓN"
            color = "#616161"
        return {"vi":vi, "vf":vf, "mu":mu, "var":var, "tipo":tipo, "color":color,
                "valores":valores, "multiplicadores":multiplicadores}

    def calcular(self):
        try:
            if self.c1.get()==0 and self.c2.get()==0 and self.c3.get()==0:
                messagebox.showwarning("Sin datos", "Ingresa al menos un cambio.")
                return
            r = self._calcular()
            if r is None:
                return
            self.resultado_vf.set(f"S/ {r['vf']:,.2f}")
            self.resultado_mu.set(str(r['mu']))
            self.resultado_var.set(f"{r['var']}%")
            self.resultado_tipo.set(r['tipo'])
            self.lbl_var.config(fg=r['color'])
            self.lbl_tipo.config(fg=r['color'])
            voz_resultado(r['vi'], r['vf'], r['mu'], r['var'], r['tipo'])
            self.estado.config(text="✅ Cálculo exitoso")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def limpiar(self):
        self.vi.set(0); self.c1.set(0); self.c2.set(0); self.c3.set(0)
        self.resultado_vf.set(""); self.resultado_mu.set("")
        self.resultado_var.set(""); self.resultado_tipo.set("")
        self.estado.config(text="✅ Limpiado")
        hablar("Campos limpiados.")

    def ver_tabla(self):
        r = self._calcular()
        if r is None:
            messagebox.showwarning("Sin datos", "Calcula primero.")
            return
        ventana = tk.Toplevel(self.root)
        ventana.title("📋 Tabla de Proporcionalidad")
        ventana.geometry("500x400")
        ventana.configure(bg="#f5f0e1")
        tk.Label(ventana, text="TABLA DE PROPORCIONALIDAD", font=("Arial", 14, "bold"),
                bg="#f5f0e1", fg="#5d4037").pack(pady=10)
        cols = ["Concepto", "%", "Valor (S/)"]
        tree = ttk.Treeview(ventana, columns=cols, show="headings", height=10)
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor="center")
        tree.insert("", "end", values=["Valor inicial", "100%", f"S/ {r['vi']:,.2f}"])
        p = 100
        cambios = [c for c in [self.c1.get(), self.c2.get(), self.c3.get()] if c != 0]
        for i, (c, v) in enumerate(zip(cambios, r['valores'][1:])):
            p *= (1 + c/100)
            s = "+" if c>0 else ""
            tree.insert("", "end", values=[f"Cambio {i+1} ({s}{c}%)", f"{p:.2f}%", f"S/ {v:,.2f}"])
        if r['mu'] > 1:
            tree.insert("", "end", values=["AUMENTO TOTAL", f"+{r['var']}%", f"+S/ {r['vi']*r['var']/100:,.2f}"])
        elif r['mu'] < 1:
            tree.insert("", "end", values=["DESCUENTO TOTAL", f"-{r['var']}%", f"-S/ {r['vi']*r['var']/100:,.2f}"])
        tree.pack(pady=10, padx=10, fill="both", expand=True)
        tk.Button(ventana, text="CERRAR", font=("Arial", 12), bg="#f44336", fg="white",
                padx=25, pady=8, command=ventana.destroy).pack(pady=10)

    def modo_ensenar(self):
        vi, c1, c2 = 60, 35, -10
        m1, m2 = 1+c1/100, 1+c2/100
        mu = m1*m2
        vf = vi*mu
        var = (mu-1)*100
        texto = f"""
📚 MODO ENSEÑANZA - Ejemplo paso a paso
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PROBLEMA: Producto cuesta S/ {vi}. 
         Aumenta {c1}% y luego descuenta {abs(c2)}%.

PASO 1: Datos → Vi=S/ {vi}, Cambio 1=+{c1}%, Cambio 2={c2}%

PASO 2: Multiplicadores
   M₁ = 1 + {c1}/100 = {m1}
   M₂ = 1 + ({c2})/100 = {m2}

PASO 3: Multiplicador único
   Mᵤ = M₁ × M₂ = {m1} × {m2} = {mu:.4f}

PASO 4: Valor final
   Vf = Vi × Mᵤ = {vi} × {mu:.4f} = S/ {vf:.2f}

PASO 5: Interpretación
   Mᵤ = {mu:.4f} > 1 → AUMENTO del {var:.2f}%

✅ Precio final: S/ {vf:.2f}
⚠️ {c1}% + ({c2}%) = {c1+c2}% ❌ INCORRECTO
   La forma correcta es multiplicar los multiplicadores.
"""
        self.txt_ensenar.config(state="normal")
        self.txt_ensenar.delete("1.0", "end")
        self.txt_ensenar.insert("1.0", texto)
        self.txt_ensenar.config(state="disabled")
        hablar(f"Ejemplo guiado. Valor inicial {vi} soles. Aumento {c1} por ciento. Descuento {abs(c2)} por ciento.")

    def nuevo_problema(self):
        prods = ["saco de papas", "quintal de quinua", "chompa tejida", "queso fresco", "miel", "frazada"]
        precs = [60, 80, 100, 120, 150, 200]
        p = random.choice(prods)
        vi = random.choice(precs)
        c1 = random.choice([20, 25, 30, 35, 40, 50])
        c2 = -random.choice([5, 10, 15, 20, 25])
        m1, m2 = 1+c1/100, 1+c2/100
        mu = m1*m2
        vf = round(vi*mu, 2)
        self.problema_actual = {"vi":vi, "c1":c1, "c2":c2, "mu":mu, "vf":vf, "prod":p}
        self.solucion_actual = vf
        texto = f"Un {p} cuesta S/ {vi}.\nAumenta {c1}% y luego descuenta {abs(c2)}%.\n¿Cuál es el precio final?"
        self.txt_enunciado.config(state="normal")
        self.txt_enunciado.delete("1.0", "end")
        self.txt_enunciado.insert("1.0", texto)
        self.txt_enunciado.config(state="disabled")
        self.entrada_respuesta.delete(0, "end")
        self.entrada_respuesta.focus_set()
        hablar("Nuevo problema generado. ¡A resolver!")

    def verificar(self):
        if self.problema_actual is None:
            messagebox.showwarning("Sin problema", "Genera un problema primero.")
            return
        try:
            r = float(self.entrada_respuesta.get())
            if abs(r - self.solucion_actual) < 0.02:
                voz_acierto()
                messagebox.showinfo("✅ ¡Correcto!", f"Precio final: S/ {self.solucion_actual:,.2f}")
                self.estado.config(text="✅ ¡Correcto!")
            else:
                voz_error()
                messagebox.showwarning("❌ Incorrecto", "Revisa tu procedimiento.\nPista: usa multiplicadores, no sumes %.")
                self.estado.config(text="❌ Intenta de nuevo")
        except ValueError:
            messagebox.showerror("Error", "Ingresa un número válido.")

    def ver_solucion(self):
        if self.problema_actual is None:
            return
        p = self.problema_actual
        m1, m2 = 1+p['c1']/100, 1+p['c2']/100
        msg = (f"Solución:\nVi=S/{p['vi']}\nM₁={m1:.2f} | M₂={m2:.2f}\n"
               f"Mᵤ={p['mu']:.4f}\nVf=S/{p['vf']:.2f}")
        messagebox.showinfo("💡 Solución", msg)

    def dibujar(self):
        self.canvas.delete("all")
        r = self._calcular()
        if r is None:
            self.canvas.create_text(400, 225, text="Primero calcula en la pestaña CALCULAR",
                                   font=("Arial", 14), fill="#8d6e63")
            return
        c = self.canvas
        c.create_text(400, 30, text="DIAGRAMA DE FLUJO", font=("Arial", 14, "bold"), fill="#5d4037")
        x, y = 400, 70
        c.create_oval(x-45, y, x+45, y+35, fill="#e8f5e9", outline="#2e7d32", width=2)
        c.create_text(x, y+17, text="INICIO", font=("Arial", 10, "bold"))
        y += 55
        c.create_rectangle(x-100, y, x+100, y+30, fill="#fff3e0", outline="#e65100", width=2)
        c.create_text(x, y+15, text=f"Vi = S/ {r['vi']:,.2f}", font=("Arial", 10, "bold"))
        y += 50
        color = r['color']
        c.create_rectangle(x-120, y, x+120, y+30, fill="#f3e5f5", outline=color, width=2)
        c.create_text(x, y+15, text=f"Mᵤ = {r['mu']:.4f} → Vf = S/ {r['vf']:,.2f}", font=("Arial", 10, "bold"))
        y += 50
        c.create_oval(x-45, y, x+45, y+35, fill="#e8f5e9", outline="#2e7d32", width=2)
        c.create_text(x, y+17, text="FIN", font=("Arial", 10, "bold"))

    def cerrar(self):
        hablar("¡Hasta luego!")
        self.root.after(1000, self.root.destroy)


# ============================================================
# INICIO
# ============================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraAumentosDescuentos(root)
    root.mainloop()
