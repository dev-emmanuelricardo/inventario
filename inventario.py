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
fileComp = "/home/emmanuel/Documentos/faculdade/Gerencia_redes/inventario/comparacao.txt"
dataAtual = datetime.datetime.now()
dataBr =("Data:  %s/%s/%s" % (dataAtual.day, dataAtual.month, dataAtual.year) )
listaHosts = []
listaInventario = []
listaComparacao = ""
arq = ""

var = commands.getoutput("figlet Inventario UNIRN")
print var

def gravarVarreduraEmArquivo():
    if len(listaInventario) > 0:
        if(os.path.isfile(file)):
            arq = open(file, "a")
            lista = []
            arq.write("\n..:: RELATORIO DE HOSTS E CONFIGURAÇOES :::..\n")
            arq.write(dataBr+" \n\n\n")
            for valor in listaInventario:
                arq.write("* "+valor+"\n")
            arq.close();
        else:
            for valor in listaInventario:
                arq = open(file, "w")
                lista = []
                arq.write("\n..:: RELATORIO DE HOSTS E CONFIGURAÇOES :::..\n")
                arq.write(dataBr+" \n\n\n")
                for valor in listaInventario:
                    arq.write("* "+valor+"\n")
            arq.close();
        print "Relatório gerado..."
        return True
    else:
        print "Nao ha informaçoes para serem gravadas. Execute a varredura antes."
        return False

#def gravarComparacaoEmArquivo():


def mostrarListaHostsVarredura():
    tamanho = len(listaHosts)
    contador = 0
    if(tamanho > 0):
        print ("::: Lista de Hosts (%s):::" % tamanho) 
        for hostIP in listaHosts:
            contador = contador + 1
            print "("+str(contador)+") "+hostIP
    else:
        print "Não existem hosts na lista de varredura :::"


def mostrarMenu():
    print "MENU ::"
    print "(1) -> Adicionar host na lista de varredura"
    print "(2) -> Remover host da lista de varredura"
    print "(3) -> Ver lista de hosts para varredura"
    print "(4) -> Realizar varredura na rede"
    print "(5) -> Gravar informaçoes da varredura em disco"
    print "(6) -> Realizar verificaçao de versões de SO"
    print "(7) -> Gravar verificaçao de versões de SO em disco"
    print "(8) -> Sair"
    print
    
mostrarMenu()
op = raw_input("Escolha uma opçao: ")
print
while op != '8':
    
    if op == '1': # Adicionar host na lista de varredura
        ip_host = raw_input("Informe o IP do host: ")
        listaHosts.append(str(ip_host))
    elif op == '2': # Remover host da lista de varredura
        mostrarListaHostsVarredura()
        print
        indexEscolhido = raw_input("Digite o número do host que deseja apagar: ")
        listaHosts.pop(int(indexEscolhido)-1)

    elif op == '3': # Ver lista de hosts para varredura
        mostrarListaHostsVarredura()

    elif op == '4': # Realizar varredura na rede
        if(len(listaHosts) > 0):
            for host in listaHosts:
                print "::::::::::::::::::::::::"
                print "Host: "+host
                print dataBr
                print "::::::::::::::::::::::::"
                print       
                
                resultadoSys = netsnmp.snmpget(
                    'sysDescr.0',
                    Version = 2,
                    DestHost = host,
                    Community = "public"
                )
                
                #listaInventario.append("teste: "+str(resultadoSys)[2:-3])
                versao = str(resultadoSys).split(" ")[2].split("-")[0]
                listaComparacao = {host: versao}
                ##
                resultadoSys = netsnmp.snmpget(
                    'sysDescr.0',
                    Version = 2,
                    DestHost = host,
                    Community = "public"
                )
                
                listaInventario.append("sistema_operacional: "+str(resultadoSys)[2:-3])
                print "* Sistema Operacional: "+str(resultadoSys)[2:-3]
                ##
                resultadoProc = netsnmp.snmpget(
                    '.1.3.6.1.2.1.25.3.2.1.3.196608',
                    Version = 2,
                    DestHost = host,
                    Community = "public"
                )

                listaInventario.append("processador: "+str(resultadoProc).split(":")[1][:-3])
                print "* Processador: "+str(resultadoProc).split(":")[1][:-3]
                ##
                resultadoMem = netsnmp.snmpget(
                    'memTotalReal.0',
                    Version = 2,
                    DestHost = host,
                    Community = "public"
                )

                listaInventario.append("RAM_total: "+str(resultadoMem).split("'")[1]+" KB")
                print "* Memoria RAM (total): "+str(resultadoMem).split("'")[1]+" KB"
                ##
                resultadoMemDisp = netsnmp.snmpget(
                    'memAvailReal.0',
                    Version = 2,
                    DestHost = host,
                    Community = "public"
                )

                listaInventario.append("RAM_disponivel: "+str(resultadoMemDisp).split("'")[1]+" KB")
                print "* Memoria RAM (disponivel): "+str(resultadoMemDisp).split("'")[1]+" KB"
                ##
                resultadoDisk = netsnmp.snmpget(
                    'dskTotal.1',
                    Version = 2,
                    DestHost = host,
                    Community = "public"
                )

                print "* Disco Rigido (total): "+str(resultadoDisk)
                print "* Disco Rigido (disponivel): "+str(resultadoDisk)
                print ":::::::       :::::::"
        else:
            print "Não existem hosts na lista. Adicione pelo menos um host na lista"

    elif op == '5': # Gravar informaçoes da varredura em disco
        if not gravarVarreduraEmArquivo():
            continue

    elif op == '6': # Realizar verificaçao de versões de SO -- teste
        print ""

    elif op == '7': # Gravar verificaçao de versões de SO em disco
        print ""

    elif op == '8': # Adicionar host na lista de hosts
        print ""

    elif op == '9': # para teste
        for item in listaComparacao:
            print item+" - "+listaComparacao[item]
    print
    mostrarMenu()

    op = raw_input("Escolha uma opçao: ")
    print
