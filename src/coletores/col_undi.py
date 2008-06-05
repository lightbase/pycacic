
from coletor import *
from globals import Globals

class Col_Undi(Coletor):
    """Classe responsavel por coletar os dados das Unidades de Disco"""
    
    # nome do arquivo de saida (DAT)
    OUTPUT_DAT = 'col_undi.dat'

    def __init__(self, computer):
        Coletor.__init__(self, computer)
        self.computer = computer
        
    def getName(self):
        return "col_undi"
    
    def getUVCKey(self):
        return 'Coleta.Undi'

    def isReady(self, dat=None):
        return self.getUVCDat(dat, self.getUVCKey()) != self.getChave('UVC')

    def setDicionario(self):
        """Monta o dicionario"""        
        self.dicionario.clear()
        self.addChave('Inicio', strftime("%H:%M:%S"))
        parts = self.computer.getPartitions()
        """
            Drive <FIELD>
            id_tipo_unid_disco <FIELD>
            FileSystem <FIELD>
            SerialNumber <FIELD>
            Capacity <FIELD>
            FreeSpace <FIELD>
            ???? <FIELD>
        """
        tripa = '<REG>'.join(['<FIELD>'.join([p.getName(), '2', p.getFileSystem(), p.getSerial(), str(p.getSize()), str(p.getFreeSize()), '']) for  p in parts ])
        self.addChave('UnidadesDiscos', tripa)
        self.addChave('Fim', strftime("%H:%M:%S"))
        self.addChave('UVC', self.getUVC(self.dicionario))
        
