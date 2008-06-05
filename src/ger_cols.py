# -*- coding: UTF-8 -*-

"""

    Modulo ger_cols
    
    Modulo com finalidade de controlar a comunicacao
    do agente local com o servidor, Gerente Web.
    
    @author: Dataprev - ES

"""

import os
import sys
import commands

import time
from time import strftime
from threading import Thread

from xml.dom import minidom, Node

from coletores.coletor import *
from coletores.col_network import *
from coletores.col_hard import *
from coletores.col_soft import *
from coletores.col_patr import *
from coletores.col_vamb import *
from coletores.col_undi import *

from coletores.lib.url import *
from coletores.lib.arquivo import *
from coletores.lib.computador import Computador

from logs.log import CLog
from lang.language import Language
from config.io import *

from globals import Globals

_l = Language()

class Ger_Cols:
    """
        Classe Ger_Cols - Gerenciador de Coletas
        
        Responsavel pelo contato inicial com o Gerente Web
        cadastrando o computador (informando ip, mac, etc.).
        
        Sendo gerado a partir desse contato um arquivo XMl
        contendo as tarefas a serem feitas (coletas) e suas
        configuracoes.
    """
    
    OUTPUT_DAT = '%s/cacic2.dat' % Globals.PATH
    MD5SUM = '%s/config/MD5SUM' % Globals.PATH

    def __init__(self, version):
        # para controle de intervalo
        self.first_time = 1 # True
        # Inicializa o objeto que representa o computador
        self.computador = Computador()
        # Coletor para auxiliar com arquivos
        self.coletor = Coletor()
        # URL para acessar o servidor
        self.url = URL()
        # mac invalidos
        self.mac_invalidos = ''
        # configuracoes gerais
        self.versao_atual = version
        self.hash_atual = open(self.MD5SUM, "r").read()
        self.hash_disponivel = ''
        self.pacote_disponivel = ''
        self.exibe_bandeja = 'N'
        self.exibe_erros_criticos = 'N'
        self.exec_apos = 0
        self.intervalo_exec = 0
        self.intervalo_renovacao_patrim = 0
        # CACIC
        server = Reader.getServer()
        self.cacic_server = server['address']
        self.cacic_ws = server['ws']
        self.cacic_user = self.coletor.encripta(server['username'])
        self.cacic_pass = self.coletor.encripta(server['password'])
        self.cacic_url = (server['address'] + server['ws'] + server['page'])
        # UPDATES
        self.update_auto = 'N'
        self.update_server = ''
        self.update_port = ''
        self.update_path = ''
        self.update_user = ''
        self.update_pass = ''
        # coletas a serem realizadas
        self.coletores = {}
        self.coletas_enviar = {}
        self.col_status = {}
        # lista com as coletas forcadas
        self.coletas_forcadas = []
        # se for True forca todas as coletas
        self.all_forcada = 0 # False
        # Informacoes a serem passadas para o Gerente Web
        self.computador.ipAtivo = self.computador.getIPAtivo(self.cacic_server)
        net = Rede()
        netmask = net.__getMask__(self.computador.ipAtivo)
        iprede = net.__getIPRede__(self.computador.ipAtivo, netmask);
        """
            'agente_linux' : self.coletor.encripta('PyCacic'),
            'user'         : self.coletor.encripta(server['username']),
            'pwd'          : self.coletor.encripta(server['password']),
            'agent'        : self.coletor.encripta(server['agent']),     
            'id_so'        : self.coletor.encripta('-1'),
            'te_so'        : self.coletor.encripta(self.computador.getSO()),
            'hostname'     : self.coletor.encripta(self.computador.getHostName()),
            'ip'           : self.coletor.encripta(self.computador.ipAtivo),
            'id_rede'      : self.coletor.encripta(iprede),
            'mac'          : self.coletor.encripta(self.computador.getMACAtivo(self.computador.ipAtivo)),
            'padding_key'  : self.coletor.getPadding(),
            """
        self.defaults = {
            'cs_cipher'   : '1',
            'AgenteLinux' : self.coletor.encripta('PyCacic'),
            'agent'        : self.coletor.encripta(server['agent']),     
            'id_so'        : self.coletor.encripta('-1'),
            'te_so'        : self.coletor.encripta(self.computador.getSO()),
            'te_nome_computador'     : self.coletor.encripta(self.computador.getHostName()),
            'id_ip_estacao'           : self.coletor.encripta(self.computador.ipAtivo),
            'id_ip_rede'      : self.coletor.encripta(iprede),
            'te_node_address'          : self.coletor.encripta(self.computador.getMACAtivo(self.computador.ipAtivo)),
            'padding_key'  : self.coletor.getPadding(),
        }
        self.dicionario = {
            'in_chkcacic'        : self.coletor.encripta(''),
            'in_teste'           : self.coletor.encripta(''),                
            'te_workgroup'       : self.coletor.encripta('Desconhecido'),
            'te_nome_computador' : self.coletor.encripta(self.computador.getHostName()),
            'id_ftp'             : self.coletor.encripta(''),
            'te_fila_ftp'        : self.coletor.encripta(''),
            'te_versao_cacic'    : self.coletor.encripta(self.versao_atual),
            'te_versao_gercols'  : self.coletor.encripta(self.versao_atual),
            'te_tripa_perfis'    : self.coletor.encripta(''),
        }       
        self.separador = '=CacicIsFree='
        
    def getInterval(self):
        """Retorna o tempo em minutos do intervalo da coleta"""
        interval = self.intervalo_exec
        if self.first_time:
            self.first_time = 0 # False
            interval = self.exec_apos
        return interval
           
    def conecta(self, server, dicionario):
        """
            Conecta ao servidor passando chaves e valores por POST
            e retorna o XML gerado no servidor
        """
        # returns void
        try:
            xml = self.url.enviaRecebeDados(dicionario, server, self.cacic_user, self.cacic_pass, self.defaults)
            # adiciona node pai ao xml
            xml = xml[:xml.find('?>')+2] + '<cacic>' + xml[xml.find('?>')+2:] + '</cacic>'
            return xml 
        except Exception, e:
            raise Exception(e)
    
    def addColeta(self, col, valor):
        """Adiciona o coletor na lista, se o seu valor for 'S'"""
        if valor.upper() == 'S':
            self.coletores[col.getName()] = col
            
    def readXML(self, xml):
        """ Le o XML gerado pelo servidor WEB """
        # returns void
        # se nao achar o status==OK, retorna
        if not self.url.isOK(xml):
            raise Exception('%s, %s.' % (_l.get('error_on_read_server_xml'), _l.get('error_not_available_status')))
        self.xml = minidom.parseString(xml)        
        root = self.xml.getElementsByTagName('CONFIGS')[0]
        # Coletores
        self.coletores.clear()
        # adiciona o coletor padrao (Col_Network)
        self.addColeta(Col_Network(self.computador), 'S')
        for no in root.childNodes:
            if no.nodeType == Node.ELEMENT_NODE:
                if no.firstChild.nodeValue != '':      
                    if no.nodeName == 'cs_auto_update':
                        self.update_auto = self.decode(no.firstChild.nodeValue)
                    # COLETAS
                    elif no.nodeName == 'cs_coleta_forcada' and self.decode(no.firstChild.nodeValue) == 'OK':
                        self.all_forcada = 1 # True
                    elif no.nodeName == 'cs_coleta_compart':                       
                        #self.addColeta(None, self.decode(no.firstChild.nodeValue))
                        pass
                    elif no.nodeName == 'cs_coleta_hardware':
                        self.addColeta(Col_Hard(self.computador), self.decode(no.firstChild.nodeValue))
                    elif no.nodeName == 'cs_coleta_monitorado':
                        #self.addColeta(None, self.decode(no.firstChild.nodeValue))
                        pass
                    elif no.nodeName == 'cs_coleta_software':
                        self.addColeta(Col_Soft(self.computador), self.decode(no.firstChild.nodeValue))
                        self.addColeta(Col_Vamb(self.computador), self.decode(no.firstChild.nodeValue))
                    elif no.nodeName == 'cs_coleta_unid_disc':
                        self.addColeta(Col_Undi(self.computador), self.decode(no.firstChild.nodeValue))
                    # VERSOES
                    elif no.nodeName == 'TE_HASH_PYCACIC':
                        self.hash_disponivel = self.decode(no.firstChild.nodeValue)
                    elif no.nodeName == 'TE_PACOTE_PYCACIC_DISPONIVEL':
                        self.pacote_disponivel = self.decode(no.firstChild.nodeValue)
                    elif no.nodeName == 'in_exibe_bandeja':
                        self.exibe_bandeja = self.decode(no.firstChild.nodeValue)
                    elif no.nodeName == 'in_exibe_erros_criticos':
                        self.exibe_erros_criticos = self.decode(no.firstChild.nodeValue)
                    # intervalo da primeira execucao em minutos
                    elif no.nodeName == 'nu_exec_apos':
                        self.exec_apos = float(self.decode(no.firstChild.nodeValue)) * 60
                    # intervalo de execucao em horas
                    elif no.nodeName == 'nu_intervalo_exec':
                        self.intervalo_exec = float(self.decode(no.firstChild.nodeValue)) * 3600
                    elif no.nodeName == 'nu_intervalo_renovacao_patrim':
                        self.intervalo_renovacao_patrim = self.decode(no.firstChild.nodeValue)
                    elif no.nodeName == 'te_senha_adm_agente':
                        Writer.setPycacic('password', self.decode(no.firstChild.nodeValue))
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

    def hasNew(self, current='', new=''):
        """Compara as versoes, atual com a disponivel."""
        if current == '' or new == '':
            current, new = self.hash_atual, self.hash_disponivel
        return (current != new)       
    
    def atualiza(self):
        """Atualiza os modulos dos coletores caso tenha alguma versao nova."""
        try:
            # se nao tem versao nova retorna
            if not self.hasNew(): return ''
            # conecta ao servidor ftp para buscar atualizacao
            self.url.ftpConecta(self.update_server, self.update_user, self.update_pass)
            # altera o diretorio do servidor para aonde esta o pacote
            self.url.ftpAlteraDir(self.update_path)
            # pega o pacote e salva no temporario
            self.url.getFile(self.pacote_disponivel, '/tmp/%s' % self.pacote_disponivel)
            self.url.ftpDesconecta()
        except Exception, e:
            raise Exception('%s: %s.' % (_l.get('error_on_try_update'), e.message))

    def startColeta(self):
        """ Inicia as Coletas"""
        # limpa o dicionario da ultima coleta
        self.coletas_enviar.clear()
        self.computador.coletar()
        for col in self.coletores.values():
            CLog.appendLine('%s' % _l.get(col.getName()), 'Coleta iniciada')
            col.start()
            self.coletor.addChave(col.getUVCKey(), col.getChave('UVC'))            
            if self.all_forcada or (col.getName() in self.coletas_forcadas) or col.isReady(self.OUTPUT_DAT):
                page = Reader.getColetor(col.getName())['page']
                dict = col.getEncryptedDict()
                self.coletas_enviar[col.getName()] = {'page': page, 'dict' : dict }

    def sendColetas(self):
        """
            Envia as coletas efetuadas para as respectivas suas paginas
            no Gerente Web
        """
        for col in self.coletas_enviar.keys():
            CLog.appendLine('%s' % _l.get(col), 'Enviando dados')
            server = '%s%s%s' % (self.cacic_server, self.cacic_ws, self.coletas_enviar[col]['page'])
            xml = self.conecta(server, self.coletas_enviar[col]['dict'])
            if self.url.isOK(xml):
                self.col_status[col] = 'Dados da Coleta Enviado Com Sucesso'
                CLog.appendLine('%s' % _l.get(col), 'Dados da Coleta Enviado Com Sucesso')
            else:
                self.col_status[col] = _l.get('error_on_send_data')
                CLog.appendLine('%s' % _l.get(col), _l.get('error_on_send_data'))

    def createDat(self):
        """Cria o arquivo .dat do gerente de coletas"""
        self.coletor.addChave('Configs.HOSTNAME', self.computador.getHostName())
        self.coletor.addChave('Configs.ID_SO', self.computador.getSO())
        self.coletor.addChave('Configs.Endereco_WS', self.cacic_ws)
        coletas_realizadas = []
        for col in self.coletores.values():
            coletas_realizadas.append('#'.join([col.getName(), col.getChave('Inicio'), col.getChave('Fim')]))           
        self.coletor.addChave('Coletas.Realizadas', '##'.join(coletas_realizadas))
        self.coletor.createDat(self.coletor.dicionario, self.OUTPUT_DAT, '')

    def toString(self):
        """Metodo toString da Classe"""
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
        """Metodo toString da Classe"""
        return self.toString()
  