# -*- coding: UTF-8 -*-

import os;
from lib.arquivo import *
from lib.ccrypt import *

class Coletor:
    """Classe Coletor"""
    
    # caminho dos arquivos temporarios
    PATH = '/tmp/'
        
    def __init__(self):
        self.dicionario = {}
        self.crpt = CCrypt()
        self.spd_key = '=CacicIsFree='
        self.spd_value = '=PyCacic='
    
    def addChave(self, chave, valor):
        """Adiciona uma nova chave ao dicionario caso nao exista"""
        if not self.dicionario.has_key(chave):
            self.dicionario[chave] = valor
            
    def getChave(self, chave):
        return self.dicionario[chave]
                    
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
        return self.crpt.key.replace(CCrypt.KEY, '')
    