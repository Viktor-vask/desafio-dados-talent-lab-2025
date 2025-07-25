# src/analise.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- Documentação ---
# Este script realiza a Análise Exploratória de Dados (EDA).
# Ele carrega o conjunto de dados tratado e gera visualizações para responder
# às seguintes questões de negócio:
# 1. (a) Volume de Vendas por Categoria.
# 2. (a) Prazos de Entrega.
# 3. (b) Impacto dos Atrasos na Satisfação do Cliente.
# 4. (b) Análise de Custos de Frete vs. Satisfação.
# 5. (b) Eficácia de Campanhas Promocionais (análise por nº de parcelas).
# Os gráficos gerados são salvos na pasta 'analises'.
# --------------------

# Define os caminhos das pastas
PASTA_RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA_ANALISES = os.path.join(PASTA_RAIZ, 'analises')
CAMINHO_DADOS_TRATADOS = os.path.join(PASTA_ANALISES, 'dados_tratados.csv')

def configurar_estilo_graficos():
    """Define um estilo visual padrão para todos os gráficos."""
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = (12, 7)
    plt.rcParams['font.size'] = 12

def salvar_grafico(nome_arquivo):
    """Salva a figura atual na pasta de análises."""
    caminho_completo = os.path.join(PASTA_ANALISES, nome_arquivo)
    plt.savefig(caminho_completo, bbox_inches='tight')
    print(f"  - Gráfico salvo como '{nome_arquivo}'.")

# 1. Análise de Performance de Vendas
def analise_vendas_por_categoria(df):
    """Identifica o volume de vendas por categoria de produto."""
    print("\nAnálise 1/5 - Gerando análise de volume de vendas por categoria...")
    plt.figure()
    contagem_categorias = df['product_category_name'].value_counts().nlargest(15)
    sns.barplot(x=contagem_categorias.values, y=contagem_categorias.index, palette='viridis', orient='h')
    plt.title('Top 15 Categorias com Maior Volume de Vendas')
    plt.xlabel('Número de Vendas')
    plt.ylabel('Categoria do Produto')
    salvar_grafico('1_vendas_por_categoria.png')
    plt.close()

# 2. Análise de Logística
def analise_prazos_de_entrega(df):
    """Calcula e visualiza o tempo médio de entrega."""
    print("\nAnálise 2/5 - Gerando análise de prazos de entrega...")
    df_entrega = df.dropna(subset=['order_purchase_timestamp', 'order_delivered_customer_date'])
    df_entrega['tempo_entrega'] = (df_entrega['order_delivered_customer_date'] - df_entrega['order_purchase_timestamp']).dt.days
    
    # FILTRO: Mantém apenas entregas com até 30 dias
    df_entrega = df_entrega[df_entrega['tempo_entrega'] <= 40]
    
    tempo_medio = df_entrega['tempo_entrega'].mean()
    print(f"  - Tempo médio de entrega: {tempo_medio:.2f} dias.")

    plt.figure()
    sns.histplot(df_entrega['tempo_entrega'], bins=30, kde=True, color='blue')
    plt.title(f'Distribuição do Tempo de Entrega (Média: {tempo_medio:.2f} dias)')
    plt.xlabel('Tempo de Entrega (dias)')
    plt.ylabel('Frequência')
    plt.axvline(tempo_medio, color='red', linestyle='--', label=f'Média ({tempo_medio:.2f} dias)')
    plt.legend()
    salvar_grafico('2_distribuicao_tempo_entrega.png')
    plt.close()

