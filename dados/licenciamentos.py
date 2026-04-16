import pandas as pd
import unidecode
import locale

def entrada_de_dados(url):
    dados = pd.read_csv(url, sep=';', encoding='latin1')
    
    dados = dados.applymap(
        lambda x: x.encode('latin1').decode('utf-8') if isinstance(x, str) else x
    )
    
    return dados


# Criando a coluna de tito de licencimanto para podermos dar o comando concat e juntar os 03 dfs
def criando_coluna_tipo_de_liceniamento(dados, dados_da_coluna):
    dados['tipo_licenciamento'] = dados_da_coluna
    return dados


def concatenando_os_treis_datasets(Urbanismo, Sanitario, Ambiental):
    df = pd.concat([Urbanismo, Sanitario, Ambiental], ignore_index=True)
    return df


# Transformar as colunas de objeto para datetime
def Transforma_as_colunas_de_ojeto_para_datatime(df):
    df['data_conclusao'] = pd.to_datetime(df['data_conclusao'], errors='coerce')
    df['data_emissao_licenca'] = pd.to_datetime(
    df['data_emissao_licenca'], errors='coerce')
    df['data_entrada'] = pd.to_datetime(df['data_entrada'], errors='coerce')
    df['data_pagamento'] = pd.to_datetime(df['data_pagamento'], errors='coerce')
    df['data_validade_licenca'] = pd.to_datetime(
    df['data_validade_licenca'], errors='coerce')
    return df


def transformar_na_coluna_data_conclusao_valores_em_branco_para_Nan(df):
    df['data_conclusao'] = df['data_conclusao'].replace('', pd.NaT)
    return df

def criar_uma_coluna_tempo_conclusao_para_mostrar_resolucao_do_pedido_de_licencimento(df):
    # Cria a coluna vazia
    df['Tempo_conclusao'] = pd.NA

    # Calcula diferença apenas onde existe data_conclusao
    mask = df['data_conclusao'].notna()
    df.loc[mask, 'Tempo_conclusao'] = (
        (df.loc[mask, 'data_conclusao'] - df.loc[mask, 'data_entrada']).dt.days
    )

    # Garante que permanece numérica
    df['Tempo_conclusao'] = pd.to_numeric(df['Tempo_conclusao'], errors='coerce')

    return df



# corrindo o nome dos bairros
def corrigindo_os_nomes_dos_bairros(df):
    df['bairro'] = df['bairro'].replace({'ALTO DO MANDU   SITIO GRANDE': 'ALTO DO MANDU',
                                    'COHAB   IBURA DE CIMA': 'COHAB',
                                     'SITIO DOS PINTOS   SAO BRAS': 'SITIO DOS PINTOS'})
    return df


# Convertendo para string (se necessário)
def convertendo_para_string_coordenadas(df):
    df['latitude'] = df['latitude'].astype(str)
    df['longitude'] = df['longitude'].astype(str)
    return df

# Substituindo o ponto por vírgula
def substituindo_o_ponto_por_virgula(df):
    # Apenas latitude
    if 'latitude' in df.columns:
        df['latitude'] = (
            df['latitude']
            .fillna('')
            .astype(str)
            .str.replace('.', ',', regex=False)
        )

    # Apenas longitude
    if 'longitude' in df.columns:
        df['longitude'] = (
            df['longitude']
            .fillna('')
            .astype(str)
            .str.replace('.', ',', regex=False)
        )

    return df


# Usar title para deixar primeira letra como maiuscula
def usar_funcao_title_nas_colunas_string(df):
    df = df.apply(lambda x: x.str.title() if x.dtype == "object" else x)
    return df

def colocar_valores_NAN_nas_colunas(df):
    # Definir as colunas que não devem ser modificadas
    colunas_excluidas = ['data_conclusao', 'data_emissao_licenca', 'data_entrada',
                         'data_pagamento', 'data_validade_licenca', 'valor_taxa', 'valor_pago']

    # Selecionar as colunas que podem ser modificadas
    colunas_modificaveis = df.columns[~df.columns.isin(colunas_excluidas)]

    for coluna in colunas_modificaveis:
        if df[coluna].dtype == 'object':
            # Substituir NaN e strings vazias por 'Não Informado' em colunas de texto
            df[coluna] = df[coluna].fillna(
                'Não Informado').replace('', 'Não Informado')
        else:
            # Apenas preencher valores NaN para colunas numéricas
            df[coluna] = df[coluna].fillna(0)

    return df

