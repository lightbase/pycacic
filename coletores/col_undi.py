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


    Modulo col_undi
    
    Modulo com finalidade de coletar as informacoes
    de unidade de disco e passar para o gerente de coletas (Ger_Cols)
    e o mesmo repassar ao servidor
    
    @author: Dataprev - ES
    
"""

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
        
