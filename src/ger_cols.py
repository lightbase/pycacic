# -*- coding: UTF-8 -*-

"""

    Modulo ger_cols
    
    Modulo com finalidade de controlar a comunicacao
    do agente local com o servidor, Gerente Web.
    
    @author: Dataprev - ES

"""

import os
import sys

from coletores.coletor import *
from coletores.col_network import *
from coletores.col_hard import *
from coletores.col_soft import *
from coletores.col_patr import *

from coletores.lib.url import *
from coletores.lib.arquivo import *
from coletores.lib.computador import Computador

import time
from time import strftime
from threading import Thread

from xml.dom import minidom, Node

from config.io import *

from globals import Globals


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
        # coletas a serem realizadas
        self.coletores = {}
        self.coletas_enviar = {}
        # lista com as coletas forcadas
        self.coletas_forcadas = []
        # se for True forca todas as coletas
        self.all_forcada = 0 # False
        # Informacoes a serem passadas para o Gerente Web
        self.computador.ipAtivo = self.computador.getIPAtivo(self.cacic_server)
        net = Rede()
        netmask = net.__getMask__(self.computador.ipAtivo)
        iprede = net.__getIPRede__(self.computador.ipAtivo, netmask);
        self.defaults = {
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
        }        
        self.dicionario = {
            'te_versao_cacic'    : version,
            'te_versao_gercols'  : version,
            'in_chkcacic'        : self.coletor.encripta(''),
            'in_teste'           : self.coletor.encripta(''),                
            'te_workgroup'       : self.coletor.encripta('Desconhecido'),
            'te_nome_computador' : self.coletor.encripta(self.computador.getHostName()),
            'id_ftp'             : self.coletor.encripta(''),
            'te_fila_ftp'        : self.coletor.encripta(''),
            'te_versao_cacic'    : self.coletor.encripta(version),
            'te_versao_gercols'  : self.coletor.encripta(version),
            'te_tripa_perfis'    : self.coletor.encripta(''),
        }     
        
        self.separador = '=CacicIsFree='
        
        
    def start(self):
        """Inicia o Gerente de Coletas em background"""
        try:
            xml = self.conecta(self.cacic_url, self.dicionario)
            print("Contato com o Gerente Web: %s" % strftime("%H:%M:%S"))
            self.readXML(xml)
            # intervalo
            interval = self.getInterval()
            print(" `---- Coleta iniciara daqui a %s minutos" % (interval/60))
            time.sleep(interval)
            #self.atualiza()
            print('Coletas a serem feitas: %s' % ', '.join(self.coletas))
            self.startColeta()
            self.createDat()
            self.sendColetas()
            print(" --- FIM ---")
        except Exception, e:
            import traceback
            traceback.print_exc()
            print(e)

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
            xml = self.url.enviaRecebeDados(dicionario, server, self.defaults)
            # adiciona node pai ao xml
            xml = xml[:xml.find('?>')+2] + '<cacic>' + xml[xml.find('?>')+2:] + '</cacic>'
            return xml 
        except Exception, e:
            raise Exception(e.message)
    
    def addColeta(self, col, valor):
        """Adiciona o coletor na lista, se o seu valor for 'S'"""
        if valor.upper() == 'S':
            self.coletores[col.getName()] = col
            
    def readXML(self, xml):
        """ Le o XML gerado pelo servidor WEB """
        # returns void
        #print "XML: "+xml
        self.xml = minidom.parseString(xml)
        # se nao achar o status==OK, retorna
        if not self.url.isOK(self.xml):
            raise Exception('Erro ao ler XML do servidor, status não disponível')
        root = self.xml.getElementsByTagName('CONFIGS')[0]
        # Coletores
        self.coletores.clear()
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
                    elif no.nodeName == 'cs_coleta_unid_disc':
                        #self.addColeta(None, self.decode(no.firstChild.nodeValue))
                        pass
                    # VERSOES
                    elif no.nodeName == 'TE_VERSAO_PYCACIC_DISPONIVEL':
                        self.versao_disponivel = self.decode(no.firstChild.nodeValue)
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
        """Compara as versoes, atual com a disponivel."""
        return (current.replace('.','') < new.replace('.',''))
    
    def atualiza(self):
        """Atualiza os modulos dos coletores"""
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
            raise Exception('Erro ao tentar atualizar: %s' % e.message)

    def startColeta(self):
        """ Inicia as Coletas"""
        # limpa o dicionario da ultima coleta
        self.coletas_enviar.clear()
        self.computador.coletar()
        # adiciona o coletor padrao (Col_Network)
        for col in self.coletores.values():
            col.start()
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
            print(' - Enviando dados de %s' % col)
            server = '%s%s%s' % (self.cacic_server, self.cacic_ws, self.coletas_enviar[col]['page'])
            xml = self.conecta(server, self.coletas_enviar[col]['dict'])
            if self.url.isOK(minidom.parseString(xml)):
                print(' `---- Envio OK')
            else:
                print(' `---- Erro no Envio')

    def createDat(self):
        """Cria o arquivo .dat do gerencte de coletas"""
        self.coletor.addChave('Configs.HOSTNAME', self.computador.getHostName())
        self.coletor.addChave('Configs.ID_SO', self.computador.getSO())
        self.coletor.addChave('Configs.Endereco_WS', self.cacic_ws)
        self.coletor.createDat(self.coletor.dicionario, self.OUTPUT_DAT)

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
  