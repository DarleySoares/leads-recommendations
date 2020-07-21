#!/usr/bin/env python
# coding: utf-8

# # Desafio 6
# 
# Neste desafio, vamos praticar _feature engineering_, um dos processos mais importantes e trabalhosos de ML. Utilizaremos o _data set_ [Countries of the world](https://www.kaggle.com/fernandol/countries-of-the-world), que contém dados sobre os 227 países do mundo com informações sobre tamanho da população, área, imigração e setores de produção.
# 
# > Obs.: Por favor, não modifique o nome das funções de resposta.

# ## _Setup_ geral

# In[1]:


import pandas as pd
import numpy as np
import seaborn as sns
import sklearn as sk

from sklearn.preprocessing import KBinsDiscretizer, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer


# In[2]:


countries = pd.read_csv("countries.csv")


# In[3]:


new_column_names = [
    "Country", "Region", "Population", "Area", "Pop_density", "Coastline_ratio",
    "Net_migration", "Infant_mortality", "GDP", "Literacy", "Phones_per_1000",
    "Arable", "Crops", "Other", "Climate", "Birthrate", "Deathrate", "Agriculture",
    "Industry", "Service"
]

countries.columns = new_column_names

countries.head(5)


# ## Observações
# 
# Esse _data set_ ainda precisa de alguns ajustes iniciais. Primeiro, note que as variáveis numéricas estão usando vírgula como separador decimal e estão codificadas como strings. Corrija isso antes de continuar: transforme essas variáveis em numéricas adequadamente.
# 
# Além disso, as variáveis `Country` e `Region` possuem espaços a mais no começo e no final da string. Você pode utilizar o método `str.strip()` para remover esses espaços.

# ## Inicia sua análise a partir daqui

# In[4]:


# Sua análise começa aqui.


# In[5]:


# Adequando vírgula para ponto nas colunas que possuem valores números descritos como string
columns = ['Pop_density', 'Coastline_ratio', 'Net_migration', 'Infant_mortality', 'Literacy', 'Phones_per_1000', 'Arable', 'Crops', 'Other','Climate', 'Birthrate', 'Deathrate', 'Agriculture', 'Industry', 'Service']

for column in columns:
    # converte todos para string
    values = countries[column].astype(str)
    # troca a vírgula por ponto e multipilica os negativos por zero
    values = list(map(lambda x: -1*float(x[1:].replace(',','.')) if '-' in x else float(x.replace(',','.')), values))
    # retorna para o dataframe
    countries[column] = values


# In[6]:


# Retirando os espaços vazios no início e fim das string
columns = ['Country', 'Region']

for column in columns:
    values = countries[column]
    values = list(map(lambda x: x.strip(), values))
    countries[column] = values


# In[7]:


# Verificando se todas as features estão nos tipos corretos
countries.info()


# ## Questão 1
# 
# Quais são as regiões (variável `Region`) presentes no _data set_? Retorne uma lista com as regiões únicas do _data set_ com os espaços à frente e atrás da string removidos (mas mantenha pontuação: ponto, hífen etc) e ordenadas em ordem alfabética.

# In[8]:


def q1():
    # gera lista com todas as regiões da lista
    regions = list(countries.Region.unique())
    # ordena
    regions.sort()
    return regions


# ## Questão 2
# 
# Discretizando a variável `Pop_density` em 10 intervalos com `KBinsDiscretizer`, seguindo o encode `ordinal` e estratégia `quantile`, quantos países se encontram acima do 90º percentil? Responda como um único escalar inteiro.

# In[9]:


def q2():
    # cria o processo de discretização
    discretizer = KBinsDiscretizer(n_bins  = 10, encode = 'ordinal', strategy = 'quantile')
    # realiza o processo de fit e transform na coluna
    discretizer.fit(countries[['Pop_density']])
    interval = discretizer.transform(countries[['Pop_density']])
    # calcula a quantidade de países do último intervalo
    return int(sum(interval[:,0] >= 9))


# # Questão 3
# 
# Se codificarmos as variáveis `Region` e `Climate` usando _one-hot encoding_, quantos novos atributos seriam criados? Responda como um único escalar.

# In[10]:


def q3():
    # calcula quantas regiões e climas únicos possui por coluna
    regions = len(countries.Region.unique())
    climate = len(countries.Climate.unique())
    return int(regions+climate)


# ## Questão 4
# 
# Aplique o seguinte _pipeline_:
# 
# 1. Preencha as variáveis do tipo `int64` e `float64` com suas respectivas medianas.
# 2. Padronize essas variáveis.
# 
# Após aplicado o _pipeline_ descrito acima aos dados (somente nas variáveis dos tipos especificados), aplique o mesmo _pipeline_ (ou `ColumnTransformer`) ao dado abaixo. Qual o valor da variável `Arable` após o _pipeline_? Responda como um único float arredondado para três casas decimais.

