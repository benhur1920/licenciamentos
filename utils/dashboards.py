import matplotlib as pl
import plotly.express as px
import streamlit as st
from utils.totalizadores import calculo_total_licenciamentos, calculo_valor_taxas, calculo_total_potencial, calculo_total_licenca, calculo_tempo_medio
from utils.graficos import grafico_zona, grafico_bairro,  grafico_situacao, grafico_total_licenciamentos,grafico_total_licenciamentos_linha, grafico_assunto, grafico_mercantil, grafico_tipo_mercantil, grafico_mapa
from utils.marcadores import divisor
from appLicenciamentos import filtros_aplicados
from utils.dataframe import mainDataframe

def graficos(df_filtrado, df_filtrado_linha):

    

    fig = grafico_zona(df_filtrado)
    fig1 = grafico_bairro(df_filtrado)
    fig5 = grafico_situacao(df_filtrado)
    fig6 = grafico_total_licenciamentos(df_filtrado)
    fig7 = grafico_total_licenciamentos_linha(df_filtrado_linha)
    fig8 = grafico_assunto(df_filtrado)
    fig9 = grafico_mercantil(df_filtrado)
    
    fig3 = grafico_mapa(df_filtrado)
    
    # Calculo dos totalizadores importando o resultado das funcoes do arquivo totalizadores.py
    totalLicenciamentos = calculo_total_licenciamentos(df_filtrado)
    total_taxas = calculo_valor_taxas(df_filtrado)
    total_urbanistico = calculo_total_licenca(df_filtrado, 'Urbanístico')
    total_sanitario = calculo_total_licenca(df_filtrado, 'Sanitário')
    total_ambiental= calculo_total_licenca(df_filtrado, 'Ambiental')
    tempoMedio = calculo_tempo_medio(df_filtrado)
    
    
    aba1, aba2, aba3, aba4, aba5 = st.tabs(['🏫 Geral', '📈 Analises', '📈 Projetos em destaque', '🗺️ Mapas', '🔍Consulte'])

    with aba1:
        col1, col2, col3  = st.columns([2, 2, 2], vertical_alignment='center', gap='small')

        with col1:
            st.metric("🏫 Total licenciamentos", value=(totalLicenciamentos),  border=True)
            
        with col2:
            st.metric("💰 Valor total das taxas", value=(total_taxas), border=True)
            
        with col3:
            st.metric("⏱️ Tempo medio de conclusão", value=(tempoMedio), border=True)

        divisor()
        st.plotly_chart(fig5, use_container_width=True, config={
                "displaylogo": False,  # remove logo do Plotly
                "modeBarButtonsToRemove": ["toImage"],  # opcional
            })

        divisor()
        st.plotly_chart(fig6, use_container_width=True, config={
                "displaylogo": False,  # remove logo do Plotly
                "modeBarButtonsToRemove": ["toImage"],  # opcional
            })

        divisor()
        st.plotly_chart(fig7, use_container_width=True, config={
                "displaylogo": False,  # remove logo do Plotly
                "modeBarButtonsToRemove": ["toImage"],  # opcional
            })

    with aba2:

        col1, col2, col3  = st.columns([2, 2, 2], vertical_alignment='center', gap='small')

        with col1:
            st.metric("🏠 Urbanístico", value=(total_urbanistico),  border=True)
            
        with col2:
            st.metric("🩺 Sanitário", value=(total_sanitario), border=True)

        with col3:
            st.metric("🌳 Ambiental", value=(total_ambiental), border=True)

        divisor()        
        st.plotly_chart(fig, use_container_width=True, config={
                "displaylogo": False,  # remove logo do Plotly
                "modeBarButtonsToRemove": ["toImage"],  # opcional
            })
        divisor()
        st.plotly_chart(fig1, use_container_width=True, config={
                "displaylogo": False,  # remove logo do Plotly
                "modeBarButtonsToRemove": ["toImage"],  # opcional
            })
        divisor()
        st.plotly_chart(fig8, use_container_width=True, config={
                "displaylogo": False,  # remove logo do Plotly
                "modeBarButtonsToRemove": ["toImage"],  # opcional
            })
        

    with aba3:
        st.plotly_chart(fig9, use_container_width=True, config={
            "displaylogo": False,  # remove logo do Plotly
            "modeBarButtonsToRemove": ["toImage"],  # opcional
        })
        divisor()
        
        df_especial = df_filtrado[df_filtrado['Potencial_empreendimento'] != "Não Informado"]

        

        if not df_especial.empty:
            
            df_especial_filtrado = filtros_aplicados(df_especial, 'Potencial_empreendimento')
            total_alto = calculo_total_potencial(df_especial_filtrado, "Alto")
            total_medio = calculo_total_potencial(df_especial_filtrado, "Médio")
            total_baixo = calculo_total_potencial(df_especial_filtrado, "Baixo")
            if not df_especial_filtrado.empty:
                fig10 = grafico_tipo_mercantil(df_especial_filtrado)
                if fig10:
                    st.plotly_chart(fig10, use_container_width=True)
                else:
                    st.warning("O gráfico 'Tipo Mercantil' não pôde ser gerado.")
                
                divisor()
                st.text('Relatório dos projetos com potencial de empreendimento informado')
                col1, col2, col3  = st.columns([2, 2, 2], vertical_alignment='center', gap='small')

                with col1:
                    st.metric("🟢 Alto", value=(total_alto),  border=True)
                    
                with col2:
                    st.metric("🟠  Médio", value=(total_medio), border=True)

                with col3:
                    st.metric("🔴 Baixo", value=(total_baixo), border=True)


                st.dataframe(df_especial_filtrado, use_container_width=True)
                divisor()
                fig4 = grafico_mapa(df_especial_filtrado)
                st.plotly_chart(fig4, use_container_width=True)
            else:
                st.warning("Nenhum dado encontrado após filtragem especial.")
        else:
            st.warning("Nenhum dado especial encontrado para 'Potencial_empreendimento'.")
      
        
    with aba4:
        
        fig3.update_layout(mapbox_style="open-street-map")
        fig3.update_layout(margin={"r":0, "t":80, "l":0, "b":0})
        st.plotly_chart(fig3, use_container_width=True)
    
   
    
    
    with aba5:
        # Inicializa os estados da sessão
        if 'numero_processo' not in st.session_state:
            st.session_state.numero_processo = ''
        if 'consultou' not in st.session_state:
            st.session_state.consultou = False

        # Função de callback para o botão "Nova consulta"
        def reset_state():
            # Limpa o número e reseta o estado de consulta.
            # É aqui que o campo de texto é realmente limpo.
            st.session_state.numero_processo = ''
            st.session_state.consultou = False

        # A lógica para exibir os resultados e o botão de Nova Consulta.
        if st.session_state.consultou:
            # Exibe o botão de Nova Consulta
            st.button("Nova consulta", on_click=reset_state)

            # Lógica para exibir os resultados (igual à sua)
            num = st.session_state.numero_processo
            
            if num.isdigit():
                num = int(num)
                df_numero_processo = df_filtrado[df_filtrado['Num_processo'] == num]

                if not df_numero_processo.empty:
                    mainDataframe(df_numero_processo)
                    fig_mapa_processo = grafico_mapa(df_numero_processo)
                    st.plotly_chart(fig_mapa_processo, use_container_width=True)
                else:
                    st.warning("Nenhum processo encontrado com esse número.")
            else:
                st.error("Digite apenas números para o processo.")

        # Se a consulta ainda não foi feita ou foi resetada, exibe o formulário.
        else:
            with st.form(key='form_consulta'):
                # O valor inicial do campo de texto é o que está em st.session_state.numero_processo
                # Isso garante que ele não seja limpo após o primeiro submit
                numero_processo_input = st.text_input("Informe o número do processo", value=st.session_state.numero_processo)
                submit = st.form_submit_button("Consultar")

                if submit:
                    # Ao clicar em Consultar, salva o valor digitado e atualiza o estado
                    st.session_state.numero_processo = numero_processo_input.strip()
                    st.session_state.consultou = True
                    # st.rerun() é chamado para atualizar a tela e exibir os resultados
                    st.rerun()

def mainGraficos(df_filtrado, df_filtrado_linha):
    divisor()
    graficos(df_filtrado, df_filtrado_linha) # Passe o df_filtrado e o df_filtrado_linha para a função graficos
    divisor()