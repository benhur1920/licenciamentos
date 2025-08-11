import pandas as pd
import unidecode
import locale

def entrada_de_dados(url):
    dados = pd.read_csv(url, sep=';', encoding='ISO-8859-1')  # Testar outra codificação
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
    # Garante que a coluna estará pronta para operações numéricas
    df['Tempo_conclusao'] = pd.NA

    # Calcula somente para os casos com data_conclusao preenchida
    mask = df['data_conclusao'].notna()
    df.loc[mask, 'Tempo_conclusao'] = (
        (df.loc[mask, 'data_conclusao'] - df.loc[mask, 'data_entrada']).dt.days
    )

    # Converte a coluna para tipo numérico
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
    # Verificar se as colunas 'latitude' e 'longitude' existem
    if 'latitude' in df.columns and 'longitude' in df.columns:
        # Tratar valores NaN antes de substituir
        df['latitude'] = df['latitude'].fillna('').astype(
            str).str.replace('.', ',', regex=False)
        df['longitude'] = df['longitude'].fillna('').astype(
            str).str.replace('.', ',', regex=False)
        # ⚠️ Remover esta linha para manter a coluna numérica:
        # df['Tempo_conclusao'] = df['Tempo_conclusao'].fillna('').astype(str).str.replace('.', ',', regex=False)
    else:
        print("As colunas 'latitude', 'longitude' não foram encontradas no DataFrame.")
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
            'Paissandu', 'Recife', 'Santo Amaro', 'Santo Antônio', 'Soledade', 'São José'
        ],
        'Noroeste': [
            'Aflitos', 'Alto Do Mandu', 'Alto José Bonifácio', 'Alto José Do Pinho', 'Apipucos',
            'Brejo Da Guabiraba', 'Brejo De Beberibe', 'Casa Amarela', 'Casa Forte',
            'Córrego Do Jenipapo', 'Derby', 'Dois Irmãos', 'Espinheiro', 'Graças', 'Guabiraba',
            'Jaqueira', 'Macaxeira', 'Mangabeira', 'Monteiro', 'Morro Da Conceição',
            'Nova Descoberta', 'Parnamirim', 'Passarinho', 'Pau Ferro', 'Poço', 'Santana',
            'Sítio Dos Pintos', 'Tamarineira', 'Vasco Da Gama'
        ],
        'Norte': [
            'Alto Santa Terezinha', 'Arruda', 'Beberibe', 'Bomba Do Hemetério', 'Cajueiro',
            'Campina Do Barreto', 'Campo Grande', 'Dois Unidos', 'Encruzilhada', 'Fundão',
            'Hipódromo', 'Linha Do Tiro', 'Peixinhos', 'Ponto De Parada', 'Porto Da Madeira',
            'Rosarinho', 'Torreão', 'Água Fria'
        ],
        'Oeste': [
            'Caxangá', 'Cidade Universitária', 'Cordeiro', 'Engenho Do Meio',
            'Ilha Do Retiro', 'Iputinga', 'Madalena', 'Prado', 'Torre',
            'Torrões', 'Várzea', 'Zumbi'
        ],
        'Sudeste': [
            'Afogados', 'Areias', 'Barro', 'Bongi', 'Caçote', 'Coqueiral', 'Curado',
            'Estância', 'Jardim São Paulo', 'Jiquiá', 'Mangueira', 'Mustardinha',
            'San Martin', 'Sancho', 'Tejipió', 'Totó'
        ],
        'Sul': [
            'Boa Viagem', 'Brasília Teimosa', 'Cohab', 'Ibura',
            'Imbiribeira', 'Ipsep', 'Jordão', 'Pina'
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
    urlUrbanismo = 'http://dados.recife.pe.gov.br/dataset/e2bd8f0b-1d62-4323-8159-8ebd6ed9eb4a/resource/77c885c4-76ca-45eb-9209-06c5d217122d/download/licenciamento_urbanistico.csv'
    urlAmbiental = 'http://dados.recife.pe.gov.br/dataset/0bc5325e-0203-4577-9d56-bd3aef192f20/resource/921244a8-fe47-4192-a57d-084830337f99/download/licenciamento_ambiental.csv'
    urlSanitario = 'http://dados.recife.pe.gov.br/dataset/3a4869e7-7021-485e-97fb-f25cd6422ea6/resource/6bb70e99-b7b9-4b2a-a213-adc757e3337a/download/licenciamento_sanitario.csv'
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
    df_filtrado.to_parquet("dados/licenciamentos.parquet", engine='pyarrow', index=False)
    #df_filtrado.to_excel("dados/licenciamentos.xlsx", index=False)
    #df_filtrado.to_parquet("dados/licenciamentosFiltros.parquet", index=False)
    
    return df_filtrado

# para iniciar o streamlit
df = main()
# Definição do programa principal será o main()
if __name__ == '__main__':
    main()
