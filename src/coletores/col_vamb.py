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
        vars = commands.getoutput("set")
        varlist = vars.split("\n")
        lista = []
        for vv in varlist:
            pos = vv.find("=")
            key = vv[0:pos]
            #key = re.escape(key)
            value = vv[pos+1:pos+1+100]
            #value = re.escape(value)
            lista.append(key+"="+value)
            value = "''"+value+"''"
        self.addChave("te_variaveis_ambiente", self.escapeSQL("#".join(lista)))
        self.addChave('UVC', self.getUVC(self.dicionario))
    
    def escapeSQL(self, sql):
        sql = sql.replace("'", "\\'")
        #sql = sql.replace("`", "\`")
        #sql = sql.replace("=", '\=')
        #sql = sql.replace(";", "\;")
        return sql