import pandas as pd
from itertools import combinations
from collections import Counter
import re

# 1. Carregar os dados
df = pd.read_excel("resultados.xlsx")

# 2. Remover vazios
df = df.dropna(subset=['Sequência'])

# 3. Limpar e transformar as sequências
def limpar_e_converter(seq):
    numeros = re.findall(r'\d+', str(seq))
    return tuple(sorted(map(int, numeros)))

df['Sequência'] = df['Sequência'].apply(limpar_e_converter)

# 4. Gerar todas combinações possíveis
todos_possiveis = list(combinations(range(1, 26), 15))

# 5. Frequência de números sorteados
todos_numeros = [n for seq in df['Sequência'] for n in seq]
freq = Counter(todos_numeros)

# 6. Função de "probabilidade"
def probabilidade(seq):
    return sum(freq[n] for n in seq)

# 7. Filtrar combinações não sorteadas
sorteadas = set(df['Sequência'])
nao_sorteadas = [seq for seq in todos_possiveis if seq not in sorteadas]

# 8. Calcular pontuações de probabilidade para todas as não sorteadas
pontuacoes = [(seq, probabilidade(seq)) for seq in nao_sorteadas]

# 9. Normalizar para porcentagem
max_pontuacao = max(p[1] for p in pontuacoes)
pontuacoes_percentual = [
    (seq, pont, (pont / max_pontuacao) * 100) for seq, pont in pontuacoes
]

# 10. Ordenar por probabilidade (maior para menor)
pontuacoes_percentual.sort(key=lambda x: x[2], reverse=True)

# 11. Mostrar top 10 com porcentagem
print("Top 10 sequências que nunca foram sorteadas e têm maior 'probabilidade':\n")
for i, (seq, pont, perc) in enumerate(pontuacoes_percentual[:10], 1):
    print(f"{i}: {' - '.join(f'{n:02}' for n in seq)} | Probabilidade estimada: {perc:.2f}%")

