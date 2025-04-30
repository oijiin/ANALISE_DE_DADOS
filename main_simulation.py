# -*- coding: utf-8 -*-

# main_simulation.py

import datetime
from decimal import Decimal

# Importar as classes principais e auxiliares dos módulos simuladores
from wms_simulator import ArmazemWMS, Item as WmsItem, Localizacao
from tms_simulator import TMS, Transportadora, Endereco, ItemTransporte
from erp_simulator import ERP, ProdutoERP, Cliente, Fornecedor, ItemPedido

# --- Funções Auxiliares de Configuração ---

def configurar_dados_mestre(erp: ERP, wms: ArmazemWMS, tms: TMS):
    """Configura produtos, parceiros, transportadoras e localizações."""
    print("\n--- CONFIGURANDO DADOS MESTRES ---")

    # 1. Endereços Comuns
    end_nosso_armazem = Endereco("Rua do Armazém Principal", "500", "São Paulo", "SP", "01000-000")
    end_cli_rj = Endereco("Avenida Atlântica", "1702", "Rio de Janeiro", "RJ", "22021-001")
    end_forn_guarulhos = Endereco("Rodovia Presidente Dutra", "km 220", "Guarulhos", "SP", "07170-000")

    # 2. Produtos (Adicionar no ERP e WMS com mesmo SKU)
    p1_sku = "SKU1001"
    p1_nome = "Componente Eletrônico Alpha"
    p1_erp = ProdutoERP(p1_sku, p1_nome, preco_venda=Decimal('150.00'), custo_medio=Decimal('50.00'))
    p1_wms = WmsItem(p1_sku, p1_nome, "Componente sensível")
    erp.adicionar_produto(p1_erp)
    wms.adicionar_item_catalogo(p1_wms)

    p2_sku = "SKU1002"
    p2_nome = "Gabinete Metálico Beta"
    p2_erp = ProdutoERP(p2_sku, p2_nome, preco_venda=Decimal('400.00'), custo_medio=Decimal('120.00'))
    p2_wms = WmsItem(p2_sku, p2_nome, "Gabinete padrão industrial")
    erp.adicionar_produto(p2_erp)
    wms.adicionar_item_catalogo(p2_wms)

    # 3. Clientes (ERP)
    cli1 = Cliente("CLI001", "Indústria Tech RJ", "11.222.333/0001-55", end_cli_rj, limite_credito=Decimal('20000.00'))
    erp.adicionar_cliente(cli1)

    # 4. Fornecedores (ERP)
    forn1 = Fornecedor("FORN001", "Metalúrgica Delta", "55.666.777/0001-99", end_forn_guarulhos, prazo_entrega_medio_dias=5)
    erp.adicionar_fornecedor(forn1)

    # 5. Transportadoras (TMS)
    t1 = Transportadora("T001", "Transportes Ágil", taxa_base_km_kg=0.11)
    t2 = Transportadora("T002", "LogExpress Brasil", taxa_base_km_kg=0.10)
    tms.adicionar_transportadora(t1)
    tms.adicionar_transportadora(t2)

    # 6. Localizações (WMS) - Essenciais para o fluxo
    loc_recv = Localizacao("RECEBIMENTO")
    loc_a1 = Localizacao("CORREDOR_A-01-N1") # Local de estoque SKU1001
    loc_b1 = Localizacao("CORREDOR_B-01-N1") # Local de estoque SKU1002
    loc_pick = Localizacao("AREA_PICKING")
    loc_exp = Localizacao("AREA_EXPEDICAO")
    wms.adicionar_localizacao(loc_recv)
    wms.adicionar_localizacao(loc_a1)
    wms.adicionar_localizacao(loc_b1)
    wms.adicionar_localizacao(loc_pick)
    wms.adicionar_localizacao(loc_exp)

    # 7. (Opcional) Adicionar distância simulada no TMS para os endereços
    tms.distancias_simuladas[(end_nosso_armazem.cidade, end_cli_rj.cidade)] = 450
    tms.distancias_simuladas[(end_cli_rj.cidade, end_nosso_armazem.cidade)] = 450 # Rota inversa

    print("--- DADOS MESTRES CONFIGURADOS ---")
    return end_nosso_armazem # Retorna endereço do armazém para uso posterior