# In[11]:


test_country = [
    'Test Country', 'NEAR EAST', -0.19032480757326514,
    -0.3232636124824411, -0.04421734470810142, -0.27528113360605316,
    0.13255850810281325, -0.8054845935643491, 1.0119784924248225,
    0.6189182532646624, 1.0074863283776458, 0.20239896852403538,
    -0.043678728558593366, -0.13929748680369286, 1.3163604645710438,
    -0.3699637766938669, -0.6149300604558857, -0.854369594993175,
    0.263445277972641, 0.5712416961268142
]


# In[12]:


# seleciona as colunas do tipo inteiro e float
columns = countries.select_dtypes(['int64', 'float64']).columns

# cria o pipeline com dois processos
pipeline = Pipeline(steps = [
    ('imputer',SimpleImputer(strategy = 'median')),
    ("standard", StandardScaler())
    ])


# In[13]:


def q4():
    # realiza o processo de fit
    pipeline.fit(countries[columns])
    # realiza o pipeline ao test_country
    test_countries_transform = pipeline.transform([test_country[2:]])
    # retorna o valor da coluna Arable
    return float(test_countries_transform[0][9].round(3))


# ## Questão 5
# 
# Descubra o número de _outliers_ da variável `Net_migration` segundo o método do _boxplot_, ou seja, usando a lógica:
# 
# $$x \notin [Q1 - 1.5 \times \text{IQR}, Q3 + 1.5 \times \text{IQR}] \Rightarrow x \text{ é outlier}$$
# 
# que se encontram no grupo inferior e no grupo superior.
# 
# Você deveria remover da análise as observações consideradas _outliers_ segundo esse método? Responda como uma tupla de três elementos `(outliers_abaixo, outliers_acima, removeria?)` ((int, int, bool)).

# In[14]:


def q5():
    # calcula IQR
    iqr = countries.Net_migration.quantile(0.75) - countries.Net_migration.quantile(0.25)
    # determina o range da lógica acima
    _range = [countries.Net_migration.quantile(0.25) - 1.5* iqr, countries.Net_migration.quantile(0.75) + 1.5* iqr]

    # cria coluna para classificar os outliers na parte inferior
    countries['Outlier_Net_migration_lower'] = countries.Net_migration.apply(lambda x: True if x < _range[0] else False)
    # cria coluna para classificar os outliers na parte superior
    countries['Outlier_Net_migration_upper'] = countries.Net_migration.apply(lambda x: True if x > _range[1] else False)

    # calcula a quantidade de outliers
    outliers_lower = int(countries.Outlier_Net_migration_lower.loc[countries.Outlier_Net_migration_lower == True].count())
    outliers_upper = int(countries.Outlier_Net_migration_upper.loc[countries.Outlier_Net_migration_upper == True].count())
    return (outliers_lower, outliers_upper, False)


# ## Questão 6
# Para as questões 6 e 7 utilize a biblioteca `fetch_20newsgroups` de datasets de test do `sklearn`
# 
# Considere carregar as seguintes categorias e o dataset `newsgroups`:
# 
# ```
# categories = ['sci.electronics', 'comp.graphics', 'rec.motorcycles']
# newsgroup = fetch_20newsgroups(subset="train", categories=categories, shuffle=True, random_state=42)
# ```
# 
# 
# Aplique `CountVectorizer` ao _data set_ `newsgroups` e descubra o número de vezes que a palavra _phone_ aparece no corpus. Responda como um único escalar.

# In[15]:


categories = ['sci.electronics', 'comp.graphics', 'rec.motorcycles']
newsgroup = fetch_20newsgroups(subset="train", categories=categories, shuffle=True, random_state=42)

# cria método de Count Vectorizer e aplica ao dataset
count_vectorizer = CountVectorizer()
newsgroup_count = count_vectorizer.fit_transform(newsgroup.data)

# cria o método de Tf-dif e aplica ao dataset
tfdif_transformer = TfidfTransformer()
tfdif_transformer.fit(newsgroup_count)
newsgroup_tfdif= tfdif_transformer.transform(newsgroup_count)

# lista com os nomes das colunas
word_list = count_vectorizer.get_feature_names()


# In[16]:


def q6():
    # cria um dicionário com a palavra e a quantidade de aparições
    count_list = newsgroup_count.toarray().sum(axis = 0)
    dic = dict(zip(word_list, count_list))
    return int(dic['phone'])


# ## Questão 7
# 
# Aplique `TfidfVectorizer` ao _data set_ `newsgroups` e descubra o TF-IDF da palavra _phone_. Responda como um único escalar arredondado para três casas decimais.

# In[17]:


def q7():
    # cria um dicionário com a palavra e o TF-IDF dela
    count_list = newsgroup_tfdif.toarray().sum(axis = 0)
    dic = dict(zip(word_list, count_list))
    return float(round(dic['phone'], 3))

