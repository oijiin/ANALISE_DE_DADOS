# -*- coding: utf-8 -*-
"""SIMULADOR_LOTERIA.ipynb
"""

!pip install streamlit pandas seaborn matplotlib altair numpy plotly scipy sklearn statsmodels bokeh

import random
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
import numpy as np
import plotly.express as px
from collections import Counter
from scipy.stats import norm, ttest_ind
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score, hamming_loss, zero_one_loss, log_loss, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor  # Import KNeighborsClassifier
import statsmodels.stats.proportion as proportion
from bokeh.plotting import figure, show
from bokeh.io import export_png, output_notebook  # Import output_notebook
from bokeh.layouts import gridplot  # Import gridplot

output_notebook()

def load_and_preprocess_data(file_path):
    """
    Carrega e pré-processa os dados do arquivo Excel.

    Args:
      file_path: Caminho para o arquivo Excel.

    Returns:
      DataFrame pré-processado.
    """
    df = pd.read_excel(file_path, usecols=['Data', 'b.1', 'b.2', 'b.3', 'b.4', 'b.5', 'b.6'])
    coluna_alvo = ['b.1', 'b.2', 'b.3', 'b.4', 'b.5', 'b.6']

    df['Data'] = pd.to_datetime(df['Data'], dayfirst=True, infer_datetime_format=True)

    df['Ano'] = df['Data'].dt.year
    df['Mes'] = df['Data'].dt.month
    df['Dia'] = df['Data'].dt.day
    df['Dia_da_Semana'] = df['Data'].dt.dayofweek  # 0: Monday, 6: Sunday

    return df, coluna_alvo

def analyze_number_frequencies(df, coluna_alvo):
    """
    Calcula e imprime a frequência de cada dezena.

    Args:
      df: DataFrame com os dados.
    """

    @st.cache(allow_output_mutation=True)
    def calcular_frequencia_dezenas(df):
        # Seu código para calcular a frequência das dezenas aqui
        frequencia_dezenas = np.bincount(df[coluna_alvo].values.ravel(), minlength=61)
        for coluna in coluna_alvo:
            frequencia_dezenas = pd.Series(frequencia_dezenas[1:], index=range(1, 61))  # Ajusta o índice para começar em 1
            return frequencia_dezenas

    frequencia_dezenas = calcular_frequencia_dezenas(df)

    # Criar um DataFrame com a frequência das dezenas
    frequencia_dezenas_df = pd.DataFrame({'Dezena': frequencia_dezenas.index, 'Frequencia': frequencia_dezenas.values})

    # Ordenar o DataFrame por frequência em ordem decrescente
    frequencia_dezenas_df = frequencia_dezenas_df.sort_values(by='Frequencia', ascending=False)

    dezenas_mais_frequentes = frequencia_dezenas.nlargest(10)
    dezenas_menos_frequentes = frequencia_dezenas.nsmallest(10)

    print("\nDezenas Mais Frequentes:")
    print(dezenas_mais_frequentes.to_markdown(numalign="left", stralign="left"))

    print("\nDezenas Menos Frequentes:")
    print(dezenas_menos_frequentes.to_markdown(numalign="left", stralign="left"))

    return frequencia_dezenas

def analyze_number_properties(df, frequencia_dezenas):
    """
    Analisa a frequência de pares, ímpares e primos.

    Args:
      df: DataFrame com os dados.
      frequencia_dezenas: Série com a frequência de cada dezena.
    """
    # Filtrar o DataFrame frequencia_dezenas para números pares e ímpares usando a coluna Dezena
    pares = frequencia_dezenas[frequencia_dezenas['Dezena'] % 2 == 0]
    impares = frequencia_dezenas[frequencia_dezenas['Dezena'] % 2 != 0]

    # Filtrar o DataFrame frequencia_dezenas para números primos usando a coluna Dezena
    primos = frequencia_dezenas[np.isin(frequencia_dezenas['Dezena'], [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59])]

    # Calcular a soma da coluna Frequencia para cada grupo
    frequencia_classificacao = pd.Series({
        'par': pares['Frequencia'].sum(),
        'ímpar': impares['Frequencia'].sum(),
        'primo': primos['Frequencia'].sum()
    })

    print("\nFrequência de Pares, Ímpares e Primos:")
    print(frequencia_classificacao.to_markdown(numalign="left", stralign="left"))

    return pares, impares, primos, frequencia_classificacao

