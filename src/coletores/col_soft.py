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
        return self.getUVCDat(dat, self.getUVCKey()) != self.getChave('UVC')

    def setDicionario(self):
        """Monta o dicionario"""
        self.dicionario.clear()
        self.addChave('Inicio', strftime("%H:%M:%S"))
        self.addChave("te_versao_bde", "0")
        self.addChave("te_versao_dao", "0")
        self.addChave("te_versao_ado", "0")
        self.addChave("te_versao_directx", "0")
        self.addChave("te_versao_acrobat_reader", "0")
        self.addChave("te_versao_ie", "0")
        self.addChave("te_versao_mozilla", "0")
        self.addChave("te_versao_jre", "0")
        self.addChave("te_inventario_softwares", "#".join(self.computer.getPacotes()))
        self.addChave('UVC', self.getUVC(self.dicionario))
        self.addChave('Fim', strftime("%H:%M:%S"))
    