def simular_entrada_estoque_inicial(erp: ERP, wms: ArmazemWMS, id_oc: str, id_fornecedor: str, itens_compra: list[tuple[str, int, Decimal]], end_armazem: Endereco):
    """Simula a compra e recebimento de estoque inicial."""
    print(f"\n--- SIMULANDO ENTRADA ESTOQUE INICIAL (OC: {id_oc}) ---")

    # 1. Criar Ordem de Compra no ERP
    oc = erp.criar_ordem_compra(id_oc, id_fornecedor, itens_compra)
    if not oc:
        print(f"ERRO CRÍTICO: Falha ao criar OC {id_oc}. Abortando simulação de estoque.")
        return False
    # ERP já atualiza status para RECEBIMENTO_PENDENTE

    # 2. Simular Recebimento Físico no WMS (item por item)
    print(f"\n--- WMS: Simulando recebimento físico da OC {id_oc} ---")
    sucesso_recebimento_wms = True
    for sku, qtd, custo in itens_compra:
        # WMS recebe na área de recebimento
        if not wms.receber_mercadoria(sku, qtd, "RECEBIMENTO"):
            print(f"ERRO WMS: Falha ao receber {qtd}x {sku} na área de recebimento.")
            sucesso_recebimento_wms = False
            continue # Tenta receber outros itens

        # WMS guarda no local de estoque definido
        # (Simplificação: determinamos o local aqui; um WMS real teria regras)
        local_destino_sku = "CORREDOR_A-01-N1" if sku == "SKU1001" else "CORREDOR_B-01-N1"
        if not wms.guardar_mercadoria(sku, qtd, "RECEBIMENTO", local_destino_sku):
             print(f"ERRO WMS: Falha ao guardar {qtd}x {sku} em {local_destino_sku}.")
             sucesso_recebimento_wms = False

    if not sucesso_recebimento_wms:
         print(f"AVISO: Houve falhas no recebimento/guarda física no WMS para OC {id_oc}.")
         # Continuar mesmo assim para fins de simulação, mas marcar o problema

    # 3. Informar o ERP sobre o Recebimento (item por item)
    print(f"\n--- WMS -> ERP: Confirmando recebimento da OC {id_oc} ---")
    for sku, qtd, custo in itens_compra:
         # O ERP usa o custo da OC para registrar financeiro, WMS confirma apenas qtd
         # Passamos o custo aqui para que o ERP possa recalcular custo médio corretamente
         erp.receber_confirmacao_recebimento_wms(id_oc, sku, qtd, novo_custo_medio=custo)

    print(f"--- ENTRADA ESTOQUE INICIAL (OC: {id_oc}) CONCLUÍDA ---")
    erp.consultar_oc(id_oc)
    erp.exibir_estoque_geral()
    wms.inventario_geral()
    return True

# --- Script Principal da Simulação ---

