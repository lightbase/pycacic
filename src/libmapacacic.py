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

from coletores.lib.ccrypt import *
from coletores.lib.url import *
from coletores.lib.computador import *
from coletores.coletor import *
from config.io import *

from xml.dom import minidom, Node

class MapaCacic:
    
    def __init__(self, user, pwd):
        self.user = user
        self.pwd = pwd
        self.id_usuario = ''
        self.nm_usuario_completo = ''
        self.url = URL()
        self.cipher = CCrypt()
        self.computer = Computador()
        self.versao_atual = '2.5.9.907'
        self.cs_cipher = 1
        self.dicionario = {}
        self.currentValues = {}
        self.labels = {}
        self.reinitDict()
        server = Reader.getServer()
        self.cacic_server = server['address']
        self.cacic_ws = server['ws']
        self.endereco = '%s%s' % (self.cacic_server, self.cacic_ws)
        #print self.endereco
        #sys.exit(0)
        
    def getVersao(self):
        """ Retorna a versão do mapa cacic """
        return self.versao_atual
    
    def reinitDict(self):
        """ Recria o dicionario de dados, contendo somente as variaveis de autenticacao """
        self.dicionario.clear()
        self.dicionario['nm_acesso'] =  self.encripta(self.user)
        self.dicionario['te_senha'] = self.encripta(self.pwd)
        self.dicionario['padding_key'] = Coletor().getPadding()
        self.dicionario['cs_compress'] = 0
        self.dicionario['AgenteLinux'] = '1'
    
    def encripta(self, text):
        """ Retorna o texto encriptado caso a encriptação esteja habilitada """
        if str(self.cs_cipher) == '1':
            return self.cipher.encrypt(text)
        return text
    
    def decripta(self, text):
        """ Retorna o texto encriptado caso a encriptação esteja habilitada """
        if str(self.cs_cipher) == '1':
            return self.cipher.decrypt(text).replace('\0', '')
        return text
    
    def auth(self):
        """ Autentica o login com o servidor e recebe o ID_USUARIO"""
        self.reinitDict()
        self.dicionario['te_versao_mapa'] = self.encripta(self.versao_atual)
        self.dicionario['cs_MapaCacic'] = self.encripta('S')
        xml = self.url.enviaRecebeDados(self.dicionario, self.endereco+'mapa_acesso.php', self.encripta('USER_CACIC'), self.encripta('PW_CACIC'), { 'cs_cipher' : self.cs_cipher, 'agent' : self.encripta('AGENTE_CACIC'), 'te_operacao' : self.encripta('Autentication') } )
        xml = xml.replace("?>", "?><REPLY>")
        xml += "</REPLY>"
        #print "XML:\n["+xml+"]\n------"
        return self.__parseAuthReply__(xml)
        
    def __parseAuthReply__(self, xmlstr):
        xml = minidom.parseString(xmlstr)   
        root = xml.getElementsByTagName('CONFIGS')[0]
        self.id_usuario = ''
        for no in root.childNodes:
            if no.nodeName == "ID_USUARIO":
                self.id_usuario = self.decripta(no.firstChild.nodeValue)
            elif no.nodeName == "NM_USUARIO_COMPLETO":
                self.nm_usuario_completo = self.decripta(no.firstChild.nodeValue)
            elif no.nodeName == "TE_VERSAO_MAPA":
                raise Exception("O servidor requer a versão %s do coletor patrimonial.\nSua versão: %s" % (self.decripta(no.firstChild.nodeValue), self.versao_atual))
        return self.id_usuario != ''
        
    def getInfo(self):
        """ 
        Recebe as labels e valores da interface e os valores atualmente salvos no servidor
        So pdoe ser chamado depois de auth() ja ter sido chamado
        """
        self.reinitDict()
        self.computer.ipAtivo = self.computer.getIPAtivo(self.cacic_server)
        net = Rede()
        netmask = net.__getMask__(self.computer.ipAtivo)
        iprede = net.__getIPRede__(self.computer.ipAtivo, netmask);
        self.dicionario['te_node_address'] = self.encripta(self.computer.getMACAtivo(self.computer.ipAtivo))
        self.dicionario['id_so'] = self.encripta('-1')
        self.dicionario['te_so'] = self.encripta(self.computer.getSO())
        self.dicionario['id_ip_rede'] = self.encripta(iprede)
        self.dicionario['te_ip'] = self.encripta(self.computer.ipAtivo)
        self.dicionario['te_nome_computador'] = self.encripta(self.computer.getHostName())
        self.dicionario['te_workgroup'] = self.encripta('Desconhecido')
        self.dicionario['id_usuario'] = self.encripta(self.id_usuario)
        #print "PADDING: "+self.dicionario['padding_key']
        xmlstr = self.url.enviaRecebeDados(self.dicionario, self.endereco+'mapa_get_patrimonio.php', self.encripta('USER_CACIC'), self.encripta('PW_CACIC'), { 'cs_cipher' : self.cs_cipher, 'agent' : self.encripta('AGENTE_CACIC') } )
        #print "XML:\n"+xmlstr+"\n---"
        xml = minidom.parseString(xmlstr)
        self.__parseLabels__(xml)
        self.__parseValues__(xml)
        dict = self.__parseCurrentValues__(xml)
        self.currentValues = dict
        
    def getCurrentValues(self):
        """ Retorna os valores atualmente salvos no servidor """
        return self.currentValues
    
    def save(self, dict):
        """ Salva os valores passados em 'dict' no servidor """
        self.reinitDict()
        self.computer.ipAtivo = self.computer.getIPAtivo(self.cacic_server)
        net = Rede()
        netmask = net.__getMask__(self.computer.ipAtivo)
        iprede = net.__getIPRede__(self.computer.ipAtivo, netmask);
        self.dicionario['te_node_address'] = self.encripta(self.computer.getMACAtivo(self.computer.ipAtivo))
        self.dicionario['id_so'] = self.encripta('-1')
        self.dicionario['te_so'] = self.encripta(self.computer.getSO())
        self.dicionario['id_ip_rede'] = self.encripta(iprede)
        self.dicionario['te_ip'] = self.encripta(self.computer.ipAtivo)
        self.dicionario['te_nome_computador'] = self.encripta(self.computer.getHostName())
        self.dicionario['te_workgroup'] = self.encripta('Desconhecido')
        self.dicionario['id_usuario'] = self.encripta(self.id_usuario)
        
        for k, v in dict.items():
            self.dicionario[k] = self.encripta(v)
        
        """
        self.dicionario['id_unid_organizacional_nivel1a'] = 1
        self.dicionario['id_unid_organizacional_nivel2'] = 163
        self.dicionario['te_localizacao_complementar'] = 'URES'
        self.dicionario['te_info_patrimonio1'] = '123'
        self.dicionario['te_info_patrimonio2'] = '234'
        self.dicionario['te_info_patrimonio3'] = '345'
        self.dicionario['te_info_patrimonio4'] = '456'
        self.dicionario['te_info_patrimonio5'] = '567'
        self.dicionario['te_info_patrimonio6'] = '678'
        """
        
        xmlstr = self.url.enviaRecebeDados(self.dicionario, self.endereco+'mapa_set_patrimonio.php', self.encripta('USER_CACIC'), self.encripta('PW_CACIC'), { 'cs_cipher' : self.cs_cipher, 'agent' : self.encripta('AGENTE_CACIC') } )
        #print "XML:\n"+xmlstr+"\n--------\n"
        return xmlstr.find("<STATUS>OK</STATUS>") != -1
        """xml = minidom.parseString(xmlstr)
        self.__parseLabels__(xml)
        self.__parseValues__(xml)"""
    
    def __parseCurrentValues__(self, xml):
        root = xml.getElementsByTagName('CONFIGS')[0]
        dict = {}
        for no in root.childNodes:
            if no.nodeName == "ID_UON1a":
                if len(no.childNodes) > 0:
                    dict['ID1a'] = self.decripta(no.firstChild.nodeValue)
                else:
                    dict['ID1a'] = ''
            elif no.nodeName == "ID_UON2":
                if len(no.childNodes) > 0:
                    dict['ID2'] = self.decripta(no.firstChild.nodeValue)
                else:
                    dict['ID2'] = ''
            elif no.nodeName == "ID_LOCAL":
                if len(no.childNodes) > 0:
                    dict['ID1'] = self.decripta(no.firstChild.nodeValue)
                else:
                    dict['ID1'] = ''
            elif no.nodeName.startswith("TE_"):
                if len(no.childNodes) > 0:
                    dict[no.nodeName] = self.decripta(no.firstChild.nodeValue)
                else:
                    dict[no.nodeName] = ''
        return dict
    
    def __parseLabels__(self, xml):
        root = xml.getElementsByTagName('CONFIGS')[0]
        for no in root.childNodes:
            if no.nodeName.startswith("te_etiqueta"):
                et_num = no.nodeName[11:]
                text = self.decripta(no.firstChild.nodeValue)
                self.__getMapaLabel__(et_num).setText(text)
            elif no.nodeName.startswith("in_exibir_etiqueta"):
                et_num = no.nodeName[18:]
                if no.hasChildNodes():
                    if self.decripta(no.firstChild.nodeValue) == 'S':
                        enabled = 1
                    else:
                        enabled = 0
                else:
                    enabled = 0
                self.__getMapaLabel__(et_num).setEnabled(enabled)
            elif no.nodeName.startswith("te_help_etiqueta"):
                et_num = no.nodeName[16:]
                text = self.decripta(no.firstChild.nodeValue)
                self.__getMapaLabel__(et_num).setHelpText(text)
                
    def __parseValues__(self, xml):
        it1 = xml.getElementsByTagName('IT1')
        for no in it1:
            value = self.__parseID1__(no)
            self.__getMapaLabel__('1').addValue(value)
            
        it1a = xml.getElementsByTagName('IT1a')
        for no in it1a:
            value = self.__parseID1a__(no)
            self.__getMapaLabel__('1').getValue(value.getDict()['ID1']).addSubItem(value)
            
        it2 = xml.getElementsByTagName('IT2')
        for no in it2:
            value = self.__parseID2__(no)
            #print value.getDict()
            for v in self.__getMapaLabel__('1').getValues():
                k = value.getDict()['ID1a']
                if v.hasItem(k):
                    v.getSubItem(k).addSubItem(value)
                #self.__getMapaLabel__('1').getValue(value.getDict()['ID1']).getValue(value.getDict()['ID1a']).addSubItem(value)
                
    def __parseID1__(self, no):
        id = ''
        value = ''
        for child in no.childNodes:
            if child.nodeName == "ID1":
                id = self.decripta(child.firstChild.nodeValue)
            elif child.nodeName == "NM1":
                value = self.decripta(child.firstChild.nodeValue)
        return MapaValue(id, value)
    
    def __parseID1a__(self, no):
        id1a = ''
        nm1a= ''
        dict = {}
        for child in no.childNodes:
            if child.nodeName == "ID1a":
                id1a = self.decripta(child.firstChild.nodeValue)
            elif child.nodeName == "NM1a":
                nm1a = self.decripta(child.firstChild.nodeValue)
            else:
                dict[child.nodeName] = self.decripta(child.firstChild.nodeValue)
        return MapaValue(id1a, nm1a, dict)
    
    def __parseID2__(self, no):
        id2 = ''
        nm2 = ''
        dict = {}
        for child in no.childNodes:
            if child.nodeName == "ID2":
                id2 = self.decripta(child.firstChild.nodeValue)
            elif child.nodeName == "NM2":
                nm2 = self.decripta(child.firstChild.nodeValue)
            else:
                dict[child.nodeName] =  self.decripta(child.firstChild.nodeValue)
        return MapaValue(id2, nm2, dict)
                
                
    def __getMapaLabel__(self, et_num):
        if not self.labels.has_key(et_num):
            self.labels[et_num] = MapaLabel()
        return self.labels[et_num]
            
        
