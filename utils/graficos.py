import matplotlib as pl
import plotly.express as px
import streamlit as st
from utils.marcadores import texto, sidebar

# Gráfico por região
def grafico_zona(df):
    if df.empty or 'Região' not in df.columns or 'Bairro' not in df.columns:
        st.warning("Não há dados disponíveis para gerar o gráfico de região.")
        return None

    df_agrupado = df.groupby('Região')[['Bairro']].count().reset_index()
    fig = px.treemap(df_agrupado, path=['Região'], values='Bairro', color='Bairro')

    fig.update_layout(
        title={
            'text': 'Tipos de Licenciamentos por Região',
            'font': {'size': 26, 'color': texto}
        },
        font=dict(color=texto)
    )
    return fig

# Gráfico por bairro
def grafico_bairro(df):
    if df.empty or 'Região' not in df.columns or 'Bairro' not in df.columns:
        st.warning("Não há dados disponíveis para gerar o gráfico de região.")
        return None

    df_bairro = df.groupby('Bairro').size().reset_index(name='TOTAL').sort_values('TOTAL', ascending=False)
    fig1 = px.bar(df_bairro, x='Bairro', y='TOTAL')

    fig1.update_layout(
        title={'text': 'Tipo de licenciamentos por bairro',   'font': {'size': 26, 'color': texto}},
        xaxis_title='Bairro',
        yaxis_title='Total',
        xaxis_title_font=dict(size=18, color=texto),
        yaxis_title_font=dict(size=18, color=texto),
        xaxis_tickfont=dict(size=14, color=texto),
        yaxis_tickfont=dict(size=14, color=texto),
    )
    return fig1


# Gráfico por situacao do processo
def grafico_situacao(df):
    if df.empty or 'Região' not in df.columns or 'Bairro' not in df.columns:
        st.warning("Não há dados disponíveis para gerar o gráfico de região.")
        return None

    df_situacao = df.groupby('Situacao_processo').size().reset_index(name='TOTAL').sort_values('TOTAL', ascending=False)
    fig5 = px.bar(df_situacao, x='Situacao_processo', y='TOTAL', labels={'Situacao_processo': 'Situação dos processos'})

    fig5.update_layout(
        font=dict(color=texto),
        xaxis=dict(showgrid=False, zeroline=False, tickfont=dict(color=texto), title_font=dict(color=texto, size=16)),
        yaxis=dict(showgrid=False, zeroline=False, tickfont=dict(color=texto), title_font=dict(color=texto, size=16))
    )
    fig5.update_layout(
        title={'text': 'Total de licenciamentos por assunto',   'font': {'size': 26, 'color': texto}}
    ),
    
    return fig5

# Gráfico total de licenciamentos
def grafico_total_licenciamentos(df):
    if df.empty or 'Região' not in df.columns or 'Bairro' not in df.columns:
        st.warning("Não há dados disponíveis para gerar o gráfico de região.")
        return None

    # Agrupar por Tipo_licenciamento
    df_situacao = (
        df.groupby('Tipo_licenciamento')
        .size()
        .reset_index(name='TOTAL')
        .sort_values('TOTAL', ascending=False)
    )

    # Gráfico de rosca
    fig6 = px.pie(
        df_situacao,
        values='TOTAL',
        names='Tipo_licenciamento',
        hole=0.5,
        color_discrete_sequence=px.colors.qualitative.Set3
    )

    fig6.update_layout(
    title={'text': 'Total de Licenciamentos por Tipo', 'font': {'size': 26, 'color': texto}},
    font=dict(color=texto),
    legend_title=dict(text='Tipo de Licenciamento', font=dict(size=20, color=texto)),
    legend=dict(font=dict(color=texto)),
)
    return fig6

