#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importaçoes
import netsnmp
import os
import commands
import os.path
import datetime

# Variaveis de configuraçao
host = 'localhost'
file = "/home/emmanuel/Documentos/faculdade/Gerencia_redes/inventario/relatorio.txt"
dataAtual = datetime.datetime.now()

var = commands.getoutput("figlet Inventario UNIRN")
print var

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

    print "::::::::::::::::::::::::"
    print "Host: "+host
    print ("Data:  %s/%s/%s" % (dataAtual.day, dataAtual.month, dataAtual.year) )
    print "::::::::::::::::::::::::"
   
    if op == '1':
        resultadoSys = netsnmp.snmpget(
            'sysDescr.0',
            Version = 2,
            DestHost = host,
            Community = "public"
        )

        print "* Sistema Operacional: "+str(resultadoSys)[2:-3]
        
        resultadoProc = netsnmp.snmpget(
            '.1.3.6.1.2.1.25.3.2.1.3.196608',
            Version = 2,
            DestHost = host,
            Community = "public"
        )

        print "* Processador: "+str(resultadoProc).split(":")[1][:-3]
        
        resultadoMem = netsnmp.snmpget(
            'memTotalReal.0',
            Version = 2,
            DestHost = host,
            Community = "public"
        )

        print "* Memoria RAM (total): "+str(resultadoMem).split("'")[1]+" KB"

        resultadoMemDisp = netsnmp.snmpget(
            'memAvailReal.0',
            Version = 2,
            DestHost = host,
            Community = "public"
        )

        print "* Memoria RAM (disponivel): "+str(resultadoMemDisp).split("'")[1]+" KB"

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
        arq = ""
        if(os.path.isfile(file)):
            arq = open(file, "a")
            lista = []
            lista.append("Adicionado pelo script novamente\n")
            lista.append("Mais umalinha\n")
            arq.writelines(lista)
            arq.close();
        else:
            arq = open(file, "w")
            lista = []
            lista.append("Mais uma coisinha\n")
            lista.append("Outra coisinha\n")
            arq.writelines(lista)
            arq.close();

    elif op == '3':
        break
    print
    mostrarMenu()

    op = raw_input("Escolha uma opçao: ")
