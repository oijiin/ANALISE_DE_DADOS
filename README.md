# Análise de Dados Logísticos Integrados: Otimização da Cadeia de Suprimentos com WMS, TMS e ERP.

## Este repositório contém um projeto de Data Science dedicado à análise e otimização de operações logísticas através da integração e análise de dados provenientes de sistemas WMS (Warehouse Management System), TMS (Transportation Management System) e ERP (Enterprise Resource Planning).

O objetivo principal é construir um pipeline de dados robusto e modelos analíticos que permitam extrair insights acionáveis para a melhoria contínua da cadeia de suprimentos.

# Simulador Integrado de Logística (WMS, TMS, ERP) em Python

## 📖 Descrição

Este projeto é um simulador educacional desenvolvido em Python que modela as interações básicas entre três sistemas cruciais na gestão da cadeia de suprimentos:

1.  **WMS (Warehouse Management System):** Sistema de Gerenciamento de Armazém
2.  **TMS (Transportation Management System):** Sistema de Gerenciamento de Transporte
3.  **ERP (Enterprise Resource Planning):** Sistema de Gestão Empresarial

O objetivo principal é fornecer uma ferramenta prática para aprender e visualizar como esses sistemas funcionam e se integram para gerenciar o fluxo de produtos e informações, desde a compra de matéria-prima até a entrega ao cliente final. O foco está na lógica dos processos logísticos e na troca de dados entre os sistemas.

Este projeto foi desenvolvido como parte de estudos em Análise e Desenvolvimento de Sistemas, com foco em Análise de Dados aplicada à Logística.

## ✨ Conceitos Simulados

* **WMS:**
    * Gerenciamento de Itens (SKUs) e Localizações de estoque (bins, prateleiras).
    * Controle de inventário (quantidades por localização).
    * Operações básicas de armazém: Recebimento, Armazenagem, Picking (Separação) e Expedição.
    * Registro de movimentações de estoque.
* **TMS:**
    * Gerenciamento de Endereços (Origem/Destino).
    * Criação de Cargas (Shipments) com itens, peso e volume.
    * Gerenciamento de Transportadoras.
    * Cálculo de frete simplificado (baseado em distância, peso, taxa).
    * Simulação de distância entre localidades.
    * Rastreamento de status da carga (Criada, Planejada, Em Trânsito, Entregue).
* **ERP:**
    * Gerenciamento de Dados Mestres: Produtos (com preço/custo), Clientes, Fornecedores.
    * Ciclo de Vendas (Simplificado): Ordem de Venda -> Liberação WMS -> Confirmação TMS -> Faturamento.
    * Ciclo de Compras (Simplificado): Ordem de Compra -> Confirmação WMS -> Liquidação.
    * Visibilidade de Estoque (Quantidade e Valor Básico).
    * Registro de Eventos Financeiros Chave (Receita, CMV, Custo de Frete, Entrada de Estoque).
    * Gerenciamento do ciclo de vida (status) das ordens.

## 🚀 Funcionalidades Atuais

* Modelagem orientada a objetos para representar entidades do mundo real (Itens, Pedidos, Cargas, etc.).
* Lógica básica para as operações de cada sistema (WMS, TMS, ERP).
* Simulação de interações chave (ex: Ordem de Venda no ERP dispara picking no WMS, que dispara criação de carga no TMS).
* Estrutura modular (cada sistema em seu próprio arquivo `.py`).
* Exemplos de uso dentro de cada módulo (`if __name__ == "__main__":`) para demonstração.
* Log de movimentações (WMS) e histórico de status (TMS, ERP).
* Cálculos básicos de custo (frete no TMS, valor de estoque no ERP).
* Uso de `Decimal` para cálculos financeiros no ERP.

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.x
* **Bibliotecas:**
    * `datetime` (para timestamps)
    * `decimal` (para precisão monetária no ERP)
    * `math` (para cálculos auxiliares)
    * (Nenhuma biblioteca externa é necessária para a funcionalidade principal atual)

## 📁 Estrutura do Projeto

```bash
/
├── wms_simulator.py        # Código do Simulador WMS
├── tms_simulator.py        # Código do Simulador TMS
├── erp_simulator.py        # Código do Simulador ERP
├── main_simulation.py      # (Opcional/Futuro) Script para orquestrar a simulação integrada
└── README.md               # Este arquivo
```

* Cada arquivo `*_simulator.py` contém as classes e a lógica para o respectivo sistema.
* Os exemplos `if __name__ == "__main__":` dentro de cada arquivo permitem testar/demonstrar cada módulo individualmente.
* Um arquivo `main_simulation.py` pode ser criado para instanciar os três sistemas e orquestrar um fluxo completo (ex: criar OV no ERP, que chama WMS, que chama TMS, etc.).

