import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def gerar_pdf(energia_final, categoria, dados):
    nome_pdf = f"Relatorio_Energia_Incidente_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    c = canvas.Canvas(nome_pdf, pagesize=A4)
    largura, altura = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, altura - 50, "Relatório de Energia Incidente - Arco Elétrico")

    c.setFont("Helvetica", 12)
    y = altura - 100
    for label, valor in dados.items():
        c.drawString(50, y, f"{label}: {valor}")
        y -= 20

    c.setFont("Helvetica-Bold", 12)
    c.setFillColorRGB(0.2, 0.2, 0.8)
    c.drawString(50, y - 10, f"⚡ Energia Incidente Estimada: {energia_final:.2f} cal/cm²")
    c.drawString(50, y - 30, f"🔰 Categoria de Risco: {categoria}")
    c.save()

    messagebox.showinfo("PDF Gerado", f"Relatório PDF salvo como:\n{nome_pdf}")

def calcular_energia_incidente():
    global energia_final, categoria, dados_pdf
    try:
        curto_circuito = float(entry_curto_circuito.get())
        tempo_atuacao = float(entry_tempo.get())
        fator_arco = float(entry_fator_arco.get())
        tensao = float(entry_tensao.get())
        frequencia = float(entry_freq.get())
        distancia_trabalho = float(entry_distancia.get())  # em mm
        tipo_equipamento = combo_tipo_equip.get()

        # Fator empírico conforme tipo de equipamento e tensão
        if tipo_equipamento == "Painel Elétrico":
            fator_equipamento = 1.0 if tensao < 600 else 1.1
        elif tipo_equipamento == "CCM":
            fator_equipamento = 1.2
        elif tipo_equipamento == "Quadro de Distribuição":
            fator_equipamento = 0.9
        else:
            fator_equipamento = 1.0

        corrente_arco = curto_circuito * fator_arco
        energia_bruta = 0.0001 * (corrente_arco ** 2) * tempo_atuacao * fator_equipamento
        energia_final = energia_bruta * (610.0 / distancia_trabalho) ** 2  # ajuste por distância

        if energia_final < 1.2:
            categoria = "Sem exigência de EPI específico (Risco mínimo)"
        elif energia_final < 4:
            categoria = "Categoria 1 - Roupa FR mínima (calça + camisa)"
        elif energia_final < 8:
            categoria = "Categoria 2 - Roupa FR + proteção para cabeça/mãos"
        elif energia_final < 25:
            categoria = "Categoria 3 - Roupa FR multicamadas + proteção avançada"
        else:
            categoria = "Categoria 4 - Máxima proteção (Arco >25 cal/cm²)"

        resultado_label.config(
            text=f"⚡ Energia Incidente: {energia_final:.2f} cal/cm²\n🔰 Recomendação: {categoria}"
        )

        # TXT
        nome_arquivo = f"relatorio_energia_incidente_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(nome_arquivo, "w") as f:
            f.write("RELATÓRIO DE ENERGIA INCIDENTE\n")
            f.write("=" * 50 + "\n")
            f.write(f"Data e hora: {datetime.now()}\n")
            f.write(f"Tensão Nominal: {tensao} V\n")
            f.write(f"Frequência: {frequencia} Hz\n")
            f.write(f"Tipo de Equipamento: {tipo_equipamento}\n")
            f.write(f"Corrente de Curto-Circuito: {curto_circuito} A\n")
            f.write(f"Fator da Corrente de Arco: {fator_arco}\n")
            f.write(f"Corrente de Arco Estimada: {corrente_arco:.2f} A\n")
            f.write(f"Tempo de Atuação: {tempo_atuacao} s\n")
            f.write(f"Distância de Trabalho: {distancia_trabalho} mm\n")
            f.write(f"Fator de Equipamento: {fator_equipamento}\n")
            f.write(f"ENERGIA INCIDENTE ESTIMADA: {energia_final:.2f} cal/cm²\n")
            f.write(f"CATEGORIA DE RISCO: {categoria}\n")
            f.write("=" * 50 + "\n")

        # PDF
        dados_pdf = {
            "Data e hora": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "Tensão Nominal (V)": tensao,
            "Frequência (Hz)": frequencia,
            "Tipo de Equipamento": tipo_equipamento,
            "Corrente de Curto-Circuito (A)": curto_circuito,
            "Fator de Corrente de Arco": fator_arco,
            "Corrente de Arco Estimada (A)": f"{corrente_arco:.2f}",
            "Tempo de Atuação (s)": tempo_atuacao,
            "Distância de Trabalho (mm)": distancia_trabalho,
            "Fator de Equipamento": fator_equipamento
        }

        gerar_pdf(energia_final, categoria, dados_pdf)

    except ValueError:
        messagebox.showerror("Erro", "Preencha todos os campos com valores válidos.")

# Interface
root = tk.Tk()
root.title("Calculadora Avançada de Energia Incidente")
root.state('zoomed')

tk.Label(root, text="🧮 Calculadora Avançada de Energia Incidente (Arco Elétrico)",
         font=("Arial", 20, "bold")).pack(pady=20)

frame = tk.Frame(root)
frame.pack()

def criar_linha_input(label_text, entry_widget, default_value=""):
    tk.Label(frame, text=label_text, font=("Arial", 12)).grid(sticky="w")
    entry_widget.insert(0, default_value)
    entry_widget.grid(sticky="we", pady=5)

entry_curto_circuito = tk.Entry(frame, font=("Arial", 12))
criar_linha_input("Corrente de Curto-Circuito (A):", entry_curto_circuito)

entry_tempo = tk.Entry(frame, font=("Arial", 12))
criar_linha_input("Tempo de Atuação da Proteção (s):", entry_tempo)

entry_fator_arco = tk.Entry(frame, font=("Arial", 12))
criar_linha_input("Fator de Corrente de Arco (ex: 0.85):", entry_fator_arco, "0.85")

entry_tensao = tk.Entry(frame, font=("Arial", 12))
criar_linha_input("Tensão Nominal (V):", entry_tensao, "480")

entry_freq = tk.Entry(frame, font=("Arial", 12))
criar_linha_input("Frequência (Hz):", entry_freq, "60")

entry_distancia = tk.Entry(frame, font=("Arial", 12))
criar_linha_input("Distância de Trabalho (mm):", entry_distancia, "610")

tk.Label(frame, text="Tipo de Equipamento:", font=("Arial", 12)).grid(sticky="w", pady=(10, 0))
combo_tipo_equip = ttk.Combobox(frame, values=["Painel Elétrico", "CCM", "Quadro de Distribuição"], font=("Arial", 12))
combo_tipo_equip.set("Painel Elétrico")
combo_tipo_equip.grid(sticky="we", pady=5)

tk.Button(frame, text="🧮 Calcular Energia Incidente", font=("Arial", 14),
          bg="#2e8b57", fg="white", command=calcular_energia_incidente).grid(pady=20)

resultado_label = tk.Label(root, text="", font=("Arial", 16, "bold"), fg="blue")
resultado_label.pack(pady=20)

root.mainloop()
