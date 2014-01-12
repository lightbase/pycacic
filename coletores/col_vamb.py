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


    Modulo col_hard
    
    Modulo com finalidade de coletar as informacoes
    de variáveis de ambiente e passar para o gerente de coletas (Ger_Cols)
    e o mesmo repassar ao servidor
    
    @author: Dataprev - ES
    
"""

import commands
import re

from coletor import *
from lib.computador import Rede


class Col_Vamb(Coletor):
    """Classe responsavel por coletar os dados de Patrimonio"""
    
    # nome do arquivo de saida (DAT)
    OUTPUT_DAT = 'col_vamb.dat'
    
    def __init__(self, computer):
        Coletor.__init__(self, computer)
        self.computer = computer
        
    def getName(self):
        return "col_vamb"
    
    def getUVCKey(self):
        return 'Coleta.Vamb'

    def isReady(self, dat=None):        
        return 1

    def setDicionario(self):
        """Monta o dicionario"""
        self.dicionario.clear()
        self.addChave('Inicio', strftime("%H:%M:%S"))
        vars = commands.getoutput("set")
        varlist = vars.split("\n")
        lista = []
        for vv in varlist:
            pos = vv.find("=")
            key = vv[0:pos]
            #key = re.escape(key)
            value = vv[pos+1:pos+1+100]
            #value = re.escape(value)
            value = value.replace('=', '&equiv;')
            lista.append(key+"="+value)
            #value = "''"+value+"''"
        self.addChave("te_variaveis_ambiente", self.escapeSQL("#".join(lista)))
        self.addChave('UVC', self.getUVC(self.dicionario))
        self.addChave('Fim', strftime("%H:%M:%S"))
    
    def escapeSQL(self, sql):
        sql = sql.replace("'", "\\'")
        #sql = sql.replace("`", "\`")
        #sql = sql.replace("=", '\\=')
        #sql = sql.replace(";", "\;")
        return sql