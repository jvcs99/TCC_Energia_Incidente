import json
import pandas as pd
import math

# Função para ler os dados do Excel
def ler_tabela_cabos_excel(arquivo_excel):
    df = pd.read_excel(arquivo_excel)
    tabela_cabos = []
    for _, row in df.iterrows():
        tabela_cabos.append({
            "potencia_kVA": row["Potência (kVA)"],
            "impedancia": row["Impedância (%)"] / 100  # Convertendo porcentagem para valor decimal
        })
    return tabela_cabos

# Função para obter a impedância do cabo com base na potência
def obter_impedancia_cabo(potencia_kVA, tabela_cabos):
    for item in tabela_cabos:
        if item["potencia_kVA"] == potencia_kVA:
            return item["impedancia"]
    return 0  # Se não encontrar, retorna 0

# Função para calcular a impedância do transformador
def calcular_impedancia_transformador(R1, X1, R2, X2):
    Z1 = complex(R1, X1)  # Sequência positiva
    Z2 = complex(R2, X2)  # Sequência negativa
    Z_eq = (Z1 + Z2) / 2  # Impedância equivalente
    return Z_eq

# Função para calcular a corrente de curto-circuito
def calcular_corrente_curto_circuito(Vn, Z_total):
    return Vn / (math.sqrt(3) * abs(Z_total))  # Corrente trifásica de curto-circuito

# Função para ler todos os transformadores do JSON
def carregar_transformadores_json(caminho_json):
    with open(caminho_json, 'r') as file:
        dados = json.load(file)
    
    # Acessar a lista de transformadores
    transformadores = dados.get("transformadores", [])
    
    if not transformadores:
        raise ValueError("Não foram encontrados transformadores no arquivo JSON.")
    
    return transformadores

# Função para calcular todos os transformadores
def calcular_transformadores(caminho_json, arquivo_excel):
    # Carregar a tabela de cabos do Excel
    tabela_cabos = ler_tabela_cabos_excel(arquivo_excel)
    
    # Carregar transformadores do JSON
    transformadores = carregar_transformadores_json(caminho_json)
    
    # Armazenar resultados
    resultados = []
    
    for transformador in transformadores:
        P = transformador.get("P", 0)
        Vn = transformador.get("Vsec", 0)
        R1 = transformador.get("R1", 0)
        X1 = transformador.get("X1", 0)
        R2 = transformador.get("R2", 0)
        X2 = transformador.get("X2", 0)
        
        # Calcular impedância do transformador
        Z_transformador = calcular_impedancia_transformador(R1, X1, R2, X2)

        # Obter impedância do cabo com base na potência
        Z_cabo = obter_impedancia_cabo(P, tabela_cabos)

        # Impedância total
        Z_total = Z_transformador + Z_cabo

        # Calcular corrente de curto-circuito
        Ibf = calcular_corrente_curto_circuito(Vn, Z_total)

        # Adicionar resultados para este transformador
        resultados.append({
            "Nome": transformador.get("nome", "Desconhecido"),
            "Potência (kVA)": P,
            "Tensão Secundária (V)": Vn,
            "Impedância Transformador": Z_transformador,
            "Impedância Cabo": Z_cabo,
            "Impedância Total": Z_total,
            "Corrente de Curto-Circuito (A)": Ibf
        })
    
    return resultados

# Caminho para o arquivo JSON
caminho_json = 'transformadores.json'

# Caminho para o arquivo Excel
arquivo_excel = 'table_one.xlsx'  # O arquivo está na mesma pasta do código

# Calcular os resultados para todos os transformadores
resultados = calcular_transformadores(caminho_json, arquivo_excel)

# Exibir resultados
for resultado in resultados:
    print(f"Nome do Transformador: {resultado['Nome']}")
    print(f"  Potência (kVA): {resultado['Potência (kVA)']}")
    print(f"  Tensão Secundária (V): {resultado['Tensão Secundária (V)']}")
    print(f"  Impedância do Transformador: {resultado['Impedância Transformador']}")
    print(f"  Impedância do Cabo: {resultado['Impedância Cabo']}")
    print(f"  Impedância Total: {resultado['Impedância Total']}")
    print(f"  Corrente de Curto-Circuito (A): {resultado['Corrente de Curto-Circuito (A)']}\n")
