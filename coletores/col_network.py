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


    Modulo col_network
    
    Modulo com finalidade de coletar as informacoes
    de rede (TCP/IP) e passar para o gerente de coletas (Ger_Cols)
    e o mesmo repassar ao servidor
    
    @author: Dataprev - ES
    
"""


import socket
import struct

from coletor import *
from lib.computador import Rede
from lib.computador import Computador
from globals import Globals

class Col_Network(Coletor):
    """Classe responsavel por coletar os dados de TCP IP"""
    
    # nome do arquivo de saida (DAT)
    OUTPUT_DAT = 'col_network.dat'

    def __init__(self, computer):
        Coletor.__init__(self, computer)
        self.computer = computer
        
    def getName(self):
        return "col_network"
    
    def getUVCKey(self):
        return 'Coleta.Network'

    def isReady(self, dat=None):
        return self.getUVCDat(dat, self.getUVCKey()) != self.getChave('UVC')

    def setDicionario(self):
        """Monta o dicionario"""
        self.dicionario.clear()
        self.addChave('Inicio', strftime("%H:%M:%S"))
        net = None        
        for nw in self.computer.getPlacaRede():
            if self.computer.ipAtivo == nw.getIP():
                net = nw
                break
        if net != None:           
            self.addChave("te_ip", self.computer.ipAtivo)
            self.addChave("te_ip_rede", net.getIPRede())
            self.addChave("te_mac", net.getMAC())
            self.addChave('te_dns_primario', net.getDNS()[0])
            self.addChave('te_dns_secundario', net.getDNS()[1])
            self.addChave('te_dominio_dns', net.getDNSDomain())
            self.addChave('te_mascara', net.getMascara())
            self.addChave('te_nome_host', self.computer.getHostName())
            self.addChave('te_gateway', net.getGateway())
            self.addChave("te_serv_dhcp", net.getDHCP())
        self.addChave('UVC', self.getUVC(self.dicionario))
        self.addChave('Fim', strftime("%H:%M:%S"))
        
    