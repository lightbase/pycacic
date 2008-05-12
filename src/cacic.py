# -*- coding: UTF-8 -*-

import os
import sys
import time
import thread
from socket import *
from ger_cols import *
from globals import Globals

class Cacic:
    
    VERSION = '1.0.0'
    
    def __init__(self):       
        try:
            
            sys.path[0] = Globals.PATH
            
            if not Globals.INSTALLED:
                Globals.install()
            
            if not self.isRoot():
                raise Exception("Para executar o programa é necessário estar como super usuário (root).")
            
            print "\n\tBem-Vindo ao PyCacic\n"
            # flags do Gerente de Coletas
            self.gc_stopped = 0 # False
            self.gc_started = 0 # False
            self.gc_ok = 0 # False
            self.isforcada = []
            # Gerente de Coletas
            self.gc = Ger_Cols(self.VERSION)
            # configuracao do socket para comunicacao interna
            self.host, self.port, self.buf, self.addr = Globals.getSocketAttr()
            # criando socket
            self.udp_sock = socket.socket(AF_INET, SOCK_DGRAM)
            self.udp_sock.bind(self.addr)
            while 1:
                # verifica se o coletor nao esta parado
                if not self.gc_stopped:
                    # muda estado do coletor para parado
                    self.gc_stopped = 1 # True
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
                    self.gc_ok = 0 # False
                    # inicia coletas
                    self.gc.coletas_forcadas = self.isforcada
                    thread.start_new_thread(self.start, ())
                # executa thread para escutar o socket
                thread.start_new_thread(self.checkSocket, ())
                time.sleep(2)
            # fechando conexao
            self.udp_sock.close()
        except Exception, e:
            import traceback
            traceback.print_exc()
            print e

    
    def isRoot(self):
        """Retorna se o usuario e root ou nao"""
        if os.getuid() != 0:
            return 0 # False
        return 1 # True
    

    def start(self):
        """Inicia as coletas"""
        try:
            self.gc_started = 1 # True            
            self.isforcada = []
            print(" --- INICIO DAS COLETAS ---")
            print 'Total Coletas: %s' % len(self.gc.coletores)
            print('\tColetas a serem feitas: \n\t(%s)' % ', '.join(self.gc.coletores.keys()))
            self.gc.startColeta()
            self.gc.createDat()
            self.gc.sendColetas()
            self.gc_started = 0 # False
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
        self.gc_stopped = 0 # False
        self.gc_ok = 1 # True

    def checkSocket(self):
        """Verifica comunicacao com a interface"""
        data, self.addr = self.udp_sock.recvfrom(self.buf)
        self.isforcada.append(data)


if __name__ == '__main__':
    ver =  sys.version_info
    version = int(''.join([ '%s' %sys.version_info[x] for x in range(3)]))
    if version < 230:
        print "ERROR: Python 2.3 or greater required"
        sys.exit(1)
    Cacic()
