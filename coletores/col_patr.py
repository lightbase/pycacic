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


    Modulo col_patr
    
    Modulo com finalidade de coletar as informacoes
    de patrimônio e passar para o gerente de coletas (Ger_Cols)
    e o mesmo repassar ao servidor
    
    @author: Dataprev - ES
    
"""


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
    