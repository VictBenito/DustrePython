import functions, env, time, copy
from datetime import datetime

def ListarPedidosOmie(N=100):

    '''
    Função com o objetivo de Listar os N primeiros pedidos da conta Omie em ordem decrescente, ou seja,
    os pedidos mais recentes serão os primeiros da lista retornada.

    A função retorna um dicionário contendo os N pedidos ou -1, caso tenha falhado. Os pedidos em sí estão contidos na chave 'pedido_venda_produto',
    que é uma lista de tamanho N na qual cada elemento é um dos pedidos.
    '''

    # Parâmetros para requisição

    endpoint = "https://app.omie.com.br/api/v1/produtos/pedido/" 
    call = "ListarPedidos"
    param = [{
            "pagina":1,
            "registros_por_pagina":N,
            "apenas_importado_api":"N",
            "ordem_descrescente": "S" # Sim, a Omie colocou de"S"crescente por algum motivo
        }]

    # Tratamento de erros na requisição

    try:
        pedidos = functions.postOmie(endpoint,env.app_key_ES,env.app_secret_ES,call,param)

        if "Max retries exceeded" in pedidos:
            print("\n Possivel problema de conexão encontrado, aguardando e tentando novamente...")
            time.sleep(50)
            pedidos = functions.postOmie(endpoint,env.app_key_ES,env.app_secret_ES,call,param)
            if "Max retries exceeded" in pedidos:
                print("\n Listagem de pedidos Omie falhou! Verifique sua conexão com a internet")
                return -1
            elif 'Bad Data from Server' in pedidos or 'HTTP error occurred' in pedidos:
                print("\n Erro de requisição encontrado!")
            else:
                print("\n Sucesso! Pedidos Omie listados")
            
        elif 'Bad Data from Server' in pedidos or 'HTTP error occurred' in pedidos:
            print("\n Erro de requisição encontrado! Tentando novamente...")
            time.sleep(50)
            pedidos = functions.postOmie(endpoint,env.app_key_ES,env.app_secret_ES,call,param)
            if 'Bad Data from Server' in pedidos or 'HTTP error occurred' in pedidos:
                print("\n Listagem de pedidos Omie falhou!")
                return -1
            else:
                print("\n Sucesso! Pedidos Omie listados")
    except:
        print("\n Erro de requisição! Tentando novamente...")

        try:
            time.sleep(30)
            pedidos = functions.postOmie(endpoint,env.app_key_ES,env.app_secret_ES,call,param)
            
            if "Max retries exceeded" in pedidos:
                print("\n Possivel problema de conexão encontrado, aguardando e tentando novamente...")
                time.sleep(50)
                pedidos = functions.postOmie(endpoint,env.app_key_ES,env.app_secret_ES,call,param)
                if "Max retries exceeded" in pedidos:
                    print("\n Listagem de pedidos Omie falhou! Verifique sua conexão com a internet")
                    return -1
                else:
                    print("\n Sucesso! Pedidos Omie listados")
            elif 'Bad Data from Server' in pedidos or 'HTTP error occurred' in pedidos:
                print("\n Erro de requisição encontrado! Tentando novamente...")
                time.sleep(50)
                pedidos = functions.postOmie(endpoint,env.app_key_ES,env.app_secret_ES,call,param)
                if 'Bad Data from Server' in pedidos or 'HTTP error occurred' in pedidos:
                    print("\n Listagem de pedidos Omie falhou!")
                    return -1
                else:
                    print("\n Sucesso! Pedidos Omie listados")             
        except:
            print("\n Listagem de pedidos Omie falhou por problemas de requisição!")
            return -1

    # Tratamento de erros na resposta da Omie

    if 'faultstring' in pedidos:
        print("\n Requisição Omie precisa ser refeita, aguarde...")
        time.sleep(30)
        pedidos = functions.postOmie(endpoint,env.app_key_ES,env.app_secret_ES,call,param)
        if 'faultstring' not in pedidos:
            print("\n Sucesso! Pedidos Omie listados")
            return pedidos
        else:
            print("\n Tentativa final de requisição Omie, aguarde...")
            time.sleep(40)
            pedidos = functions.postOmie(endpoint,env.app_key_ES,env.app_secret_ES,call,param)
            if 'faultstring' not in pedidos:
                print("\n Sucesso! Pedidos Omie listados")
                return pedidos     
            else:
                print("\n Listagem de pedidos Omie falhou por erros na resposta da Omie!")
                return -1
    
    return pedidos

