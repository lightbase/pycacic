# -*- coding: utf-8 -*-

import os
import sys
import codecs
from xml.dom import minidom, Node

from logs.log import CLog
from globals import Globals

class Language:
    """Classe que controla o idioma do aplicativo"""
    
    # default language
    DEFAULT = 'en_US'
    
    def __init__(self):
        """Construtor da classe"""
        self.dict = {}
        self.languages = []
        self.scanAvailableLanguages()
        self.lang = self.getSOLang()
        self.setActiveLanguageDict(self.openXML(self.lang))
        
    def scanAvailableLanguages(self):
        list = os.listdir('%s/lang/' % Globals.PATH)
        for file in list:
            if file.endswith(".xml"):
                try:
                    langInfo = self.getXMLHeader(file)
                    self.languages.append(langInfo.getCode().lower())
                except Exception, e:
                    # log error
                    CLog.appendLine('Language', e)
    
    def addLanguage(self, langInfo):
        Language.languages[langInfo.getCode().lower()] = langInfo;
        
    def getLanguageByCode(self, code):
        try:
            return Language.languages[code.lower()]
        except:
            return None
    
    def getXMLHeader(self, file):
        xml = minidom.parse(Globals.PATH + '/lang/' + file)
        try:
            return self.parseLanguageInfo(file, xml)
        except Exception, e:
            raise Exception("Failed to load: lang/"+file+" - Reason: %s" % e)        
        
    def parseLanguageInfo(self, file, xml):
        root = self.getRoot(xml)
        for child in root.childNodes:
            if child.nodeType == Node.ELEMENT_NODE and child.nodeName == "header":
                code = ''
                name = ''
                for c in child.childNodes:
                    if c.nodeType == Node.ELEMENT_NODE:
                        if c.nodeName == "code":
                            code = c.firstChild.nodeValue
                        elif c.nodeName == "name":
                            name = c.firstChild.nodeValue
                if code != '' and name != '':
                    return LanguageInfo(file, code, name)
        raise Exception("Language code and/or name missing/empty.")
    
    def getLanguageInfoByCode(self, code):
        for lang in self.languages:
            if lang.getCode() == code:
                return lang
        return None
    
    def loadLanguageByCode(self, code):
        langInfo = Language.getLanguageInfoByCode(code)
        if langInfo != None:
            langInfo.load()
    
    def loadFromFile(self, file):
        pass
    
    def setActiveLanguageDict(self, xml):
        root = self.getRoot(xml)
        body = root.getElementsByTagName('body')[0]
        for cat in body.childNodes:
            if cat.nodeType == Node.ELEMENT_NODE:
                self.dict[cat.nodeName] = {}
                for item in cat.childNodes:
                    if item.nodeType == Node.ELEMENT_NODE and item.nodeName == 'string':
                        self.dict[cat.nodeName][item.attributes.get('name').nodeValue] = item.firstChild.nodeValue           
    
    def openXML(self, lang):
        """Abre o arquivo XML contendo o idioma escolhido"""
        path = '%s/lang/%s.xml' % (Globals.PATH, self.lang.lower())
        try:
            xml_file = codecs.open(path, "r", "utf-8")
            xml = u"%s" % xml_file.read()
            return minidom.parseString(xml.encode("utf-8"))
        except:
            raise Exception("Error on open language file: %s" % path)
       
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
            return 0 # False
        header = {}
        for filho in no.childNodes:
            if filho.nodeType == Node.ELEMENT_NODE and filho.nodeName == 'header':
                for item in filho.childNodes:
                    if item.nodeType == Node.ELEMENT_NODE:
                        header[item.nodeName] = item.firstChild.nodeValue
        return header   
                    
    def getRoot(self, xml):
        """Retorna o no raiz do XML"""        
        root = xml.getElementsByTagName('pycacic')[0]
        return root
    
    def getSOLang(self):
        so_lang = os.environ['LANG'].lower()
        for lang in self.languages:
            if so_lang.find(lang) != -1:
                return lang
        return self.DEFAULT
    
    def get(self, name):
        """"""
        for item in self.dict.keys():
            try:
                return self.dict[item][name]
            except:
                pass
        return 'Translation of "%s" not Found' % name    
        
    
class LanguageInfo:
    
    def __init__(self, file, code, name):
        self.file = file
        self.code = code
        self.name = name
    
    def getName(self):
        return self.name
    
    def getCode(self):
        return self.code
    
    def getFile(self):
        return self.file
    
    def load(self):
        Language.loadFromFile(self, self.getFile())     
    

class LanguageDictionary:
    
    def __init__(self, langInfo):
        self.langInfo = langInfo
        self.load()
    
    def load(self):
        file = Globals.PATH + '/lang/' + langInfo.getFile()
        xml = minidom.parse(file)
        root = Language.getRoot(xml)
        
        