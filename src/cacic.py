# -*- coding: UTF-8 -*-

import os
import sys
import time
import thread

from socket import *
from ger_cols import *
from globals import Globals

import gc as garbage_collector

class Cacic:
    
    VERSION = '0.0.1'
    
    def __init__(self):       
        try:
            # somente executa se estiver como root
            if not self.isRoot():
                raise Exception("Para executar o programa é necessário ser super-usuário (root).")
            
            # Habilita o coletor de lixo do Python
            garbage_collector.enable()                        
            print "\n\tBem-Vindo ao PyCacic\n"
            # flags do Gerente de Coletas
            self.gc_stopped = 0 # False
            self.gc_ok = 0 # False
            self.isforcada = []
            # Gerente de Coletas
            self.gc = Ger_Cols(self.VERSION)
            # configuracao do socket para comunicacao interna
            self.host, self.port, self.buf, self.addr = Globals.getSocketAttr()
            # criando socket
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind(self.addr)
            # executa thread para escutar o socket
            thread.start_new_thread(self.checkSocket, ())
            while 1:
                # verifica se o coletor nao esta parado
                if not self.gc_stopped:
                    # muda estado do coletor para parado
                    self.gc_stopped = 1 # True
                    # conecta ao servidor para pegar as informacoes
                    self.conecta()
                    # com o coletor parado (dormindo) dispara timeout para iniciar a coleta
                    # apos o intervalo de tempo definido pelo servidor
                    thread.start_new_thread(self.timeout, ())
                    # intervalo
                    self.interval = self.gc.getInterval()
                    print(" `---- Coleta iniciara em %s minutos" % (self.interval/60))
                # se esta habilitado a executar ou e uma coleta forcada
                if self.gc_ok or len(self.isforcada) > 0:
                    # muda estado para nao habilitado
                    self.gc_ok = 0 # False
                    # conecta ao servidor para pegar as informacoes
                    # pode ter ocorrido alguma mudanca desde a ultima
                    self.conecta()
                    # inicia coletas
                    self.gc.coletas_forcadas = self.isforcada
                    self.start()                    
                    # Executa o coletor de lixo
                    garbage_collector.collect()
                time.sleep(2)
            # sai
            self.quit()
        except socket.error, e:   
            print 'PyCacic already is running.'
        except Exception, e:
            print e        
        # remover depois
        import traceback
        traceback.print_exc()
    
    def isRoot(self):
        """Retorna se o usuario e root ou nao"""
        if os.getuid() != 0:
            return 0 # False
        return 1 # True

    def start(self):
        """Inicia as coletas"""
        self.isforcada = []
        print(" --- INICIO DAS COLETAS ---")
        print 'Total Coletas: %s' % len(self.gc.coletores)
        print('\tColetas a serem feitas: \n\t(%s)' % ', '.join(self.gc.coletores.keys()))
        self.gc.startColeta()
        self.gc.createDat()
        self.gc.sendColetas()
        print(" --- FIM DAS COLETAS ---")

    def timeout(self):
        """
            Espera determinado intervalo de tempo. E apos isto marca o estado
            do Gerente de Coletas como nao parado e habilita execucao das coletas
        """       
        time.sleep(self.interval)
        self.gc_stopped = 0 # False
        self.gc_ok = 1 # True
        
    def conecta(self):
        """Conecta ao Gerente Web para pegar informacoes de configuracao"""
        xml = self.gc.conecta(self.gc.cacic_url, self.gc.dicionario)
        print(" Contato com o Gerente Web: %s" % strftime("%H:%M:%S"))
        self.gc.readXML(xml)
        """
        # verifica atualizacao
        if self.gc.hasNew():
            print ' Versao nova disponivel !!!'
            print ' `--- Iniciando atualizacao...'
            self.gc.atualiza()
            print ' `--- Novo pacote salvo'
            #chama atualizador e sai
            os.system('python %s/update.py -pkg %s -hash %s -tmp %s &' % (Globals.PATH, self.gc.pacote_disponivel, self.gc.hash_disponivel, 'pycacic_temp'))
            self.quit()
        """

    def checkSocket(self):
        """Verifica comunicacao com a interface"""
        while 1:
            data, self.addr = self.sock.recvfrom(self.buf)
            self.isforcada.append(data)

    def quit(self):
        """Sai do programa fechando conexao do socket"""
        self.sock.close()
        sys.exit()

if __name__ == '__main__':
    ver =  sys.version_info
    version = int(''.join([ '%s' %sys.version_info[x] for x in range(3)]))
    if version < 230:
        print "ERROR: Python 2.3 or greater required"
        sys.exit(1)
    Cacic()