def analyze_number_sequences(df, coluna_alvo):
    """
    Investiga a ocorrência de sequências numéricas.

    Args:
      df: DataFrame com os dados.
    """
    def check_sequence(window):
        # Check if window has at least 3 values before accessing elements
        if len(window) >= 3:
            return (window.iloc[0] == window.iloc[1] - 1 and window.iloc[1] == window.iloc[2] - 1)
        else:
            return False  # Return False if window has less than 3 values

    sequencias = []
    for col in coluna_alvo:
        for window in df[col].rolling(window=3):
            if len(window) == 3 and check_sequence(window):
                sequencias.append(tuple(window))

    frequencia_sequencias = pd.Series(sequencias).value_counts()

    print("\nFrequência de Sequências Numéricas:")
    print(frequencia_sequencias.to_markdown(numalign="left", stralign="left"))

    return frequencia_sequencias

def analyze_seasonal_patterns(df, coluna_alvo):
    """
    Avalia a presença de padrões sazonais.

    Args:
      df: DataFrame com os dados.
    """
    df['Trimestre'] = df['Data'].dt.quarter

    frequencia_dezenas_trimestre = df.groupby('Trimestre')[coluna_alvo].agg(['mean', 'std', 'min', 'max'])

    print("\nFrequência das Dezenas por Trimestre:")
    print(frequencia_dezenas_trimestre.to_markdown(numalign="left", stralign="left"))

    return frequencia_dezenas_trimestre

def calculate_descriptive_statistics(df, coluna_alvo):
    """
    Calcula as estatísticas descritivas.

    Args:
      df: DataFrame com os dados.
    """
    estatisticas_descritivas = pd.DataFrame({
        'Média': np.mean(df[coluna_alvo].values, axis=0),
        'Desvio Padrão': np.std(df[coluna_alvo].values, axis=0),
        'Amplitude': np.ptp(df[coluna_alvo].values, axis=0),  # ptp calcula a amplitude (peak-to-peak)it 'amplitude'
        'moda': lambda x: x.mode()[0],  # Calculate the mode and name it 'moda'
        'mediana': 'median'  # Calculate the median and name it 'mediana'
    }, index=coluna_alvo)

    estatisticas_descritivas = df[coluna_alvo].agg(['mean', 'std', lambda x: x.max() - x.min(), lambda x: x.mode()[0], 'median'])  # Calculate all stats at once
    estatisticas_descritivas = estatisticas_descritivas.T  # Transpose to have stats as columns
    estatisticas_descritivas.columns = ['Média', 'Desvio Padrão', 'Amplitude', 'moda', 'mediana']  # Rename columns

    print("\nEstatísticas Descritivas:")
    print(estatisticas_descritivas.to_markdown(numalign="left", stralign="left"))

    return estatisticas_descritivas

def perform_extra_analyses(df, coluna_alvo):
    """
    Realiza análises extras.

    Args:
      df: DataFrame com os dados.
    """
    frequencia_dezenas_dia_semana = df.groupby('Dia_da_Semana')[coluna_alvo].agg(
        lambda x: x.value_counts().sum()  # Sum the frequencies without specifying an axis
    ).fillna(0).astype(int)

    print("\nFrequência das Dezenas por Dia da Semana:")
    print(frequencia_dezenas_dia_semana.to_markdown(numalign="left", stralign="left"))  # Corrigido: adicionado .to_markdown() e fechado o parênteses

    media_desvio_padrao = df[coluna_alvo].agg(['mean', 'std'])
    print("\nMédia e Desvio Padrão dos Números Sorteados:")
    print(media_desvio_padrao.to_markdown(numalign="left", stralign="left"))

    df['Soma_Dezenas'] = df[coluna_alvo].sum(axis=1)
    print("\nSoma das Dezenas:")
    print(df['Soma_Dezenas'].describe().to_markdown(numalign="left", stralign="left"))

    correlacao_dezenas = df[coluna_alvo].corr()
    print("\nCorrelação entre as Dezenas:")
    print(correlacao_dezenas.to_markdown(numalign="left", stralign="left"))

    return frequencia_dezenas_dia_semana, media_desvio_padrao, correlacao_dezenas

