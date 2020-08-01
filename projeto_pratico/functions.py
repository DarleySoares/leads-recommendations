#!/usr/bin/env python
# -*- coding: utf-8 -*-

import main
import streamlit as st
import pandas as pd 
import numpy as np 
import pystaticplot as ps
import pipeline as pp
import plotly.express as px
import math
import base64

# Função para carregar o dataset 
@st.cache(suppress_st_warning = True, show_spinner = False, )
def get_market():
    global market 
    market = pd.read_csv('../../market_preprocessing.csv')
    return market

# Gera o market
global market
market = get_market()
# Carrega o modelo
global model
model = pp.load_model('model.pkl')
# Gera classe para exibições
obj = ps.dataviz()

# Função para estilizar a página
def style():
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html = True)

# Função do menu lateral
def sidebar():
    # Seção no menu lateral para seleção das páginas 
    st.sidebar.subheader('Menu')
    paginas = st.sidebar.selectbox('Selecione a página', ['Introdução','Exemplos','Gerar leads'])

    # Retorna função de cada página
    if paginas == 'Introdução':
        introducao()
        pass

    elif paginas == 'Exemplos':
        exemplos()
        pass
    elif paginas == 'Gerar leads':
        leads()
        pass
    else:
        introducao()

    return

# Função da página de Introdução
def introducao():

    # Seção no menu lateral para informar os contatos do desenvolvedor
    st.sidebar.subheader('Contatos')
    st.sidebar.markdown('')
    st.sidebar.markdown("[![Linkedin](https://cdn4.iconfinder.com/data/icons/materia-social-free/24/038_002_linkedin_social_network_android_material-32.png)](https://www.linkedin.com/in/darley-soares)&nbsp&nbsp&nbsp&nbsp[![Github](https://cdn4.iconfinder.com/data/icons/vector-brand-logos/40/GitHub-32.png)](https://github.com/DarleySoares/Data-Science/)")
        
    # Descrição do projeto
    st.image('images/intro.png')
    
    return

# Função da página de exemplos
def exemplos():

    # Seleção do portfólio para exibição do projeto
    st.sidebar.subheader('Opções')
    portfolio = st.sidebar.selectbox('Selecione o portfólio',['','Portfólio 1','Portfólio 2','Portfólio 3'])

    # Seleção do número de leads que serão retornadas
    n_leads =  st.sidebar.slider('Número de leads', 0, 100, 20)

    # Limpa qualquer cache 
    df_pf = None

    # Seleção de qual portfólio carregar
    if portfolio == 'Portfólio 1':
        df_pf = pp.get_portfolio('data/estaticos_portfolio1.csv', '../../market_preprocessing.csv')
        pass
    elif portfolio == 'Portfólio 2':
        df_pf = pp.get_portfolio('data/estaticos_portfolio2.csv', '../../market_preprocessing.csv')
        pass
    elif portfolio == 'Portfólio 3':
        df_pf = pp.get_portfolio('data/estaticos_portfolio3.csv', '../../market_preprocessing.csv')
    else:
        # Imagem para selecionar uma opção
        st.image('images/selecionar_opcao.png')
        pass

    # Ações quando um portfólio é carregado
    if df_pf is not None:
        
        # Realiza as análises do portfólio
        st.image('images/analise_portfolio.png')
        analises(portfolio, df_pf)
        
        # Realiza a geração de leads 
        st.image('images/gerando_leads.png')
        gerar_leads(df_pf, n_leads)
        
    return

