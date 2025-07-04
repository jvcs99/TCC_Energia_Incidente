import tkinter as tk
from tkinter import messagebox, filedialog
import math
import pandas as pd
from fpdf import FPDF


# Funções de Cálculo
def calcular():

    try:
        # Dados fixos do caso 2
        Vn = 380  # Volts
        f = 60  # Hz
        G = 32  # mm (gap)

        # Impedâncias dos transformadores
        Z1 = complex(30.81, 59.93)  # mΩ
        Z2 = complex(54.55, 98.16)  # mΩ

        # Impedâncias dos cabos
        Z3 = complex(4.45, 1.127)   # mΩ
        Z4 = complex(17.78, 2.328)  # mΩ

        # Impedância equivalente de cada ramo
        Zeq1 = Z1 + Z3
        Zeq2 = Z2 + Z4

        # Impedância total (paralelo dos dois ramos)
        Z_total = (Zeq1 * Zeq2) / (Zeq1 + Zeq2)

        Z_modulo = abs(Z_total)
        Z_real = Z_total.real
        Z_imag = Z_total.imag
        theta = math.atan2(Z_imag, Z_real)
        theta_deg = math.degrees(theta)

        # Corrente de Curto Ibf
        Ibf = Vn / (math.sqrt(3) * (Z_modulo / 1000))  # A → kA
        Ibf_kA = Ibf / 1000

        # Corrente Transitória
        Ct = Z_imag / (2 * math.pi * f * Z_real)
        omega = 2 * math.pi * f
        beta = math.radians(45)  # 45 graus em radianos
        t_trans = float(entry_t_trans.get())  # tempo para corrente transitória (ex.: 0.004)

        Icc = math.sqrt(2) * Ibf * (
            math.sin(omega * t_trans + beta - theta) +
            math.exp(-t_trans / Ct) * math.sin(beta - theta)
        )
        Icc_kA = Icc / 1000

        # Corrente de arco
        K = 0.097
        log_Ibf = math.log10(Ibf_kA)

        log_Ia = (
            K + 0.662 * log_Ibf +
            0.0966 * (Vn / 1000) +
            0.000526 * G +
            0.5588 * (Vn / 1000) * log_Ibf -
            0.00304 * G * log_Ibf
        )
        Ia = 10 ** log_Ia
        Ia85 = Ia * 0.85

        # Energia incidente (En)
        K1 = 0.555
        K2 = 0.113

        log_En = K1 + K2 + 1.081 * log_Ia + 0.0011 * G
        En = 10 ** log_En  # J/cm²

        # Energia do arco elétrico
        Cf = 1.5
        x = 1.473
        D = 610  # mm (distância de cálculo padrão)

        t_energia = float(entry_t_energia.get())  # tempo para energia (ex.: 0.025)

        E = 4.184 * Cf * En * (t_energia / 0.2) * ((610 ** x) / (D ** x))  # J/cm²
        E_cal = E / 4.184  # cal/cm²

        # Distância segura
        Eb = 5  # Energia limite para queimadura (5 J/cm²)
        Db = (4.184 * Cf * En * (t_energia / 0.2) * (610 ** x) / Eb) ** (1 / x)

        # Resultado formatado
        resultado = f"""
🔧 Resultados do Cálculo:
──────────────────────────────
Impedância equivalente: {Z_real:.2f} + j{Z_imag:.2f} mΩ
Corrente de Curto (Ibf): {Ibf_kA:.2f} kA
Corrente Transitória: {Icc_kA:.2f} kA
Corrente de Arco: {Ia:.2f} kA
Corrente de Arco (85%): {Ia85:.2f} kA
Energia Incidente: {En:.2f} J/cm²
Energia do Arco: {E_cal:.2f} cal/cm²
Distância Segura (Db): {Db:.2f} mm
"""

        txt_resultado.delete(1.0, tk.END)
        txt_resultado.insert(tk.END, resultado)

        # Exportação Excel
        if var_excel.get():
            dados = {
                "Impedância Real (mΩ)": [Z_real],
                "Impedância Imag (mΩ)": [Z_imag],
                "Ibf (kA)": [Ibf_kA],
                "Icc (kA)": [Icc_kA],
                "Ia (kA)": [Ia],
                "Ia (85%) (kA)": [Ia85],
                "Energia Incidente (J/cm²)": [En],
                "Energia do Arco (cal/cm²)": [E_cal],
                "Distância Segura (mm)": [Db]
            }
            df = pd.DataFrame(dados)
            df.to_excel("resultado_arco.xlsx", index=False)

        # Exportação PDF
        if var_pdf.get():
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, resultado)
            pdf.output("resultado_arco.pdf")

        messagebox.showinfo("Sucesso", "Cálculo realizado com sucesso!")

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")


# GUI
janela = tk.Tk()
janela.title("Calculadora de Arco Elétrico")
janela.geometry("700x600")

# Labels
tk.Label(janela, text="Tempo para corrente transitória (s):").pack()
entry_t_trans = tk.Entry(janela)
entry_t_trans.insert(0, "0.004")
entry_t_trans.pack()

tk.Label(janela, text="Tempo para energia incidente (s):").pack()
entry_t_energia = tk.Entry(janela)
entry_t_energia.insert(0, "0.025")
entry_t_energia.pack()

# Checkboxes
var_excel = tk.BooleanVar()
check_excel = tk.Checkbutton(janela, text="Exportar para Excel", variable=var_excel)
check_excel.pack()

var_pdf = tk.BooleanVar()
check_pdf = tk.Checkbutton(janela, text="Gerar Relatório PDF", variable=var_pdf)
check_pdf.pack()

# Botão de cálculo
btn_calcular = tk.Button(janela, text="Calcular", command=calcular, bg="green", fg="white")
btn_calcular.pack(pady=10)

# Área de texto para resultados
txt_resultado = tk.Text(janela, height=20, width=80)
txt_resultado.pack()

janela.mainloop()
