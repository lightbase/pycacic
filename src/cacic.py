#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
    Copyright 2000, 2001, 2002, 2003, 2004, 2005 Dataprev - Empresa de Tecnologia e Informações da Previdência Social, Brasil
    
    Este arquivo é parte do programa CACIC - Configurador Automático e Coletor de Informações Computacionais
    
    O CACIC é um software livre; você pode redistribui-lo e/ou modifica-lo dentro dos termos da Licença Pública Geral GNU como 
    publicada pela Fundação do Software Livre (FSF); na versão 2 da Licença, ou (na sua opnião) qualquer versão.
    
    Este programa é distribuido na esperança que possa ser  util, mas SEM NENHUMA GARANTIA; sem uma garantia implicita de ADEQUAÇÂO a qualquer
    MERCADO ou APLICAÇÃO EM PARTICULAR. Veja a Licença Pública Geral GNU para maiores detalhes.
    
    Você deve ter recebido uma cópia da Licença Pública Geral GNU, sob o título "LICENCA.txt", junto com este programa, se não, escreva para a Fundação do Software
    Livre(FSF) Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""

import os
import sys
import time
import thread

from socket import *
from ger_cols import *

from globals import Globals
from lang.language import Language
from logs.log import CLog

import gc as garbage_collector

# Languages
_l = Language()

