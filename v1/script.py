import json
import tkinter as tk
from tkinter import messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Função para salvar os dados no arquivo JSON
def salvar_dados(transformadores):
    with open("ele_trafos.json", "w") as arquivo_json:
        json.dump(transformadores, arquivo_json, indent=4)

# Função para carregar os dados dos transformadores (caso o arquivo já exista)
def carregar_dados():
    try:
        with open("ele_trafos.json", "r") as arquivo_json:
            transformadores = json.load(arquivo_json)
    except FileNotFoundError:
        transformadores = {}
    return transformadores

# Função para converter texto para float, aceitando vírgula como separador decimal
def converter_para_float(valor_str):
    try:
        return float(valor_str.replace(',', '.'))
    except ValueError:
        return None

# Função para adicionar um novo transformador
def adicionar_transformador():
    transformadores = carregar_dados()

    # Coletar dados inseridos pelo usuário
    nome_transformador = entry_nome.get().strip()
    if not nome_transformador:
        nome_transformador = "ELE-TRAF-" + str(len(transformadores) + 1).zfill(2)

    Pt = converter_para_float(entry_Pt.get())
    Vprim = converter_para_float(entry_Vprim.get())
    Vsec = converter_para_float(entry_Vsec.get())
    Z_percent = converter_para_float(entry_Z_percent.get())
    Pcut = converter_para_float(entry_Pcut.get())
    Iprim = converter_para_float(entry_Iprim.get())
    Isec = converter_para_float(entry_Isec.get())
    R0 = converter_para_float(entry_R0.get())
    X0 = converter_para_float(entry_X0.get())
    Z0 = converter_para_float(entry_Z0.get())
    R1 = converter_para_float(entry_R1.get())
    X1 = converter_para_float(entry_X1.get())
    Z1 = converter_para_float(entry_Z1.get())

    # Verificar se algum valor é inválido
    if None in [Pt, Vprim, Vsec, Z_percent, Pcut, Iprim, Isec, R0, X0, Z0, R1, X1, Z1]:
        messagebox.showerror("Erro", "Por favor, insira valores válidos para todos os campos.")
        return

    # Dados do novo transformador
    novo_transformador = {
        "Pt": Pt,
        "Vprim": Vprim,
        "Vsec": Vsec,
        "Z_percent": Z_percent,
        "Pcut": Pcut,
        "Iprim": Iprim,
        "Isec": Isec,
        "R0": R0, "X0": X0, "Z0": Z0,
        "R1": R1, "X1": X1, "Z1": Z1
    }

    # Adicionar ao banco de dados
    if nome_transformador not in transformadores:
        transformadores[nome_transformador] = novo_transformador
        salvar_dados(transformadores)
        messagebox.showinfo("Sucesso", f"Transformador {nome_transformador} adicionado com sucesso!")
    else:
        messagebox.showerror("Erro", "Transformador com este nome já existe.")
        return

    # Preencher automaticamente os campos com os valores do último transformador
    entry_Pt.delete(0, tk.END)
    entry_Pt.insert(0, f"{novo_transformador['Pt']:.2f}")
    
    entry_Vprim.delete(0, tk.END)
    entry_Vprim.insert(0, f"{novo_transformador['Vprim']:.2f}")
    
    entry_Vsec.delete(0, tk.END)
    entry_Vsec.insert(0, f"{novo_transformador['Vsec']:.2f}")
    
    entry_Z_percent.delete(0, tk.END)
    entry_Z_percent.insert(0, f"{novo_transformador['Z_percent']:.2f}")
    
    entry_Pcut.delete(0, tk.END)
    entry_Pcut.insert(0, f"{novo_transformador['Pcut']:.2f}")
    
    entry_Iprim.delete(0, tk.END)
    entry_Iprim.insert(0, f"{novo_transformador['Iprim']:.2f}")
    
    entry_Isec.delete(0, tk.END)
    entry_Isec.insert(0, f"{novo_transformador['Isec']:.2f}")
    
    entry_R0.delete(0, tk.END)
    entry_R0.insert(0, f"{novo_transformador['R0']:.2f}")
    
    entry_X0.delete(0, tk.END)
    entry_X0.insert(0, f"{novo_transformador['X0']:.2f}")
    
    entry_Z0.delete(0, tk.END)
    entry_Z0.insert(0, f"{novo_transformador['Z0']:.2f}")
    
    entry_R1.delete(0, tk.END)
    entry_R1.insert(0, f"{novo_transformador['R1']:.2f}")
    
    entry_X1.delete(0, tk.END)
    entry_X1.insert(0, f"{novo_transformador['X1']:.2f}")
    
    entry_Z1.delete(0, tk.END)
    entry_Z1.insert(0, f"{novo_transformador['Z1']:.2f}")

