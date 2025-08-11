import streamlit as st
import os
from utils.totalizadores import *
from utils.marcadores import divisor

def sobre(df):
    
    
    # Imagens
    imagem_path1 = os.path.join(os.path.dirname(__file__), '..', 'images', 'Recife.jpg')
    

    st.markdown("<h2 style='text-align: center; '>Panorama dos pedidos de licenciamentos no Recife</h2>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Primeira seção com imagem e texto
    col1, col2 = st.columns([2, 3], gap="small")

    with col1:
        st.image(imagem_path1, use_container_width=True, clamp=True, caption="Rua da Aurora, Recife")

    with col2:
        
        st.markdown(
            """
            <div style="text-align: justify; font-size: 17px">
                <p>
                    Este painel utiliza dados abertos da Prefeitura do Recife referentes aos licenciamentos urbanos emitidos no município. As informações são oriundas de três categorias distintas de licenciamento:
                </p>
                <ul>
                    <li><strong>Licenciamento Urbanístico</strong></li>
                    <li><strong>Licenciamento Sanitário</strong></li>
                    <li><strong>Licenciamento Ambiental</strong></li>
                </ul>
                <p>
                    Os três conjuntos de dados foram concatenados em um único banco, possibilitando a análise integrada dos diferentes tipos de licenças emitidas. Cada registro contém informações como data de entrada, data de conclusão, bairro, situação do processo, tipo de licenciamento, valor pago, entre outros.
                </p>
                <p>
                    O objetivo é facilitar a transparência e a compreensão do andamento dos processos de licenciamento na cidade.
                </p>
            </div>
            """,
        unsafe_allow_html=True
    )

  

def mainSobre(df):
    divisor()
    sobre(df)
    divisor()
