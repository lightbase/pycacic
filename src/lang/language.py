# -*- coding: utf-8 -*-

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

import os
import sys
import time
import codecs
import commands

from xml.dom import minidom, Node

from logs.log import CLog


class Language:
    """Classe que controla o idioma do aplicativo"""
    
    # default language
    DEFAULT = 'en_US'
    
    def __init__(self):
        """Construtor da classe"""
        self.dict = {}
        self.langInfo = {}
        self.languages = []        
        self.scanAvailableLanguages()
        self.lang = self.getLang()
        self.setActiveLanguageDict(self.openXML(self.lang))
        
        
    def convertDate(self, date):
        """ date = 'YYYYMMDD' """
        dtformat = self.getLanguageInfo().getDateFormat() 
        dtformat = dtformat.replace('Y', date[0:4])
        dtformat = dtformat.replace('m', date[4:6])
        dtformat = dtformat.replace('d', date[6:8])
        return dtformat
    
        
    def scanAvailableLanguages(self):
        """Procura no diretório por arquivos de tradução"""
        list = os.listdir('/usr/share/pycacic/lang/')
        for file in list:
            if file.endswith(".xml"):
                try:
                    langInfo = self.getXMLHeader(file)
                    self.languages.append(langInfo.getCode().lower())
                    self.langInfo[langInfo.getCode().lower()] = langInfo 
                except Exception, e:
                    # log error
                    CLog.appendLine('Language', e)
    
    def addLanguage(self, langInfo):
        Language.languages[langInfo.getCode().lower()] = langInfo;
        
    def getLanguageByCode(self, code):
        """Retorna o código do arquivo de idioma"""
        try:
            return self.languages[code.lower()]
        except:
            return None
    
    def getXMLHeader(self, file):
        """Retorna o cabeçalho contendo informações sobre o arquivo de idioma"""
        xml = minidom.parse('/usr/share/pycacic/lang/' + file)
        try:
            return self.parseLanguageInfo(file, xml)
        except Exception, e:
            raise Exception("Failed to load: lang/"+file+" - Reason: %s" % e)        
        
    def parseLanguageInfo(self, file, xml):
        """Trata as informações do arquivo de idioma"""
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
                        elif c.nodeName == "dateformat":
                            dtformat = c.firstChild.nodeValue
                if code != '' and name != '' and dtformat != '':
                    return LanguageInfo(file, code, name, dtformat)
        raise Exception("Language code and/or name and/or dateformat missing/empty.")
    
    def getLanguageInfo(self):
        try:
            return self.langInfo[self.lang.lower()]
        except:
            return LanguageInfo('', '', '', '')
    
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
        path = '/usr/share/pycacic/lang/%s.xml' % self.lang.lower()
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
                    
    def getRoot(self, xml):
        """Retorna o no raiz do XML"""        
        root = xml.getElementsByTagName('pycacic')[0]
        return root    
    
    def getLang(self):
        """Retorna o idioma salvo no arquivo de configuracao"""
        from config.io import Reader
        pycacic = Reader.getPycacic()
        if pycacic.has_key('locale'): 
            return pycacic['locale']
        return self.DEFAULT
    
    def getSOLang(self):
        """Retorna o idioma padrão do sistema operacional"""
        so_lang = ''
        # tenta pegar idioma das variaveis de ambiente do python
        if os.environ.has_key('LANG'):
            so_lang = os.environ['LANG'].lower()
        # caso contrario pega do sistema
        else:
            so_lang = commands.getoutput('set | grep LANG=').lower()
        for lang in self.languages:
            if so_lang.find(lang) != -1:
                return lang
        return self.DEFAULT
    
    
    def get(self, name):
        """Retorna a tradução da string passada por parâmetro"""
        for item in self.dict.keys():
            try:
                return self.dict[item][name]
            except:
                pass
        return 'Translation of "%s" not Found' % name    
        
    
class LanguageInfo:
    
    def __init__(self, file, code, name, dtformat):
        self.file = file
        self.code = code
        self.name = name
        self.dateformat = dtformat
    
    def getName(self):
        return self.name
    
    def getCode(self):
        return self.code
    
    def getFile(self):
        return self.file
    
    def getDateFormat(self):
        return self.dateformat
    
    def load(self):
        Language.loadFromFile(self, self.getFile())     
    

class LanguageDictionary:
    
    def __init__(self, langInfo):
        self.langInfo = langInfo
        self.load()
    
    def load(self):
        file = '/usr/share/pycacic/lang/' + langInfo.getFile()
        xml = minidom.parse(file)
        root = Language.getRoot(xml)
        
        