# -*- coding: UTF-8 -*-

import os
import sys
import time
import thread
from config.io import *
from socket import *
from ger_cols import *
from config.io import Writer
from globals import Globals

class Cacic:
    
    VERSION = '1.0.0'
    
    def __init__(self):       
        #try:            
            if not Globals.INSTALLED:
                self.install()

            if not self.isRoot():
                raise Exception("Para executar o programa é necessário estar como super usuário (root).")
            
            print "\n\tBem-Vindo ao PyCacic\n"
            # flags do Gerente de Coletas
            self.gc_stopped = False
            self.gc_started = False
            self.gc_ok = False
            self.isforcada = []
            # Gerente de Coletas
            self.gc = Ger_Cols(self.VERSION)
            # configuracao do socket para comunicacao interna
            sock = Reader.getSocket()
            self.host = sock['host']
            self.port = int(sock['port'])
            self.buf  = int(sock['buffer'])
            self.addr = (self.host, self.port)
            # criando socket
            self.udp_sock = socket.socket(AF_INET, SOCK_DGRAM)
            self.udp_sock.bind(self.addr)
            while True:
                # verifica se o coletor nao esta parado
                if not self.gc_stopped:
                    # muda estado do coletor para parado
                    self.gc_stopped = True
                    # conecta ao servidor para pegar as informacoes
                    xml = self.gc.conecta(self.gc.cacic_url, self.gc.dicionario)
                    print(" Contato com o Gerente Web: %s" % strftime("%H:%M:%S"))
                    self.gc.readXML(xml)
                    # com o coletor parado (dormindo) dispara timeout para iniciar a coleta
                    # apos o intervalo de tempo definido pelo servidor 
                    thread.start_new_thread(self.timeout, ())
                    # intervalo
                    self.interval = self.gc.getInterval()
                    print(" `---- Coleta iniciara daqui a %s minutos" % (self.interval/60))
                    #self.atualiza()
                # se nao estiver executando e esta habilitado a executar
                # ou e uma coleta forcada
                if not self.gc_started and (self.gc_ok or len(self.isforcada) > 0):
                    # muda estado para nao habilitado
                    self.gc_ok = False
                    # inicia coletas
                    self.gc.coletas_forcadas = self.isforcada
                    thread.start_new_thread(self.start, ())
                # executa thread para escutar o socket
                thread.start_new_thread(self.checkSocket, ())
                time.sleep(2)
            # fechando conexao
            self.udp_sock.close()
        #except Exception, e:
        #    print e 
    
    def isRoot(self):
        """Retorna se o usuario e root ou nao"""
        if os.getuid() != 0:
            return False
        return True
    
    def install(self):
        """Abre console para configuracao do PyCacic"""
        print "\n\t--- Bem-Vindo a Configuracao do PyCacic ---"
        print "\n\tapos preencher as informacoes abaixo o programa ira iniciar\n"
        addr = raw_input("End. do  Servidor ('ex: http://10.0.0.1'): ")
        user = raw_input("Usuario do Servidor: ")
        pwd = raw_input("Senha: ")
        if raw_input("\n\t*** Os dados estao corretos? [y|n]").lower() != 'y':
            self.install()
        else:
            Writer.setStatus('installed', True)
            if addr[len(addr)-1] == '/': addr = addr[:-1]
            Writer.setServer('address', addr)
            Writer.setServer('username', user)
            Writer.setServer('password', pwd)
        print "\t--- Configuracao concluida com sucesso ---\n\n"

    def start(self):
        """Inicia as coletas"""
        try:
            self.gc_started = True            
            self.isforcada = []
            print(" --- INICIO DAS COLETAS ---")
            print 'Total Coletas: %s' % len(self.gc.coletores)
            print('\tColetas a serem feitas: \n\t(%s)' % ', '.join(self.gc.coletores.keys()))
            self.gc.startColeta()
            self.gc.createDat()
            self.gc.sendColetas()
            self.gc_started = False
            print(" --- FIM DAS COLETAS ---")
        except Exception, e:
            print e

    def timeout(self):
        """
            Espera determinado intervalo de tempo. E apos isto marca o estado
            do Gerente de Coletas como nao parado e habilita execucao das coletas
        """
        print '---- esperando intervalo'        
        time.sleep(self.interval)
        print '---- timeout !!!'
        self.gc_stopped = False
        self.gc_ok = True

    def checkSocket(self):
        """Verifica comunicacao com a interface"""
        data, self.addr = self.udp_sock.recvfrom(self.buf)
        self.isforcada.append(data)
        time.sleep(1)


if __name__ == '__main__':
    ver =  sys.version_info
    version = int(''.join([ '%s' %sys.version_info[x] for x in range(3)]))
    if version < 240:
        print "ERROR: Python 2.4 or greater required"
        sys.exit(1)
    Cacic()
