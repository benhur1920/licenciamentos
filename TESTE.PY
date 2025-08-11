"""
def dados_estao_atualizados(df):
    if "Data_emissao" not in df.columns:
        return False
    # Verifica se existe alguma linha com data no mês corrente
    try:
        df['Data_emissao'] = pd.to_datetime(df['Data_emissao'], errors='coerce')
        mes_ano_atual = datetime.today().strftime("%Y-%m")
        return df['Data_emissao'].dt.strftime("%Y-%m").eq(mes_ano_atual).any()
    except Exception:
        return False

@st.cache_data
def carregar_dados():
    if os.path.exists(CAMINHO_ARQUIVO):
        df = pd.read_parquet(CAMINHO_ARQUIVO)
        if dados_estao_atualizados(df):
            print("✅ Dados carregados do .parquet.")
            return df
        else:
            print("⚠️ Dados desatualizados. Recarregando...")
    else:
        print("📦 Arquivo .parquet não encontrado. Recarregando...")

    from dados.licenciamentos import main
    df = main()  # pode demorar se estiver puxando da internet
    df.to_parquet(CAMINHO_ARQUIVO, index=False)
    print("💾 Novo .parquet salvo.")
    return df

"""


