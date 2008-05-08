# -*- coding: UTF-8 -*-

"""

    Modulo arquivo
    
    Modulo com finalidade de facilitar a
    interacao com arquivos no disco.
    Tratando as excecoes.
    
    @author: Dataprev - ES
    
"""

import os


class Arquivo:
    """
        Classe Arquivo
        para controle de acesso aos arquivos
    """    
   
    def saveFile(path, content):
        """Salva um arquivo com o caminho especificado por parametro"""
        try:            
            file = open(path, 'w')
            file.write(content)
            file.close()
        except:
            raise ('Erro ao salvar arquivo: %s' % path)
        
    def openFile(path):
        """Retorna uma String com o conteudo do arquivo especificado"""
        try:
            if os.path.exists(path):
                f = open(path, 'r')
                data = f.read()
                f.close()
                return data                
            return ''
        except:
            raise Exception('Erro ao abrir arquivo: %s' % path)
   
    def deleteFile(path):
        """Exclui o arquivo especificado"""
        try:
            if os.path.exists(path):
                os.remove(path)
        except:
            raise Exception('Erro ao tentar remover arquivo: %s' % path)

    saveFile = staticmethod(saveFile)
    openFile = staticmethod(openFile)
    deleteFile = staticmethod(deleteFile)
            