def grafico_total_licenciamentos_linha(df):
    if df.empty or 'Tipo_licenciamento' not in df.columns or 'Ano' not in df.columns:
        st.warning("Não há dados disponíveis para gerar o gráfico por tipo e ano.")
        return None

    # Agrupa os dados por Tipo_licenciamento e Ano
    df_agrupado = (
        df.groupby(['Ano', 'Tipo_licenciamento'])
        .size()
        .reset_index(name='TOTAL')
        .sort_values(['Ano', 'Tipo_licenciamento'])
    )

    # Gráfico de linha
    fig7 = px.line(
        df_agrupado,
        x='Ano',
        y='TOTAL',
        color='Tipo_licenciamento',
        markers=True,
        labels={'TOTAL': 'Total de Licenciamentos', 'Ano': 'Ano'},
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    fig7.update_layout(
        title={'text':'Evolução dos Licenciamentos por Tipo', 'font': {'size': 26, 'color': texto}},
        font=dict(color=texto),
        xaxis=dict(
            title='Ano',
            tickfont=dict(color=texto),
            title_font=dict(color=texto, size=16)
        ),
        yaxis=dict(
            title='Total de Licenciamentos',
            tickfont=dict(color=texto),
            title_font=dict(color=texto, size=20)
        ),
        legend_title=dict(text='Tipo de Licenciamento', font=dict(size=20, color=texto)),
        legend=dict(font=dict(color=texto)),
    )

    return fig7

# Gráfico por assunto
def grafico_assunto(df):
    if df.empty or 'Região' not in df.columns or 'Bairro' not in df.columns:
        st.warning("Não há dados disponíveis para gerar o gráfico de região.")
        return None

    df_situacao = df.groupby('Assunto').size().reset_index(name='TOTAL').sort_values('TOTAL', ascending=False)
    fig8 = px.bar(df_situacao, x='Assunto', y='TOTAL')

    fig8.update_layout(
        title={'text':'Evolução dos Licenciamentos por Assunto', 'font': {'size': 26, 'color': texto}},
        font=dict(color=texto),
        xaxis=dict(showgrid=False, zeroline=False, tickfont=dict(color=texto), title_font=dict(color=texto, size=16)),
        yaxis=dict(showgrid=False, zeroline=False, tickfont=dict(color=texto), title_font=dict(color=texto, size=16))
    )
    return fig8

# Gráfico por tipo mercantil
def grafico_mercantil(df):
    if df.empty or 'Região' not in df.columns or 'Bairro' not in df.columns:
        st.warning("Não há dados disponíveis para gerar o gráfico de região.")
        return None

    df_situacao = df.groupby('Tipo_mercantil').size().reset_index(name='TOTAL').sort_values('TOTAL', ascending=False)
    fig9 = px.bar(df_situacao, x='Tipo_mercantil', y='TOTAL',  labels={'Tipo_mercantil': 'Tipo Mercantil'})

    fig9.update_layout(
        title={'text':'Total de licenciamentos por tipo mercantil', 'font': {'size': 26, 'color': texto}},
        font=dict(color=texto),
        xaxis=dict(showgrid=False, zeroline=False, tickfont=dict(color=texto), title_font=dict(color=texto, size=16)),
        yaxis=dict(showgrid=False, zeroline=False, tickfont=dict(color=texto), title_font=dict(color=texto, size=16))
    )
    return fig9

# Gráfico tipo mercantil
def grafico_tipo_mercantil(df):
    if df.empty or 'Região' not in df.columns or 'Bairro' not in df.columns:
        st.warning("Não há dados disponíveis para gerar o gráfico de região.")
        return None


    # Remover linhas onde Tipo_mercantil é "Não informado"
    df = df[df['Potencial_empreendimento'] != "Não Informado"]

    # Agrupar por Tipo_licenciamento
    df_mercantil = (
        df.groupby('Potencial_empreendimento')
        .size()
        .reset_index(name='TOTAL')
        .sort_values('TOTAL', ascending=False)
    )

    # Gráfico de rosca
    fig10 = px.pie(
        df_mercantil,
        values='TOTAL',
        names='Potencial_empreendimento',
        hole=0.5,
        color_discrete_sequence=px.colors.qualitative.Set3
    )

    fig10.update_layout(
    title={'text': 'Total de licenciamentos por potencial do empreendimento', 'font': {'size': 26, 'color': texto}},
    font=dict(color=texto),
    legend_title=dict(text='Tipo de Licenciamento por Potencial do Empreendimento', font=dict(size=20, color=texto)),
    legend=dict(font=dict(color=texto)),
)


    return fig10


# Gráfico com mapa
def grafico_mapa(df):
    if df.empty or 'Região' not in df.columns or 'Bairro' not in df.columns:
        st.warning("Não há dados disponíveis para gerar o gráfico de região.")
        return None

    fig3 = px.scatter_mapbox(
        df.dropna(subset=['Latitude', 'Longitude']),
        hover_name='Tipo_licenciamento',
        hover_data={'Tipo_licenciamento': True, 'Região': True, 'Bairro': True, 'Endereco_empreendimento': True, 'Razao_social': True},
        lat='Latitude',
        lon='Longitude',
        color='Tipo_licenciamento',
        zoom=11,
        height=700
    )
    fig3.update_traces(marker=dict(size=15))
    fig3.update_layout(
        mapbox_style="open-street-map",
        mapbox_center={"lat": -8.0476, "lon": -34.8770},
        legend=dict(
            title_text='Licenciamentos',
            title_font=dict(size=18, color=texto),
            font=dict(size=12, color=texto),
            orientation='h',
            x=0.5,
            y=1.05,
            xanchor='right',
            yanchor='bottom',
            borderwidth=1
        ),
        margin=dict(t=150, b=20, l=10, r=10)
    )
    return fig3
"""

# Gráfico por sala de recursos
def grafico_sala(df):
    if df.empty or 'Região' not in df.columns or 'Bairro' not in df.columns:
        st.warning("Não há dados disponíveis para gerar o gráfico de região.")
        return None

    df_sala = df.groupby('Sala_recurso').size().reset_index(name='TOTAL').sort_values('TOTAL', ascending=False)
    fig6 = px.bar(df_sala, x='Sala_recurso', y='TOTAL', labels={'Sala_recurso': 'Escolas com Sala de recursos'})

    fig6.update_layout(
        font=dict(color=texto),
        xaxis=dict(showgrid=False, zeroline=False, tickfont=dict(color=texto), title_font=dict(color=texto, size=16)),
        yaxis=dict(showgrid=False, zeroline=False, tickfont=dict(color=texto), title_font=dict(color=texto, size=16))
    )
    return fig6

# Gráfico por bibliotecas
def grafico_bibliotecas(df):
    if df.empty or 'Região' not in df.columns or 'Bairro' not in df.columns:
        st.warning("Não há dados disponíveis para gerar o gráfico de região.")
        return None

    df_bibliotecas = df.groupby('Biblioteca').size().reset_index(name='TOTAL').sort_values('TOTAL', ascending=False)
    fig7 = px.bar(df_bibliotecas, x='Biblioteca', y='TOTAL', labels={'Biblioteca': 'Escolas com bibliotecas'})

    fig7.update_layout(
        font=dict(color=texto),
        xaxis=dict(showgrid=False, zeroline=False, tickfont=dict(color=texto), title_font=dict(color=texto, size=16)),
        yaxis=dict(showgrid=False, zeroline=False, tickfont=dict(color=texto), title_font=dict(color=texto, size=16))
    )
    return fig7
"""