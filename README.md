#Análise de Dados Logísticos Integrados: Otimização da Cadeia de Suprimentos com WMS, TMS e ERP.

##Este repositório contém um projeto de Data Science dedicado à análise e otimização de operações logísticas através da integração e análise de dados provenientes de sistemas WMS (Warehouse Management System), TMS (Transportation Management System) e ERP (Enterprise Resource Planning).

O objetivo principal é construir um pipeline de dados robusto e modelos analíticos que permitam extrair insights acionáveis para a melhoria contínua da cadeia de suprimentos.

🎯 Objetivos

Consolidação de Dados: Desenvolver processos de ETL (Extract, Transform, Load) para unificar dados heterogêneos dos sistemas WMS, TMS e ERP em um Data Lake ou Data Warehouse centralizado.
Análise Diagnóstica: Identificar gargalos, ineficiências e padrões nas operações de armazenagem (WMS), transporte (TMS) e planejamento de recursos (ERP).
Análise Preditiva: Implementar modelos (potencialmente usando Machine Learning) para prever demandas, tempos de entrega, custos de frete e otimizar níveis de estoque.
Otimização Prescritiva: Desenvolver algoritmos ou heurísticas para otimização de rotas (e.g., VRP - Vehicle Routing Problem), alocação de recursos no armazém e planejamento de capacidade.
Monitoramento de KPIs: Calcular e visualizar Key Performance Indicators (KPIs) logísticos essenciais (e.g., OTD - On-Time Delivery, Custo por KM, Tempo de Ciclo do Pedido, Acurácia de Inventário, Utilização de Frota/Armazém).

Visualização de Dados: Criar dashboards interativos para monitoramento em tempo real e suporte à decisão gerencial.

🛠️ Arquitetura e Metodologia

Extração de Dados: Conexão com as fontes de dados (Bancos de Dados SQL, APIs REST/SOAP, arquivos CSV/Excel) dos sistemas WMS, TMS e ERP. Scripts automatizados para coleta periódica.
Transformação e Limpeza: Scripts em Python (utilizando bibliotecas como Pandas) para limpeza, padronização, tratamento de valores ausentes (missing values) e enriquecimento dos dados.
Carga de Dados: Inserção dos dados processados em um ambiente analítico (e.g., PostgreSQL, BigQuery, Redshift, Snowflake) ou datalake (e.g., S3, ADLS).
Análise Exploratória de Dados (EDA): Utilização de Jupyter Notebooks para explorar os dados, identificar correlações e gerar hipóteses.
Modelagem e Análise: Desenvolvimento de modelos estatísticos e de Machine Learning (Regressão, Classificação, Clustering, Séries Temporais) com bibliotecas como Scikit-learn, Statsmodels, Prophet.
Cálculo de KPIs: Lógica de negócio implementada em SQL ou Python para calcular os indicadores chave.
Visualização: Construção de dashboards utilizando ferramentas como Power BI, Tableau, Looker, ou bibliotecas Python como Plotly Dash/Streamlit.

💻 Tecnologias (Exemplo)

Linguagem: Python 3.x
Bibliotecas Principais:
pandas: Manipulação e análise de dados tabulares.
numpy: Computação numérica.
sqlalchemy / psycopg2 / pyodbc: Conexão com bancos de dados SQL.
requests: Requisições HTTP para APIs.
scikit-learn: Modelos de Machine Learning.
statsmodels: Modelos estatísticos.
matplotlib / seaborn / plotly: Visualização de dados estática e interativa.
jupyter: Notebooks para desenvolvimento e exploração.
Banco de Dados/DW (Exemplo): PostgreSQL / Google BigQuery
Orquestração (Opcional): Apache Airflow / Prefect
Visualização (Exemplo): Power BI / Streamlit
Controle de Versão: Git / GitHub

# Simulador WMS Avançado em Python

## Descrição

Este projeto implementa um simulador de Sistema de Gerenciamento de Armazém (WMS - Warehouse Management System) em Python puro, utilizando conceitos de Programação Orientada a Objetos (OOP). O objetivo é modelar e simular as principais entidades e operações de um armazém, como gerenciamento de catálogo de itens, controle de localizações com capacidade, rastreamento de estoque por lotes (FIFO/LIFO), processamento de pedidos e persistência de dados.