## ⚙️ Instalação e Execução

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git](https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git)
    cd SEU_REPOSITORIO
    ```
2.  **Pré-requisitos:** Certifique-se de ter o Python 3 instalado em seu sistema.
3.  **Execução:**
    * **Para executar os exemplos individuais de cada módulo:**
        ```bash
        python wms_simulator.py
        python tms_simulator.py
        python erp_simulator.py
        ```
    * **(Futuro) Para executar uma simulação integrada (se `main_simulation.py` for criado):**
        ```bash
        python main_simulation.py
        ```

## 🎮 Como Usar (Exemplos Básicos)

* **WMS:**
    ```python
    # Dentro de wms_simulator.py (exemplo)
    from wms_simulator import ArmazemWMS, Item, Localizacao

    armazem = ArmazemWMS("CD Principal")
    item1 = Item("SKU001", "Produto A")
    loc1 = Localizacao("A1-01")
    armazem.adicionar_item_catalogo(item1)
    armazem.adicionar_localizacao(loc1)
    armazem.receber_mercadoria("SKU001", 100, "RECEBIMENTO")
    armazem.guardar_mercadoria("SKU001", 100, "RECEBIMENTO", "A1-01")
    armazem.inventario_geral()
    ```
* **TMS:**
    ```python
    # Dentro de tms_simulator.py (exemplo)
    from tms_simulator import TMS, Transportadora, Endereco, ItemTransporte

    tms = TMS()
    t1 = Transportadora("T001", "Transportadora Veloz")
    tms.adicionar_transportadora(t1)
    origem = Endereco(...)
    destino = Endereco(...)
    item_carga = ItemTransporte("SKU001", 50, 0.5, 0.001)
    carga = tms.criar_carga("CARGA01", origem, destino, [item_carga])
    tms.planejar_transporte("CARGA01")
    tms.consultar_carga("CARGA01")
    ```
* **ERP:**
    ```python
    # Dentro de erp_simulator.py (exemplo)
    from erp_simulator import ERP, ProdutoERP, Cliente, Endereco
    from decimal import Decimal

    erp = ERP("Minha Empresa")
    prod1 = ProdutoERP("SKU001", "Produto A", preco_venda=Decimal('10.0'), custo_medio=Decimal('4.0'))
    erp.adicionar_produto(prod1)
    end_cli = Endereco(...)
    cli1 = Cliente("C001", "Cliente Teste", "...", end_cli)
    erp.adicionar_cliente(cli1)
    ov = erp.criar_ordem_venda("OV001", "C001", [("SKU001", 10)]) # Cria OV e libera p/ WMS
    erp.consultar_ov("OV001")
    ```

## 🔗 Pontos de Integração (Conceitual)

A interação ideal entre os módulos segue fluxos como:

1.  **Venda:** `ERP.criar_ordem_venda` -> `ERP.liberar_ov_para_wms` -> `WMS.receber_pedido_separacao` -> `WMS` (executa picking) -> `WMS.confirmar_expedicao` -> `ERP.receber_confirmacao_separacao_wms` -> `ERP.solicitar_transporte_tms` -> `TMS.criar_carga` -> `TMS.planejar_transporte` -> `TMS` (executa transporte) -> `TMS.registrar_entrega` -> `ERP.receber_confirmacao_entrega_tms` -> `ERP.faturar_ordem_venda`.
2.  **Compra:** `ERP.criar_ordem_compra` -> `WMS.agendar_recebimento` (aguarda chegada) -> `WMS.receber_mercadoria` (confere c/ OC) -> `WMS.confirmar_recebimento` -> `ERP.receber_confirmacao_recebimento_wms` (atualiza estoque/OC) -> `ERP` (liquida OC).

A implementação atual define os métodos para essas interações, mas a orquestração completa idealmente ocorreria em um script `main_simulation.py`.

## 📈 Melhorias Futuras (Roadmap)

* [ ] **Interface de Usuário:** Criar uma interface de linha de comando (CLI) ou gráfica (GUI com Tkinter/PyQt) para interagir com a simulação.
* [ ] **Persistência de Dados:** Salvar e carregar o estado da simulação (inventário, pedidos, cargas) em arquivos (JSON, CSV) ou banco de dados (SQLite).
* [ ] **Lógica Avançada:**
    * WMS: Estratégias de armazenagem (slotting), picking (FIFO/LIFO/FEFO), contagem cíclica.
    * TMS: Roteirização (multi-stop), consolidação de cargas, gerenciamento de frota/veículos, cálculo de frete mais complexo (tabelas).
    * ERP: Cálculo de Custo Médio Ponderado real, Disponibilidade para Promessa (ATP), relatórios financeiros/operacionais básicos.
* [ ] **Integração Real:** Implementar a comunicação direta entre os objetos dos diferentes módulos em `main_simulation.py`.
* [ ] **Análise de Dados:** Gerar e coletar dados da simulação para análise com Pandas (KPIs de estoque, transporte, vendas).
* [ ] **Visualização:** Usar Matplotlib ou outras bibliotecas para visualizar dados (níveis de estoque, custos, etc.).
* [ ] **Testes Unitários:** Adicionar testes para garantir a corretude da lógica.

## 🙌 Contribuições

Contribuições são bem-vindas! Se você tiver sugestões, correções de bugs ou novas funcionalidades, sinta-se à vontade para abrir uma *Issue* ou enviar um *Pull Request*.

1.  Faça um *Fork* do projeto.
2.  Crie uma *Branch* para sua feature (`git checkout -b feature/MinhaNovaFeature`).
3.  Faça o *Commit* de suas alterações (`git commit -m 'Adiciona MinhaNovaFeature'`).
4.  Faça o *Push* para a Branch (`git push origin feature/MinhaNovaFeature`).
5.  Abra um *Pull Request*.

## 📄 Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo `LICENSE` (você precisará criar um) para mais detalhes.

*(Sugestão: Crie um arquivo chamado LICENSE e cole o texto padrão da Licença MIT nele. Você pode encontrar o texto facilmente online.)*

## 👤 Autor

* **[Felipe Sampaio]**
* **GitHub:** [https://github.com/oijiin](https://github.com/oijiin)
* **(Opcional) LinkedIn:** [(https://www.linkedin.com/in/felipe-sampaio-5868b5165/)]

---

*Este README foi gerado em: 30 de Abril de 2025.*