def calculate_and_print_metrics(df, coluna_alvo):
    """
    Calcula e imprime as métricas.

    Args:
      df: DataFrame com os dados.
    """
    total_sorteios = len(df) * len(coluna_alvo)

    frequencia_relativa = df[coluna_alvo].apply(pd.value_counts, normalize=True).sum(axis=1).fillna(0)

    print("\nFrequência Relativa das Dezenas:")
    print(frequencia_relativa.to_markdown(numalign="left", stralign="left"))

    z = norm.ppf(0.975)  # Valor crítico para intervalo de confiança de 95%
    margem_erro = z * (frequencia_relativa * (1 - frequencia_relativa) / total_sorteios) ** 0.5

    intervalo_confianca = proportion.proportion_confint(frequencia_relativa, total_sorteios, alpha=0.05, method='normal')

    print("\nIntervalo de Confiança para a Frequência das Dezenas:")
    print(pd.DataFrame({
        "Dezena": frequencia_relativa.index,
        "Frequência Relativa": frequencia_relativa,
        "Total Sorteios": [total_sorteios] * len(frequencia_relativa),
        "Margem de Erro": margem_erro,
        "Limite Inferior": intervalo_confianca[0],
        "Limite Superior": intervalo_confianca[1],
    }).to_markdown(numalign="left", stralign="left"))

    dezena1 = 10
    dezena2 = 26
    t_stat, p_valor = ttest_ind(df[df['b.1'] == dezena1]['b.1'], df[df['b.1'] == dezena2]['b.1'])
    print(f"\nTeste de Hipóteses para comparar a frequência das dezenas {dezena1} e {dezena2}:")
    print(f"t-statistic: {t_stat:.2f}")
    print(f"p-value: {p_valor:.3f}")

    return frequencia_relativa, intervalo_confianca

def perform_feature_engineering(df, coluna_alvo):
    """
    Realiza a engenharia de atributos.

    Args:
      df: DataFrame com os dados.

    Returns:
      DataFrame com os atributos modificados.
    """
    for col in coluna_alvo:
        for lag in range(1, 4):
            df[f'{col}_lag{lag}'] = df[col].shift(lag).fillna(0).astype(int)
        df.loc[:2, [f'{col}_lag{lag}' for lag in range(1, 4)]] = 0

    for col in coluna_alvo:
        df[f'{col}_freq'] = df[col].rolling(window=100, min_periods=1).apply(lambda x: x.value_counts().get(x.iloc[-1], 0), raw=False).fillna(0).astype(int)

    df['Dia_Semana'] = df['Data'].dt.dayofweek
    df['Dia_Ano'] = df['Data'].dt.dayofyear
    df['Semana_Ano'] = df['Data'].dt.isocalendar().week

    df['Media_Dezenas'] = df[coluna_alvo].mean(axis=1)
    df['Range_Dezenas'] = df[coluna_alvo].apply(lambda row: row.max() - row.min(), axis=1)

    return df