def ListarPedidosPloomes(N=50):

    ListarPedidosPloomes = "https://api2.ploomes.com/Orders?$orderby=OrderNumber+desc&$expand=OtherProperties&$top="+str(N)

    try:
        pedidosPloomes = functions.getPloomes(ListarPedidosPloomes,env.ploomes_api_key)['value']

    except:
        print("\n Erro na listagem de pedidos Ploomes, tentando novamente...")
        time.sleep(45)
        try:
            pedidosPloomes = functions.getPloomes(ListarPedidosPloomes,env.ploomes_api_key)['value']
            print("\n Sucesso! Pedidos Ploomes listados")
        except:
            print("\n Listagem de pedidos Ploomes falhou!")
            return -1

    return pedidosPloomes

def AlterarPedidoVendaOmie(req=dict):

    """
    Função que altera determinado pedido na Omie.
    Recebe como parâmetro "req", que deve ser um dicionário com as informações básicas requisitadas pela Omie.

    A função retorna um status obtido da Omie pela requisição HTTP feita.
    """

    # Parâmetros para requisição
    endpoint = "https://app.omie.com.br/api/v1/produtos/pedido/" 
    call = "AlterarPedidoVenda"

    param = [
        req
    ]

    alterado = functions.postOmie(endpoint,env.app_key_ES,env.app_secret_ES,call,param)

    return print("\n", alterado)

def MudarPedidoVendaOmie(ped, nOmie=100):
    '''
    Altera determinado pedido na Omie para utilização com a Ploomes.
    
    A função retorna um print do status obtido da Omie pela requisição HTTP feita.
    '''

    # Verificações básicas para garantir que o pedido pode ser alterado

    if 'id' not in ped:
        print("\n AVISO: Pedido não alterado, é necessário campo de integração!")
        return -1

    elif 'integracao' not in ped['id']:
        print("\n AVISO: Pedido não alterado, é necessário campo de integração!")
        return -1

    # Lista pedidos da Omie

    pedidosOmie = ListarPedidosOmie(nOmie)

    # Tratamento de erros na listagem Omie

    if pedidosOmie == -1:
        print("Erro nos pedidos Omie, tentando novamente...")
        time.sleep(30)
        pedidosOmie = ListarPedidosOmie(nOmie)
        if pedidosOmie == -1:
            print("ERRO: Não foi possível listar os pedidos Omie!")
            return -1

    # Encontrando o pedido específico

    pedido = -1

    for i in range(len(pedidosOmie['pedido_venda_produto'])):
        if pedidosOmie['pedido_venda_produto'][i]['cabecalho']['codigo_pedido'] == ped['id']['integracao']:
            pedido = pedidosOmie['pedido_venda_produto'][i]
            break

    # Tratamento de pedido não encontrado
    
    if pedido == -1:
        print("AVISO: Pedido não encontrado nos pedidos Omie. Você pode tentar aumentar o tamanho de pedidos Omie para encontrá-lo.")
        return -1

    # Retira partes do pedido que impedem a requisição caso não estejam preenchidas

    if 'numero_pedido' in pedido['cabecalho']:
        pedido['cabecalho'].pop('numero_pedido')
    if 'codigo_cenario_impostos' in pedido['cabecalho']:
        pedido['cabecalho'].pop('codigo_cenario_impostos')
    if 'codigo_transportadora' in pedido['frete']:
        pedido['frete'].pop('codigo_transportadora')
    if 'placa' in pedido['frete']:
        pedido['frete'].pop('placa')
    if 'placa_estado' in pedido['frete']:
        pedido['frete'].pop('placa_estado')
    if 'codigo_tipo_entrega' in pedido['frete']:        
        pedido['frete'].pop('codigo_tipo_entrega')
    if 'codProj' in pedido['informacoes_adicionais']:   
        pedido['informacoes_adicionais'].pop('codProj')

    pedido_original = copy.deepcopy(pedido) # Cópia para monitorar mudanças no pedido

    # Altera informações no pedido

    if 'obs' in ped:
        if ped['obs'] != '':
            pedido['informacoes_adicionais']['dados_adicionais_nf'] = ped['obs']
        else:
            print("\n AVISO: Dados adicionais nf não alterados!")
    else:
        print("\n AVISO: Dados adicionais nf não alterados!")

    if 'peso' in ped:
        pedido['frete']['peso_bruto'] = ped['peso']
        #pedido['frete']['peso_liquido'] = ped['peso']
    else:
        print("\n AVISO: Peso não mudado!")

    if 'espec' in ped:
        if ped['espec'] != []:
            for i in range(len(pedido['det'])):
                pedido['det'][i]['inf_adic']['dados_adicionais_item'] = ped['espec'][i]
                pedido['det'][i]['observacao']['obs_item'] = ped['espec'][i]
        else:
            print("\n AVISO: Dados adicionais item e obs item não alterados!")
    else:
        print("\n AVISO: Dados adicionais item e obs item não alterados!")

    # Verificação de mudanças no pedido para alteração

    if pedido != pedido_original:
        return AlterarPedidoVendaOmie(pedido) 
    else:
        print("AVISO: Pedido não alterado, informações para mudança não encontradas!")
        return -1