class MapaLabel:
    
    def __init__(self):
        self.text = ''
        self.enabled = 0
        self.helptext = ''
        self.values = {}
    
    def getText(self):
        return self.text#.encode("latin_1")
    
    def setText(self, text):
        self.text = text
    
    def isEnabled(self):
        return self.enabled
    
    def setEnabled(self, enabled):
        self.enabled = enabled
    
    def getHelpText(self):
        return self.helptext
    
    def setHelpText(self, text):
        self.helptext = text
        
    def addValue(self, value):
        self.values[value.getId()] = value
    
    def hasValue(self, key):
        return self.values.has_key(key)    
    
    def getValue(self, key):
        return self.values[key]
    
    def getValues(self):
        return self.values.values()
        
class MapaValue:
    
    def __init__(self, id, text, dict = {}):
        self.id = id
        self.text = text
        self.dict = dict
        self.subitems = {}
    
    def getId(self):
        return self.id
    
    def getText(self):
        return self.text#.encode("latin_1")
    
    def getDict(self):
        return self.dict
    
    def hasItem(self, key):
        return self.subitems.has_key(key)  
    
    def addSubItem(self, item):
        self.subitems[item.getId()] = item
    
    def getSubItem(self, id):
        return self.subitems[id]
        
    def getSubItems(self):
        return self.subitems.values()
