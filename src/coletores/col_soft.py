from coletor import *
from lib.computador import Rede


class Col_Soft(Coletor):
    """Classe responsavel por coletar os dados de Software"""

    def __init__(self, computer):
        Coletor.__init__(self, computer)
        self.computer = computer
        
    def getName(self):
        return "col_soft"

    def isReady(self, dat=None):        
        return False
    
    def start(self):
        self.setDicionario()

    def setDicionario(self):
        """Monta o dicionario"""      
        return
    