def MontaCampos(campo, obs, listafinal, listaindex, pedido):

    ItensPloomes = "https://api2.ploomes.com/Orders@Products?$expand=OtherProperties,ContactProduct($expand=OtherProperties),Currency&$filter=OrderId+eq+"

    if campo['FieldId'] == env.prazo_entrega_ploomes:
        obs['Prazo'] = "Prazo: "+campo['ObjectValueName']

    if campo['FieldId'] == env.previsao_faturamento_ploomes:
        previsao = datetime.strptime(campo['DateTimeValue'][:10], '%Y-%m-%d') 
        obs['Previsao'] = "Previsão: " + previsao.strftime("%d/%m/%Y")

    if campo['FieldId'] == env.tipo_do_frete_ploomes:
        obs['Frete'] = "Frete: " + campo['ObjectValueName']

    if campo['FieldId'] == env.peso_total_ploomes:
        listafinal[listaindex]['peso'] = campo['DecimalValue']

    if campo['FieldId'] == env.observacoes_ploomes:
        listafinal[listaindex]['obs'] = campo['BigStringValue']

    if campo['FieldId'] == env.campo_integracao:
        listafinal[listaindex]['espec'] = []
        listafinal[listaindex]['id'] = {'integracao':int(campo['StringValue']), 'idPloomes':[campo['OrderId'], pedido['OrderNumber']], 'numero_pedido_omie':''}
        ItensPloomes += str(campo['OrderId']) # criação da url para pegar os produtos do id específico
        try:
            itens = functions.getPloomes(ItensPloomes,env.ploomes_api_key)['value']
        except:
            print("\n Erro na requisição dos itens do pedido" + str(pedido['OrderNumber']) + "," + " tentando novamente...")
            time.sleep(30)
            try:
                itens = functions.getPloomes(ItensPloomes,env.ploomes_api_key)['value']
            except:
                print("\n ERRO: itens do pedido"+str(pedido['OrderNumber'])+" não encontrados.")
            
        for item in itens: # pega todas as descrições dos itens
            for k in range(len(item['OtherProperties'])):
                if item['OtherProperties'][k]['FieldId'] == 10204576:
                    stringitem = item['OtherProperties'][k]['BigStringValue']
                    if stringitem.startswith("<p>"):
                        stringitem = stringitem.strip("<p>")
                    elif stringitem.startswith("&lt;p&gt;"):
                        stringitem = stringitem.strip("&lt;p&gt;")
                    listafinal[listaindex]['espec'].append(stringitem)
        ItensPloomes = ItensPloomes[:len(ItensPloomes)-len(str(campo['OrderId']))] # reset da url para pegar produtos de id específico

    return obs, listafinal

