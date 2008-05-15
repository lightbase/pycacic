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
from globals import Globals

class IOConfig:
    """
        Classe IOConfig
        
        Responsavel por guardar o caminho do arquivo de
        configuracao do PyCacic e efetuar a leitura dos nos principais
        dele.        
    """

    FILE = '%s/config/cacic.conf' % Globals.PATH
    
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
    
    def getPycacic():
        """Retorna o node do Pycacic"""
        root = IOConfig.getRoot()
        return root.getElementsByTagName('pycacic')[0]
    
    def getPycacicStatus():
        """Retorna o node de status"""
        pycacic = IOConfig.getPycacic()
        for no in pycacic.childNodes:
            if no.nodeType == Node.ELEMENT_NODE and no.nodeName == 'status':
                return no
    
    def getSocket():
        """Retorna o node de socket"""
        root = IOConfig.getRoot()
        return root.getElementsByTagName('socket')[0]
    
    exists = staticmethod(exists)
    getFile = staticmethod(getFile)
    getRoot = staticmethod(getRoot)
    getServer = staticmethod(getServer)
    getColetores = staticmethod(getColetores)
    getPycacic = staticmethod(getPycacic)
    getPycacicStatus = staticmethod(getPycacicStatus)
    getSocket = staticmethod(getSocket)

class Reader:
    """
        Classe Reader
        
        Responsavel por efetuar a leitura do arquivo de configuracao
        do PyCacic. Informando dados como endereco do Gerente Web,
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
    
    def getPycacic():
        """Retorna um dicionario contendo as informacoes sobre o PyCacic"""
        pycacic = {'dir' : '', 'hash' : '', 'password' : ''}
        config = IOConfig.getPycacic()
        for no in config.childNodes:
            if no.nodeType == Node.ELEMENT_NODE:
                pycacic[no.nodeName] = no.firstChild.nodeValue                
        return pycacic

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
    
    def getPycacicStatus(id):
        """
            Retorna um dicionario contendo as informacoes de
            status (param) especificado por parametro
        """
        status = {'id' : '', 'value' : ''}
        sts = IOConfig.getPycacicStatus()
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
    getPycacic = staticmethod(getPycacic)
    getColetor = staticmethod(getColetor)
    getPycacicStatus = staticmethod(getPycacicStatus)
    getSocket = staticmethod(getSocket)    
    
class Writer:
    """
        Classe Write
        
        Responsavel por efetuar a escrita no arquivo de configuracao
        do PyCacic. Alterando dados como se e instalacao, endereco do
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

    def setServer(node, value):
        """Altera o no especificado das informacoes do servidor"""
        config = IOConfig.getFile()
        re_sv = re.compile('<server(?:.|\n)*</server>')
        re_node = re.compile('<%s.*</%s>' % (node, node))
        sv = re_sv.findall(config)[0]        
        if len(re_node.findall(sv)) == 0:
            return 0 # False
        node = re_node.findall(sv)[0]        
        server = sv
        server = server.replace(node, Writer.setNodeValue(node, value))
        Writer.saveXML(config.replace(sv, server))
        
    def setPycacicStatus(s, v):
        """Modifica o status do Pycacic"""
        config = IOConfig.getFile()
        re_pc = re.compile('<pycacic(?:.|\n)*</pycacic>')
        re_st = re.compile('<status(?:.|\n)*</status>')
        re_pr = re.compile('<param.*?id="'+s+'".*?/>')
        pc = re_pc.findall(config)[0]
        st = re_st.findall(config)[0]
        pr = re_pr.findall(config)[0]
        status = st
        pycacic = pc
        if (v):
            v = "yes"
        else:
            v = "no"
        status = status.replace(pr, Writer.setNodeAttrib(pr, "value", v))
        pycacic = pycacic.replace(st, status)
        Writer.saveXML(config.replace(pc, pycacic))

    saveXML = staticmethod(saveXML)
    setServer = staticmethod(setServer)
    setPycacicStatus = staticmethod(setPycacicStatus)
    setNodeValue = staticmethod(setNodeValue)
    setNodeAttrib = staticmethod(setNodeAttrib)
    