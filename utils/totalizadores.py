
import pandas as pd








# Calculo dos totalizadores
def calculo_total_licenciamentos(df):
    totalLicenciamentos = df.shape[0]
    totalLicenciamentos = formatar_milhar(totalLicenciamentos)
    return totalLicenciamentos


def calculo_valor_taxas(df):
    df['Valor_pago'] = (
        df['Valor_pago'].astype(str)
        .str.replace(r'[^\d,.-]', '', regex=True)
        .str.replace(',', '.')
    )
    df['Valor_pago'] = pd.to_numeric(df['Valor_pago'], errors='coerce')
    total_taxas = round(df['Valor_pago'].sum(),2)
    total_taxas = formatar_moeda_br(total_taxas)
    return total_taxas

def calculo_total_urbanistico(df):
    totalUrbanistico = (df['Tipo_licenciamento'] == "Urbanístico").sum()
    totalUrbanistico = formatar_milhar(totalUrbanistico)
    return totalUrbanistico

def calculo_total_sanitario(df):
    totalSanitario = (df['Tipo_licenciamento'] == "Sanitário").sum()
    totalSanitario = formatar_milhar(totalSanitario)
    return totalSanitario

def calculo_total_ambiental(df):
    totalAmbiental = (df['Tipo_licenciamento'] == "Ambiental").sum()
    totalAmbiental = formatar_milhar(totalAmbiental)
    return totalAmbiental

def calculo_total_baixo(df):
    totalUrbanistico = (df['Potencial_empreendimento'] == "Baixo").sum()
    totalUrbanistico = formatar_milhar(totalUrbanistico)
    return totalUrbanistico

def calculo_total_medio(df):
    totalSanitario = (df['Potencial_empreendimento'] == "Médio").sum()
    totalSanitario = formatar_milhar(totalSanitario)
    return totalSanitario

def calculo_total_alto(df):
    totalAmbiental = (df['Potencial_empreendimento'] == "Alto").sum()
    totalAmbiental = formatar_milhar(totalAmbiental)
    return totalAmbiental


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
    tempoMedio = round((df['Tempo_conclusao']).mean(),2)
    return tempoMedio             