class Cacic:
    
    # seconds to sleep (socket errors)
    SLEEP_TIME = 600
    VERSION = Reader.getPycacic()['version']
    
    def __init__(self):
        try:            
            CLog.appendLine(_l.get('pycacic'), _l.get('program_started'))
            print _l.get('welcome')
            self.running = 0
            # abre conexao por socket
            self.setSocket()
            # flags do Gerente de Coletas
            self.gc_stopped = 0 # False
            self.gc_ok = 0 # False
            self.coletas_forcadas = []
            # Gerente de Coletas
            self.gc = Ger_Cols(self.VERSION)
                       
        except socket.error:
            CLog.appendLine(_l.get('pycacic'), '%s %s %s' % (_l.get('sleeping'), self.SLEEP_TIME, _l.get('seconds')))             
            time.sleep(SLEEP_TIME)
            
        except:
            print 'Erro ao instanciar Cacic()'
            self.quit()
    
    def run(self):
        """Inicia o Cacic"""
        try:
            # somente executa se estiver como root
            if not self.isRoot():
                raise Exception(_l.get('need_root'))
            self.running = 1
            # Habilita o coletor de lixo do Python
            garbage_collector.enable()           
            # executa thread para escutar o socket
            thread.start_new_thread(self.checkSocket, ())
            while 1:
                # verifica se o coletor nao esta parado
                if not self.gc_stopped:
                    # muda estado do coletor para parado
                    self.gc_stopped = 1 # True
                    # conecta ao servidor para pegar as informacoes
                    self.conecta()
                    CLog.appendLine(_l.get('col_manager'), '%s %s' % (_l.get('contact_with'), _l.get('web_manager')))
                    # com o coletor parado (dormindo) dispara timeout para iniciar a coleta
                    # apos o intervalo de tempo definido pelo servidor
                    thread.start_new_thread(self.timeout, ())
                    # intervalo
                    self.interval = self.gc.getInterval()
                    CLog.appendLine(_l.get('col_manager'),'%s %s %s' % (_l.get('collection_starts_in'), (self.interval/60), _l.get('minutes')))
                # se esta habilitado a executar ou e uma coleta forcada
                if self.gc_ok or len(self.coletas_forcadas) > 0:
                    # muda estado para nao habilitado
                    self.gc_ok = 0 # False
                    # conecta ao servidor para pegar as informacoes
                    # pode ter ocorrido alguma mudanca desde a ultima
                    self.conecta()
                    CLog.appendLine(_l.get('col_manager'), '%s %s' % (_l.get('contact_with'), _l.get('web_manager')))
                    # inicia coletas
                    self.gc.coletas_forcadas = self.coletas_forcadas
                    self.start()
                    # Executa o coletor de lixo
                    garbage_collector.collect()
                time.sleep(2)
            # sai
            self.quit()
        except socket.error, e:
            error = "Socket %s: %s" % (_l.get('error'), e)
            CLog.appendLine(_l.get('pycacic'), error)
            raise socket.error
        
        except SystemExit:          
            raise SystemExit('Programa encerrado com sucesso')
                        
        
        except GCException, e:
            error = "%s: %s" % (_l.get('error'), e.getMessage())
            CLog.appendLine(_l.get('pycacic'), error)
            
        except Exception, e:
            error = "%s: %s" % (_l.get('error'), e)
            CLog.appendLine(_l.get('pycacic'), error)
        
        
    
    def isRoot(self):
        """Retorna se o usuario e root ou nao"""
        if os.getuid() != 0:
            return 0 # False
        return 1 # True


    def start(self):
        """Inicia as coletas"""
        self.coletas_forcadas = []
        CLog.appendLine(_l.get('col_manager'), _l.get('collections_started'))
        CLog.appendLine(_l.get('col_manager'), '%s: %s' % (_l.get('collection_count'), len(self.gc.coletores)))
        CLog.appendLine(_l.get('col_manager'), '%s: (%s)' % (_l.get('active_collections'), ', '.join([_l.get(col) for col in self.gc.coletores.keys()])))
        self.gc.startColeta()
        self.gc.createDat()
        self.gc.sendColetas()
        CLog.appendLine(_l.get('col_manager'), _l.get('collections_finished'))


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
        try:
            xml = self.gc.conecta(self.gc.cacic_url, self.gc.dicionario)
            self.gc.readXML(xml) 
            # verifica atualizacao
            if self.gc.hasNew():
                self.update()
        
        except GCException, e:
            error = "%s: %s" % (_l.get('error'), e.getMessage())
            CLog.appendLine(_l.get('pycacic'), error)               
        
        except SystemExit:
            raise SystemExit
        
    
    def setSocket(self):
        # configuracao do socket para comunicacao interna
        self.host, self.port, self.buf, self.addr = Globals.getSocketAttr()
        # criando socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(self.addr)


    def checkSocket(self):
        """Verifica comunicacao com a interface"""
        while 1:
            try:
                data, self.addr = self.sock.recvfrom(self.buf)
                self.coletas_forcadas = data.split()
            except:
                self.quit()
           
    
    def update(self):
        try:
            """Faz atualizacao do programa"""        
            CLog.appendLine(_l.get('pycacic'), _l.get('new_version'))
            CLog.appendLine(_l.get('pycacic'), _l.get('starting_update'))
            # baixa o novo pacote para o diretorio temporario
            self.gc.atualiza()
            CLog.appendLine(_l.get('pycacic'), '%s: %s' % (_l.get('download_sucess'), self.gc.pacote_disponivel))
            # chama atualizador e sai
            os.system('python %s/update.py -pkg %s -hash %s &' % (Globals.PATH, self.gc.pacote_disponivel, self.gc.hash_disponivel))
            self.quit()
        except SystemExit:
            raise SystemExit


    def quit(self):
        """Sai do programa fechando conexao do socket"""
        self.sock.close()
        sys.exit(1)


if __name__ == '__main__':
    ver =  sys.version_info
    version = int(''.join([ '%s' %sys.version_info[x] for x in range(3)]))
    if version < 230:
        print _l.get('python_required')
        sys.exit(1)
    
    
    cacic = Cacic()
    while 1:
        try:
            if not cacic.running:
                cacic.run()
                
        except socket.error:
            CLog.appendLine(_l.get('pycacic'), '%s %s %s' % (_l.get('sleeping'), cacic.SLEEP_TIME, _l.get('seconds')))             
            time.sleep(SLEEP_TIME)
        
        except SystemExit, e:
            CLog.appendLine(_l.get('pycacic'), e)
            break
            
        except GCException, e:
            CLog.appendLine(_l.get('pycacic'), '!%s: %s' % (_l.get('error'), e.getMessage()))
            cacic.quit()
            break
        
        except:
            CLog.appendLine(_l.get('pycacic'), 'Erro desconhecido')
            cacic.quit()
            break
        