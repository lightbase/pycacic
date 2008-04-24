# -*- coding: UTF-8 -*-
import re
from IOConfig import *

class Writer:
    
    def saveXML(xml):
        """Salva o XML de configuracoes"""
        if (IOConfig.exists()):
            open(IOConfig.FILE, 'w').write(xml)
            
    
    def setNodeValue(node, value):
        """Altera o valor do node passado por parametro"""
        re_open = re.compile('<.+?>')
        re_close = re.compile('</.*>')
        re_value = re.compile('.*')
        open = re_open.findall(node)[0]
        close = re_close.findall(node)[0]
        old = re_value.findall(node)[0]
        return '%s%s%s' % (open, value, close) 

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
        config = config.replace(sv, server)
        Writer.saveXML(config)
        

    saveXML = staticmethod(saveXML)
    setServer = staticmethod(setServer)
    setNodeValue = staticmethod(setNodeValue)