def perform_predictive_modeling(df, coluna_alvo):
    """
    Realiza a modelagem preditiva.

    Args:
      df: DataFrame com os dados.
    """
    X = df[['Dia_Semana', 'Dia_Ano', 'Semana_Ano', 'Soma_Dezenas', 'Media_Dezenas', 'Range_Dezenas'] + [f'{col}_lag{lag}' for col in coluna_alvo for lag in range(1, 4)] + [f'{col}_freq' for col in coluna_alvo]]

    for target_col in coluna_alvo:
        y = df[target_col].apply(lambda x: 1 if x > 0 else 0)

        if len(np.unique(y)) < 2:
            print(f"Target column '{target_col}' has only one class. Skipping Logistic Regression for this column.")
            continue

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        modelo_rl = LogisticRegression(max_iter=10000)
        modelo_rl.fit(X_train, y_train)

        previsoes_rl = modelo_rl.predict_proba(X_test)[:, 1]

        log_loss_rl = log_loss(y_test, previsoes_rl)
        print(f"\nLog Loss da Regressão Logística para {target_col}: {log_loss_rl:.2f}")

        modelo_knn = KNeighborsClassifier()
        modelo_knn.fit(X_train, y_train)

        previsoes_knn = modelo_knn.predict(X_test)

        hamming_loss_knn = hamming_loss(y_test, previsoes_knn)
        print(f"\nHamming Loss do KNN para {target_col}: {hamming_loss_knn:.2f}")

        accuracy_knn = accuracy_score(y_test, previsoes_knn)
        print(f"Accuracy do KNN para {target_col}: {accuracy_knn:.2f}")

        mse_knn = mean_squared_error(y_test, previsoes_knn)
        r2_knn = r2_score(y_test, previsoes_knn)
        print(f"\nMean Squared Error do KNN para {target_col}: {mse_knn:.2f}")
        print(f"R-squared do KNN para {target_col}: {r2_knn:.2f}")

    # 13.2. Classificação de Números com Random Forest
    # ... (código para Random Forest)

    # 13.3. Agrupamento de Resultados com K-Means
    # ... (código para K-Means)

def visualize_results(df, coluna_alvo, frequencia_dezenas, frequencia_classificacao, frequencia_dezenas_ano, estatisticas_descritivas, frequencia_dezenas_trimestre):
    """
    Visualiza os resultados.

    Args:
      df: DataFrame com os dados.
      # ... (outros argumentos)
    """
    plt.figure(figsize=(12, 6))
    frequencia_dezenas.sort_index().plot(kind='bar')
    plt.title('Frequência das Dezenas da Mega Sena')
    plt.xlabel('Dezena')
    plt.ylabel('Frequência')
    plt.show()

    plt.figure(figsize=(8, 8))
    plt.pie(frequencia_classificacao, labels=frequencia_classificacao.index, autopct='%1.1f%%', startangle=140)
    plt.title('Proporção de Pares, Ímpares e Primos')
    plt.show()

    plt.figure(figsize=(12, 8))
    sns.heatmap(frequencia_dezenas_ano.T, cmap='viridis', annot=True, fmt='.0f')
    plt.title('Frequência das Dezenas ao Longo dos Anos')
    plt.xlabel('Ano')
    plt.ylabel('Dezena')
    plt.show()

    plt.figure(figsize=(8, 6))
    plt.scatter(frequencia_dezenas.sort_index(), frequencia_dezenas.sort_index().shift(1))
    plt.title('Comparação da Frequência de Duas Dezenas Consecutivas')
    plt.xlabel('Dezena')
    plt.ylabel('Frequência da Dezena Anterior')
    plt.show()
    # 9.5. Gráficos de dispersão para cada par de dezenas (Altair)
    for i in range(1, 6):
        for j in range(i + 1, 7):
            alvo1 = f'b.{i}'
            alvo2 = f'b.{j}'
            chart = alt.Chart(df).mark_point().encode(
                x=alvo1,
                y=alvo2,
                tooltip=[alvo1, alvo2]
            ).properties(title=f'Dispersão entre {alvo1} e {alvo2}')
            chart.save(f'dispersao_{alvo1}_{alvo2}.json')

    # 9.6. Gráfico de linhas para a média das dezenas ao longo do tempo (Altair)
    estatisticas_descritivas['Data'] = df['Data']

    # ***CHANGE***: Calculate 'moda' and 'mediana' before creating the chart
    # These should be calculated on the entire columns, not element-wise
    estatisticas_descritivas['moda'] = df[coluna_alvo].mode().iloc[0]  # Get the first mode of each column
    estatisticas_descritivas['mediana'] = df[coluna_alvo].median()

    # ***CHANGE***: Convert 'Data' column to ISO format strings
    estatisticas_descritivas['Data'] = estatisticas_descritivas['Data'].dt.strftime('%Y-%m-%d')

    chart = alt.Chart(estatisticas_descritivas.reset_index()).mark_line().encode(
        x='Data:T',  # Specify 'Data' as a temporal field
        y='Média:Q',  # Specify 'Média' as a quantitative field
        tooltip=['Data:T', 'Média:Q']
    ).properties(title='Média das Dezenas Sorteadas ao Longo do Tempo')

    # ***CHANGE***: Use 'json' format and specify 'vega-lite' spec
    chart.save('media_dezenas_tempo.json', format='json')  # Use 'json' format

    # 9.7. Gráfico de barras para a frequência das dezenas em cada trimestre (Altair)
    df_melted = df.melt(id_vars=['Trimestre'], value_vars=coluna_alvo, var_name='Dezena', value_name='Valor')
    frequencia_dezenas_trimestre = df_melted.groupby(['Trimestre', 'Valor'], as_index=False).size()
    chart = alt.Chart(frequencia_dezenas_trimestre).mark_bar().encode(
        x=alt.X('Valor:N', axis=None),
        y=alt.Y('size:Q', title='Frequência'),
        color='Valor:N',
        column='Trimestre:N',
        tooltip=['Trimestre', 'Valor', 'size']
    ).properties(title='Frequência das Dezenas por Trimestre')
    chart.save('frequencia_dezenas_trimestre.json')

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Load the dataframe
df = pd.read_excel('/content/2786_crescente (1).xlsx')

