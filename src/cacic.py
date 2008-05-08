# -*- coding: UTF-8 -*-

import os
import sys
import time
import thread
from config.io import *
from socket import *
from ger_cols import *

class Cacic:
    
    VERSION = '1.0.0'
    
    def __init__(self):
        
        sys.path[0] = self.getDir()
        
        print "\n\tBem-Vindo ao PyCacic\n"
        try:
            if not self.isRoot():
                raise Exception("Para executar o programa é necessário estar como super usuário (root).")
            # flags do Gerente de Coletas
            self.gc_stopped = False
            self.gc_started = False
            self.gc_ok = False
            self.isforcada = False
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
                if not self.gc_started and (self.gc_ok or self.isforcada):
                    # muda estado para nao habilitado
                    self.gc_ok = False
                    # inicia coletas
                    self.gc.coleta_forcada = self.isforcada
                    thread.start_new_thread(self.start, ())                    
                # executa thread para escutar o socket
                thread.start_new_thread(self.checkSocket, ())
                time.sleep(2)
            # fechando conexao
            self.udp_sock.close()
        except Exception, e:
            print e 
            
    def getDir(self):
        av = sys.argv[0]
        if av[0] == "/":
            return os.path.dirname(av)
        else:
            return os.path.dirname(os.getcwd() + "/" + av)
    
    def isRoot(self):
        """Retorna se o usuario e root ou nao"""
        if os.getuid() != 0:
            return False
        return True

    def start(self):
        """Inicia as coletas"""
        try:
            self.gc_started = True            
            if self.isforcada:
                self.isforcada = False
                print '*** iniciando coleta forcada ***'
            print(" --- INICIO DAS COLETAS ---")
            print('\tColetas a serem feitas: \n\t%s' % ', '.join(self.gc.coletas))
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
        self.isforcada = (data == 'col_hard')
        time.sleep(1)


if __name__ == '__main__':
    Cacic()
    