# Função para simular os cálculos
def simular_calculos():
    transformadores = carregar_dados()
    if len(transformadores) == 0:
        messagebox.showerror("Erro", "Não há transformadores cadastrados.")
        return

    # Obter o último transformador adicionado
    ultimo_transformador = list(transformadores.values())[-1]

    Pt = ultimo_transformador['Pt']
    Vprim = ultimo_transformador['Vprim']
    Vsec = ultimo_transformador['Vsec']
    Z_percent = ultimo_transformador['Z_percent']

    # Calcular corrente de curto-circuito
    Icc = Vsec / (Z_percent / 100)

    # Mostrar o resultado na tela
    label_resultado.config(text=f"Corrente de Curto-Circuito: {Icc:.2f} A")

# Função para gerar PDF
def gerar_pdf():
    transformadores = carregar_dados()
    if len(transformadores) == 0:
        messagebox.showerror("Erro", "Não há transformadores cadastrados para gerar o PDF.")
        return

    # Criar o PDF
    c = canvas.Canvas("relatorio_transformador.pdf", pagesize=letter)
    c.setFont("Helvetica", 12)
    c.drawString(100, 750, "Relatório de Transformadores Cadastrados")

    y_position = 730
    for id_transformador, dados in transformadores.items():
        c.drawString(100, y_position, f"ID: {id_transformador}")
        y_position -= 20
        for key, value in dados.items():
            c.drawString(120, y_position, f"{key}: {value}")
            y_position -= 20
        y_position -= 10  # Espaço entre transformadores

    c.save()
    messagebox.showinfo("Sucesso", "Relatório PDF gerado com sucesso!")

# Função para validar entrada de números com vírgula
def validar_entrada(event, campo):
    valor = campo.get()
    if ',' in valor:
        campo.delete(0, tk.END)
        campo.insert(0, valor.replace(',', '.'))

# Configuração da interface gráfica
root = tk.Tk()
root.title("Simulador de Transformadores")
root.geometry("500x650")

# Campo para nome do transformador
tk.Label(root, text="Nome do Transformador (opcional)").pack()
entry_nome = tk.Entry(root)
entry_nome.pack()

# Valores predefinidos
valores_iniciais = {
    "Pt": 1500.0,
    "Vprim": 13800.0,
    "Vsec": 440.0,
    "Z_percent": 4.4,
    "Pcut": 16.0,
    "Iprim": 62.76,
    "Isec": 1968.24,
    "R0": 0.71,
    "X0": 3.59,
    "Z0": 3.66,
    "R1": 0.71,
    "X1": 3.59,
    "Z1": 3.66
}

# Campos de entrada
tk.Label(root, text="Potência (kVA)").pack()
entry_Pt = tk.Entry(root)
entry_Pt.pack()
entry_Pt.insert(0, f"{valores_iniciais['Pt']:.2f}")
entry_Pt.bind("<FocusOut>", lambda event: validar_entrada(event, entry_Pt))

tk.Label(root, text="Tensão Primária (V)").pack()
entry_Vprim = tk.Entry(root)
entry_Vprim.pack()
entry_Vprim.insert(0, f"{valores_iniciais['Vprim']:.2f}")
entry_Vprim.bind("<FocusOut>", lambda event: validar_entrada(event, entry_Vprim))

