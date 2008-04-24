# -*- coding: UTF-8 -*-
import os
from cacic import *

from coletores import *
from coletores.lib.url import *
from coletores.coletor import *
from coletores.col_hard import *
from coletores.lib.arquivo import *
from coletores.lib.computador import Computador

from xml.dom import minidom, Node

from config.read import Reader
from config.write import Writer


class Ger_Cols:
    """Gerenciador de Coletas"""

    def __init__(self, version):
        # Coletor para auxiliar com arquivos
        self.coletor = Coletor()
        # URL para acessar o servidor
        self.url = URL()
        # mac invalidos
        self.mac_invalidos = ''
        # configuracoes gerais
        self.versao_atual = version
        self.versao_disponivel = ''
        self.exibe_bandeja = 'N'
        self.exibe_erros_criticos = 'N'
        self.exec_apos = 0
        self.intervalo_exec = 0
        self.intervalo_renovacao_patrim = 0
        # CACIC
        server = Reader.getServer()            
        self.cacic_server = server['address']
        self.cacic_ws = server['ws']
        self.cacic_pass = server['password']
        self.cacic_url = (server['address'] + server['ws'] + server['page'])
        # UPDATES
        self.update_auto = 'N'
        self.update_server = ''
        self.update_port = ''
        self.update_path = ''
        self.update_user = ''
        self.update_pass = ''
        # coletores
        self.col_hard = Col_Hard() 
        # coletas a serem realizadas
        self.coletas = []
        self.coletas_enviar = {}
        # Informacoes a serem passadas para o Gerente Web
        ip_ativo = self.col_hard.computer.getIPAtivo(self.cacic_server)
        self.defaults = {
            'agente_cacic' : self.coletor.encripta('pycacic'),
            'user'         : self.coletor.encripta(server['username']),
            'pwd'          : self.coletor.encripta(server['password']),
            'agent'        : self.coletor.encripta(server['agent']),
            'id_so'        : self.coletor.encripta('-1'),
            'te_so'        : self.coletor.encripta(self.col_hard.computer.getSO()),
            'hostname'     : self.coletor.encripta(self.col_hard.computer.getHostName()),
            'ip'           : self.coletor.encripta(ip_ativo),
            'mac'          : self.coletor.encripta(self.col_hard.computer.getMACAtivo(ip_ativo).replace(':','-')),
            'padding_key'  : self.coletor.getPadding(),  
        }
        self.dicionario = {
                'te_versao_cacic'    : version,
                'te_versao_gercols'  : version,
                'in_chkcacic'        : self.coletor.encripta(Reader.getStatus('install')['value']),
                'in_teste'           : self.coletor.encripta(Reader.getStatus('test')['value']),                
                'te_workgroup'       : self.coletor.encripta('Desconhecido'),
                'te_nome_computador' : self.coletor.encripta(self.col_hard.computer.getHostName()),
                'id_ftp'             : self.coletor.encripta(''),
                'te_fila_ftp'        : self.coletor.encripta(''),
                'te_versao_cacic'    : self.coletor.encripta(version),
                'te_versao_gercols'  : self.coletor.encripta(version),
                'te_tripa_perfis'    : self.coletor.encripta(''),
        }        
        self.separador = '=CacicIsFree='        
           
    def conecta(self, server, dicionario):
        """
            Conecta ao servidor passando chaves e valores por POST
            e retorna o XML gerado no servidor
        """
        # returns void
        try:
            xml = self.url.enviaRecebeDados(dicionario, server, self.defaults)
            # adiciona node pai ao xml
            xml = xml[:xml.find('?>')+2] + '<cacic>' + xml[xml.find('?>')+2:] + '</cacic>'
            return xml 
        except Exception, e:
            print e.message
    
    
    def addColeta(self, col, valor):
        """Adiciona a coleta na lista, se o seu valor for 'S'"""
        if valor.upper() == 'S':
            self.coletas.append(col)
            
    
    def readXML(self, xml):
        """ Le o XML gerado pelo servidor WEB """
        # returns void
        self.xml = minidom.parseString(xml)
        # se nao achar o status==OK, retorna
        if not self.url.isOK(self.xml):
            raise Exception('Erro ao ler XML do servidor, status não disponível')
        root = self.xml.getElementsByTagName('CONFIGS')[0]
        for no in root.childNodes:
            if no.nodeType == Node.ELEMENT_NODE:
                if no.firstChild.nodeValue != '':
                    if no.nodeName == 'cs_auto_update':
                        self.update_auto = self.decode(no.firstChild.nodeValue)
                    # COLETAS
                    elif no.nodeName == 'cs_coleta_compart':
                        self.addColeta('col_comp', self.decode(no.firstChild.nodeValue))
                    elif no.nodeName == 'cs_coleta_hardware':
                        self.addColeta('col_hard', self.decode(no.firstChild.nodeValue))
                    elif no.nodeName == 'cs_coleta_monitorado':
                        self.addColeta('col_moni', self.decode(no.firstChild.nodeValue))
                    elif no.nodeName == 'cs_coleta_software':
                        self.addColeta('col_soft', self.decode(no.firstChild.nodeValue))
                    elif no.nodeName == 'cs_coleta_unid_disc':
                        self.addColeta('col_undi', self.decode(no.firstChild.nodeValue))
                    # VERSOES
                    elif no.nodeName == 'DT_VERSAO_CACIC2_DISPONIVEL':
                        self.versao_disponivel = self.decode(no.firstChild.nodeValue)
                    elif no.nodeName == 'in_exibe_bandeja':
                        self.exibe_bandeja = self.decode(no.firstChild.nodeValue)
                    elif no.nodeName == 'in_exibe_erros_criticos':
                        self.exibe_erros_criticos = self.decode(no.firstChild.nodeValue)
                    elif no.nodeName == 'nu_exec_apos':
                        self.exec_apos = self.decode(no.firstChild.nodeValue)
                    elif no.nodeName == 'nu_intervalo_exec':
                        self.intervalo_exec = self.decode(no.firstChild.nodeValue)
                    elif no.nodeName == 'nu_intervalo_renovacao_patrim':
                        self.intervalo_renovacao_patrim
                    elif no.nodeName == 'te_senha_adm_agente':
                        self.cacic_pass = self.decode(no.firstChild.nodeValue)
                    elif no.nodeName == 'te_enderecos_mac_invalidos':
                        self.mac_invalidos = (self.decode(no.firstChild.nodeValue)).replace('-',':')
                    elif no.nodeName == 'TE_SERV_CACIC':
                        #self.cacic_server = self.decode(no.firstChild.nodeValue)
                        pass
                    # UPDATES
                    elif no.nodeName == 'TE_SERV_UPDATES':
                        self.update_server = self.decode(no.firstChild.nodeValue)
                    elif no.nodeName == 'NU_PORTA_SERV_UPDATES':
                        self.update_port = self.decode(no.firstChild.nodeValue)
                    elif no.nodeName == 'TE_PATH_SERV_UPDATES':
                        self.update_path = self.decode(no.firstChild.nodeValue)
                    elif no.nodeName == 'NM_USUARIO_LOGIN_SERV_UPDATES':
                        self.update_user = self.decode(no.firstChild.nodeValue)
                    elif no.nodeName == 'TE_SENHA_LOGIN_SERV_UPDATES':
                        self.update_pass = self.decode(no.firstChild.nodeValue)

    def decode(self, data):
        """Decodifica a string vindo do Servidor, e remove os caracteres nulos"""
        return self.coletor.decripta(data).replace('\x00','')

    def isNew(self, current, new):
        """
            Compara o as versoes, atual com a disponivel.
        """
        return (current.replace('.','') < new.replace('.',''))
    
    
    def atualiza(self):
        """Atualiza os modulos dos coletores"""
        # returns void
        """
            TODO: definir como vai ficar a string de destino dos arquivos
        """
        try:
            # se nao tem versao nova retorna
            if not self.isNew(self.versao_atual, self.versao_disponivel):
                return
            # conecta ao servidor ftp para buscar atualizacao
            self.url.ftpConecta(self.update_server, self.update_user, self.update_pass)
            self.url.ftpAlteraDir(self.update_path)
            #self.url.getFile('vaca.exe', 'vaca.exe')
            self.url.ftpDesconecta()
        except Exception, e:
            print 'Erro ao tentar atualizar: %s' % e.message

    def startColeta(self):
        """ Inicia as Coletas """
        # returns void
        """
            TODO: Habilitar outras coletas alem do Col_Hard (apos as mesmas estarem prontas)
        """        
        for col in self.coletas:
            if col == 'col_hard':
                self.col_hard.start()
                self.coletor.addChave('Coleta.Hardware', self.col_hard.getChave('UVC'))
                if self.coletor.getUVCDat('cacic2.dat', 'Coleta.Hardware') != self.col_hard.getChave('UVC'): 
                    self.coletas_enviar[col] = {'page': Reader.getColetor(col)['page'], 'dict' : self.col_hard.dictToPost()}
            #elif ...

    def createDat(self):
        self.coletor.addChave('Configs.HOSTNAME', self.col_hard.computer.getHostName())
        self.coletor.addChave('Configs.ID_SO', self.col_hard.computer.getSO())
        self.coletor.addChave('Configs.Endereco_WS', self.cacic_ws)
        self.coletor.createDat(self.coletor.dicionario, 'cacic2.dat')

    def toString(self):
        s = []
        s.append("Cacic")
        s.append("Servidor: %s" % self.cacic_server)
        s.append("Pass: %s" % self.cacic_pass)
        s.append("\nUpdate")
        s.append("Auto-Update: %s" % self.update_auto)
        s.append("Update Server: %s" % self.update_server)
        s.append("Porta: %s" % self.update_port)
        s.append("Path: %s" % self.update_path)
        s.append("User: %s" % self.update_user)
        s.append("Pass: %s" % self.update_pass)
        s.append("\nColetas a Serem feitas")
        s.append('\n'.join(self.coletas))
        return '\n'.join(s)

    def __tostring(self):
        return self.toString()
    
    
if __name__ == '__main__':
    import sys
    sys.path.append(sys.path[0])
  
    try:
        g = Ger_Cols(Cacic.VERSION)
        xml = g.conecta(g.cacic_url, g.dicionario)
        g.readXML(xml)
        #g.atualiza()
        print 'Coletas a serem feitas: %s' % ', '.join(g.coletas)
        g.startColeta()
        g.createDat()
        for col in g.coletas_enviar.keys():
            print ' - Enviando dados de %s' % col
            server = '%s%s%s' % (g.cacic_server, g.cacic_ws, g.coletas_enviar[col]['page'])
            xml = g.conecta(server, g.coletas_enviar[col]['dict'])
            if g.url.isOK(minidom.parseString(xml)):
                print ' `---- Envio OK'
            else:
                print ' `---- tErro no Envio'
            #print '=============\n%s\n=============\n' % g.toString()
    except Exception, e:
        print e.message