# Display the first 5 rows
print(df.head().to_markdown(index=False, numalign="left", stralign="left"))

# Print the column names and their data types
print(df.info())

# Convert `Data` to datetime
df['Data'] = pd.to_datetime(df['Data'], dayfirst=True)

# Create a new column `Trimestre`
df['Trimestre'] = df['Data'].dt.quarter

# Print the first 5 rows of the dataframe
print(df.head().to_markdown(index=False, numalign="left", stralign="left")
)
# Print the column name and their data types
print(df.info())

# Group by `Trimestre` and aggregate
coluna_alvo = ['b.1', 'b.2', 'b.3', 'b.4', 'b.5', 'b.6']
frequencia_dezenas_trimestre = df.groupby('Trimestre')[coluna_alvo].agg(['mean', 'std', 'min', 'max'])

# Print the results
print(frequencia_dezenas_trimestre.to_markdown(numalign="left", stralign="left"))

# Mostre as primeiras 5 linhas do DataFrame
print(df.head().to_markdown(index=False, numalign="left", stralign="left"))

# Imprima os nomes das colunas e seus tipos de dados
print(df.info())

# Converta a coluna `Data` para o tipo datetime
df['Data'] = pd.to_datetime(df['Data'], dayfirst=True)

# Crie uma nova coluna `Trimestre` com base no trimestre da coluna `Data`
df['Trimestre'] = df['Data'].dt.quarter

# Mostre as primeiras 5 linhas do DataFrame
print(df.head().to_markdown(index=False, numalign="left", stralign="left"))

# Imprima os nomes das colunas e seus tipos de dados
print(df.info())

# Corpo principal do script
if __name__ == "__main__":
    file_path = "/content/2786_crescente (1).xlsx"  # Substitua pelo caminho correto do arquivo
    df, coluna_alvo = load_and_preprocess_data(file_path)

    frequencia_dezenas = analyze_number_frequencies(df, coluna_alvo)
    pares, impares, primos, frequencia_classificacao = analyze_number_properties(df, frequencia_dezenas)
    analyze_number_sequences(df, coluna_alvo)
    analyze_seasonal_patterns(df, coluna_alvo)
    estatisticas_descritivas = calculate_descriptive_statistics(df, coluna_alvo)
    perform_extra_analyses(df, coluna_alvo)
    calculate_and_print_metrics(df, coluna_alvo)
    df = perform_feature_engineering(df, coluna_alvo)
    perform_predictive_modeling(df, coluna_alvo)

    # Visualizar os resultados
    frequencia_dezenas_ano = df.groupby('Ano')[coluna_alvo].apply(lambda x: x.apply(pd.value_counts).sum(axis=0))

    # ... (preparar outros dados para visualização)
    visualize_results(
        df,
        coluna_alvo,
        frequencia_dezenas,
        frequencia_classificacao,
        frequencia_dezenas_ano,
        estatisticas_descritivas,
        frequencia_dezenas_trimestre
      )

