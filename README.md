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

## Como Usar

### Pré-requisitos

*   Python 3.7 ou superior (devido ao uso de `namedtuple` com type hints e f-strings avançadas).
*   Nenhuma biblioteca externa é necessária além das incluídas na instalação padrão do Python (`json`, `datetime`, `os`, `uuid`, `enum`, `collections`).

### Instalação

Basta baixar o arquivo Python (`wms_simulator.py`, por exemplo).

### Execução

Execute o script a partir do seu terminal:

```bash
python wms_simulator.py
