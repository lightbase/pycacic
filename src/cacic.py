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
    
    VERSION = '0.0.1'
    
    def __init__(self):
        try:
            # somente executa se estiver como root
            if not self.isRoot():
                raise Exception(_l.get('need_root'))
            
            # Habilita o coletor de lixo do Python
            garbage_collector.enable()
            CLog.appendLine(_l.get('pycacic'), _l.get('program_started'))
            print _l.get('welcome')
            # flags do Gerente de Coletas
            self.gc_stopped = 0 # False
            self.gc_ok = 0 # False
            self.coletas_forcadas = []
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
            CLog.appendLine(_l.get('pycacic'), e)
            # remover depois
            import traceback
            traceback.print_exc()
            
        except GCException, e:
            error = "%s: %s" % (_l.get('error'), e.getMessage())
            CLog.appendLine(_l.get('pycacic'), error)
            # remover depois
            import traceback
            traceback.print_exc()
        except Exception, e:
            error = "%s: %s" % (_l.get('error'), e)
            CLog.appendLine(_l.get('pycacic'), error)            
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
        xml = self.gc.conecta(self.gc.cacic_url, self.gc.dicionario)
        self.gc.readXML(xml)
        """
        # verifica atualizacao
        if self.gc.hasNew():
            CLog.appendLine('Cacic', 'Nova Versao Disponivel !!!')
            CLog.appendLine('Cacic', 'Iniciando Atualização')
            self.gc.atualiza()
            #chama atualizador e sai
            CLog.appendLine('Cacic', 'Programa Atualizado Com Sucesso')
            os.system('python %s/update.py -pkg %s -hash %s -tmp %s &' % (Globals.PATH, self.gc.pacote_disponivel, self.gc.hash_disponivel, 'pycacic_temp'))
            CLog.appendLine('Cacic', 'O Programa vai ser reiniciado em instantes.')
            self.quit()
        """

    def checkSocket(self):
        """Verifica comunicacao com a interface"""
        while 1:
            data, self.addr = self.sock.recvfrom(self.buf)
            self.coletas_forcadas = data.split()

    def quit(self):
        """Sai do programa fechando conexao do socket"""
        self.sock.close()
        sys.exit()

if __name__ == '__main__':
    ver =  sys.version_info
    version = int(''.join([ '%s' %sys.version_info[x] for x in range(3)]))
    if version < 230:
        print _l.get('python_required')
        sys.exit(1)
    Cacic()
