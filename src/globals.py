# -*- coding: UTF-8 -*-

"""

    Modulo globals
    
    Modulo contendo variáveis globais do sistema
    
    @author: Dataprev - ES

"""

import os
import re
import sys
import commands


class Globals:
        
    VERSION = "1.0.0"
    PATH = ""
    INSTALLED = 0 # False
    PC_XML = ""
    
    def __init__(self):
        pass
    
    def getSocketAttr():
        """Retorna as informacoes do Socket"""
        from config.io import Reader
        sock = Reader.getSocket()
        host = sock['host']
        port = int(sock['port'])
        buf  = int(sock['buffer'])
        addr = (host, port)
        return host, port, buf, addr
    
    def install():
        """Abre console para configuracao do PyCacic"""
        from config.io import Writer
        print "\n\t--- Bem-Vindo a Configuracao do PyCacic ---"
        print "\n\tapos preencher as informacoes abaixo o programa ira iniciar\n"
        addr = raw_input("End. do  Servidor ('ex: http://10.0.0.1'): ")
        print "Testando conexao..."
        p = re.compile('[0-9]{1,3}(?:\.[0-9]{1,3}){3}')
        if len(p.findall(addr)) == 0:
            print "Endereco invalido"
            Globals.install()
            return 
        ip = p.findall(addr)[0]            
        if commands.getoutput('ping %s -c 1; echo $?' % ip)[-1:] != '0':
            print "Erro ao tentar conectar ao servidor"
            Globals.install()
            return
        user = raw_input("Usuario do Servidor: ")
        pwd = raw_input("Senha: ")
        if raw_input("\n\t*** Os dados estao corretos? [y|n]").lower() != 'y':
            Globals.install()
            return
        Writer.setPycacicStatus('installed', 1)
        if addr[len(addr)-1] == '/': addr = addr[:-1]
        Writer.setServer('address', addr)
        Writer.setServer('username', user)
        Writer.setServer('password', pwd)            
        print "\t--- Configuracao concluida com sucesso ---\n\n"
        
    getSocketAttr = staticmethod(getSocketAttr)
    install = staticmethod(install)
# fim classe

# staticos
def getDir():
    va = sys.argv[0]
    if va[0] == "/":
        return os.path.dirname(va)
    else:
        return os.path.dirname(os.getcwd()+"/"+va)
        
def getArgs():
    for arg in sys.argv:
        if arg[0:4] == "-xml":
            Globals.PC_XML = arg[5:]

def isInstalled():
    from config.io import Reader
    return (Reader.getPycacicStatus('installed')['value'] == 'yes')


    
Globals.PATH = getDir()
Globals.INSTALLED = isInstalled()

getArgs()