tk.Label(root, text="Tensão Secundária (V)").pack()
entry_Vsec = tk.Entry(root)
entry_Vsec.pack()
entry_Vsec.insert(0, f"{valores_iniciais['Vsec']:.2f}")
entry_Vsec.bind("<FocusOut>", lambda event: validar_entrada(event, entry_Vsec))

tk.Label(root, text="Impedância (%)").pack()
entry_Z_percent = tk.Entry(root)
entry_Z_percent.pack()
entry_Z_percent.insert(0, f"{valores_iniciais['Z_percent']:.2f}")
entry_Z_percent.bind("<FocusOut>", lambda event: validar_entrada(event, entry_Z_percent))

tk.Label(root, text="Potência de Curto (kVA)").pack()
entry_Pcut = tk.Entry(root)
entry_Pcut.pack()
entry_Pcut.insert(0, f"{valores_iniciais['Pcut']:.2f}")
entry_Pcut.bind("<FocusOut>", lambda event: validar_entrada(event, entry_Pcut))

tk.Label(root, text="Corrente Primária (A)").pack()
entry_Iprim = tk.Entry(root)
entry_Iprim.pack()
entry_Iprim.insert(0, f"{valores_iniciais['Iprim']:.2f}")
entry_Iprim.bind("<FocusOut>", lambda event: validar_entrada(event, entry_Iprim))

tk.Label(root, text="Corrente Secundária (A)").pack()
entry_Isec = tk.Entry(root)
entry_Isec.pack()
entry_Isec.insert(0, f"{valores_iniciais['Isec']:.2f}")
entry_Isec.bind("<FocusOut>", lambda event: validar_entrada(event, entry_Isec))

tk.Label(root, text="R0").pack()
entry_R0 = tk.Entry(root)
entry_R0.pack()
entry_R0.insert(0, f"{valores_iniciais['R0']:.2f}")
entry_R0.bind("<FocusOut>", lambda event: validar_entrada(event, entry_R0))

tk.Label(root, text="X0").pack()
entry_X0 = tk.Entry(root)
entry_X0.pack()
entry_X0.insert(0, f"{valores_iniciais['X0']:.2f}")
entry_X0.bind("<FocusOut>", lambda event: validar_entrada(event, entry_X0))

tk.Label(root, text="Z0").pack()
entry_Z0 = tk.Entry(root)
entry_Z0.pack()
entry_Z0.insert(0, f"{valores_iniciais['Z0']:.2f}")
entry_Z0.bind("<FocusOut>", lambda event: validar_entrada(event, entry_Z0))

tk.Label(root, text="R1").pack()
entry_R1 = tk.Entry(root)
entry_R1.pack()
entry_R1.insert(0, f"{valores_iniciais['R1']:.2f}")
entry_R1.bind("<FocusOut>", lambda event: validar_entrada(event, entry_R1))

tk.Label(root, text="X1").pack()
entry_X1 = tk.Entry(root)
entry_X1.pack()
entry_X1.insert(0, f"{valores_iniciais['X1']:.2f}")
entry_X1.bind("<FocusOut>", lambda event: validar_entrada(event, entry_X1))

tk.Label(root, text="Z1").pack()
entry_Z1 = tk.Entry(root)
entry_Z1.pack()
entry_Z1.insert(0, f"{valores_iniciais['Z1']:.2f}")
entry_Z1.bind("<FocusOut>", lambda event: validar_entrada(event, entry_Z1))

# Botões para ações
button_adicionar = tk.Button(root, text="Adicionar Transformador", command=adicionar_transformador)
button_adicionar.pack()

button_simular = tk.Button(root, text="Simular Cálculos", command=simular_calculos)
button_simular.pack()

button_gerar_pdf = tk.Button(root, text="Gerar PDF", command=gerar_pdf)
button_gerar_pdf.pack()

# Label para exibir o resultado da simulação
label_resultado = tk.Label(root, text="")
label_resultado.pack()

root.mainloop()