# Convert the string in the `numeros_apostados` column to a list of integers
df_resultados['numeros_apostados'] = df_resultados['numeros_apostados'].astype(str).str.replace('[\[\]]', '', regex=True)
df_resultados['numeros_apostados'] = df_resultados['numeros_apostados'].str.split(', ').apply(lambda x: [int(i) for i in x])

# Convert the list to a NumPy array
numeros_apostados_array = np.array(df_resultados['numeros_apostados'].tolist())

# Reshape the array to 7 x 6 (because there are 7 rows in df_resultados)
numeros_apostados_array = numeros_apostados_array.reshape(len(df_resultados), 6)
# This assumes each row in df_resultados has 6 numbers.

# Print the first 5 rows of the dataframe
print(df_dados_historicos.head().to_markdown(index=False, numalign="left", stralign="left"))

# Print the column name and their data types
print(df_dados_historicos.info())

# Convert the NumPy array to a pandas Series
numeros_apostados_series = pd.Series(numeros_apostados_array.flatten())

# Concatenate the two series
combined_series = pd.concat([numeros_apostados_series, frequencia_dezenas])

# Create a DataFrame from the combined series
df_combined = pd.DataFrame({'Number': combined_series.index, 'Frequency': combined_series.values})

# Group the DataFrame by 'Number' and calculate the sum of 'Frequency' for each group
probabilidades = df_combined.groupby('Number')['Frequency'].sum()

# Normalize the probabilities
probabilidades_normalizadas = probabilidades / probabilidades.sum()

# Extract the values from the probabilidades_normalizadas series
pesos = probabilidades_normalizadas.values

# Print the pesos array
print(pesos)

class Jogo:
    def __init__(self):
        self.numeros_sorteados = []

    def sortear(self):
        self.numeros_sorteados = random.sample(range(1, 61), 6)
        return self.numeros_sorteados

class Jogador:
    def __init__(self, df_historico, pesos):
        self.df_historico = df_historico
        self.numeros_apostados = []
        self.recompensa_total = 0
        self.pesos = pesos

    def analisar_dados(self):
        # Analisar o histórico de jogos e escolher os números com base nos pesos
        numeros_possiveis = list(range(1, 61))

        # Ajustar o tamanho do array de pesos para corresponder ao número de números possíveis
        self.pesos = np.resize(self.pesos, len(numeros_possiveis))

        self.numeros_apostados = random.choices(numeros_possiveis, weights=self.pesos, k=6)

    def apostar(self):
        self.analisar_dados()
        return self.numeros_apostados

    def calcular_recompensa(self, acertos):
        """
        Calcula a recompensa com base no número de acertos e na quantidade de números frequentes escolhidos.

        Args:
          acertos: Número de acertos.

        Returns:
          Valor da recompensa.
        """
        qtd_numeros_frequentes = len(set(self.numeros_apostados).intersection(set(top_10_mais_frequentes.index)))
        recompensa_base = {
            0: -100,
            1: 200,
            2: 1000,
            3: 5000,
            4: 200000,
            5: 20000000,
            6: 500000000
        }

        recompensa = recompensa_base[acertos]

        # Penalizar o jogador por escolher números frequentes demais
        if qtd_numeros_frequentes >= 4:
            recompensa *= 0.8

        self.recompensa_total += recompensa
        return recompensa

# Imprimir as recompensas para diferentes combinações de acertos e números frequentes
for acertos in range(7):
    for qtd_numeros_frequentes in range(7):
        recompensa = jogador.calcular_recompensa(acertos)
        print(f'Acertos: {acertos}, Números frequentes: {qtd_numeros_frequentes}, Recompensa: {recompensa}')

def comparar_numeros(numeros_sorteados, numeros_apostados):
    acertos = set(numeros_sorteados).intersection(numeros_apostados)
    return len(acertos)

def armazenar_resultados(resultados, jogo, jogador, acertos):
    novo_resultado = {
        'numeros_sorteados': jogo.numeros_sorteados,
        'numeros_apostados': jogador.numeros_apostados,
        'acertos': acertos
    }
    resultados.append(novo_resultado)

