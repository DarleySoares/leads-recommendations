#!/usr/bin/env python
# coding: utf-8

# # Desafio 3
# 
# Neste desafio, iremos praticar nossos conhecimentos sobre distribuições de probabilidade. Para isso,
# dividiremos este desafio em duas partes:
#     
# 1. A primeira parte contará com 3 questões sobre um *data set* artificial com dados de uma amostra normal e
#     uma binomial.
# 2. A segunda parte será sobre a análise da distribuição de uma variável do _data set_ [Pulsar Star](https://archive.ics.uci.edu/ml/datasets/HTRU2), contendo 2 questões.
# 
# > Obs.: Por favor, não modifique o nome das funções de resposta.

# ## _Setup_ geral

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as sct
import seaborn as sns
from statsmodels.distributions.empirical_distribution import ECDF


# ## Parte 1

# ### _Setup_ da parte 1

# In[2]:


np.random.seed(42)
    
dataframe = pd.DataFrame({"normal": sct.norm.rvs(20, 4, size=10000),
                     "binomial": sct.binom.rvs(100, 0.2, size=10000)})


# ## Inicie sua análise a partir da parte 1 a partir daqui

# In[3]:


# Sua análise da parte 1 começa aqui.
# Verifica o tamanho do dataframe
dataframe.shape


# In[4]:


# verifica os valores estatísticos das duas distribuições
dataframe.describe().transpose()


# In[5]:


# plota a distribuição normal
fig, ax = plt.subplots()
sns.distplot(dataframe.normal, hist_kws={'color': 'darkcyan'}, kde_kws={'color': 'darkslategray'})
ax.set_title("Distribuição normal")
plt.show()


# In[6]:


# plota a distribuição binomial
fig, ax = plt.subplots()
sns.distplot(dataframe.binomial, hist_kws={'color': 'darkcyan'}, kde_kws={'color': 'darkslategray'})
ax.set_title("Distribuição binomial")
plt.show()


# ## Questão 1
# 
# Qual a diferença entre os quartis (Q1, Q2 e Q3) das variáveis `normal` e `binomial` de `dataframe`? Responda como uma tupla de três elementos arredondados para três casas decimais.
# 
# Em outra palavras, sejam `q1_norm`, `q2_norm` e `q3_norm` os quantis da variável `normal` e `q1_binom`, `q2_binom` e `q3_binom` os quantis da variável `binom`, qual a diferença `(q1_norm - q1 binom, q2_norm - q2_binom, q3_norm - q3_binom)`?

# In[7]:


def q1():
    # calcula a diferença entre o valor do 1, 2 e 3 quantil da função normal e binomial
    q1 = dataframe.normal.quantile(0.25) - dataframe.binomial.quantile(0.25)
    q2 = dataframe.normal.quantile(0.5) - dataframe.binomial.quantile(0.5)
    q3 = dataframe.normal.quantile(0.75) - dataframe.binomial.quantile(0.75)
    answer = (round(q1,3), round(q2,3), round(q3,3))
    return answer


# In[8]:


q1()


# Para refletir:
# 
# * Você esperava valores dessa magnitude?
# 
# * Você é capaz de explicar como distribuições aparentemente tão diferentes (discreta e contínua, por exemplo) conseguem dar esses valores?

# ## Questão 2
# 
# Considere o intervalo $[\bar{x} - s, \bar{x} + s]$, onde $\bar{x}$ é a média amostral e $s$ é o desvio padrão. Qual a probabilidade nesse intervalo, calculada pela função de distribuição acumulada empírica (CDF empírica) da variável `normal`? Responda como uma único escalar arredondado para três casas decimais.

# In[9]:


def q2():
    # calcula da média, desvio padrão e intervalos superior e inferior
    mean = dataframe.normal.mean()
    std = dataframe.normal.std()
    upper_limit = mean + std
    bottom_limit = mean - std

    # retorna a função de distribuição cumulativa
    normal = ECDF(dataframe.normal)

    # calcula a função cumulativa nos intervalos e determina probabilidade do intervalo
    answer = float(round(normal(upper_limit) - normal(bottom_limit),3))
    return answer


# In[10]:


q2()


# Para refletir:
# 
# * Esse valor se aproxima do esperado teórico?
# * Experimente também para os intervalos $[\bar{x} - 2s, \bar{x} + 2s]$ e $[\bar{x} - 3s, \bar{x} + 3s]$.

# ## Questão 3
# 
# Qual é a diferença entre as médias e as variâncias das variáveis `binomial` e `normal`? Responda como uma tupla de dois elementos arredondados para três casas decimais.
# 
# Em outras palavras, sejam `m_binom` e `v_binom` a média e a variância da variável `binomial`, e `m_norm` e `v_norm` a média e a variância da variável `normal`. Quais as diferenças `(m_binom - m_norm, v_binom - v_norm)`?