def renomear_coluna_area(df):
    df = df.rename(columns={"ÿareatotalconstruida": "areatotalconstruida"})
    return df

def transformar_colunas_coordenadas_para_float(df, nome):
    df[nome] = df[nome].str.replace(',', '.', regex=False)
    df[nome] = pd.to_numeric(df[nome], errors='coerce')
    return df

def aplicar_capitalize_nas_colunas(df):
    df.columns = [col.capitalize() for col in df.columns]
    return df

def criar_a_coluna_Regiao(df):
    dicionario = {
        'Centro': [
            'Boa Vista', 'Cabanga', 'Coelhos', 'Ilha Do Leite', 'Ilha Joana Bezerra',
            'Paissandu', 'Recife', 'Santo Amaro', 'Santo Antônio', 'Santo Antonio','Soledade', 'São José', 'Sao Jose'
        ],
        'Noroeste': [
            'Aflitos', 'Alto Do Mandu', 'Alto José Bonifácio', 'Alto Jose Bonifacio','Alto José Do Pinho','Alto Jose Do Pinho',  'Apipucos', 'Brejo Da Guabiraba', 'Brejo De Beberibe', 'Casa Amarela', 'Casa Forte',
            'Córrego Do Jenipapo', 'Corrego Do Jenipapo', 'Derby', 'Dois Irmãos','Dois Irmaos' , 'Espinheiro', 'Graças', 'Gracas', 'Guabiraba', 'Jaqueira', 'Macaxeira', 'Mangabeira', 'Monteiro', 'Morro Da Conceição','Morro Da Conceicao',
            'Nova Descoberta', 'Parnamirim', 'Passarinho', 'Pau Ferro', 'Poço', 'Poco', 'Santana',
            'Sítio Dos Pintos','Sitio Dos Pintos' ,'Tamarineira', 'Vasco Da Gama'
        ],
        'Norte': [
            'Alto Santa Terezinha', 'Arruda', 'Beberibe', 'Bomba Do Hemetério', 'Bomba Do Hemeterio', 'Cajueiro',
            'Campina Do Barreto', 'Campo Grande', 'Dois Unidos', 'Encruzilhada', 'Fundão', 'Fundao',
            'Hipódromo','Hipodromo' ,'Linha Do Tiro', 'Peixinhos', 'Ponto De Parada', 'Porto Da Madeira',
            'Rosarinho', 'Torreão', 'Torreao', 'Água Fria', 'Agua Fria'
        ],
        'Oeste': [
            'Caxangá', 'Caxanga', 'Cidade Universitária', 'Cidade Universitaria', 'Cordeiro', 'Engenho Do Meio',
            'Ilha Do Retiro', 'Iputinga', 'Madalena', 'Prado', 'Torre',
            'Torrões','Torroes', 'Várzea', 'Varzea', 'Zumbi'
        ],
        'Sudeste': [
            'Afogados', 'Areias', 'Barro', 'Bongi', 'Caçote', 'Cacote', 'Coqueiral', 'Curado',
            'Estância', 'Estancia', 'Jardim São Paulo', 'Jardim Sao Paulo', 'Jiquiá', 'Jiquia', 'Mangueira', 'Mustardinha',
            'San Martin', 'Sancho', 'Tejipió','Tejipio', 'Totó', 'Toto'
        ],
        'Sul': [
            'Boa Viagem', 'Brasília Teimosa', 'Brasilia Teimosa', 'Cohab', 'Ibura',
            'Imbiribeira', 'Ipsep', 'Jordão', 'Jordao', 'Pina'
        ]
    }

    # Criar dicionário com bairros sem acento como chave
    bairro_para_regiao = {
        unidecode.unidecode(bairro).strip().title(): regiao
        for regiao, bairros in dicionario.items()
        for bairro in bairros
    }

    # Normalizar a coluna 'Bairro' (sem acento e formatado corretamente)
    df['Bairro_norm'] = df['Bairro'].astype(str).apply(lambda x: unidecode.unidecode(x).strip().title())

    # Criar a coluna Região
    df['Região'] = df['Bairro_norm'].map(bairro_para_regiao)

    # (Opcional) remover a coluna auxiliar
    df.drop(columns='Bairro_norm', inplace=True)

    return df
