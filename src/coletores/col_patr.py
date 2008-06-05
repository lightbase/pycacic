from coletor import *
from lib.computador import Rede


class Col_Patr(Coletor):
    """Classe responsavel por coletar os dados de Patrimonio"""

    def __init__(self, computer):
        Coletor.__init__(self, computer)
        self.computer = computer
        
    def getName(self):
        return "col_patr"

    def isReady(self, dat=None):        
        return 0
    
    def start(self):
        self.setDicionario()

    def setDicionario(self):
        """Monta o dicionario"""
        self.dicionario.clear()
        self.addChave('Inicio', strftime("%H:%M:%S"))
        self.addChave('UVC', self.getUVC(self.dicionario))
        self.addChave('Fim', strftime("%H:%M:%S"))
        return
    