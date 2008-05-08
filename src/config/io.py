# -*- coding: UTF-8 -*-

"""

    Modulo io
    
    Modulo com finalidade de controlar a comunicacao
    do agente local com o servidor, Gerente Web. 
    
    @author: Dataprev - ES
    
"""
import re
import sys, os
from xml.dom import minidom, Node


class IOConfig:
    """
        Classe IOConfig
        
        Responsavel por guardar o caminho do arquivo de
        configuracao do Cacic e efetuar a leitura dos nos principais
        dele.        
    """
    
    FILE = '%s/config/cacic.conf' % sys.path[0]
    
    def exists():
        """Retorna se um arquivo existe ou nao"""
        return (os.path.exists(IOConfig.FILE))
    
    def getFile():
        """
            Retorna o conteudo do arquivo de configuracao
            caso nao exista gera uma excecao
        """
        if not IOConfig.exists():
            raise Exception('Arquivo de configuração não encontrado.')
        else:
            return open(IOConfig.FILE, 'r').read()

    def getRoot():
        """Retorna o node principal do XML"""
        if not IOConfig.exists():
            raise Exception('Arquivo de configuração não encontrado.')
        else:
            xml = minidom.parse(IOConfig.FILE)
            root = xml.getElementsByTagName('config')[0]
            return root
        
    def getServer():
        """Retorna o node do server"""
        root = IOConfig.getRoot()
        return root.getElementsByTagName('server')[0]
    
    def getColetores():
        """Retorna o node dos coletores"""
        root = IOConfig.getRoot()
        return root.getElementsByTagName('coletores')[0]
    
    def getStatus():
        """Retorna o node de status"""
        root = IOConfig.getRoot()
        return root.getElementsByTagName('status')[0]    
    
    def getSocket():
        """Retorna o node de socket"""
        root = IOConfig.getRoot()
        return root.getElementsByTagName('socket')[0]
    
    exists = staticmethod(exists)
    getFile = staticmethod(getFile)
    getRoot = staticmethod(getRoot)
    getServer = staticmethod(getServer)
    getColetores = staticmethod(getColetores)
    getStatus = staticmethod(getStatus)
    getSocket = staticmethod(getSocket)

class Reader:
    """
        Classe Reader
        
        Responsavel por efetuar a leitura do arquivo de configuracao
        do cacic. Informando dados como endereco do Gerente Web,
        usuario e senha, etc.
        
    """

    def getServer():
        """
            Retorna um dicionario contendo o endereco do servidor,
            a  e o arquivo
        """
        server = {'address':'', 'page': '', 'agent':'', 'username':'', 'password':''}
        config = IOConfig.getServer()
        for no in config.childNodes:
            if no.nodeType == Node.ELEMENT_NODE:
                server[no.nodeName] = no.firstChild.nodeValue                
        return server

    def getColetor(id):
        """
            Retorna um dicionario contendo as informacoes do
            coletor especificado por parametro
        """
        coletor = {'id':'','page':''}
        cols = IOConfig.getColetores()
        for no in cols.childNodes:
            if no.nodeType == Node.ELEMENT_NODE:
                if no.nodeName == 'coletor' and no.attributes['id'].nodeValue == id:
                    coletor['id'] = no.attributes['id'].nodeValue
                    coletor['page'] = no.attributes['page'].nodeValue
                    return coletor
    
    def getStatus(id):
        """
            Retorna um dicionario contendo as informacoes de
            status (param) especificado por parametro
        """
        status = {'id' : '', 'value' : ''}
        sts = IOConfig.getStatus()
        for no in sts.childNodes:
            if no.nodeType == Node.ELEMENT_NODE:
                if no.nodeName == 'param' and no.attributes['id'].nodeValue == id:
                    status['id'] = no.attributes['id'].nodeValue
                    status['value'] = no.attributes['value'].nodeValue
                    return status
                
    def getSocket():
        """Retorna um dicionario contendo as informacoes de socket"""
        socket = {'host' : '', 'port' : '', 'buffer' : ''}
        sock = IOConfig.getSocket()
        for no in sock.childNodes:
            if no.nodeType == Node.ELEMENT_NODE:
                socket[no.nodeName] = no.firstChild.nodeValue
        return socket
    
    
    getServer = staticmethod(getServer)
    getColetor = staticmethod(getColetor)
    getStatus = staticmethod(getStatus)
    getSocket = staticmethod(getSocket)
    
    
class Writer:
    """
        Classe Write
        
        Responsavel por efetuar a escrita no arquivo de configuracao
        do cacic. Alterando dados como se e instalacao, endereco do
        Gerente Web, usuario e senha, etc.        
    """
    
    def saveXML(xml):
        """Salva o XML de configuracoes"""
        if (IOConfig.exists()):
            open(IOConfig.FILE, 'w').write(xml)
            
    
    def setNodeValue(node, value):
        """Altera o valor do node passado por parametro"""
        re_open = re.compile('<.+?>')
        re_close = re.compile('</.*>')
        open = re_open.findall(node)[0]
        close = re_close.findall(node)[0]
        return '%s%s%s' % (open, value, close)
    
    def setNodeAttrib(node, attrib, value):
        """Altera o valor do atributo do node passado por parametro"""
        re_att = re.compile('%s=".*?"' % attrib)
        old = re_att.findall(node)[0]        
        return node.replace(old, ('%s="%s"' % (attrib, value)))

    def setServer(address, agent, password):
        """Grava endereco, arquivo e password do Gerente Web no XML"""
        config = IOConfig.getFile()
        re_sv = re.compile('<server(?:.|\n)*</server>')
        re_ws = re.compile('<ws.*</ws>')
        re_ad = re.compile('<address.*</address>')
        re_ag = re.compile('<agent.*</agent>')
        re_pw = re.compile('<password.*</password>')
        sv = re_sv.findall(config)[0]
        ws = re_ws.findall(sv)[0]
        ad = re_ad.findall(sv)[0] 
        ag = re_ag.findall(sv)[0]
        pw = re_pw.findall(sv)[0]        
        server = sv
        server = server.replace(ws, Writer.setNodeValue(ws, address))
        server = server.replace(ad, Writer.setNodeValue(ad, address))
        server = server.replace(ag, Writer.setNodeValue(ag, agent))
        server = server.replace(pw, Writer.setNodeValue(pw, password))
        Writer.saveXML(config.replace(sv, server))
        
    def setStatus(s, v):
        """Modifica o status"""
        config = IOConfig.getFile()
        re_st = re.compile('<status(?:.|\n)*</status>')
        re_pr = re.compile('<param.*?id="'+s+'".*?/>')
        st = re_st.findall(config)[0]
        pr = re_pr.findall(config)[0]
        status = st
        if (v):
            v = "OK"
        else:
            v = "NOK"
        status = status.replace(pr, Writer.setNodeAttrib(pr, "value", v))
        Writer.saveXML(config.replace(st, status))
        

    saveXML = staticmethod(saveXML)
    setServer = staticmethod(setServer)
    setStatus = staticmethod(setStatus)
    setNodeValue = staticmethod(setNodeValue)
    setNodeAttrib = staticmethod(setNodeAttrib)
    