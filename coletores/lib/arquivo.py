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
        except IOError, e:
            raise (e)
        
    def openFile(path):
        """Retorna uma String com o conteudo do arquivo especificado"""
        try:
            if os.path.exists(path):
                f = open(path, 'r')
                data = f.read()
                f.close()
                return data                
            return ''
        except IOError, e:
            raise (e)
   
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
            