import pandas as pd 
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler, KBinsDiscretizer
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.externals import joblib

def data_collection(filepath):

    # lê o dataset
    df = pd.read_csv(filepath)

    # monta um dataframe com todas as features e a porcentagem dos dados nulos
    null_data = pd.DataFrame(data = [list(df.columns), list(df.isnull().sum())]).transpose()
    null_data.columns = ['feature', 'null_data']

    # filtra o dataframe para colunas com no máximo 50% dos dados ausentes
    df = df.filter(items = null_data.feature.loc[null_data.null_data < 0.5 * df.shape[0]])

    # exclui as colunas que não serão usadas na análise
    df.drop(columns = ['Unnamed: 0', 'fl_matriz','natureza_juridica_macro','de_ramo','fl_spa', 'fl_antt',
    'idade_empresa_anos','vl_total_veiculos_pesados_grupo','vl_total_veiculos_leves_grupo','fl_veiculo',
    'fl_me','fl_sa','fl_epp','fl_mei','fl_ltda','dt_situacao','fl_st_especial','fl_email','fl_telefone',
    'fl_rm','nm_divisao','fl_optante_simples','sg_uf_matriz','de_saude_tributaria','de_saude_rescencia',
    'nu_meses_rescencia','fl_simples_irregular','empsetorcensitariofaixarendapopulacao','nm_meso_regiao',
    'nm_micro_regiao','fl_passivel_iss','idade_media_socios','idade_maxima_socios','idade_minima_socios',
    'qt_socios_st_regular','de_faixa_faturamento_estimado','vl_faturamento_estimado_grupo_aux',
    'vl_faturamento_estimado_aux','qt_socios','qt_socios_pj','qt_socios_pf', 'qt_filiais','fl_optante_simei'], axis = 1, inplace = True)

    return df

def data_preprocessing(df):

    # realiza o filtro para selecionar somente as features que serão utilizadas no modelo
    df = df.filter(items = ['id','de_natureza_juridica','sg_uf', 'setor', 'nm_segmento', 'idade_emp_cat','de_nivel_atividade',
    'de_faixa_faturamento_estimado_grupo'])

    # todos os setores que estão nulos serão classificados na nova categoria OUTROS
    df.setor.fillna('OUTROS', inplace = True)

    # todos os segmentos que estão nulos serão classificados na nova categoria OUTROS
    df.nm_segmento.fillna('OUTROS', inplace =  True)

    # para os dados que estiverem com dado nulo será inserido a categoria que mais se repete
    df.de_faixa_faturamento_estimado_grupo.fillna(df.de_faixa_faturamento_estimado_grupo.mode().values[0], inplace = True)

    # para os dados que estiverem com dado nulo será inserido a categoria que mais se repete, porém será realizado um group 
    # by a partir do nível de ativade da empresa
    faixa_faturamento_por_nivel = df.groupby(['de_faixa_faturamento_estimado_grupo'])['de_nivel_atividade'].agg(pd.Series.mode)
    df.de_nivel_atividade.fillna(df.de_faixa_faturamento_estimado_grupo.map(faixa_faturamento_por_nivel), inplace = True)

    df_return = df.copy()

    # transforma as variáveis categóricas em variáveis discretas
    labelencoder = LabelEncoder()
    df.de_natureza_juridica = labelencoder.fit_transform(df.de_natureza_juridica)
    df.sg_uf = labelencoder.fit_transform(df.sg_uf)
    df.setor = labelencoder.fit_transform(df.setor)
    df.nm_segmento = labelencoder.fit_transform(df.nm_segmento)
    df.idade_emp_cat = labelencoder.fit_transform(df.idade_emp_cat)
    df.de_nivel_atividade = labelencoder.fit_transform(df.de_nivel_atividade)
    df.de_faixa_faturamento_estimado_grupo = labelencoder.fit_transform(df.de_faixa_faturamento_estimado_grupo)

    # cria a classe para padronizar o dataset
    scaler = StandardScaler()

    # separa os id's
    ids = df.id

    # separa as features
    features = df.filter(items = ['de_natureza_juridica','sg_uf', 'setor', 'nm_segmento', 'idade_emp_cat','de_nivel_atividade',
    'de_faixa_faturamento_estimado_grupo'])

    # padroniza os dados
    features = scaler.fit_transform(features)

    # redução de dimensionalidade utilizando método PCA - Análise das Componentes Principais para 3 dimensões
    pca = PCA(n_components= 3)
    features = pca.fit_transform(features)

    return df_return, ids, features

def model(features):

    # gera o modelo de KMeans
    kmeans = KMeans(n_clusters= 6, init = 'k-means++')

    # treina o modelo
    kmeans.fit(features)

    # pega os valores dos centróides
    centroides = kmeans.cluster_centers_

    # pega as distancias para o centróides
    distancia = kmeans.fit_transform(features)

    # pega o agrupamento de cada id
    labels = kmeans.labels_

    # salva o modelo
    joblib.dump(kmeans, 'model.pkl')
    
    return  kmeans

def load_model(filepath):

    # carrega modelo
    model = joblib.load(filepath)

    return model

def save_data(df, kmeans):

    df['label'] = kmeans.labels_
    df.to_csv('../../market_preprocessing.csv', index = False)

def predict(kmeans, features):

    # realiza a previsão com base no modelo
    output = kmeans.predict(features)

    return output

def get_portfolio(filepath, market):

    # lê o portfolio e o banco de informações com as labels 
    portfolio = pd.read_csv(filepath)
    market_label = pd.read_csv(market)
    portfolio = portfolio.id

    # verifica quais as labels dos ids que estão no portfolio
    df = market_label[market_label['id'].isin(portfolio)]  

    return df