# Função da página de gerar leads
def leads():

    # Seleção do modo de operação
    st.sidebar.subheader('Modos de operação')
    modo = st.sidebar.selectbox('',['','Selecionar grupo','Carregar base de dados'])

    # Seleção escolhida foi gerar com base nas características informadas
    if modo == 'Selecionar grupo':

        # Seleção das características que podem ser informadas
        st.sidebar.subheader('Informações do grupo')

        natureza_juridica = list(market.de_natureza_juridica.unique())
        natureza_juridica = st.sidebar.multiselect('Natureza Jurídica', natureza_juridica)
            
        uf = list(market.sg_uf.unique())
        uf = st.sidebar.multiselect('Estado', uf)

        setor = list(market.setor.unique())
        setor = st.sidebar.multiselect('Setor', setor)

        segmento = list(market.nm_segmento.unique())
        segmento = st.sidebar.multiselect('Segmento', segmento)

        idade_empresa = list(market.idade_emp_cat.unique())
        idade_empresa = st.sidebar.multiselect('Idade da empresa', idade_empresa)

        nivel_atividade = list(market.de_nivel_atividade.unique())
        nivel_atividade = st.sidebar.multiselect('Nível de ativade', nivel_atividade)

        faturamento = list(market.de_faixa_faturamento_estimado_grupo.unique())
        faturamento = st.sidebar.multiselect('Faixa de faturamento', faturamento)     

        # Lista com a features selecionadas
        features = list([natureza_juridica, uf, setor, segmento, idade_empresa, nivel_atividade, faturamento])

        if natureza_juridica != [] and uf != [] and setor != [] and segmento != [] and idade_empresa != [] and faturamento != []:
            
            # Seleção do número de leads que serão retornadas
            n_leads =  st.sidebar.slider('Número de leads', 0, 100, 20)

            # Cria as features, associando randomicamente entre elas
            values = []
            for i in range(0, 100):
                for x in range(0, len(features)):
                    if len(features[x]) < 100:
                        features[x].append(np.random.choice(features[x]))
                
                values.append([i,natureza_juridica[i], uf[i], setor[i], segmento[i], idade_empresa[i], nivel_atividade[i], faturamento[i]])
            
            #  Cria um dataframe com as features
            features = pd.DataFrame(values)
            # Renomeia as colunas conforme market original
            features.columns = ['id', 'de_natureza_juridica','sg_uf', 'setor', 'nm_segmento', 'idade_emp_cat','de_nivel_atividade', 'de_faixa_faturamento_estimado_grupo']

            # Realiza a geração de leads 
            st.image('images/gerando_leads.png')
            gerar_leads(features, n_leads)
        
        else:
            # Imagem para selecionar uma opção
            st.image('images/carregar_dados.png')
            
        pass

    # Seleção escolhida foi gerar com uma base de dados
    elif modo == 'Carregar base de dados':

        # Entrada no arquivo em tipo .csv
        file = st.sidebar.file_uploader('',type = 'csv')

        # Realiza os próximos procedimentos se arquivo for validado
        if file is not None:
            # Cria dataframe com o arquivo
            df = pd.read_csv(file)

            # Tratativa se o  arquivo só tiver o id dos cliente
            if df.shape[1] <= 2:
                market_label = pd.read_csv('../../market_preprocessing.csv')
                portfolio = df.id

                # Verifica quais as labels dos ids que estão no portfolio
                df = market_label[market_label['id'].isin(portfolio)]        
        
            # Seleção do número de leads que serão retornadas
            n_leads =  st.sidebar.slider('Número de leads', 0, 100, 20)

            # Gera as análises e a geração dos leads
            if df is not None:
                # Realiza as análises do portfólio
                st.image('images/analise_portfolio.png')
                analises('fornecido', df)
                
                # Realiza a geração de leads 
                st.image('images/gerando_leads.png')
                gerar_leads(df, n_leads)
        else:
            # Imagem para selecionar uma opção
            st.image('images/carregar_dados.png')
    
    else:
        # Imagem para selecionar uma opção
        st.image('images/selecionar_opcao.png')
    return

