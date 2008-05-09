
import socket
import struct

from coletor import *
from lib.computador import Rede
from lib.computador import Computador
from globals import Globals

class Col_Network(Coletor):
    """Classe responsavel por coletar os dados de TCP IP"""

    def __init__(self, computer):
        Coletor.__init__(self, computer)
        self.computer = computer

    def isReady(self, dat=None):
        # evita coletar network se estiver usando uma XML de outra maquina
        return Globals.PC_XML == ""

    def getName(self):
        return "col_network"
    
    def start(self):
        self.setDicionario()

    def setDicionario(self):
        """Monta o dicionario"""      
        net = None;  
        for nw in self.computer.getPlacaRede():
            if nw.getIP() == self.computer.ipAtivo:
                net = nw
                break
        self.dicionario.clear()
        if net != None:
            self.addChave("te_ip", self.computer.ipAtivo)        
            self.addChave('te_dns_primario', net.getDNS()[0])
            self.addChave('te_dns_secundario', net.getDNS()[1])
            self.addChave('te_dominio_dns', net.getDNSDomain())
            self.addChave('te_mascara', net.getMascara())
            self.addChave('te_nome_host', self.computer.getHostName())
            self.addChave('te_gateway', net.getGateway())
            self.addChave("te_serv_dhcp", net.getDHCP())
    