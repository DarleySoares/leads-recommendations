import streamlit as st
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns
import time
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
    fig = obj.progress_chart(56,4)
    st.image('images/figsize.png', width = 300)

    df = input_data()

    if df is not None:
        st.dataframe(df)

