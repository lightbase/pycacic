# -*- coding: UTF-8 -*-

"""

    Copyright 2000, 2001, 2002, 2003, 2004, 2005 Dataprev - Empresa de Tecnologia e Informações da Previdência Social, Brasil
    
    Este arquivo é parte do programa CACIC - Configurador Automático e Coletor de Informações Computacionais
    
    O CACIC é um software livre; você pode redistribui-lo e/ou modifica-lo dentro dos termos da Licença Pública Geral GNU como 
    publicada pela Fundação do Software Livre (FSF); na versão 2 da Licença, ou (na sua opnião) qualquer versão.
    
    Este programa é distribuido na esperança que possa ser  util, mas SEM NENHUMA GARANTIA; sem uma garantia implicita de ADEQUAÇÂO a qualquer
    MERCADO ou APLICAÇÃO EM PARTICULAR. Veja a Licença Pública Geral GNU para maiores detalhes.
    
    Você deve ter recebido uma cópia da Licença Pública Geral GNU, sob o título "LICENCA.txt", junto com este programa, se não, escreva para a Fundação do Software
    Livre(FSF) Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
    

    Modulo coletor
    
    Possui a classe pai (Coletor) dos demais
    coletores.
    
    @author: Dataprev - ES
    
"""

import os
from time import strftime

from lib.arquivo import *
from lib.ccrypt import *
from lib.computador import Computador

from lang.language import Language

_l = Language()

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
        self.STRPKEY = '=CacicIsFree='
        self.STRPVALUE = '=PyCacic='
        self.reserved_keys = ('UVC', 'Fim', 'Inicio')
    
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
        raise Exception('%s: Coletor.getName().' % _l.get('error_abstract_method'))
    
    def getUVCKey(self):
        """ Retorna o nome da chave do UVC """
        raise Exception('%s: Coletor.getUVCKey().' % _l.get('error_abstract_method'))
    
    def getDatKeyPrefix(self):
        """Retorna o prefixo do nome da chave no dat"""
        s = self.getName().split('_')
        return '%s%s_%s%s.' % (s[0][0].upper(), s[0][1:], s[1][0].upper(), s[1][1:])
    
    def getEncryptedDict(self, reserveds = False):
        """ Retorna o dicionario de dados da coleta encryptado """
        dicionario = {}
        for key, value in self.dicionario.items():
            # todo o dicionario
            if reserveds:
                dicionario[key] = self.encripta(self.dicionario[key])
            # pula as chaves reservadas
            elif not key in self.reserved_keys:
                dicionario[key] = self.encripta(self.dicionario[key])
        return dicionario
    
    def isReady(self, dat=None):
        """ Retorna True se o coletor está pronto/pretende enviar uma coleta, False caso contrário """
        return 1 # True
                    
    def createDat(self, chaves, path, prefixo=None):
        """
            Percorre o dicionario montando uma string
            com chave e valor separadas por uma string padrao
        """
        try:
            if prefixo == None:
                prefixo = self.getDatKeyPrefix()
            data = self.STRPKEY.join([str(prefixo) + str(k) + str(self.STRPVALUE) + str(chaves[k]) for k in chaves.keys()])
            Arquivo.saveFile(path, self.encripta(data))
        except Exception, e:
            raise Exception('%s (%s): %s' % (_l.get('error_on_save_file'), path, e))
        
    def getDatToDict(self, path, prefixo=None):
        """Restaura o Dicionario do Coletor a partir do seu Arquivo .DAT temporario"""
        try:
            dic = {}
            if prefixo == None:
                prefixo = self.getDatKeyPrefix()
            dat = Arquivo.openFile(path)
            data = self.decripta(dat)
            itens = data.split(self.STRPKEY)
            for item in itens:
                key_value = item.split(self.STRPVALUE)
                if len(key_value) >= 2:
                    dic[key_value[0].replace(prefixo, '')] = key_value[1] 
            return dic
        except Exception, e:
            raise Exception('%s (%s): %s' % (_l.get('error_on_open_file'), path, e))
        
            
    def getUVCDat(self, path, chave):
        """
            Retorna uma string contendo os valores da
            ultima coleta contida no arquivo .dat
        """
        data = Arquivo.openFile(path)
        dat = self.decripta(data)
        for i in dat.split(self.STRPKEY):
            item = i.split(self.STRPVALUE)
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
        return ';'.join([ str(dicionario[i]) for i in keys if not i in self.reserved_keys])
    
    def start(self):
        """Inicia a coleta do coletor atual"""
        self.setDicionario()
        self.createDat(self.dicionario, self.PATH + self.OUTPUT_DAT)
        
    def encripta(self, text):
        """Encripta o texto passado por parametro"""
        return self.crpt.encrypt(text)
    
    def decripta(self, text):
        """Desencripta o texto passado por parametro"""
        return self.crpt.decrypt(text)
    
    def getPadding(self):
        """Retorna o preenchemento utilizado para encriptar"""
        return self.crpt.getKeyPadding()
    