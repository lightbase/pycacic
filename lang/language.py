# -*- coding: utf-8 -*-

import os
import sys
import codecs
from xml.dom import minidom, Node

class Language:
    """Classe que controla o idioma do aplicativo"""
    
    # xml infos
    version = ''
    author = ''
    date = ''
    language = ''
    description = ''
    
    # Supported Languages Dictonary
    langs = {
             'pt_BR' : 'pt_br.xml', # (Portuguese - Brasil)
             'pt_PT' : 'pt_pt.xml', # (Portuguese - Portugal)
             'en_US' : 'en_us.xml', # (English - USA)
             #'es_ES' : 'es_ES.xml', # (Spanish - Spain)
             #'es_ AR' : 'es_ar.xml' # (Spanish - Argentina)
             #'es_ MX' : 'es_mx.xml' # (Spanish - Mexico)
             #'fr_FR' : 'fr_fr.xml', # (French - France)
             #'fr_CA' : 'fr_fr.xml', # (French - Canada)
             #'de_ DE' : 'de_de.xml', # (German - Germany)
    }
    # default language
    DEFAULT = 'en_US'
    
    
    def __init__(self, mode = 'text'):
        """Construtor da classe"""
        self.setMode(mode)
        self.lang = self.getSOLang()
        self.openXML()
        self.setXMLInfo()
        
    
    def openXML(self):
        """Abre o arquivo XML contendo o idioma escolhido"""
        xml_file = open(sys.path[0] + '/lang/' + self.langs[self.lang], 'r').read()
        self.xml = minidom.parseString(xml_file)
    
    
    def setXMLInfo(self):
        """Set XML info in the class vars"""
        root = self.getRoot()
        about = root.getElementsByTagName('about')[0]
        for info in about.childNodes:
            if info.nodeType == Node.ELEMENT_NODE:
                if info.nodeName == 'version':
                    self.version = info.firstChild.nodeValue
                if info.nodeName == 'author':
                    self.author = info.firstChild.nodeValue
                if info.nodeName == 'date':
                    self.date = info.firstChild.nodeValue
                if info.nodeName == 'language':
                    self.language = info.firstChild.nodeValue    
                if info.nodeName == 'description':
                    self.description = info.firstChild.nodeValue
    
    
    def setMode(self, mode):
        """
            Seta o modo de exibicao do programa (texto ou grafico)
            para pegar a respectiva traducao
        """
        if not mode in ('text', 'gui'):
            self.mode = 'text'
        else:
            self.mode = mode
    
    
    def chooseLang(self, lang):
        """
            Altera o idioma do aplicativo caso o mesmo esteja
            disponivel
        """
        if self.langs.has_key(lang):
            self.lang = lang
        else:
            self.lang = DEFAULT
        self.openXML()
        self.setXMLInfo()
        
    
    def getHeader(self):
        """Retorna o cabecalho do programa"""
        no = self.getMode(self.mode)
        if not no:
            return False
        header = {}
        for filho in no.childNodes:
            if filho.nodeType == Node.ELEMENT_NODE and filho.nodeName == 'header':
                for item in filho.childNodes:
                    if item.nodeType == Node.ELEMENT_NODE:
                        header[item.nodeName] = item.firstChild.nodeValue
        return header

    
    def getMenu(self):
        """Retorna o menu principal do programa"""
        no = self.getMode(self.mode)
        if not no:
            return False
        menu = {}
        for filho in no.childNodes:
            if filho.nodeType == Node.ELEMENT_NODE and filho.nodeName == 'menu':
                for item in filho.childNodes:
                    if item.nodeType == Node.ELEMENT_NODE:
                        menu[item.attributes.get('href').nodeValue] = item.firstChild.nodeValue
        return menu
    
    
    def getMessagesHitKeys(self):
        """Retorna as mensagens de pressionar botao"""
        no = self.getMessages()
        if not no:
            return False
        messages = {}
        for filho in no.childNodes:
            if filho.nodeType == Node.ELEMENT_NODE and filho.nodeName == 'hitkeys':
                for item in filho.childNodes:
                    if item.nodeType == Node.ELEMENT_NODE:
                        messages[item.attributes.get('key').nodeValue] = item.firstChild.nodeValue
        return messages
    
    
    def getMessages(self):
        """Retorna todas a mensagens do programa"""
        no = self.getMode(self.mode)
        if not no:
            return False
        return no.getElementsByTagName('messages')[0]
    
    
    def getMode(self, mode):
        """
            Retorna todas as informacoes do 
            programa do modo especificado
        """
        if not mode in ('text', 'gui'):
            return False
        root = self.getRoot()
        for no in root.childNodes:
            if no.nodeType == Node.ELEMENT_NODE and no.nodeName == 'mode':
                atributos = no.attributes
                for a in atributos.keys():
                    valor = atributos.get(a).nodeValue
                    if a == 'type' and valor == mode:
                        return no
                    
    def getRoot(self):
        """Retorna o no raiz do XML"""        
        root = self.xml.getElementsByTagName('pycacic')[0]
        return root

    
    def getSOLang(self):
        so_lang = os.environ['LANG']
        for lang in self.langs:
            if so_lang.find(lang.lower()) != -1:
                return lang
        return self.DEFAULT