# In[11]:


def q3():
    # calcula a diferença entre a média e variância das distribuições binomial e normal
    mean = dataframe.binomial.mean() - dataframe.normal.mean()
    variance = dataframe.binomial.var() - dataframe.normal.var()
    answer = (round(mean,3), round(variance,3))
    return answer


# In[12]:


q3()


# Para refletir:
# 
# * Você esperava valore dessa magnitude?
# * Qual o efeito de aumentar ou diminuir $n$ (atualmente 100) na distribuição da variável `binomial`?

# ## Parte 2

# ### _Setup_ da parte 2

# In[13]:


stars = pd.read_csv("pulsar_stars.csv")

stars.rename({old_name: new_name
              for (old_name, new_name)
              in zip(stars.columns,
                     ["mean_profile", "sd_profile", "kurt_profile", "skew_profile", "mean_curve", "sd_curve", "kurt_curve", "skew_curve", "target"])
             },
             axis=1, inplace=True)

stars.loc[:, "target"] = stars.target.astype(bool)


# ## Inicie sua análise da parte 2 a partir daqui

# In[14]:


# Sua análise da parte 2 começa aqui.
# verifica as primeiras linhas do dataset
stars.head()


# In[15]:


# verifica os dados estatístico do dataset
stars.describe().transpose()


# ## Questão 4
# 
# Considerando a variável `mean_profile` de `stars`:
# 
# 1. Filtre apenas os valores de `mean_profile` onde `target == 0` (ou seja, onde a estrela não é um pulsar).
# 2. Padronize a variável `mean_profile` filtrada anteriormente para ter média 0 e variância 1.
# 
# Chamaremos a variável resultante de `false_pulsar_mean_profile_standardized`.
# 
# Encontre os quantis teóricos para uma distribuição normal de média 0 e variância 1 para 0.80, 0.90 e 0.95 através da função `norm.ppf()` disponível em `scipy.stats`.
# 
# Quais as probabilidade associadas a esses quantis utilizando a CDF empírica da variável `false_pulsar_mean_profile_standardized`? Responda como uma tupla de três elementos arredondados para três casas decimais.

# In[16]:


def q4():
    # filtra somente os valores de target igual a 0
    mean_profile = stars.mean_profile.loc[stars.target == 0] 
    # normaliza os dados com média 0 e variância 1 utilizando função z-score  
    false_pulsar_mean_profile_standardized = (mean_profile - mean_profile.mean()) / mean_profile.std()

    # calcula a função de ponto percentual
    quantil_80, quantil_90,quantil_95 = sct.norm.ppf([0.8, 0.9,0.95],loc= 0, scale= 1)

    # calcula a função de distribuição normal para a série normalizada
    normal = ECDF(false_pulsar_mean_profile_standardized)

    answer = (round(normal(quantil_80),3), round(normal(quantil_90),3), round(normal(quantil_95),3))

    return answer


# In[17]:


q4()


# Para refletir:
# 
# * Os valores encontrados fazem sentido?
# * O que isso pode dizer sobre a distribuição da variável `false_pulsar_mean_profile_standardized`?

# ## Questão 5
# 
# Qual a diferença entre os quantis Q1, Q2 e Q3 de `false_pulsar_mean_profile_standardized` e os mesmos quantis teóricos de uma distribuição normal de média 0 e variância 1? Responda como uma tupla de três elementos arredondados para três casas decimais.

# In[18]:


def q5():
    # filtra somente os valores de target igual a 0
    mean_profile = stars.mean_profile.loc[stars.target == 0] 
    # normaliza os dados com média 0 e variância 1 utilizando função z-score  
    false_pulsar_mean_profile_standardized = (mean_profile - mean_profile.mean()) / mean_profile.std()

    # calcula a diferença entre o quantil da série false_pulsar... e o quantil teórico de uma distribuição normal
    q1 = false_pulsar_mean_profile_standardized.quantile(0.25) - sct.norm.ppf(0.25)
    q2 = false_pulsar_mean_profile_standardized.quantile(0.5) - sct.norm.ppf(0.5)
    q3 = false_pulsar_mean_profile_standardized.quantile(0.75) - sct.norm.ppf(0.75)

    answer = (round(q1,3), round(q2,3), round(q3,3))
    return answer


# In[19]:


q5()


# Para refletir:
# 
# * Os valores encontrados fazem sentido?
# * O que isso pode dizer sobre a distribuição da variável `false_pulsar_mean_profile_standardized`?
# * Curiosidade: alguns testes de hipóteses sobre normalidade dos dados utilizam essa mesma abordagem.