# Função para gerar as análises do portfólio
def analises(portfolio, df_pf):

    st.markdown(f'Para o {portfolio} foram gerados os insights abaixo, sendo que nele contêm {df_pf.shape[0]} clientes, no qual é possível analisar os principais estados, setores, segmento, faixa salarial da empresa e nível de atividade. Caso não deseje ver essas informações marque o check box.')
    
    # Check box para mostrar análises ou não
    check_box = st.checkbox('Esconder insights')

    # Se check não estiver marcado mostra as análieses
    if not check_box:

        # Listas de todos os estados e valores do portfólio
        estados = list(df_pf.sg_uf.value_counts().index)
        estados_valores = list(df_pf.sg_uf.value_counts().values)

        st.markdown(f'Esse portfólio contém {len(estados)} estados, sendo que o estado {estados[0]} é o que representa a maior porção com {round(100*estados_valores[0]/df_pf.shape[0],2)}%.')
        
        # Gera gráfico de barras horizontais com os estados do portfólio
        sg_uf = obj.horizontal_bar_chart(estados, estados_valores, fname = 'output/sg_uf.png')
        st.image('output/sg_uf.png', width = 600)

        # Listas de todos os setores e valores do portfólio
        setores = list(df_pf.setor.value_counts().index)
        setores_valores = list(df_pf.setor.value_counts().values)

        # Gera gráfico de barras horizontais com os top 5 setores do portfólio  
        if len(setores) > 5:
            st.markdown(f'Já para o número de setores, o portfólio contém {len(setores)}, sendo que o setor {setores[0]} é o que possui o maior número de clientes com {setores_valores[0]}, representando {round(100*setores_valores[0]/df_pf.shape[0],2)}%. No gráfico abaixo foram representados os 5 principais.')
            setor = obj.bar_chart(setores[:5],[setores_valores[:5]], fname = 'output/setor.png')
        # Gera gráfico de barras horizontais com os estados do portfólio
        else:
            st.markdown(f'Já para o número de setores, o portfólio contém {len(setores)}, sendo que o setor {setores[0]} é o que possui o maior número de clientes com {setores_valores[0]}, representando {round(100*setores_valores[0]/df_pf.shape[0],2)}%.')
            setor = obj.bar_chart(setores,[setores_valores], fname = 'output/setor.png')
        st.image('output/setor.png', width =600)

        # Listas de todos os segmentos e valores do portfólio
        segmentos = list(df_pf.nm_segmento.value_counts().index)
        segmentos_valores = list(df_pf.nm_segmento.value_counts().values)

        # Gera gráfico de barras horizontais com os top 5 segmentos do portfólio  
        if len(segmentos) > 5:
            st.markdown(f'Para o número de segmentos, o portfólio contém {len(segmentos)}, sendo que o segmento {segmentos[0]} é o que possui o maior número de clientes, com {segmentos_valores[0]}, representando {round(100*segmentos_valores[0]/df_pf.shape[0],2)}%. No gráfico abaixo foram representados os 5 principais.')
            st.markdown(f'Legenda: {[segmentos[i] for i in range(0,4)]}')
            segmento = obj.horizontal_bar_chart(segmentos[:5],segmentos_valores[:5], fname = 'output/segmento.png')
        # Gera gráfico de barras horizontais com os segmentos do portfólio
        else:
            st.markdown(f'Para o número de segmentos, o portfólio contém {len(segmentos)}, sendo que o segmento {segmentos[0]} é o que possui o maior número de clientes, com {segmentos_valores[0]}, representando {round(100*segmentos_valores[0]/df_pf.shape[0],2)}%.')
            st.markdown(f'Legenda: {[segmentos[i] for i in range(0,len(segmentos))]}')
            segmento = obj.horizontal_bar_chart(segmentos,segmentos_valores, fname = 'output/segmento.png')
        st.image('output/segmento.png', width = 600)

        # Valor da faixa de faturamento mais exibida no portfólio
        faturamentos = list(df_pf.de_faixa_faturamento_estimado_grupo.value_counts().index)[0]
        faturamento_valor = list(df_pf.de_faixa_faturamento_estimado_grupo.value_counts().values)[0]

        st.markdown(f'Do total de {df_pf.shape[0]} clientes, {faturamento_valor} pertencem ao grupo de faixa salarial: {faturamentos}, esse valor representa:')
        # Gera gráfico de progresso com quantidade representativa no todo 
        faturamento = obj.progress_chart(round(100*faturamento_valor/df_pf.shape[0],2), 2, fname = 'output/faturamento.png')
        st.image('output/faturamento.png', width = 400)

        # Valor do nível de atividade mais exibido no portfólio
        atividade = list(df_pf.de_nivel_atividade.value_counts().index)[0]
        atividade_valor = list(df_pf.de_nivel_atividade.value_counts().values)[0]

        st.markdown(f'Do total de {df_pf.shape[0]} clientes, {atividade_valor} pertencem ao grupo de faixa salarial: {atividade}, esse valor representa:')
        # Gera gráfico de progresso com quantidade representativa no todo 
        atividades = obj.progress_chart(round(100*atividade_valor/df_pf.shape[0],2), 2, fname = 'output/atividade.png')
        st.image('output/atividade.png', width = 400)
    
    return