if __name__ == "__main__":
    print("=============================================")
    print("=== INICIANDO SIMULAÇÃO INTEGRADA WMS-TMS-ERP ===")
    print("=============================================")

    # 1. Instanciar os Sistemas
    erp_main = ERP("Empresa Simulada Principal")
    wms_main = ArmazemWMS("Armazém Central SP")
    tms_main = TMS()
    print("\n[Sistemas ERP, WMS, TMS instanciados]")

    # 2. Configurar Dados Mestres e Obter Endereço do Armazém
    endereco_armazem = configurar_dados_mestre(erp_main, wms_main, tms_main)

    # 3. Simular Estoque Inicial via Compra/Recebimento
    itens_compra_inicial = [
        ("SKU1001", 100, Decimal('50.00')), # Comprando 100 unidades a R$ 50.00
        ("SKU1002", 50, Decimal('120.00')) # Comprando 50 unidades a R$ 120.00
    ]
    simular_entrada_estoque_inicial(erp_main, wms_main, "OC0001", "FORN001", itens_compra_inicial, endereco_armazem)

    print("\n=============================================")
    print("=== INICIANDO FLUXO DE VENDA (ORDER-TO-CASH) ===")
    print("=============================================")

    # 4. Criar Ordem de Venda no ERP
    id_cliente_venda = "CLI001"
    id_ov_venda = "OV2001"
    itens_venda = [
        ("SKU1001", 10), # Vender 10 unidades do SKU1001
        ("SKU1002", 5)   # Vender 5 unidades do SKU1002
    ]
    print(f"\n--- ERP: Criando Ordem de Venda {id_ov_venda} para Cliente {id_cliente_venda} ---")
    ov = erp_main.criar_ordem_venda(id_ov_venda, id_cliente_venda, itens_venda)

    if not ov:
        print(f"ERRO CRÍTICO: Falha ao criar OV {id_ov_venda}. Abortando fluxo de venda.")
        exit() # Termina a simulação se a OV falhar

    erp_main.consultar_ov(id_ov_venda)
    # ERP já tentou liberar para WMS (status deve ser LIBERADA_WMS)

    # 5. Simular Processo de Picking no WMS (disparado pela OV liberada)
    print(f"\n--- WMS: Iniciando separação para OV {id_ov_venda} ---")
    sucesso_picking_wms = True
    itens_separados_info = [] # Guardar o que foi realmente separado
    if ov.status == ov.STATUS_LIBERADA_WMS:
        for item_pedido in ov.itens:
            sku = item_pedido.produto.sku
            qtd = item_pedido.quantidade
            # WMS precisa encontrar de onde pegar (simplificação: usamos o local conhecido)
            local_origem_sku = "CORREDOR_A-01-N1" if sku == "SKU1001" else "CORREDOR_B-01-N1"
            # WMS faz o picking para a área de picking
            if wms_main.fazer_picking(sku, qtd, local_origem_sku, "AREA_PICKING"):
                itens_separados_info.append((sku, qtd))
            else:
                print(f"ERRO WMS: Falha no picking de {qtd}x {sku} para OV {id_ov_venda}.")
                sucesso_picking_wms = False
                # O que fazer em caso de falha no picking? Cancelar OV? Backorder?
                # Simulação: Apenas registrar a falha e continuar informando o ERP

        # (Opcional) Simular movimentação da área de picking para expedição
        if sucesso_picking_wms:
             print(f"\n--- WMS: Movendo itens separados para Área de Expedição ---")
             for sku, qtd in itens_separados_info:
                 # Mover da área de picking para expedição antes de informar o ERP
                 wms_main.guardar_mercadoria(sku, qtd, "AREA_PICKING", "AREA_EXPEDICAO")

    else:
        print(f"ERRO: OV {id_ov_venda} não está no status correto ({ov.STATUS_LIBERADA_WMS}) para iniciar separação no WMS.")
        sucesso_picking_wms = False

    # 6. Informar ERP sobre a conclusão (ou falha) da separação
    print(f"\n--- WMS -> ERP: Confirmando resultado da separação da OV {id_ov_venda} ---")
    if sucesso_picking_wms and itens_separados_info:
        erp_main.receber_confirmacao_separacao_wms(id_ov_venda, itens_separados_info)
    else:
        # Informar ERP sobre a falha (ERP poderia cancelar ou tratar)
        ov.atualizar_status("ERRO_SEPARACAO", f"Falha na separação WMS para OV {id_ov_venda}.")
        print(f"ERRO CRÍTICO: Falha na separação WMS para OV {id_ov_venda}. Abortando fluxo.")
        exit()

    erp_main.consultar_ov(id_ov_venda)
    # ERP já tentou solicitar transporte (status deve ser ENVIADA, com id_carga simulado)

    # 7. Simular Criação e Planejamento da Carga no TMS (disparado pelo ERP)
    print(f"\n--- TMS: Criando e planejando transporte para OV {id_ov_venda} (Carga: {ov.id_carga_tms}) ---")
    id_carga_real_tms = ov.id_carga_tms # Usar o ID que o ERP simulou
    cliente_ov = erp_main.get_cliente(ov.cliente.id_parceiro)
    endereco_destino_tms = cliente_ov.endereco

    itens_carga_tms = []
    for item_erp in ov.itens:
        # Buscar peso/volume (simulado aqui, idealmente viria do ProdutoERP ou WMS)
        peso_unit = 0.5 if item_erp.produto.sku == "SKU1001" else 3.0 # kg
        vol_unit = 0.001 if item_erp.produto.sku == "SKU1001" else 0.05 # m³
        item_t = ItemTransporte(item_erp.produto.sku, item_erp.quantidade, peso_unit, vol_unit)
        itens_carga_tms.append(item_t)

    carga_tms = tms_main.criar_carga(id_carga_real_tms, endereco_armazem, endereco_destino_tms, itens_carga_tms)

    custo_frete_final = Decimal('0.00')
    if carga_tms:
        if tms_main.planejar_transporte(id_carga_real_tms):
            carga_planejada = tms_main.cargas[id_carga_real_tms]
            custo_frete_final = Decimal(str(carga_planejada.custo_frete_estimado)) # Converter float para Decimal
            print(f"--- TMS: Transporte planejado para {id_carga_real_tms}. Custo: R$ {custo_frete_final:.2f} ---")
        else:
            print(f"ERRO TMS: Falha ao planejar transporte para {id_carga_real_tms}.")
            # Tratar erro - talvez tentar outra transportadora?
    else:
        print(f"ERRO TMS: Falha ao criar a carga {id_carga_real_tms}.")
        # Tratar erro

    # 8. Informar ERP sobre o Custo do Frete (se aplicável)
    if custo_frete_final > 0:
        print(f"\n--- TMS -> ERP: Informando custo do frete (R$ {custo_frete_final:.2f}) para carga {id_carga_real_tms} ---")
        erp_main.registrar_custo_frete_tms(id_carga_real_tms, custo_frete_final)

    # 9. Simular Despacho e Entrega no TMS
    print(f"\n--- TMS: Simulando despacho e entrega da carga {id_carga_real_tms} ---")
    if carga_tms and carga_tms.status == carga_tms.STATUS_PLANEJADA:
        tms_main.despachar_carga(id_carga_real_tms)
        # Simular passagem do tempo...
        print("...carga em trânsito...")
        data_entrega_simulada = datetime.datetime.now() + datetime.timedelta(days=3)
        tms_main.registrar_entrega(id_carga_real_tms)
    else:
        print(f"AVISO TMS: Carga {id_carga_real_tms} não pôde ser despachada/entregue (Status: {carga_tms.status if carga_tms else 'Não criada'}).")

    tms_main.consultar_carga(id_carga_real_tms)

    # 10. Informar ERP sobre a Entrega
    print(f"\n--- TMS -> ERP: Confirmando entrega da carga {id_carga_real_tms} ---")
    if carga_tms and carga_tms.status == carga_tms.STATUS_ENTREGUE:
        erp_main.recer_confirmacao_entrega_tms(id_carga_real_tms, data_entrega_simulada)
    else:
         print(f"AVISO: Entrega da carga {id_carga_real_tms} não confirmada no TMS. ERP não será atualizado para entrega.")

    # 11. Verificação Final
    print("\n=============================================")
    print("========= VERIFICAÇÃO FINAL DO ESTADO =========")
    print("=============================================")
    erp_main.consultar_ov(id_ov_venda)
    erp_main.exibir_estoque_geral()
    wms_main.inventario_geral() # Verificar se estoque físico diminuiu
    erp_main.exibir_log_financeiro() # Verificar lançamentos de venda, cmv, frete

    print("\n=============================================")
    print("========= SIMULAÇÃO INTEGRADA CONCLUÍDA ========")
    print("=============================================")