O simulador permite:
*   Cadastrar itens (SKUs) com atributos como nome, descrição, volume e peso.
*   Definir localizações no armazém com capacidades máximas baseadas em volume, peso ou quantidade.
*   Rastrear o estoque em cada localização através de lotes, registrando a data/hora de entrada.
*   Simular operações como recebimento, armazenagem (com estratégias), picking (separação baseada em FIFO/LIFO global ou por pedido) e expedição.
*   Gerenciar pedidos de clientes, desde a criação até a expedição.
*   Manter um log detalhado de todas as movimentações.
*   Salvar e carregar o estado completo do armazém (catálogo, localizações, inventário, pedidos, logs) em um arquivo JSON, permitindo a continuidade entre execuções.

## Funcionalidades Principais

*   **Gerenciamento de Catálogo:** Adição e consulta de itens (SKUs) com seus atributos.
*   **Gerenciamento de Localizações:** Criação de locais com `id`, `capacidade_maxima` e `tipo_capacidade` (volume, peso, quantidade).
*   **Controle de Inventário por Lotes:** O estoque em cada localização é rastreado por lotes (`Lote`), cada um com `quantidade` e `timestamp_entrada`.
*   **Operações de Movimentação:**
    *   **Recebimento:** Entrada de mercadorias em uma localização designada (ex: `RECEBIMENTO`).
    *   **Armazenagem (`guardar_mercadoria`):** Movimentação de itens da origem para um local de estoque, utilizando estratégias como:
        *   `PRIMEIRO_DISPONIVEL`: Primeiro local com capacidade encontrada.
        *   `MENOR_OCUPACAO`: Local com menor ocupação relativa que comporte o item.
        *   `EXISTENTE_SKU`: Prioriza locais que já contêm o mesmo SKU e têm capacidade.
        Inclui lógica de *rollback* em caso de falha ao adicionar no destino.
    *   **Picking (`fazer_picking`, `processar_picking_pedido`):** Coleta de itens do estoque para uma área de separação (ex: `PICKING_AREA`).
        *   Suporta estratégias globais **FIFO** (First-In, First-Out) ou **LIFO** (Last-In, First-Out) ao buscar lotes no armazém.
        *   Pode ser executado para um item específico ou para todos os itens de um `Pedido`.
    *   **Expedição (`expedir_mercadoria`, `expedir_pedido`):** Saída de mercadorias do armazém, geralmente da área de picking/expedição.
*   **Gerenciamento de Pedidos:**
    *   Criação de `Pedido` com ID único, cliente e lista de itens/quantidades.
    *   Ciclo de vida do pedido com `StatusPedido` (PENDENTE, EM_PICKING, PICKING_FALHOU, PICKING_COMPLETO, EXPEDIDO, CANCELADO).
    *   Processamento de picking e expedição baseado em pedidos.
*   **Validação e Tratamento de Erros:** Utiliza exceções customizadas (`WMSError`, `EstoqueInsuficienteError`, `CapacidadeExcedidaError`, etc.) para lidar com cenários como falta de estoque, capacidade excedida, itens/locais não encontrados.
*   **Log de Movimentações:** Registra todas as operações significativas com timestamp, tipo, SKU, quantidade, origem, destino, lotes afetados e ID do pedido associado.
*   **Persistência de Dados:** Salva o estado completo do WMS em um arquivo JSON (`armazem_estado.json` por padrão) e carrega automaticamente ao iniciar o script.

## Conceitos e Arquitetura

O código é estruturado em torno das seguintes classes principais:

1.  **`Item`**: Representa a definição de um tipo de produto (SKU), contendo `sku`, `nome`, `descricao`, `volume` e `peso`. Não armazena quantidade aqui.
2.  **`Lote` (namedtuple)**: Representa uma quantidade específica de um SKU que entrou no estoque em um determinado momento. Contém `quantidade`, `timestamp_entrada` e `id_lote`. Usado para implementar FIFO/LIFO.
3.  **`Localizacao`**: Modela um local físico no armazém (`id_local`). Armazena o inventário como um dicionário `{sku: [Lote, Lote, ...]}`. Gerencia a `capacidade_maxima` e o `tipo_capacidade`. Contém métodos para `adicionar_lote`, `remover_item` (baseado em estratégia FIFO/LIFO local), `verificar_estoque` e `verificar_capacidade`.
4.  **`Pedido`**: Representa um pedido de cliente com `pedido_id`, `cliente`, `itens_solicitados` (dicionário `{sku: quantidade}`) e `status` (`StatusPedido`).
5.  **`ArmazemWMS`**: Classe orquestradora principal. Gerencia o `catalogo_itens`, as `localizacoes`, os `pedidos` e o `log_movimentacoes`. Contém os métodos que implementam as operações WMS (receber, guardar, picking, expedir) e as lógicas de seleção de localização e lotes. Também lida com a persistência (`_salvar_estado`, `carregar_estado`).
6.  **Exceções Customizadas**: Classes como `ItemNaoEncontradoError`, `EstoqueInsuficienteError`, etc., herdam de `WMSError` para sinalizar erros específicos da operação do WMS.

