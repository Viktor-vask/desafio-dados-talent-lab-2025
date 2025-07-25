# Desafio: Análise de Dados do E-commerce Brasileiro (Olist)

Este projeto contém a solução para o desafio de dados "Dados que transformam", focado na realização de um processo de ETL (Extração, Transformação e Carregamento) e uma Análise Exploratória de Dados (EDA) sobre um conjunto de dados público de e-commerce brasileiro.

O objetivo é extrair insights de negócio a partir dos dados brutos, seguindo um roteiro de análise que abrange vendas, logística, satisfação do cliente, finanças e marketing.

## Análises Selecionadas

Para a Análise Exploratória de Dados, foi necessário escolher uma questão de cada um dos cinco tópicos propostos. As seguintes questões foram selecionadas:

#### Questões Escolhidas
* **1. Análise de Performance de Vendas:**
    * (a) Volume de Vendas por Categoria: Identificar quais categorias de produtos têm o maior volume de vendas.
* **2. Análise de Logística:**
    * (a) Prazos de Entrega: Calcular o tempo médio de entrega e identificar os fatores que influenciam atrasos nas entregas.
* **3. Análise de Satisfação do Cliente:**
    * (b) Impacto dos Atrasos na Satisfação do Cliente: Examinar a relação entre atrasos na entrega e a satisfação do cliente.
* **4. Análise Financeira:**
    * (b) Análise de Custos de Frete: Investigar a relação entre custos de frete, distância de entrega e a satisfação do cliente.
* **5. Análise de Marketing:**
    * (b) Eficácia de Campanhas Promocionais: Avaliar o impacto de campanhas promocionais e descontos no volume de vendas e na aquisição de novos clientes.

#### Justificativa da Escolha

Esta combinação foi escolhida para contar uma história coesa sobre a **jornada do cliente e a eficiência operacional** da empresa. A narrativa segue um fluxo lógico:
1.  Começamos por entender **o que os clientes mais compram** (Vendas por Categoria).
2.  Em seguida, investigamos **como esses produtos são entregues** (Prazos de Entrega).
3.  Conectamos a eficiência da entrega com a **percepção do cliente** (Impacto do Atraso na Satisfação).
4.  Aprofundamos a análise logística, explorando a **relação financeira do frete** com a satisfação (Custos de Frete).
5.  Finalmente, analisamos uma **alavanca de marketing** que impulsiona o volume de vendas (Eficácia de Campanhas).

Esta abordagem permite não apenas responder a perguntas isoladas, mas também entender as interconexões entre as diferentes áreas do negócio.

## Estrutura do Projeto

O repositório está organizado em três pastas principais para garantir a separação de responsabilidades e a clareza do projeto:

* `/dados`: Contém os múltiplos arquivos `.csv` originais que compõem o dataset.
* `/src`: Contém os scripts Python desenvolvidos para o projeto.
    * `etl.py`: Script responsável por todo o processo de Extração, Transformação e Carregamento. Ele lê os dados brutos, une as tabelas, limpa as informações e salva um único ficheiro tratado.
    * `analise.py`: Script que carrega os dados já tratados e executa as cinco análises exploratórias, gerando um gráfico para cada uma.
* `/analises`: Contém os resultados gerados pelos scripts.
    * `dados_tratados.csv`: O dataset consolidado e limpo, pronto para a análise.
    * Gráficos (`.png`): As cinco visualizações de dados geradas pelo script `analise.py`.

## Resultados e Interpretação dos Gráficos

A execução do script `analise.py` gerou as seguintes visualizações, que nos permitem tirar conclusões importantes sobre o negócio.

### 1. Volume de Vendas por Categoria
*Gráfico correspondente: `1_vendas_por_categoria.png`*

**Interpretação:** A análise revela uma forte concentração de vendas em poucas categorias. Categorias como `cama_mesa_banho`, `beleza_saude` e `esporte_lazer` dominam o volume de transações. Isso indica quais são os "carros-chefe" da empresa e onde os esforços de marketing e gestão de stock devem ser mais intensos. Também aponta para uma oportunidade de crescimento em categorias menos populares.

### 2. Prazos de Entrega
*Gráfico correspondente: `2_distribuicao_tempo_entrega.png`*

**Interpretação:** O histograma mostra a distribuição do tempo de entrega em dias. Observa-se que a maioria das entregas ocorre num período entre 5 a 15 dias. No entanto, o gráfico também evidencia uma "cauda longa" à direita, indicando a existência de um número significativo de pedidos que demoram muito mais do que a média para serem entregues. Estes outliers são os principais candidatos a gerar insatisfação.

### 3. Impacto dos Atrasos na Satisfação do Cliente
*Gráfico correspondente: `3_impacto_atraso_satisfacao.png`*

**Interpretação:** Este é um dos insights mais diretos e acionáveis. O boxplot mostra de forma inequívoca que os pedidos entregues com atraso recebem notas de satisfação drasticamente mais baixas (mediana em torno de 1-2 estrelas) em comparação com os pedidos entregues dentro do prazo (mediana em 5 estrelas). Isso confirma que a pontualidade da entrega é um fator crítico para a satisfação e lealdade do cliente.

### 4. Análise de Custos de Frete vs. Satisfação
*Gráfico correspondente: `4_custo_frete_satisfacao.png`*

**Interpretação:** A análise sugere que não há uma correlação simples e direta entre o valor pago pelo frete e a nota de satisfação. Clientes que pagam fretes mais caros não necessariamente avaliam pior o serviço. Isso pode indicar que os clientes estão mais sensíveis ao *prazo* de entrega do que ao *custo* do frete, ou que os fretes mais caros estão associados a entregas mais rápidas, compensando o custo.

### 5. Eficácia de Campanhas Promocionais (via Parcelamento)
*Gráfico correspondente: `5_eficacia_promocao_parcelas.png`*

**Interpretação:** Utilizando o número de parcelas como um indicador de condições promocionais, o gráfico mostra que um volume significativo do valor total vendido está concentrado em pagamentos com alto número de parcelas (e.g., 8 a 10 vezes). Isso sugere que a oferta de parcelamento sem juros (ou com juros baixos) é uma alavanca de marketing extremamente eficaz para impulsionar as vendas, especialmente para produtos de maior valor.