def salvar_resultados(resultados):
    df_resultados = pd.DataFrame(resultados)
    df_resultados.to_csv('resultados_simulacao.csv', index=False)

# Carregar o histórico de jogos
file_path = ('/content/2786_crescente (1).xlsx')
df_historico, coluna_alvo = load_and_preprocess_data(file_path)

# Inicializar o jogo e o jogador
jogo = Jogo()
jogador = Jogador(df_historico, pesos)

# Inicializar a lista de resultados
resultados = []

# Executar a simulação até que o jogador acerte pelo menos uma dezena
acertos = 0
while acertos == 0:
    numeros_sorteados = jogo.sortear()
    numeros_apostados = jogador.apostar()
    acertos = comparar_numeros(numeros_sorteados, numeros_apostados)
    armazenar_resultados(resultados, jogo, jogador, acertos)

# Salvar os resultados da simulação
salvar_resultados(resultados)

# Imprimir os resultados
print("\nResultados da Simulação:")
for resultado in resultados:
    print(f"Números sorteados: {resultado['numeros_sorteados']}")
    print(f"Números apostados: {resultado['numeros_apostados']}")
    print(f"Acertos: {resultado['acertos']}\n")
    print(f"Recompensa: {jogador.calcular_recompensa(resultado['acertos'])}\n")  # Imprimir a recompensa da rodada

# Imprimir a recompensa total do jogador
print(f'Recompensa total do jogador: {jogador.recompensa_total}')

# Carregar os resultados da simulação
df_resultados = pd.read_csv('resultados_simulacao.csv')

# Imprimir as primeiras 5 linhas
print(df_resultados.head().to_markdown(index=False, numalign="left", stralign="left"))

# Imprimir os nomes das colunas e seus tipos de dados
print(df_resultados.info())

# Calcular a média de acertos por rodada
media_acertos = df_resultados['acertos'].mean()
print(f'Média de acertos por rodada: {media_acertos}')

# Calcular a frequência das dezenas apostadas
numeros_apostados_serie = df_resultados['numeros_apostados'].astype(str).str.replace('[\[\]]', '', regex=True)

# Contar as ocorrências de cada número na série numeros_apostados_serie
frequencia_dezenas_apostadas = Counter(numeros_apostados_serie.str.split(', ').sum())

# Converter frequencia_dezenas_apostadas em um DataFrame
df_frequencia_dezenas_apostadas = pd.DataFrame(
    {
        'Dezena': [int(x) for x in frequencia_dezenas_apostadas.keys()],
        'Frequencia': list(frequencia_dezenas_apostadas.values()),
    }
)

# Imprimir o DataFrame com a frequência das dezenas apostadas
print("\nDataFrame com a frequência das dezenas apostadas:")
print(df_frequencia_dezenas_apostadas.to_markdown(index=False, numalign="left", stralign="left"))

# Criar um gráfico de barras com as dezenas apostadas no eixo x e suas frequências no eixo y
chart = alt.Chart(df_frequencia_dezenas_apostadas).mark_bar().encode(
    x=alt.X('Dezena', title='Dezena'),
    y=alt.Y('Frequencia', title='Frequência'),
    tooltip=['Dezena', 'Frequencia']
).properties(
    title='Frequência das Dezenas Apostadas',
).interactive()
chart.save('frequencia_dezenas_apostadas.json')

# Load the dataframe.
df_dados_historicos = pd.read_excel('/content/2786_crescente (1).xlsx')

# Calculate the frequency of each number drawn.
coluna_alvo = ['b.1', 'b.2', 'b.3', 'b.4', 'b.5', 'b.6']
frequencia_dezenas = np.bincount(df_dados_historicos[coluna_alvo].values.ravel(), minlength=61)
frequencia_dezenas = pd.Series(frequencia_dezenas[1:], index=range(1, 61))

# Identify the top 10 most frequent numbers.
top_10_mais_frequentes = frequencia_dezenas.nlargest(10)

# Print the top 10 most frequent numbers.
print(top_10_mais_frequentes.to_markdown(numalign="left", stralign="left"))
