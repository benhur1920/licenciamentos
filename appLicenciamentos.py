import os
import pandas as pd
from datetime import datetime
import streamlit as st

st.set_page_config(
    layout="wide",
    page_title="Licenciamentos"
)

from streamlit_option_menu import option_menu
from utils import sobre, graficos, dataframe, dashboards
from utils.totalizadores import hoje, ultima_data,primeira_data

CAMINHO_ARQUIVO_ORIGINAL = "dados/licenciamentos.parquet"

@st.cache_data
def carregar_arquivo_parquet():
    try:
        return pd.read_parquet(CAMINHO_ARQUIVO_ORIGINAL, engine='pyarrow')
    except Exception as e:
        st.error(f"Erro ao carregar arquivo: {e}")
        return pd.DataFrame()  # retorna dataframe vazio para evitar crash

df_Original = carregar_arquivo_parquet()
df = df_Original

# Mostra a data mais recente, importar dos totalizadores.py
st.write(f"📅 Última atualização dos dados: {ultima_data.strftime('%d/%m/%Y')}")

def titulo_pagina():
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(
            "<h1>Licenciamentos do Recife</h1>"
            "<p>Fonte: Dados abertos da Prefeitura do Recife</p>",
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
                """
                <div style="margin-top: 40px;">
                    <a href="https://dados.recife.pe.gov.br/" target="_blank" class="botao-link">
                        🔗 Acessar fonte dos dados
                    </a>
                </div>
                """, unsafe_allow_html=True
        )
        # Exibe a data no formato desejado
        st.write(f"📅 Dados atualizados em: {hoje.strftime('%d/%m/%Y')}")


def filtros_aplicados(df, nome_do_filtro):
    # Opções são os nomes das colunas
    opcoes_disponiveis = sorted(df[nome_do_filtro].dropna().unique())

    # Multiselect para escolher o filtro com uma chave única
    filtro_opcao = st.multiselect(
        f'Selecione {nome_do_filtro}',
        opcoes_disponiveis,
        key=f'main_filtro_{nome_do_filtro}'
    )

    # Se o usuário selecionar colunas
    if filtro_opcao:
        return df[df[nome_do_filtro].isin(filtro_opcao)]
    else:
        # Se não selecionar nada, retorna o DataFrame original
        return df
    
def filtros_aplicados_grafico_linha(df, nome_do_filtro):
    # Opções são os nomes das colunas
    opcoes_disponiveis = sorted(df[nome_do_filtro].dropna().unique())

    # Multiselect para escolher o filtro com uma chave única para o gráfico de linha
    filtro_opcao = st.multiselect(
        f'Selecione {nome_do_filtro}',
        opcoes_disponiveis,
        key=f'linha_filtro_{nome_do_filtro}'
    )

    # Se o usuário selecionar colunas
    if filtro_opcao:
        return df[df[nome_do_filtro].isin(filtro_opcao)]
    else:
        # Se não selecionar nada, retorna o DataFrame original
        return df
    
# Funcao de filtro apenas para o mes
@st.cache_data
def filtro_mes_nome(df):
    meses_ordenados = {
        'Janeiro': 1, 'Fevereiro': 2, 'Março': 3, 'Abril': 4,
        'Maio': 5, 'Junho': 6, 'Julho': 7, 'Agosto': 8,
        'Setembro': 9, 'Outubro': 10, 'Novembro': 11, 'Dezembro': 12
    }

    opcoes_disponiveis = sorted(
        df['Mês'].dropna().unique(),
        key=lambda x: meses_ordenados.get(x, 99)
    )

    # Multiselect para o mês com uma chave única
    filtro_opcao = st.multiselect('Selecione o Mês', opcoes_disponiveis, key='main_filtro_mes')
    
    if filtro_opcao:
        return df[df['Mês'].isin(filtro_opcao)]
    return df

def criacao_navegacao_e_filtros():
    # Cópia do DataFrame original
    df_filtrado = df
    
    # Sidebar: Menu + Filtros
    with st.sidebar:
        # Menu de navegação
        selected = option_menu(
            menu_title="Conheça",
            options=["Sobre", "Dashboards", "Dataframe"],
            icons=["info-circle", "bar-chart", "table"],
            menu_icon="cast",
            default_index=0
        )

        # Título dos filtros
        st.markdown("<h1>Filtros</h1>", unsafe_allow_html=True)

        
        df_filtrado = filtros_aplicados(df_filtrado, 'Ano')
        df_filtrado = filtro_mes_nome(df_filtrado)
        df_filtrado = filtros_aplicados(df_filtrado, 'Tipo_licenciamento')
        df_filtrado = filtros_aplicados(df_filtrado, 'Situacao_processo')
        df_filtrado = filtros_aplicados(df_filtrado, 'Região')
        df_filtrado = filtros_aplicados(df_filtrado, 'Bairro')
        
    # Criar um novo DataFrame para o gráfico de linha que usará apenas alguns filtros
    df_filtrado_linha = df.copy()

    # Aplica os filtros de Situacao_processo, Região e Bairro a df_filtrado_linha
    # usando os valores selecionados nos widgets da barra lateral
    if 'main_filtro_Situacao_processo' in st.session_state and st.session_state.main_filtro_Situacao_processo:
        df_filtrado_linha = df_filtrado_linha[df_filtrado_linha['Situacao_processo'].isin(st.session_state.main_filtro_Situacao_processo)]
    if 'main_filtro_Região' in st.session_state and st.session_state.main_filtro_Região:
        df_filtrado_linha = df_filtrado_linha[df_filtrado_linha['Região'].isin(st.session_state.main_filtro_Região)]
    if 'main_filtro_Bairro' in st.session_state and st.session_state.main_filtro_Bairro:
        df_filtrado_linha = df_filtrado_linha[df_filtrado_linha['Bairro'].isin(st.session_state.main_filtro_Bairro)]


    # Calcular o total de linhas filtradas
    totalLinhas = df_filtrado.shape[0]

    # Conteúdo principal
    if selected == "Sobre":
        sobre.mainSobre(totalLinhas)
    elif selected == "Dashboards":
        # Antes de gerar o gráfico de linha, converta a coluna 'Ano' para string
        # para que o eixo x seja tratado como categórico, evitando valores como 2021.5.
        df_filtrado_linha['Ano'] = df_filtrado_linha['Ano'].astype(str)
        dashboards.mainGraficos(df_filtrado, df_filtrado_linha)
    else:
        dataframe.mainDataframe(df_filtrado)


def main():
    titulo_pagina()
    criacao_navegacao_e_filtros()
    

# Definição do programa principal será o main()
if __name__ == '__main__':
    main()