# Função para gerar os leads
def gerar_leads(df_pf, n_leads):
    # Carrega o modelo preditivo
    model = pp.load_model('model.pkl')

    # Realiza o pré processamento no conjunto de dados do portfólio
    df, ids, features = pp.data_preprocessing(df_pf)
    # Realiza a predição para os dados informados
    output = pp.predict(model, features)

    # No dataset retornado sem alterar os dados adiciona a colunna do cluster
    df['Cluster'] = output.astype(str)

    # Cria  um dataframe com os dados já tratados para plotar 
    output_df = pd.DataFrame(features, columns = ['f1', 'f2', 'f3'])
    # Aciona a coluna do cluster
    output_df['Cluster'] = output.astype(str)
    # Adiciona a string cluster antes do número
    output_df['Cluster'] = output_df.Cluster.map('Cluster {}'.format)   

    st.markdown('Com base nos dados apresentados no portfólio, os clientes foram agrupados em 6 possíveis clusters por similaridade, no gráfico abaixo é possível ver a quantidade por grupo.')

    # Pega os clusters e as ocorrências de cada um
    clusters = list(output_df.Cluster.value_counts().index)
    # Armazena em outra variável para usar no próximo gráfico
    labels = clusters
    clusters_valores = list(output_df.Cluster.value_counts().values)

    # Plota um gráfico com a quantidade de cada cluster 
    leads = obj.horizontal_bar_chart(clusters, clusters_valores, fname = 'output/leads.png')
    st.image('output/leads.png', width = 700)

    st.markdown('No gráfico abaixo é possível ter uma visão da densidade de cada grupo no gráfico em 3D. Nele é informado visualmente qual a proximidade entre os clusters.')
    
    # Passa as informações para o gráfico scatter 3D com os clusters, configurando a cor de cada cluster
    fig = px.scatter_3d(output_df, x = 'f3', y = 'f1', z = 'f2', 
        color = 'Cluster', color_discrete_map = {
            f'{clusters[0]}':'#F63366',
            f'{clusters[1]}':'#2AD5F5',
            f'{clusters[2]}':'#F5E55B',
            f'{clusters[3]}':'#A81D59',
            f'{clusters[4]}':'#2594A8',
            f'{clusters[5]}':'#A89914'
        })
    
    # Configura os eixos para a cor branca
    fig.update_xaxes(showline = True, linecolor = '#FFFFFF')
    fig.update_yaxes(showline = True, linecolor = '#FFFFFF')
    
    # Configura para legenda ficar no lado esquerdo
    fig.update_layout(legend = dict(
        yanchor = 'top',
        y=0.8,
        xanchor="left",
        x=-0.05,
        font=dict(
        color="white"
        )
    ))

    # Configura a cor do fundo para transparente
    fig.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)'
    })

    # Plota o gráfico
    st.plotly_chart(fig)
    
    # Retira os dados do portfólio
    df_lead = market[~market.isin(df)].dropna()

    # Pega os clusters e as ocorrências de cada um
    clusters = df.Cluster.value_counts().index.to_list()
    values = (df.Cluster.value_counts().values/df.shape[0]).round(1)

    # Verifica a porcentagem de cada cluster  e gera amostras randômicas de cada cluster
    ids = []
    for cluster, value in zip(clusters, values):
        df_filter = df_lead.loc[df_lead.label == int(cluster)]
        random_id = np.random.choice(df_filter.id, math.ceil(value*n_leads))
        ids.extend(random_id)
    
    # Pega somente as informações dos leads que foram gerados
    df_lead = market[market['id'].isin(ids[:n_leads])]

    # Realiza o pré processamento dos dados para gerar informações para plotar
    df, ids, features = pp.data_preprocessing(df_lead)
    # Pega a lista dos clusters
    cluster = list(df_lead.label.astype(str))
    
    # Cria  um dataframe com os dados já tratados para plotar 
    output_df = pd.DataFrame(features, columns = ['f1', 'f2', 'f3'])
    # Aciona a coluna do cluster
    output_df['Cluster'] = cluster
    # Adiciona a string cluster antes do número
    output_df['Cluster'] = output_df.Cluster.map('Cluster {}'.format)

    st.markdown('No gráfico abaixo é mostrado as recomendações que foram geradas com base no portfólio passado. Esses dados estão disponíveis para download na barra lateral e caso queira ver os clientes clique no checkbox!')

    # Passa as informações para o gráfico scatter 3D com os clusters, configurando a cor de cada cluster
    fig = px.scatter_3d(output_df, x = 'f3', y = 'f1', z = 'f2', 
        color = 'Cluster', color_discrete_map = {
            f'{labels[0]}':'#F63366',
            f'{labels[1]}':'#2AD5F5',
            f'{labels[2]}':'#F5E55B',
            f'{labels[3]}':'#A81D59',
            f'{labels[4]}':'#2594A8',
            f'{labels[5]}':'#A89914'
        })
    
    # Configura os eixos para a cor branca
    fig.update_xaxes(showline = True, linecolor = '#FFFFFF')
    fig.update_yaxes(showline = True, linecolor = '#FFFFFF')

    # Configura para legenda ficar no lado esquerdo
    fig.update_layout(legend = dict(
        yanchor = 'top',
        y=0.8,
        xanchor="left",
        x=-0.05,
        font=dict(
        color="white"
        )
    ))

    # Configura a cor do fundo para transparente
    fig.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)'
    })

    # Plota o gráfico
    st.plotly_chart(fig)

    check_box = st.checkbox('Mostrar leads')
        
    if check_box:
        st.dataframe(df_lead)
    
    st.sidebar.subheader('Download leads')
    # Gera o link para download dos leads
    st.sidebar.markdown(get_table_download_link(df_lead), unsafe_allow_html=True)

    return

# Função para converter dataframe para csv e gerar download
def get_table_download_link(df):

    # Converte o dataframe dos leads para um arquivo csv
    csv = df.to_csv(index=False)
    
    b64 = base64.b64encode(
        csv.encode()
    ).decode() 
    return f'<a href="data:file/csv;base64,{b64}" download="leads.csv"> ![](https://raw.githubusercontent.com/DarleySoares/codenation_data_science/master/projeto_pratico/images/download.png?token=AMWWAS4QTWDSUYR4SEA6YTS7FN52I) </a>'