# src/etl.py

import pandas as pd
import os

# --- Documentação ---
# Este script realiza o processo de ETL (Extração, Transformação e Carregamento).
# 1. Extração: Carrega os dados dos arquivos CSV da pasta 'dados'.
# 2. Transformação:
#    - Une as tabelas para criar um conjunto de dados único e coeso.
#    - Converte colunas de data para o formato datetime.
#    - Remove dados ausentes em colunas críticas.
# 3. Carregamento: Salva o DataFrame transformado num novo arquivo CSV na pasta 'analises'.
# --------------------

# Define os caminhos das pastas
PASTA_RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA_DADOS = os.path.join(PASTA_RAIZ, 'dados')
PASTA_ANALISES = os.path.join(PASTA_RAIZ, 'analises')

def extrair_dados(pasta_dados):
    """
    Carrega todos os arquivos CSV da pasta de dados especificada.
    Retorna um dicionário de DataFrames.
    """
    arquivos = [f for f in os.listdir(pasta_dados) if f.endswith('.csv')]
    dataframes = {}
    print("Iniciando extração dos dados...")
    for arquivo in arquivos:
        nome_df = arquivo.replace('_dataset.csv', '').replace('.csv', '')
        caminho_arquivo = os.path.join(pasta_dados, arquivo)
        dataframes[nome_df] = pd.read_csv(caminho_arquivo)
        print(f"  - Arquivo '{arquivo}' carregado como '{nome_df}'.")
    return dataframes

def transformar_dados(dataframes):
    """
    Une e limpa os DataFrames para criar um conjunto de dados consolidado.
    """
    print("\nIniciando transformação dos dados...")

    # Tradução de categorias de produtos
    produtos = dataframes['olist_products']
    traducoes = dataframes['product_category_name_translation']
    produtos = pd.merge(produtos, traducoes, on='product_category_name', how='left')
    # Substitui os nomes das categorias em inglês, mantendo o original se não houver tradução
    produtos['product_category_name'] = produtos['product_category_name_english'].fillna(produtos['product_category_name'])
    produtos = produtos.drop(columns=['product_category_name_english'])
    print("  - Nomes de categorias de produtos traduzidos.")

    # Junção das tabelas principais
    df = pd.merge(dataframes['olist_orders'], dataframes['olist_order_reviews'], on='order_id', how='left')
    df = pd.merge(df, dataframes['olist_order_payments'], on='order_id', how='left')
    df = pd.merge(df, dataframes['olist_order_items'], on='order_id', how='left')
    df = pd.merge(df, produtos, on='product_id', how='left')
    df = pd.merge(df, dataframes['olist_customers'], on='customer_id', how='left')
    print("  - Tabelas principais unidas.")

    # Limpeza e conversão de tipos de dados
    colunas_data = [
        'order_purchase_timestamp', 'order_approved_at', 'order_delivered_carrier_date',
        'order_delivered_customer_date', 'order_estimated_delivery_date'
    ]
    for coluna in colunas_data:
        df[coluna] = pd.to_datetime(df[coluna], errors='coerce')
    print(f"  - Colunas de data convertidas: {', '.join(colunas_data)}")
    
    # Remover linhas onde informações essenciais para a análise estão ausentes
    df.dropna(subset=['order_purchase_timestamp', 'product_category_name', 'review_score'], inplace=True)
    print("  - Dados ausentes em colunas críticas removidos.")

    print("Transformação concluída.")
    return df

def carregar_dados(df, pasta_destino):
    """
    Salva o DataFrame final num arquivo CSV.
    """
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)
    
    caminho_saida = os.path.join(pasta_destino, 'dados_tratados.csv')
    print(f"\nIniciando carregamento dos dados para '{caminho_saida}'...")
    df.to_csv(caminho_saida, index=False)
    print("Carregamento concluído com sucesso!")

def main():
    """
    Orquestra a execução do pipeline de ETL.
    """
    # 1. Extração
    dfs = extrair_dados(PASTA_DADOS)

    # 2. Transformação
    df_transformado = transformar_dados(dfs)

    # 3. Carregamento
    carregar_dados(df_transformado, PASTA_ANALISES)

if __name__ == "__main__":
    main()