
import pandas as pd

# Calculo dos totalizadores
def calculo_total_licenciamentos(df):
    return formatar_milhar(df.shape[0])


def calculo_valor_taxas(df):
    df['Valor_pago'] = (
        df['Valor_pago'].astype(str)
        .str.replace(r'[^\d,.-]', '', regex=True)
        .str.replace(',', '.')
    )
    df['Valor_pago'] = pd.to_numeric(df['Valor_pago'], errors='coerce')
    total_taxas = formatar_moeda_br(round(df['Valor_pago'].sum(),2))
    return total_taxas

def calculo_total_licenca(df, tipo):
    return formatar_milhar((df['Tipo_licenciamento'] == tipo).sum())

def calculo_total_potencial(df, potencial):
    return formatar_milhar((df['Potencial_empreendimento'] == potencial).sum())


def formatar_moeda_br(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def formatar_milhar(valor):
    if pd.isna(valor):
        return ""
    try:
        return f"{int(valor):,}".replace(",", ".")
    except (ValueError, TypeError):
        return ""

def calculo_tempo_medio(df):
    df['Tempo_conclusao'] = pd.to_numeric(df['Tempo_conclusao'], errors='coerce')
    tempoMedio = int(round(df['Tempo_conclusao'].mean(), 0))
    return tempoMedio