# 3. Análise de Satisfação do Cliente
def analise_impacto_atrasos(df):
    """Examina a relação entre atrasos na entrega e a satisfação do cliente."""
    print("\nAnálise 3/5 - Gerando análise do impacto de atrasos na satisfação...")
    df_atraso = df.dropna(subset=['order_delivered_customer_date', 'order_estimated_delivery_date'])
    df_atraso['dias_atraso'] = (df_atraso['order_delivered_customer_date'] - df_atraso['order_estimated_delivery_date']).dt.days
    df_atraso['atrasado'] = df_atraso['dias_atraso'] > 0
    
    media_satisfacao = df_atraso.groupby('atrasado')['review_score'].mean().reset_index()
    print("  - Média de satisfação:")
    print(media_satisfacao.to_string(index=False))

    plt.figure()
    sns.boxplot(x='atrasado', y='review_score', data=df_atraso, palette='coolwarm')
    plt.title('Impacto do Atraso na Entrega vs. Satisfação do Cliente')
    plt.xlabel('Pedido Entregue com Atraso?')
    plt.ylabel('Nota de Satisfação (Review Score)')
    plt.xticks([0, 1], ['Não', 'Sim'])
    salvar_grafico('3_impacto_atraso_satisfacao.png')
    plt.close()

# 4. Análise Financeira
def analise_custos_frete(df):
    """Investiga a relação entre custos de frete e a satisfação do cliente."""
    print("\nAnálise 4/5 - Gerando análise de custo de frete vs. satisfação...")
    df_frete = df.dropna(subset=['freight_value', 'review_score'])
    # Categorizar o frete para melhor visualização
    df_frete['faixa_frete'] = pd.qcut(df_frete['freight_value'], q=4, labels=['Baixo', 'Médio', 'Alto', 'Muito Alto'], duplicates='drop')

    plt.figure()
    sns.boxplot(x='faixa_frete', y='review_score', data=df_frete, palette='plasma')
    plt.title('Satisfação do Cliente por Faixa de Custo de Frete')
    plt.xlabel('Faixa de Custo do Frete')
    plt.ylabel('Nota de Satisfação (Review Score)')
    salvar_grafico('4_custo_frete_satisfacao.png')
    plt.close()

# 5. Análise de Marketing
def analise_eficacia_promocoes(df):
    """Avalia o impacto de promoções, usando o número de parcelas como proxy."""
    print("\nAnálise 5/5 - Gerando análise de eficácia de promoções (por parcelas)...")
    df_pagamento = df.dropna(subset=['payment_installments', 'payment_value'])
    
    # Análise do valor total de compra por número de parcelas
    vendas_por_parcela = df_pagamento.groupby('payment_installments')['payment_value'].sum().reset_index()

    plt.figure()
    sns.barplot(x='payment_installments', y='payment_value', data=vendas_por_parcela, palette='magma')
    plt.title('Valor Total de Vendas por Número de Parcelas')
    plt.xlabel('Número de Parcelas')
    plt.ylabel('Valor Total Vendido (em milhões)')
    # Formatar o eixo Y para melhor leitura
    plt.gca().get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x/1e6), ',')))
    salvar_grafico('5_eficacia_promocao_parcelas.png')
    plt.close()

def main():
    """
    Orquestra a execução do pipeline de Análise.
    """
    print("--- Iniciando Pipeline de Análise Exploratória de Dados ---")
    
    # Verifica se o arquivo de dados tratados existe
    if not os.path.exists(CAMINHO_DADOS_TRATADOS):
        print(f"ERRO: O arquivo '{CAMINHO_DADOS_TRATADOS}' não foi encontrado.")
        print("Por favor, execute o script 'src/etl.py' primeiro.")
        return

    # Carrega os dados
    print(f"Carregando dados tratados de '{CAMINHO_DADOS_TRATADOS}'...")
    df = pd.read_csv(CAMINHO_DADOS_TRATADOS, parse_dates=colunas_data)
    
    # Configura o estilo dos gráficos
    configurar_estilo_graficos()
    
    # Executa cada função de análise
    analise_vendas_por_categoria(df)
    analise_prazos_de_entrega(df)
    analise_impacto_atrasos(df)
    analise_custos_frete(df)
    analise_eficacia_promocoes(df)

    print("\n--- A Análise Exploratória de Dados ---\n---   STATUS: Concluído    ---")
    print(f"Todos os gráficos foram salvos na pasta '{PASTA_ANALISES}'.")

# Definindo 'colunas_data' globalmente para ser acessível no main
colunas_data = [
    'order_purchase_timestamp', 'order_approved_at', 'order_delivered_carrier_date',
    'order_delivered_customer_date', 'order_estimated_delivery_date'
]

if __name__ == "__main__":
    main()