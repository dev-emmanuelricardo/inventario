#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importaçoes
import netsnmp
import os
import commands
import os.path
import datetime

# Variaveis de configuraçao
file = "/home/emmanuel/Documentos/faculdade/Gerencia_redes/inventario/relatorio.txt"
#fileComp = "/home/emmanuel/Documentos/faculdade/Gerencia_redes/inventario/comparacao.txt"
dataAtual = datetime.datetime.now()
dataBr =("Data:  %s/%s/%s" % (dataAtual.day, dataAtual.month, dataAtual.year) )
listaHosts = []
listaInventario = {}
sublistInventario = {}
listaComparacao = {}
arq = ""
maiorKernel = ""
maiorKernelHost = ""

var = commands.getoutput("figlet pyinfo Inventario")
print var

def gravarVarreduraEmArquivo():
    if len(listaInventario) > 0:
        if(os.path.isfile(file)):
            arq = open(file, "a")
            lista = []
            arq.write("\n..:: RELATORIO DE HOSTS E CONFIGURAÇOES :::..\n")
            arq.write(dataBr+" \n\n\n")
            for x in listaInventario:
                arq.write("::: "+x+" :::")
                arq.write("\n")
                for k, v in listaInventario[x].iteritems():
                    print arq.write(k+": "+v+"\n")
                arq.write("\n")
                arq.write("\n")
        else:
            arq = open(file, "w")
            arq.write("\n..:: RELATORIO DE HOSTS E CONFIGURAÇOES :::..\n")
            arq.write(dataBr+" \n\n\n")
            for x in listaInventario:
                arq.write("::: "+x+" :::")
                arq.write("\n")
                for k, v in listaInventario[x].iteritems():
                    print arq.write(k+": "+v+"\n")
                arq.write("\n")
                arq.write("\n")
        arq.close();
        print "Relatório gerado..."
    else:
        print "Nao ha informaçoes para serem gravadas. Execute a varredura antes."

def mostrarListaHostsVarredura():
    tamanho = len(listaHosts)
    contador = 0
    if(tamanho > 0):
        print ("::: Lista de Hosts (total de %s host(s) na lista):::" % tamanho) 
        for hostIP in listaHosts:
            contador = contador + 1
            print "("+str(contador)+") "+hostIP
    else:
        print "Não existem hosts na lista de varredura :::"
#
def mostrarMenu():
    """ Mostra o menu de opções do programa """

    print "MENU ::"
    print "(1) -> Adicionar host na lista de varredura"
    print "(2) -> Remover host da lista de varredura"
    print "(3) -> Ver lista de hosts para varredura"
    print "(4) -> Realizar varredura na rede"
    print "(5) -> Gravar informaçoes da varredura em disco"
    print "(6) -> Realizar verificaçao de versões de SO"
    print "(7) -> Sair"
    print

def realizarBusca(propriedade, host):
    resultadoSys = netsnmp.snmpget(
        propriedade,
        Version = 2,
        DestHost = host,
        Community = "public"
    )

    return resultadoSys
    
mostrarMenu()
op = raw_input("Escolha uma opçao: ")
print
while op != '7':
    
    if op == '1': # Adicionar host na lista de varredura
        ip_host = raw_input("Informe o IP do host: ")
        listaHosts.append(str(ip_host))
    elif op == '2': # Remover host da lista de varredura
        mostrarListaHostsVarredura()
        print
        indexEscolhido = raw_input("Digite o número do host que deseja apagar: ")
        try:
            listaHosts[int(indexEscolhido)-1]
            listaHosts.pop(int(indexEscolhido)-1)
        except IndexError:
            print
            print "Não existe host nessa posição."            

    elif op == '3': # Ver lista de hosts para varredura
        mostrarListaHostsVarredura()

    elif op == '4': # Realizar varredura na rede

        if(len(listaHosts) > 0):
            for host in listaHosts:
                sublistInventario = {}
                print
                print "::::::::::::::::::::::::"
                print "Host: "+host
                print dataBr
                print "::::::::::::::::::::::::"
                print       
                ##
                resultadoSys = realizarBusca("sysDescr.0", host)
                versao = str(resultadoSys)[2:-3].split(" ")[2].split("-")[0] # 2.16.3
                listaComparacao[host] = versao
                ##
                sublistInventario ["sistema_operacional"] = str(resultadoSys)[2:-3]
                listaInventario[host] = sublistInventario
                print "* Sistema Operacional: "+str(resultadoSys)[2:-3]
                ##
                resultadoProc = realizarBusca(".1.3.6.1.2.1.25.3.2.1.3.196608", host)
                stringProcessador = str(resultadoProc)
                if "None" in stringProcessador:
                    stringProcessador = "Nao Disponivel"
                    sublistInventario ["processador"] = "Nao disponivel"
                    listaInventario[host].update(sublistInventario)
                else:
                    stringProcessador = stringProcessador[2:-3]
                    sublistInventario ["processador"] = stringProcessador
                    listaInventario[host].update(sublistInventario)
                     
                print "* Processador: "+stringProcessador
                ##
                resultadoMem = realizarBusca("memTotalReal.0", host)
                sublistInventario ["RAM_total"] = str(resultadoMem).split("'")[1]+" KB"
                listaInventario[host].update(sublistInventario)
                print "* Memoria RAM (total): "+str(resultadoMem)[2:-3]+" KB"
                ##
                resultadoMemDisp = realizarBusca("memAvailReal.0", host)
                sublistInventario["RAM_disponivel"] = str(resultadoMemDisp).split("'")[1]+" KB"
                listaInventario[host].update(sublistInventario)
                print "* Memoria RAM (disponivel): "+str(resultadoMemDisp)[2:-3]+" KB"
                ##
                print ":::::::       :::::::"
                
        else:
            print "Não existem hosts na lista de varredura. Adicione pelo menos um host na lista"

    elif op == '5': # Gravar informaçoes da varredura em disco
        gravarVarreduraEmArquivo()
            
    elif op == '6': # Realizar verificação nas versões do kernel dos SO
        if(len(listaComparacao) > 0):
            v1 = "0.0.0"
            for item in listaComparacao:
                v2 = listaComparacao[item]

                v1list = v1.split('.')
                v2list = v2.split('.')

                for i in range(len(v1list)):
                    if v1list[i] < v2list[i]: 
                        maiorKernelHost = item
                        maiorKernel = listaComparacao[item]
                        v1 = maiorKernel
                        break
                    elif v2list[i] < v1list[i]:
                        maiorKernelHost = item
                        maiorKernel = listaComparacao[item]
                        v1 = maiorKernel
                        break
                    else:
                        continue
            print
            print ":::: RESULTADO DA COMPARAÇÃO ::::"
            print "Host com kernel do SO mais atual: "+maiorKernelHost
            print "Versão do kernel: "+maiorKernel
        else:
            print "Para realizar a comparação nas versões de SO você deve antes fazer uma varredura."

    elif op == '7': # Sair do programa
        print ""

    print
    mostrarMenu()

    op = raw_input("Escolha uma opçao: ")
    print
