# -*- coding: UTF-8 -*-
from IOConfig import *

class Reader:
    

    def getServer():
        """Retorna uma dicionario contendo o servidor e o arquivo"""
        server = {'address':'', 'page': '', 'agent':'', 'username':'', 'password':''}
        config = IOConfig.getServer()
        for no in config.childNodes:
            if no.nodeType == Node.ELEMENT_NODE:
                if no.nodeName == 'address':
                    server['address'] = no.firstChild.nodeValue
                elif no.nodeName == 'page':
                    server['page'] = no.firstChild.nodeValue
                elif no.nodeName == 'ws':
                    server['ws'] = no.firstChild.nodeValue
                elif no.nodeName == 'agent':
                    server['agent'] = no.firstChild.nodeValue
                elif no.nodeName == 'username':
                    server['username'] = no.firstChild.nodeValue
                elif no.nodeName == 'password':
                    server['password'] = no.firstChild.nodeValue
        return server

    def getColetor(id):
        coletor = {'id':'','page':''}
        cols = IOConfig.getColetores()
        for no in cols.childNodes:
            if no.nodeType == Node.ELEMENT_NODE:
                if no.nodeName == 'coletor' and no.attributes['id'].nodeValue == id:
                    coletor['id'] = no.attributes['id'].nodeValue
                    coletor['page'] = no.attributes['page'].nodeValue
                    return coletor
    
    def getStatus(id):
        status = {'id' : '', 'value' : ''}
        sts = IOConfig.getStatus()
        for no in sts.childNodes:
            if no.nodeType == Node.ELEMENT_NODE:
                if no.nodeName == 'param' and no.attributes['id'].nodeValue == id:
                    status['id'] = no.attributes['id'].nodeValue
                    status['value'] = no.attributes['value'].nodeValue
                    return status
    
    getServer = staticmethod(getServer)
    getColetor = staticmethod(getColetor)
    getStatus = staticmethod(getStatus)