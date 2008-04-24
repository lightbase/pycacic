# -*- coding: UTF-8 -*-
import sys, os
from xml.dom import minidom, Node

class IOConfig:
    
    FILE = sys.path[0] + '/config/default.xml'
    
    def exists():
        return (os.path.exists(IOConfig.FILE))
    
    def getFile():
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
        root = IOConfig.getRoot()
        return root.getElementsByTagName('coletores')[0]
    
    def getStatus():
        root = IOConfig.getRoot()
        return root.getElementsByTagName('status')[0]
    
    exists = staticmethod(exists)
    getFile = staticmethod(getFile)
    getRoot = staticmethod(getRoot)
    getServer = staticmethod(getServer)
    getColetores = staticmethod(getColetores)
    getStatus = staticmethod(getStatus)