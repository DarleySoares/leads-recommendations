#!/usr/bin/env python
# coding: utf-8

# # Desafio 1
# 
# Para esse desafio, vamos trabalhar com o data set [Black Friday](https://www.kaggle.com/mehdidag/black-friday), que reúne dados sobre transações de compras em uma loja de varejo.
# 
# Vamos utilizá-lo para praticar a exploração de data sets utilizando pandas. Você pode fazer toda análise neste mesmo notebook, mas as resposta devem estar nos locais indicados.
# 
# > Obs.: Por favor, não modifique o nome das funções de resposta.

# ## _Set up_ da análise

# In[2]:


import pandas as pd
import numpy as np


# In[3]:


black_friday = pd.read_csv("black_friday.csv")


# ## Inicie sua análise a partir daqui

# In[3]:


black_friday.head()


# ## Questão 1
# 
# Quantas observações e quantas colunas há no dataset? Responda no formato de uma tuple `(n_observacoes, n_colunas)`.

# In[13]:


def q1():
    # Retorne aqui o resultado da questão 1.
    return black_friday.shape


# ## Questão 2
# 
# Há quantas mulheres com idade entre 26 e 35 anos no dataset? Responda como um único escalar.

# In[11]:


def q2():
    # Retorne aqui o resultado da questão 2.
    return int(black_friday.User_ID.loc[black_friday.Gender == 'F'][black_friday.Age == '26-35'].count())


# ## Questão 3
# 
# Quantos usuários únicos há no dataset? Responda como um único escalar.

# In[91]:


def q3():
    # Retorne aqui o resultado da questão 3.
    return black_friday.User_ID.nunique()


# ## Questão 4
# 
# Quantos tipos de dados diferentes existem no dataset? Responda como um único escalar.

# In[51]:


def q4():
    # Retorne aqui o resultado da questão 4.
    lista = pd.Series(black_friday.dtypes.values)
    return lista.nunique()


# ## Questão 5
# 
# Qual porcentagem dos registros possui ao menos um valor null (`None`, `ǸaN` etc)? Responda como um único escalar entre 0 e 1.

# In[21]:


def q5():
    # Retorne aqui o resultado da questão 5.
    tamanho_do_conjunto = black_friday.shape[0]
    amostra_null = (black_friday.Product_Category_2.isnull() | black_friday.Product_Category_3.isnull()).sum()
    return float(amostra_null/tamanho_do_conjunto)
q5()


# ## Questão 6
# 
# Quantos valores null existem na variável (coluna) com o maior número de null? Responda como um único escalar.

# In[56]:


def q6():
    # Retorne aqui o resultado da questão 6.
    return max(black_friday.isnull().sum())


# ## Questão 7
# 
# Qual o valor mais frequente (sem contar nulls) em `Product_Category_3`? Responda como um único escalar.

# In[81]:


def q7():
    # Retorne aqui o resultado da questão 7.
    lista = pd.Series(black_friday.Product_Category_3.value_counts().sort_values(ascending = False)).index
    return lista[0]


# ## Questão 8
# 
# Qual a nova média da variável (coluna) `Purchase` após sua normalização? Responda como um único escalar.

# In[84]:


def q8():
    # Retorne aqui o resultado da questão 8.
    purchase = black_friday.Purchase
    purchase = (purchase - min(purchase))/(max(purchase) - min(purchase))
    return float(purchase.mean())


# ## Questão 9
# 
# Quantas ocorrências entre -1 e 1 inclusive existem da variáel `Purchase` após sua padronização? Responda como um único escalar.

# In[14]:


def q9():
    # Retorne aqui o resultado da questão 9.
    purchase = black_friday.Purchase
    purchase = (purchase - purchase.mean())/purchase.std()
    return int(purchase.between(-1,1).sum())
q9()


# ## Questão 10
# 
# Podemos afirmar que se uma observação é null em `Product_Category_2` ela também o é em `Product_Category_3`? Responda com um bool (`True`, `False`).

# In[129]:


def q10():
    # Retorne aqui o resultado da questão 10.
    null_cat_2 = black_friday.loc[pd.isnull(black_friday.Product_Category_2)]
    null_cat_3 = null_cat_2.loc[pd.isnull(null_cat_2.Product_Category_3)]
    if (null_cat_2.shape[0] == null_cat_3.shape[0]):
        return True
    else:
        return False
    pass

