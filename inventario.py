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
dataAtual = datetime.datetime.now()
dataBr =("Data:  %s/%s/%s" % (dataAtual.day, dataAtual.month, dataAtual.year) )
listaHosts = ['127.0.0.1']
listaInventario = []
arq = ""

var = commands.getoutput("figlet Inventario UNIRN")
print var

def gravarEmArquivo():
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
        return True
    else:
        print "Nao ha informaçoes para serem gravadas. Execute a varredura antes."
        return False

def mostrarMenu():
    print "MENU ::"
    print "(1) -> Realizar varredura na rede"
    print "(2) -> Gravar informaçoes da varredura em disco"
    print "(3) -> Sair"
    print
    
mostrarMenu()
op = raw_input("Escolha uma opçao: ")
print
while op != '3':
    for host in listaHosts:
        if op == '1':
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
        elif op == '2':
            if not gravarEmArquivo():
                continue
        elif op == '3':
            buffer
    print
    mostrarMenu()

    op = raw_input("Escolha uma opçao: ")
    print