# Salvando o DataFrame no arquivo CSV com codificação UTF-8 para subir para o BI

def criar_a_coluna_ano_e_mes(df):
    # Cria um dicionário fixo de número do mês para nome em português
    meses_pt = {
        1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
        5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
        9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
    }

    df['Ano'] = df['Data_entrada'].dt.year
    df['Mês'] = df['Data_entrada'].dt.month.map(meses_pt)
    return df


def main():
    urlUrbanismo = 'https://dados.recife.pe.gov.br/dataset/f79dbcdf-ec99-4f4c-9b84-b33175c35528/resource/39927a3d-3235-436a-9dc8-df7f4ea3b720/download/licenciamento_urbanistico.csv'
    urlAmbiental = 'https://dados.recife.pe.gov.br/dataset/75869ab7-ccce-40d6-aed6-4afca4c8cc82/resource/982d6c85-906a-4ea8-90e0-31f55eac63f9/download/licenciamento_ambiental.csv'
    urlSanitario = 'https://dados.recife.pe.gov.br/dataset/8535916b-588f-4006-bb1a-5d9c587a92d7/resource/d09900c8-14f2-4dc4-a128-b73a514ec791/download/licenciamento_sanitario.csv'
    Urbanismo = entrada_de_dados(urlUrbanismo)
    Ambiental = entrada_de_dados(urlAmbiental)
    Sanitario = entrada_de_dados(urlSanitario)
    Urbanismo = criando_coluna_tipo_de_liceniamento(Urbanismo,'Urbanístico')
    Sanitario = criando_coluna_tipo_de_liceniamento(Sanitario, 'Sanitário')
    Ambiental = criando_coluna_tipo_de_liceniamento(Ambiental, 'Ambiental')
    df = concatenando_os_treis_datasets(Urbanismo, Sanitario, Ambiental)
    df = Transforma_as_colunas_de_ojeto_para_datatime(df)
    df = transformar_na_coluna_data_conclusao_valores_em_branco_para_Nan(df)
    df = criar_uma_coluna_tempo_conclusao_para_mostrar_resolucao_do_pedido_de_licencimento(df)
    df = convertendo_para_string_coordenadas(df)
    df = substituindo_o_ponto_por_virgula(df)
    df = usar_funcao_title_nas_colunas_string(df)
    df = colocar_valores_NAN_nas_colunas(df)
    df = renomear_coluna_area(df)
    df = transformar_colunas_coordenadas_para_float(df, 'latitude')
    df = transformar_colunas_coordenadas_para_float(df, 'longitude')
    df = aplicar_capitalize_nas_colunas(df)
    df = criar_a_coluna_Regiao(df)
    df = criar_a_coluna_ano_e_mes(df)
    df_filtrado = df[['Num_processo', 'Situacao_processo', 'Tipo_licenciamento', 'Assunto', 'Região','Bairro', 'Tipo_mercantil','Potencial_empreendimento', 'Longitude', 'Latitude', 'Ano', 'Mês', 'Valor_pago', 'Endereco_empreendimento', 'Razao_social', 'Data_entrada', 'Tempo_conclusao', 'Cnpj', 'Data_conclusao']]
    df_filtrado = df_filtrado[df_filtrado['Data_entrada'].dt.year > 2020]


    #print(df.columns)
    #print(df.info())
    #criar_arquivo_csv(df)
    # Salvar o parquet
    df_filtrado.to_parquet(r"C:\Users\Ben-Hur\Desktop\Emprel\streamlit_licenciamentos\dados\licenciamentos.parquet", engine='pyarrow', index=False)
    #df_filtrado.to_excel("dados/licenciamentos.xlsx", index=False)
    #df_filtrado.to_parquet("dados/licenciamentosFiltros.parquet", index=False)
    
    return df_filtrado

# para iniciar o streamlit
df = main()
# Definição do programa principal será o main()
if __name__ == '__main__':
    main()
