import tkinter as tk
from tkinter import messagebox
import json
import os


# Função para gerar o nome automaticamente (ELE-Pxx-TRF-xx)
def gerar_nome_transformador():
    try:
        # Tenta abrir o arquivo de dados dos transformadores
        with open("transformadores.json", "r") as file:
            dados_arquivo = json.load(file)

        # Obtém a lista de transformadores
        transformadores = dados_arquivo.get("transformadores", [])
        
        # Se a lista de transformadores estiver vazia, começa com o nome ELE-P01-TRF-01
        if not transformadores:
            return "ELE-P01-TRF-01"
        
        # Caso contrário, encontra o maior número de transformador e incrementa
        ultimo_numero = 0
        for trafo in transformadores:
            try:
                # Extrai o número do nome (ex: ELE-P01-TRF-01)
                numero = int(trafo["nome"].split('-')[2][1:])
                ultimo_numero = max(ultimo_numero, numero)
            except (IndexError, ValueError):
                # Caso o nome não siga o formato esperado, ignora e continua
                continue

        novo_numero = ultimo_numero + 1
        return f"ELE-P{novo_numero:02d}-TRF-{novo_numero:02d}"
    
    except FileNotFoundError:
        # Caso o arquivo não exista, começa com o nome ELE-P01-TRF-01
        return "ELE-P01-TRF-01"


# Função para verificar se o nome do transformador já existe
def verificar_nome_existe(nome):
    try:
        with open("transformadores.json", "r") as file:
            dados_arquivo = json.load(file)
        transformadores = dados_arquivo.get("transformadores", [])
        for trafo in transformadores:
            if trafo["nome"] == nome:
                return True
        return False
    except FileNotFoundError:
        return False


# Função para salvar os dados dos transformadores em um arquivo JSON
def salvar_dados():
    nome = entry_nome.get()
    
    # Verifica se o campo nome está vazio
    if nome.strip() == "":
        messagebox.showerror("Erro", "Nome do transformador não pode estar vazio!")
        return

    # Verifica se o nome já existe
    if verificar_nome_existe(nome):
        sobrescrever = messagebox.askyesno("Aviso", "Transformador já cadastrado. Deseja sobrescrever os dados?")
        if not sobrescrever:
            return

    # Coleta os dados de entrada
    dados = {
        "nome": nome,
        "P": float(entry_potencia.get()) if entry_potencia.get() else None,
        "Vprim": float(entry_vprim.get()) if entry_vprim.get() else None,
        "Vsec": float(entry_vsec.get()) if entry_vsec.get() else None,
        "Z_percent": float(entry_zpercent.get()) if entry_zpercent.get() else None,
        "Pcut": float(entry_pcut.get()) if entry_pcut.get() else None,
        "Iprim": float(entry_iprim.get()) if entry_iprim.get() else None,
        "Isec": float(entry_isec.get()) if entry_isec.get() else None,
        "R0": float(entry_r0.get()) if entry_r0.get() else None,
        "X0": float(entry_x0.get()) if entry_x0.get() else None,
        "Z0": float(entry_z0.get()) if entry_z0.get() else None,
        "R1": float(entry_r1.get()) if entry_r1.get() else None,
        "X1": float(entry_x1.get()) if entry_x1.get() else None,
        "Z1": float(entry_z1.get()) if entry_z1.get() else None,
        "R2": float(entry_r2.get()) if entry_r2.get() else None,
        "X2": float(entry_x2.get()) if entry_x2.get() else None,
        "Z2": float(entry_z2.get()) if entry_z2.get() else None
    }

    # Remover campos com valores None antes de salvar no JSON
    dados = {key: value for key, value in dados.items() if value is not None}

    try:
        with open("transformadores.json", "r") as file:
            dados_arquivo = json.load(file)
    except FileNotFoundError:
        dados_arquivo = {"transformadores": []}

    # Verifica se o nome já existe, e se for o caso, sobreescreve
    for idx, trafo in enumerate(dados_arquivo["transformadores"]):
        if trafo["nome"] == nome:
            dados_arquivo["transformadores"][idx] = dados
            break
    else:
        # Se não encontrou o transformador, adiciona um novo
        dados_arquivo["transformadores"].append(dados)

    # Salva os dados no arquivo JSON
    with open("transformadores.json", "w") as file:
        json.dump(dados_arquivo, file, indent=4)

    messagebox.showinfo("Sucesso", f"Dados do transformador {nome} salvos com sucesso!")


# Função para limpar os dados do arquivo JSON
def limpar_dados():
    confirmacao = messagebox.askyesno("Confirmação", "Tem certeza que deseja limpar todos os dados?")
    if confirmacao:
        with open("transformadores.json", "w") as file:
            json.dump({"transformadores": []}, file, indent=4)
        messagebox.showinfo("Limpeza", "Todos os dados foram apagados com sucesso!")


# Interface gráfica
root = tk.Tk()
root.title("Cadastro de Transformadores")

# Tamanho da janela para ser maximizada
root.state("zoomed")

# Centraliza a janela
root.geometry("1000x1000+100+100")

# Frame para o cadastro de dados do transformador
frame_transformador = tk.LabelFrame(root, text="Cadastro do Transformador", padx=20, pady=20)
frame_transformador.pack(padx=40, pady=40, fill="both", expand=True)

# Definindo o layout de centralização das caixas de entrada
frame_content = tk.Frame(frame_transformador)
frame_content.grid(row=0, column=0, padx=20, pady=20)

# Seção de dados do transformador
tk.Label(frame_content, text="Nome do Transformador:", font=("Arial", 11)).grid(row=0, column=0, sticky="w", padx=5, pady=10)
entry_nome = tk.Entry(frame_content, width=40, font=("Arial", 11))
entry_nome.grid(row=0, column=1, padx=5, pady=10)
entry_nome.insert(0, gerar_nome_transformador())  # Preenche automaticamente

