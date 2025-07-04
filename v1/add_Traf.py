import json

# Função para salvar os dados no arquivo JSON
def salvar_dados(transformadores):
    with open("ele_trafos.json", "w") as arquivo_json:
        json.dump(transformadores, arquivo_json, indent=4)

# Função para adicionar um novo transformador
def adicionar_transformador(transformadores, id_transformador, dados):
    # Verificar se o id já existe
    if id_transformador in transformadores:
        print(f"Transformador {id_transformador} já existe!")
    else:
        transformadores[id_transformador] = dados
        print(f"Transformador {id_transformador} adicionado com sucesso!")

    # Salvar os dados atualizados no JSON
    salvar_dados(transformadores)

# Função para carregar os dados dos transformadores (caso o arquivo já exista)
def carregar_dados():
    try:
        with open("ele_trafos.json", "r") as arquivo_json:
            transformadores = json.load(arquivo_json)
    except FileNotFoundError:
        transformadores = {}
    return transformadores

# Exemplo de uso
if __name__ == "__main__":
    # Carregar os transformadores já cadastrados
    transformadores = carregar_dados()

    # Dados do novo transformador a ser adicionado (transformador T04 como exemplo)
    novo_transformador = {
        "Pt": 600,  # Potência nominal (kVA)
        "Vprim": 13800,  # Tensão primária (V)
        "Vsec": 480,  # Tensão secundária (V)
        "Z_percent": 6.0,  # Impedância percentual (%)
        "Pcut": 35000,  # Potência de curto (kVA)
        "Iprim": 25.45,  # Corrente primária (A)
        "Isec": 720.83,  # Corrente secundária (A)
        "R0": 0.18, "X0": 0.95, "Z0": 1.0,  # Sequência zero
        "R1": 0.08, "X1": 0.85, "Z1": 0.88,  # Sequência positiva
        "R2": 0.12, "X2": 0.80, "Z2": 0.82   # Sequência negativa
    }

    # Adicionar o novo transformador
    adicionar_transformador(transformadores, "ELE-TRAF-04", novo_transformador)

    # Mostrar os dados dos transformadores para verificar
    print(json.dumps(transformadores, indent=4))