# Basic TMS Simulation in Python

Um projeto simples em Python que simula as funcionalidades centrais de um Transportation Management System (TMS). Este código demonstra o gerenciamento do ciclo de vida de uma carga, desde a criação até a entrega, incluindo a interação básica com transportadoras e um mecanismo de rastreamento.

## Sobre o Projeto

Este repositório contém um exemplo didático e funcional de como modelar e simular um sistema de gerenciamento de transporte (TMS) utilizando Programação Orientada a Objetos em Python. O objetivo é ilustrar os conceitos fundamentais envolvidos na orquestração do fluxo de cargas, desde sua origem até o destino, considerando características logísticas e a seleção de transportadoras.

**Status Atual:** Simulação básica, focada na estrutura de dados e fluxo lógico.

## Funcionalidades Implementadas

* **Modelagem de Entidades:** Definição de classes para representar Endereços, Itens de Transporte, Cargas e Transportadoras.
* **Gerenciamento de Cargas:**
    * Criação de novas cargas com origem, destino e lista de itens.
    * Acompanhamento do status da carga (`CRIADA`, `PLANEJADA`, `EM_TRANSITO`, `ENTREGUE`, `CANCELADA`).
    * Histórico de rastreamento detalhado a cada mudança de status.
    * Cálculo agregado de peso e volume total da carga.
* **Gerenciamento de Transportadoras:**
    * Cadastro de transportadoras com taxas básicas.
    * Cálculo de custo de frete estimado (modelo simplificado).
* **Workflow do TMS:**
    * **Planejamento:** Seleção automática da transportadora com menor custo estimado para uma carga (baseado em distância simulada e peso). Cálculo de data prevista de entrega simplificada.
    * **Despacho:** Transição de status para `EM_TRANSITO`.
    * **Registro de Entrega:** Transição de status para `ENTREGUE`.
    * Consulta detalhada de cargas por ID.
* **Simulação de Distância:** Mecanismo interno simples para simular a distância entre cidades (placeholder para futuras integrações de geolocalização/roteamento).

## Estrutura do Código

O código é organizado em classes que representam os principais conceitos do domínio de transporte:

* `Endereco`: Representa um local geográfico com logradouro, número, cidade, estado e CEP.
* `ItemTransporte`: Representa um item individual ou agrupamento de itens com o mesmo SKU, quantidade, peso e volume unitário. Inclui propriedades para calcular peso e volume totais do item.
* `Carga`: Representa a unidade de transporte. Contém origem, destino, uma lista de `ItemTransporte`, status, histórico de rastreamento e informações sobre a transportadora designada e custo estimado. Age como o agregado raiz (`Aggregate Root` no DDD).
* `Transportadora`: Representa uma empresa de transporte com um modelo de custo básico.
* `TMS`: A classe principal do sistema, agindo como orquestrador. Gerencia coleções de `Carga` e `Transportadora` e implementa os workflows de negócio (criar, planejar, despachar, entregar). Contém a lógica para simular distâncias e selecionar transportadoras.

### Pré-requisitos

*   Python 3.7 ou superior (devido ao uso de `namedtuple` com type hints e f-strings avançadas).
*   Nenhuma biblioteca externa é necessária além das incluídas na instalação padrão do Python (`json`, `datetime`, `os`, `uuid`, `enum`, `collections`).

### Instalação

Basta baixar o arquivo Python (`wms_simulator.py`, por exemplo).

### Execução

Execute o script a partir do seu terminal:

```bash
python wms_simulator.py

🤝 Contribuição
Contribuições são bem-vindas! Por favor, leia as diretrizes de contribuição (se houver um arquivo CONTRIBUTING.md) antes de submeter pull requests. Issues podem ser abertas para reportar bugs ou sugerir novas funcionalidades.

📄 Licença
Este projeto é licenciado sob a Licença [Nome da Licença - e.g., MIT]. Veja o arquivo LICENSE para mais detalhes.