# Adicionando os campos de entrada
tk.Label(frame_content, text="Potência (P) [kVA]:", font=("Arial", 11)).grid(row=1, column=0, sticky="w", padx=5, pady=10)
entry_potencia = tk.Entry(frame_content, width=40, font=("Arial", 11))
entry_potencia.grid(row=1, column=1, padx=5, pady=10)

tk.Label(frame_content, text="Tensão Primária (Vprim) [V]:", font=("Arial", 11)).grid(row=2, column=0, sticky="w", padx=5, pady=10)
entry_vprim = tk.Entry(frame_content, width=40, font=("Arial", 11))
entry_vprim.grid(row=2, column=1, padx=5, pady=10)

tk.Label(frame_content, text="Tensão Secundária (Vsec) [V]:", font=("Arial", 11)).grid(row=3, column=0, sticky="w", padx=5, pady=10)
entry_vsec = tk.Entry(frame_content, width=40, font=("Arial", 11))
entry_vsec.grid(row=3, column=1, padx=5, pady=10)

tk.Label(frame_content, text="Impedância (%) [Z%]:", font=("Arial", 11)).grid(row=4, column=0, sticky="w", padx=5, pady=10)
entry_zpercent = tk.Entry(frame_content, width=40, font=("Arial", 11))
entry_zpercent.grid(row=4, column=1, padx=5, pady=10)

tk.Label(frame_content, text="Potência de Curto (Pcut) [kVA]:", font=("Arial", 11)).grid(row=5, column=0, sticky="w", padx=5, pady=10)
entry_pcut = tk.Entry(frame_content, width=40, font=("Arial", 11))
entry_pcut.grid(row=5, column=1, padx=5, pady=10)

tk.Label(frame_content, text="Corrente Primária (Iprim) [A]:", font=("Arial", 11)).grid(row=6, column=0, sticky="w", padx=5, pady=10)
entry_iprim = tk.Entry(frame_content, width=40, font=("Arial", 11))
entry_iprim.grid(row=6, column=1, padx=5, pady=10)

tk.Label(frame_content, text="Corrente Secundária (Isec) [A]:", font=("Arial", 11)).grid(row=7, column=0, sticky="w", padx=5, pady=10)
entry_isec = tk.Entry(frame_content, width=40, font=("Arial", 11))
entry_isec.grid(row=7, column=1, padx=5, pady=10)

tk.Label(frame_content, text="R0 (pu):", font=("Arial", 11)).grid(row=8, column=0, sticky="w", padx=5, pady=10)
entry_r0 = tk.Entry(frame_content, width=40, font=("Arial", 11))
entry_r0.grid(row=8, column=1, padx=5, pady=10)

tk.Label(frame_content, text="X0 (pu):", font=("Arial", 11)).grid(row=9, column=0, sticky="w", padx=5, pady=10)
entry_x0 = tk.Entry(frame_content, width=40, font=("Arial", 11))
entry_x0.grid(row=9, column=1, padx=5, pady=10)

tk.Label(frame_content, text="Z0 (pu):", font=("Arial", 11)).grid(row=10, column=0, sticky="w", padx=5, pady=10)
entry_z0 = tk.Entry(frame_content, width=40, font=("Arial", 11))
entry_z0.grid(row=10, column=1, padx=5, pady=10)

tk.Label(frame_content, text="R1 (pu):", font=("Arial", 11)).grid(row=11, column=0, sticky="w", padx=5, pady=10)
entry_r1 = tk.Entry(frame_content, width=40, font=("Arial", 11))
entry_r1.grid(row=11, column=1, padx=5, pady=10)

tk.Label(frame_content, text="X1 (pu):", font=("Arial", 11)).grid(row=12, column=0, sticky="w", padx=5, pady=10)
entry_x1 = tk.Entry(frame_content, width=40, font=("Arial", 11))
entry_x1.grid(row=12, column=1, padx=5, pady=10)

tk.Label(frame_content, text="Z1 (pu):", font=("Arial", 11)).grid(row=13, column=0, sticky="w", padx=5, pady=10)
entry_z1 = tk.Entry(frame_content, width=40, font=("Arial", 11))
entry_z1.grid(row=13, column=1, padx=5, pady=10)

# Adicionando R2, X2, Z2
tk.Label(frame_content, text="R2 (pu):", font=("Arial", 11)).grid(row=14, column=0, sticky="w", padx=5, pady=10)
entry_r2 = tk.Entry(frame_content, width=40, font=("Arial", 11))
entry_r2.grid(row=14, column=1, padx=5, pady=10)

tk.Label(frame_content, text="X2 (pu):", font=("Arial", 11)).grid(row=15, column=0, sticky="w", padx=5, pady=10)
entry_x2 = tk.Entry(frame_content, width=40, font=("Arial", 11))
entry_x2.grid(row=15, column=1, padx=5, pady=10)

tk.Label(frame_content, text="Z2 (pu):", font=("Arial", 11)).grid(row=16, column=0, sticky="w", padx=5, pady=10)
entry_z2 = tk.Entry(frame_content, width=40, font=("Arial", 11))
entry_z2.grid(row=16, column=1, padx=5, pady=10)

# Botões de ação
frame_buttons = tk.Frame(frame_content)
frame_buttons.grid(row=17, column=0, columnspan=2, pady=20)

tk.Button(frame_buttons, text="Salvar Dados", command=salvar_dados, width=20, font=("Arial", 12)).grid(row=0, column=0, padx=5)
tk.Button(frame_buttons, text="Limpar Dados", command=limpar_dados, width=20, font=("Arial", 12)).grid(row=0, column=1, padx=5)

root.mainloop()