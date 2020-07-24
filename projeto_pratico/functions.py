import pandas as pd 
import numpy as np 

def data_collection(filepath):

    # lê o dataset
    df = pd.read_csv(filepath)

    # monta um dataframe com todas as features a porcentagem dos dados nulos
    null_data = pd.DataFrame(data = [list(df.columns), list(df.isnull().sum())]).transpose()
    null_data.columns = ['feature', 'null_data']

    # filtra o dataframe para colunas com no máximo 50% dos dados ausentes
    df = df.filter(items = null_data.feature.loc[null_data.null_data < 0.5 * df.shape[0]])

    # exclui as colunas que não serão usadas na análise
    df.drop(columns = ['Unnamed: 0', 'fl_matriz','natureza_juridica_macro','de_ramo','fl_spa', 'fl_antt',
    'idade_empresa_anos','vl_total_veiculos_pesados_grupo','vl_total_leves_pesados_grupo','fl_veiculo',
    'fl_me','fl_sa','fl_epp','fl_mei','fl_ltda','dt_situacao','fl_st_especial','fl_email','fl_telefone',
    'fl_rm','nm_divisao','fl_optante_simples','sg_uf_matriz','de_saude_tributaria','de_saude_rescencia',
    'nu_meses_rescencia','fl_simples_irregular','empsetorcensitariofaixarendapopulacao','nm_meso_regiao',
    'nm_micro_regiao','fl_passivel_iss','idade_media_socios','idade_maxima_socios','idade_minima_socios',
    'qt_socios_st_regular','de_faixa_faturamento_estimado','vl_faturamento_estimado_grupo_aux',
    'vl_faturamento_estimado_aux'], axis = 1, inplace = True)

    return df

def data_preprocessing(df):

    # todos os setores que estão nulos serão classificados na nova categoria OUTROS
    df.setor.fillna('OUTROS', inplace = True)
    # todos os segmentos que estão nulos serão classificados na nova categoria OUTROS
    df.nm_segmento.fillna('OUTROS', inplace =  True)
    df.vl_total_veiculos_pesados_grupo.fillna(0, inplace = True)
    # os dados nulos dos sócios jurídicos e físicos serão completados com zero
    df.qt_socios_pf.fillna(0, inplace = True)
    df.qt_socios_pj.fillna(0, inplace = True)
    # o número total de sócios que estiver nulo será a soma do sócios físicos e jurídicos
    df.qt_socios.fillna(df.qt_socios_pf + df.qt_socios_pj, inplace = True)
    # para os dados que estiverem com dado nulo será inserido a categoria que mais se repete
    df.de_faixa_faturamento_estimado_grupo.fillna(df.de_faixa_faturamento_estimado_grupo.mode().values[0], inplace = True)
    # para os dados que estiverem com dado nulo será inserido a categoria que mais se repete, porém será realizado um group 
    # by a partir do nível de ativade da empresa
    faixa_faturamento_por_nivel = df.groupby(['de_faixa_faturamento_estimado_grupo'])['de_nivel_atividade'].agg(pd.Series.mode)
    df.de_nivel_atividade.fillna(df.de_faixa_faturamento_estimado_grupo.map(faixa_faturamento_por_nivel), inplace = True)

    # realiza o filtro para selecionar somente as features que serão utilizadas no modelo
    df = df.filter(items = ['id','de_natureza_juridica','sg_uf', 'setor', 'nm_segmento', 'idade_empresa_cat','de_nivel_atividade','qt_socios',
    'de_faixa_faturamento_estimado_grupo','qt_filiais'])

    return df





    

