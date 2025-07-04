import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np


def calc_impedancia_transformador(S_kva, Z_percent, R_percent, V):
    Z_base = (Z_percent * (V ** 2)) / (S_kva * 100)
    R = (R_percent * (V ** 2)) / (S_kva * 100)
    X = np.sqrt(Z_base ** 2 - R ** 2)
    return complex(R, X)


def calc_impedancia_cabo(resistencia, reatancia, comprimento):
    R = resistencia * comprimento
    X = reatancia * comprimento
    return complex(R, X)


def calc_impedancia_total(Z1, Z2):
    return (Z1 * Z2) / (Z1 + Z2)


def calc_corrente_curto(V_linha, Z_total):
    V_fase = V_linha / np.sqrt(3)
    return (V_fase * 1000) / abs(Z_total)  # A


def calc_ct(X, R, freq):
    return X / (2 * np.pi * freq * R)


def calc_corrente_simetrica(Ibf, omega, Ct, beta, theta, t):
    seno = np.sin(omega * t + beta - theta)
    exp = np.exp(-t / Ct) * np.sin(beta - theta)
    return np.sqrt(2) * Ibf * (seno + exp)


def calc_corrente_arco(Ibf, V_kV, G):
    logIbf = np.log10(Ibf)
    logIa = (0.00402 + 0.983 * logIbf + 0.00616 * V_kV + 0.000526 * G +
             0.5588 * V_kV * logIbf - 0.00304 * G * logIbf)
    return 10 ** logIa


def calc_energia_incidente(Ia, G, V_kV):
    logIa = np.log10(Ia)
    logEn = (-0.792 + 0.555 * np.log10(G) + 0.636 * logIa + 0.103 * V_kV)
    En = 10 ** logEn
    return En


def calc_energia_arco(En, t, Cf, D, x=1.473):
    E = 4.184 * Cf * En * (t / 0.2) * (610 ** x / D ** x)
    return E


def calc_distancia_segura(En, t, Cf, Eb, x=1.473):
    numerador = 4.184 * Cf * En * (t / 0.2) * (610 ** x)
    D = (numerador / Eb) ** (1 / x)
    return D


# Interface

def calcular():
    try:
        # Dados fixos
        V_linha = 380  # V
        V_fase = V_linha / np.sqrt(3)  # Fase-Terra
        V_kV = V_fase / 1000  # Em kV
        freq = 60
        omega = 2 * np.pi * freq
        G = 32  # GAP mm
        Cf = 1.5
        Eb = 5  # cal/cm²
        D = 610  # mm
        t = 0.025  # 25 ms

        # Impedâncias
        Zt1 = calc_impedancia_transformador(75, 3.5, 1.6, V_linha)
        Zc1 = calc_impedancia_cabo(0.445, 0.1127, 10)

        Zt2 = calc_impedancia_transformador(45, 3.5, 1.7, V_linha)
        Zc2 = calc_impedancia_cabo(0.8891, 0.1164, 20)

        Zeq1 = Zt1 + Zc1
        Zeq2 = Zt2 + Zc2
        Z_total = calc_impedancia_total(Zeq1, Zeq2)

        # Corrente de curto
        Ibf = calc_corrente_curto(V_linha, Z_total)

        # Parâmetros
        R_total = Z_total.real
        X_total = Z_total.imag
        Ct = calc_ct(X_total, R_total, freq)
        theta = np.arctan(X_total / R_total)
        beta = np.deg2rad(45)

        # Corrente simétrica
        Icc = calc_corrente_simetrica(Ibf, omega, Ct, beta, theta, t)

        # Corrente de arco
        Ia = calc_corrente_arco(Ibf, V_kV, G)
        Ia85 = 0.85 * Ia

        # Energia incidente
        En = calc_energia_incidente(Ia, G, V_kV)

        # Energia do arco
        E = calc_energia_arco(En, t, Cf, D)
        E_cal = E / 4.184

        # Distância segura
        D_safe = calc_distancia_segura(En, t, Cf, Eb)

        # Resultado
        resultado = (
            f"🔧 Impedância Total: {abs(Z_total):.2f} mΩ ∠ {np.degrees(np.arctan(X_total / R_total)):.2f}°\n"
            f"🔵 Corrente de Curto: {Ibf/1000:.2f} kA\n"
            f"🔴 Corrente de Arco: {Ia:.2f} kA (85%: {Ia85:.2f} kA)\n"
            f"🟡 Energia Incidente: {E_cal:.2f} cal/cm²\n"
            f"🛑 Distância Segura: {D_safe:.2f} mm"
        )
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, resultado)

    except Exception as e:
        messagebox.showerror("Erro", str(e))


# Janela
janela = tk.Tk()
janela.title("Calculadora de Arco Elétrico")

# Layout
frame = ttk.Frame(janela, padding=20)
frame.grid()

ttk.Label(frame, text="Calculadora de Curto-Circuito e Arco Elétrico", font=("Arial", 14, "bold")).grid(
    column=0, row=0, columnspan=2, pady=10
)

output_text = tk.Text(frame, width=60, height=10, font=("Courier", 10))
output_text.grid(column=0, row=1, columnspan=2, pady=10)

ttk.Button(frame, text="Calcular", command=calcular).grid(column=0, row=2, padx=5)
ttk.Button(frame, text="Sair", command=janela.destroy).grid(column=1, row=2, padx=5)

janela.mainloop()