def mapearPedidos(nPloomes = int, nOmie = int, mapearpedidosOmie = True):
    
    print("\n"+"Mapeando pedidos...")
    
    pedidosOmie = ListarPedidosOmie(nOmie)

    # Tratamento de erro na listagem de pedidos Omie

    if pedidosOmie == -1:
        print("\n Erro nos pedidos Omie, tentando novamente...")
        time.sleep(30)
        pedidosOmie = ListarPedidosOmie(nOmie)
        if pedidosOmie == -1:
            print("\n ERRO: Não foi possível listar os pedidos Omie!")
            return -1

    pedidosPloomes = ListarPedidosPloomes(nPloomes)

    # Tratamento de erro na listagem de pedidos Ploomes

    if pedidosPloomes == -1:
        print("\n Erro nos pedidos Ploomes, tentando novamente...")
        time.sleep(30)
        pedidosPloomes = ListarPedidosPloomes(nPloomes)
        if pedidosPloomes == -1:
            print("\n ERRO: Não foi possível listar os pedidos Ploomes!")
            return -1

    listafinal = []
    listaindex = 0

    # Construindo uma lista com dicionários para armazenar as infos importantes de cada pedido, no formato:
    #   [
    #       {
    #           'espec': [espec de cada item do pedido],
    #           'id':  {
    #                       'integracao': numero_integração (int),
    #                       'idPloomes': [Id Ploomes (int), OrderNumber (int)]
    #                       'numero_pedido_omie': 'numero_pedido Omie' (str)
    #                  },
    #           'obs': 'concat com as infos' (str) --> observações (str)
    #           'peso': peso total ploomes 
    #             
    #       },
    # ]

    for i in pedidosPloomes:
        listafinal.append({})
        obs = {'Prazo':'','Frete':'','Previsao':''}
        tentativa_integracao = 0

        for j in i['OtherProperties']:
            obs, listafinal = MontaCampos(j,obs,listafinal,listaindex,i)
            
            if j == i['OtherProperties'][len(i['OtherProperties'])-1] and 'espec' not in listafinal[listaindex] and tentativa_integracao < 1:
                print("\n Campo de integração não encontrado: Pedido "+str(i['OrderNumber'])+".","Tentando novamente...")
                time.sleep(35)
                obs, listafinal = MontaCampos(j,obs,listafinal,listaindex,i)
                if 'espec' in listafinal[listaindex]:
                    print("\n Campo de integração encontrado!")
                tentativa_integracao += 1
            
        if ('obs' not in listafinal[listaindex] and 'espec' in listafinal[listaindex]) and (obs['Frete'] != [''] or obs['Prazo'] != [''] or obs['Previsao'] != ['']):
            print("\n AVISO: Venda Ploomes sem campo de observações: "+str(listafinal[listaindex]['id']['idPloomes'][1])+", "+"montando observações a partir dos outros campos...")
            concatobs = obs['Prazo']+"|"+str(obs['Previsao'])+"|"+obs['Frete']
            listafinal[listaindex]['obs'] = concatobs
    
        if 'espec' in listafinal[listaindex]:
            if listafinal[listaindex]['espec'] == []:
                print("\n AVISO: Venda Ploomes sem descrição dos itens: "+str(listafinal[listaindex]['id']['idPloomes'][1]))
        
        listaindex += 1


    if mapearpedidosOmie:
        for i in pedidosOmie['pedido_venda_produto']:
            for j in range(listaindex):
                if 'id' in listafinal[j]:
                    if i['cabecalho']['codigo_pedido'] == listafinal[j]['id']['integracao']:
                        listafinal[j]['id']['numero_pedido_omie'] = i['cabecalho']['numero_pedido']

    print("\n"+"Pedidos mapeados!")

    return listafinal  

def main():

    inicial = mapearPedidos(3, 100)[0]

    if 'id' in inicial:
        if 'idPloomes' in inicial['id']:
            print("\n Último pedido:", inicial['id']['idPloomes'][1])
    else:
        print("\n Último pedido (sem integração):", inicial)
    
    while True:
        print("\n Programa rodando...")

        ultimopedido = mapearPedidos(3,100)[0]

        if 'id' in ultimopedido:
            if 'idPloomes' in ultimopedido['id']:
                print("\n Último pedido:", ultimopedido['id']['idPloomes'][1])
        else:
            print("\n Último pedido (sem integração):", ultimopedido)

        if ultimopedido != inicial and 'id' in ultimopedido:
            print("Novo pedido detectado! Fazendo alterações...")
            MudarPedidoVendaOmie(ultimopedido)
            inicial = copy.deepcopy(ultimopedido)

        time.sleep(20)
        
main()


