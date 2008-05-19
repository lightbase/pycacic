# -*- coding: UTF-8 -*-

"""

    Modulo coletor
    
    Possui a classe pai (Coletor) dos demais
    coletores.
    
    @author: Dataprev - ES
    
"""

import os;
from lib.arquivo import *
from lib.ccrypt import *
from lib.computador import Computador

class Coletor:
    """
        Classe Coletor
    
        Classe pai dos coletores. Possui atributos e metodos
        comuns entre eles.    
    """
    
    # caminho dos arquivos temporarios
    PATH = '/tmp/'
        
    def __init__(self, computer=None):
        self.dicionario = {}
        self.crpt = CCrypt()
        self.computer = computer
        self.spd_key = '=CacicIsFree='
        self.spd_value = '=PyCacic='
    
    def addChave(self, chave, valor):
        """
            Adiciona uma nova chave ao dicionario
            Caso nao exista retorna True, caso contrario retorna False
        """
        if not self.dicionario.has_key(chave):
            self.dicionario[chave] = valor
            return 1 # True
        self.setChave(chave, valor)
        return 0 # False
    
    def setChave(self, chave, valor):
        self.dicionario[chave] = valor
            
    def getChave(self, chave):
        """Retorna o valor da chave passada por parametro"""
        return self.dicionario[chave]
    
    def getName(self):
        """ Retorna o nome do coletor """
        raise Exception("Abstract method getName(), must override")
    
    def getUVCKey(self):
        """ Retorna o nome da chave do UVC """
        raise Exception("Abstract method getUVCKey(), must override")
    
    def getEncryptedDict(self):
        """ Retorna o dicionario de dados da coleta encryptado """
        for key, value in self.dicionario.items():
            self.dicionario[key] = self.encripta(self.dicionario[key])
        return self.dicionario
    
    def isReady(self, dat=None):
        """ Retorna True se o coletor está pronto/pretende enviar uma coleta, False caso contrário """
        return 1 # True
                    
    def createDat(self, chaves, path, prefixo=''):
        """
            Percorre o dicionario montando uma string
            com chave e valor separadas por uma string padrao
        """
        try:
            data = self.spd_key.join(["%s%s%s%s" % (prefixo, k, self.spd_value, chaves[k]) for k in chaves.keys()])
            Arquivo.saveFile(path, self.encripta(data))
        except:
            raise Exception('Erro ao gravar dat: %s' % path)
            
    def getUVCDat(self, path, chave):
        """
            Retorna uma string contendo os valores da
            ultima coleta contida no arquivo .dat
        """
        data = Arquivo.openFile(path)
        dat = self.decripta(data)       
        for i in dat.split(self.spd_key):
            item = i.split(self.spd_value)
            if item[0] == chave:
                return item[1] 
        return ''

    def getUVC(self, dicionario):
        """
            Retorna uma string contendo os valores da
            ultima coleta no dicionario
        """
        keys = dicionario.keys()
        keys.sort()
        return ';'.join(['%s' % dicionario[i] for i in keys if i != 'UVC'])
        
    def encripta(self, text):
        """Encripta o texto passado por parametro"""
        return self.crpt.encrypt(text)
    
    def decripta(self, text):
        """Desencripta o texto passado por parametro"""
        return self.crpt.decrypt(text)
    
    def getPadding(self):
        """Retorna o preenchemento utilizado para encriptar"""
        return self.crpt.getKeyPadding()
    