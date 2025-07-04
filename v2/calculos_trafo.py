import json
import math

# Função para carregar os dados do transformador do arquivo JSON
def carregar_transformadores():
    try:
        with open("transformadores.json", "r") as file:
            dados_arquivo = json.load(file)
        return dados_arquivo["transformadores"]
    except FileNotFoundError:
        print("Arquivo de transformadores não encontrado.")
        return []

# Função para calcular a impedância equivalente
def calcular_impedancia_equivalente(R1, X1, R2, X2):
    Z1 = complex(R1, X1)  # Sequência positiva
    Z2 = complex(R2, X2)  # Sequência negativa
    Z_eq = (Z1 + Z2) / 2
    return Z_eq

# Função para calcular a corrente eficaz (usando a fórmula I = P / (√3 * V * cosφ))
def calcular_corrente_eficaz(P, V, cos_phi=1):
    I = P * 1000 / (math.sqrt(3) * V * cos_phi)  # Potência em kVA, convertida para VA
    return I

# Função para calcular a corrente de curto-circuito trifásica simétrica
def calcular_corrente_curto(P, V, Z_eq):
    Icc = (P * 1000) / (math.sqrt(3) * V * Z_eq)  # Potência em kVA, convertida para VA
    return Icc

# Função para calcular a constante de tempo (aproximadamente: T = L / R)
def calcular_constante_tempo(L, R):
    tau = L / R
    return tau

# Função para calcular o tempo de curto-circuito (tempo = (constante de tempo * ln(2)))
def calcular_tempo_curto(tau):
    tempo_curto = tau * math.log(2)
    return tempo_curto

# Função para determinar a corrente do arco elétrico
def calcular_corrente_arco(Icc):
    Ia = math.log(Icc)  # Corrente do arco elétrico (aproximada por logaritmo da corrente de curto-circuito)
    return Ia

# Função para calcular todos os parâmetros do transformador
def calcular_parametros(nome):
    # Carrega os dados do transformador
    transformadores = carregar_transformadores()

    for trafo in transformadores:
        if trafo["nome"] == nome:
            # Coleta os dados necessários
            P = trafo.get("P", 0)  # Potência nominal (kVA)
            Vprim = trafo.get("Vprim", 0)  # Tensão primária (V)
            Vsec = trafo.get("Vsec", 0)  # Tensão secundária (V)
            R1 = trafo.get("R1", 0)  # Impedância sequência positiva (R1)
            X1 = trafo.get("X1", 0)  # Impedância sequência positiva (X1)
            R2 = trafo.get("R2", 0)  # Impedância sequência negativa (R2)
            X2 = trafo.get("X2", 0)  # Impedância sequência negativa (X2)
            L = 0.5  # Exemplo de valor da indutância (H), deve ser definido conforme especificações
            cos_phi = 0.9  # Fator de potência (valor padrão, pode ser ajustado)
            
            # Calculando os parâmetros
            Z_eq = calcular_impedancia_equivalente(R1, X1, R2, X2)
            I_eficaz = calcular_corrente_eficaz(P, Vsec, cos_phi)
            Icc = calcular_corrente_curto(P, Vsec, Z_eq)
            tau = calcular_constante_tempo(L, R1)  # L e R podem ser ajustados conforme necessidade
            tempo_curto = calcular_tempo_curto(tau)
            Ia = calcular_corrente_arco(Icc)

            # Exibindo os resultados
            print(f"Nome do Transformador: {nome}")
            print(f"Impedância Equivalente: {Z_eq}")
            print(f"Corrente Eficaz: {I_eficaz} A")
            print(f"Corrente de Curto-Circuito: {Icc} A")
            print(f"Constante de Tempo: {tau} s")
            print(f"Tempo de Curto-Circuito: {tempo_curto} s")
            print(f"Corrente do Arco Elétrico: {Ia} A")
            return {
                "Z_eq": Z_eq,
                "I_eficaz": I_eficaz,
                "Icc": Icc,
                "tau": tau,
                "tempo_curto": tempo_curto,
                "Ia": Ia
            }
    
    print("Transformador não encontrado.")
    return None


# Função principal para rodar os cálculos
if __name__ == "__main__":
    nome_trafo = input("Digite o nome do transformador (ex: ELE-P01-TRF-01): ")
    resultados = calcular_parametros(nome_trafo)

    if resultados:
        print("\nResultados Calculados:")
        print(f"Impedância Equivalente: {resultados['Z_eq']}")
        print(f"Corrente Eficaz: {resultados['I_eficaz']} A")
        print(f"Corrente de Curto-Circuito: {resultados['Icc']} A")
        print(f"Constante de Tempo: {resultados['tau']} s")
        print(f"Tempo de Curto-Circuito: {resultados['tempo_curto']} s")
        print(f"Corrente do Arco Elétrico: {resultados['Ia']} A")
