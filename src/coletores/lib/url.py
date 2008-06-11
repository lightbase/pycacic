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
    

    Modulo url
    
    Modulo com finalidade de efetuar a comunicacao
    HTTP com o servidor e resgatar as informacoes
    retornadas por ele.
    
    Tem como funcao tambem baixar os arquivos do
    servidor por FTP.
    
    @author: Dataprev - ES
    
"""

import re
import sys
import base64
import urllib, urllib2
import ftplib
from coletores.coletor import *
from xml.dom import minidom, Node

class URL :
    """Responsavel por efetuar acessos HTTP e FTP ao servidor"""
    
    def __init__(self) :
        self.ftp = ''
    
    def enviaRecebeDados(self, dados, url, user, pwd, defaults):
        """
            Envia os dados passados por parametro ao servidor por metodo POST
            e retorna o conteudo da pagina gerada
            
            @param dados: dict
        """
        # returns string
        """
        dados['cs_cipher']          = '1'
        dados['id_ip_estacao']      = defaults['ip']
        dados['id_ip_rede']         = defaults['id_rede']
        dados['te_node_address']    = defaults['mac']
        dados['id_so']              = defaults['id_so']
        dados['te_so']              = defaults['te_so']
        dados['te_nome_computador'] = defaults['hostname']
        dados['padding_key']        = defaults['padding_key']
        dados['AgenteLinux']        = defaults['agente_linux']
        """
        for key, value in defaults.items():
            dados[key] = value
        
        query = urllib.urlencode(dados)
        
        base64string = base64.encodestring('%s:%s' % (user,pwd))[:-1]
        
        passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passman.add_password(None, url, user, pwd)
        auth_handler = urllib2.HTTPBasicAuthHandler(passman)
        opener = urllib2.build_opener(auth_handler)
        urllib2.install_opener(opener)
        request = urllib2.Request(url)
        request.add_header("Authorization", "Basic %s" % base64string)
        opener.addheaders = [('User-Agent', defaults['agent']), ('Accept','text/html, */*')]        
        data = opener.open(request, data=query).read()
        opener.close()
        return data

    def isOK(self, xml):
        """Retorna se o XML gerado esta valido ou nao"""
        try:
            xml = minidom.parseString(xml)
            status = xml.getElementsByTagName('STATUS')[0].firstChild.nodeValue
            if status != "OK":
                return 0 # False
            return 1 # True
        except:
            return 0
    
    def ftpConecta(self, server, login, senha):
        """Conecta a um servidor FTP"""
        try:
            self.ftp = ftplib.FTP(server)
            self.ftp.login(login, senha)
        except Exception, e:
            raise Exception('Tentando conectar ao FTP. %s' % e.message)

    def ftpAlteraDir(self, dir):
        self.ftp.cwd(dir)
    
    def ftpDesconecta(self):
        """Desconecta do servidor FTP"""
        try:
            self.ftp.close()
        except Exception, e:
            raise Exception('Tentando disconectar. %s' % e.message)
    
    def getFile(self, arquivo, destino) :
        """ Salva arquivo via FTP no disco local """
        # returns void
        try:
            self.ftp.retrbinary("RETR " + arquivo, open(destino, 'wb').write)
        except Exception, e:
            raise Exception('Tentando baixar arquivo %s. %s' % (arquivo, e.message))
