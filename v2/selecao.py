import tkinter as tk
import subprocess
import os

def chamar_cadastro():
    # Define o nome do arquivo que você quer rodar ao clicar no botão
    arquivo_cadastro = 'z_teste_cadastro.py'
    
    # Verifica se o arquivo existe na mesma pasta
    if os.path.isfile(arquivo_cadastro):
        subprocess.run(['python', arquivo_cadastro])
    else:
        print(f"O arquivo {arquivo_cadastro} não foi encontrado.")

def chamar_calculo():
    # Define o nome do arquivo que você quer rodar ao clicar no botão
    arquivo_calculo = 'z_teste_calculo.py'
    
    # Verifica se o arquivo existe na mesma pasta
    if os.path.isfile(arquivo_calculo):
        subprocess.run(['python', arquivo_calculo])
    else:
        print(f"O arquivo {arquivo_calculo} não foi encontrado.")

# Configuração da janela principal
root = tk.Tk()
root.title("Seleção de Funções")

# Configura a janela para abrir maximizada
root.state('zoomed')  # Maximiza a janela, mas não a coloca em tela cheia

# Cor de fundo da janela
root.configure(bg='#ADD8E6')  # Azul claro

# Cria um frame centralizado para os botões
frame = tk.Frame(root, bg='#4682B4')  # Azul escuro
frame.pack(expand=True)

# Cria o botão para cadastro de cargas
btn_cadastro = tk.Button(frame, text="Cadastro de Cargas", width=30, height=3, font=("Arial", 14), fg="white", bg="#4682B4", activebackground="#5F9EA0", command=chamar_cadastro)
btn_cadastro.grid(row=0, column=0, padx=40, pady=40)

# Cria o botão para cálculo
btn_calculo = tk.Button(frame, text="Cálculo", width=30, height=3, font=("Arial", 14), fg="white", bg="#4682B4", activebackground="#5F9EA0", command=chamar_calculo)
btn_calculo.grid(row=0, column=1, padx=40, pady=40)

# Ajuste do layout para melhor centralização
frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1)

# Inicia o loop da interface gráfica
root.mainloop()
