import streamlit as st
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import pystaticplot as ps

obj = ps.dataviz()

def style():
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html = True)

def input_data():

    st.sidebar.image('images/data_input.png')
    file = st.sidebar.file_uploader('',type = 'csv')
    
    if file is not None:
        df = pd.read_csv(file)
        st.sidebar.markdown('Dados carregados com sucesso!')
        return df

def analysis_data():
    st.image('images/current_customers.png')
    return

# imageLocation = st.empty()
# imageLocation.st.image(old_image)
# if st.checkbox('New Layer'):
#     imageLocation.st.image(new_image)

if __name__ == '__main__':
    style()
    fig = obj.progress_chart(56,4, fname = 'progress.png')
    st.image('progress.png', width = 300)

    fig = obj.gauge(78, fname = 'gauge.png')
    st.image('gauge.png', width = 300)

    x = np.linspace(-np.pi, np.pi, 1000)
    y = np.sin(x)

    fig = obj.line_chart(x = [x], y = [y], fname = 'line.png')
    st.image('line.png', width = 600)

    labels = ['A', 'B', 'C', 'D']
    women = [1,3,4,5]
    men = [3,2,5,1]

    fig = obj.bar_chart(labels = labels, values = [women, men], fname = 'bar.png')
    st.image('bar.png', width = 600)

    fig = obj.horizontal_bar_chart(labels = labels, values = women, fname= 'horizontal_bar.png')
    st.image('horizontal_bar.png', width = 700)

    # TESTE

    df = input_data()

    if df is not None:
        st.dataframe(df)

