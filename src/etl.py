import pandas as pd
import os

# ============ Documentação ============
# Este script realiza o processo de ETL (Extração, Transformação e Carregamento).
# 1. Extração: Carrega os dados dos arquivos CSV da pasta 'dados'.
# 2. Transformação: Une as tabelas, traduz colunas e converte tipos de dados.
# 3. Carregamento: Salva o DataFrame transformado num novo arquivo CSV na pasta 'analises'.
# ========================================

PASTA_RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA_DADOS = os.path.join(PASTA_RAIZ, 'dados')
PASTA_ANALISES = os.path.join(PASTA_RAIZ, 'analises')

def extrair_dados(pasta_dados):
    arquivos = [f for f in os.listdir(pasta_dados) if f.endswith('.csv')]
    dataframes = {}
    print("iniciando extração")
    for arquivo in arquivos:
        nome_df = arquivo.replace('_dataset.csv', '').replace('.csv', '')
        caminho_arquivo = os.path.join(pasta_dados, arquivo)
        dataframes[nome_df] = pd.read_csv(caminho_arquivo)
        print(f' - Arquivo {arquivo} carregad ocomo {nome_df}')
    return dataframes

def transformar_dados(dataframes):
    
    '''
    Une e limpa os dataframes para criar um conjunto de dados fundamentado
    '''
    print("\nIniciando transformação...")
    
    # Tradução de categoria de produtos
    produtos = dataframes['olist_products']
    traducao = dataframes['product_category_name_translation']
    produtos  = pd.merge(produtos, traducao, on='product_category_name', how='left')
    
    # Substitui  os nomes  das categorias em ingles, mantendo original se não tiver tradução
    produtos['product_category_name'] = produtos['products_category_name_english'].fillna(produtos['product_category_name'])
    produtos = produtos.drop(columns=['products_category_name_english'])
    print(" - Tradução de categorias de produtos concluída")
    
    # união das tabelas principais
    df = pd.merge(dataframes['olist_orders'], dataframes['olist_order_items'], on='order_id', how='left')
    df = pd.merge(df, dataframes['olist_orders_payments'], on = 'order_id', how='left')
    df = pd.merge(df, dataframes['olist_order_items'], on = 'order_id', how = 'left')
    df = pd.merge(df, produtos, on = 'product_id', how = 'left')
    df = pd.merge(df, dataframes['olist_customers'], on = 'customer_id', how = 'left')
    print(" - Tabelas principais unidas !")
    
    # limpeza e conversão de tipos
    colunas_data = [
        'order_purchase_timestamp',
        'order_approved_at',
        'order_delivered_carrier_date',
        'orer_delivered_customer_date',
        'order_estimated_delivered_date'
    ] 
    
    for coluna in colunas_data:
        df[coluna] = pd.to_datetime(df[coluna],errors = 'coerce')
    print(f" - Colunas de data convertidas: {', '.join(colunas_data)}")

    # REMOVER LINHAS ONDE INFORMAÇÕES ESSENCIAIS ESTÃO FALTANDO
    df = df.dropna(subset=[
        'order_purchase_timestamp',
        'product_category_name',
        'review_score'
    ], inplance=True)
    print("  - Dados ausentes em colunas críticas removidos.")

    print("Transformação concluída!")
    return df

def carregar_dados(df, pasta_destino):
    '''
    Salva o dataframe  final em um arquivo CSV na pasta de análises
    '''
    
    if not os.path.exists(pasta_destino):
        os.mkdir(pasta_destino)
    
    caminho_saida = os.path.join(pasta_destino, 'dados_tratados.csv')
    print(f"\nIniciando carregamento dos dados  para {caminho_saida}...")
    df.to_csv(caminho_saida, index = False)
    print(' - Dados carregados com sucesso!')
    
    
    def main():
        '''
        Função principal que executa o processo de ETL
        '''
        
        # 1. Extração
        dfs = extrair_dados(PASTA_DADOS)
        
        # 2. Transformação
        df_transformado = transformar_dados(dfs)

        # 3. Carregamento
        carregar_dados(df_transformado, PASTA_ANALISES)
        
    if __name__ == "__main__":
        main()