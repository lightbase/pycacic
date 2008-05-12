from coletor import *
from lib.computador import Rede


class Col_Soft(Coletor):
    """Classe responsavel por coletar os dados de Software"""

    # nome do arquivo de saida (DAT)
    OUTPUT_DAT = 'col_soft.dat'

    def __init__(self, computer):
        Coletor.__init__(self, computer)
        self.computer = computer
        
    def getName(self):
        return "col_soft"
    
    def getUVCKey(self):
        return 'Coleta.Software'

    def isReady(self, dat=None):
        return 0
    
    def start(self):
        self.setDicionario()
        self.createDat(self.dicionario, self.PATH + self.OUTPUT_DAT, 'Col_Soft.')

    def setDicionario(self):
        """Monta o dicionario"""
        self.addChave('UVC', self.getUVC(self.dicionario))
    